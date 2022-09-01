# Rust 非同期整理

## 事前知識

### async

- [Asynchronous Programming in Rust - async/.await Primer](https://rust-lang.github.io/async-book/01_getting_started/04_async_await_primer.html)

```rust
use futures::executor::block_on;

async fn hello_world() {
    println!("hello, world!");
}

fn main() {
    // let future: impl Future<Output = ()>
    // Nothing is printed
    let future = hello_world();
    // `future` is run and "hello, world!" is printed
    block_on(future);
}
```

- `async` は、非同期関数を構築します。返り値は、`Future<Output = ()>`です。
- `hello_world` を実行したタイミングでは、`println!`は実行されません。
- `futures` クレートにより提供される`futures::executor::block_on`は、現在のスレッドで`Future`の完了まで実行します。
- `async` の返り値は、`Future<Output> = ()`であり、`Future` 記法のシンタックスシュガーです。

```rust
fn hello_world() -> impl std::future::Future<Output = ()> {
    async {
        println!("hello, world!");
    }
}
```

### await

- `await` は、スレッドを並列実行可能状態にさせ、複数のスレッドを同時実行させることができます。
- `await` を使わない以下の例では、`sing_song`の実行の後に直列で`dance`が実行されます。
  - これは、`block_on`が現在実行している同一スレッドにて`Future`を実行するためです。

```rust
async fn learn_song() -> Song { ... }
async fn sing_song(song: Song) { ... }
async fn dance() { ... }

fn main() {
    let song = block_on(learn_song());
    block_on(sing_song(song));
    block_on(dance());
}
```

- `await`により、`async`な関数を中断しながら実行することができ、同一`async`内では直列な関数となります。
  - `learn_song`と`sing_song`は直列に実行されます。
- `future::join!`を利用することで、`await`で実行されている`async`関数を並列に実行することが可能となります。
  - もし`let song = block_on(learn_song())`とした場合は、`dance()`と`learn_and_sing()`はたとえ`join!`に渡されたとしても直列で実行されます。
    - 実行順序は不明ですが、一度`learn_and_sing()`が実行されてしまったら、`learn_song()`が完了するまで別の`async`な処理（ここでは`dance()`）に入ることはできません。

```rust

async fn learn_song() -> Song { ... }
async fn sing_song(song: Song) { ... }
async fn dance() { ... }

async fn learn_and_sing() {
    let song = learn_song().await;
    sing_song(song).await;
}

async fn async_main() {
    let f1 = learn_and_sing();
    let f2 = dance();

    // 実行順序は不明
    // 仮にf1, f2の中にblock_onが有る場合、その時点で当スレッドはブロックされる
    futures::join!(f1, f2);
}

fn main() {
    block_on(async_main());
}
```

### Future

- `Future`は、非同期な関数を表します。JavaScriptの`Promise`と似ていますが、処理の成功／失敗を内包しているわけではありません。
- 

```rust
pub trait Future {
    // Futureの返り値オブジェクト
    type Output;

    // Futureが実行可能であるかどうかの判定を行うメソッド
    fn poll(self: Pin<&mut Self>, cx: &mut Context<'_>) -> Poll<Self::Output>;
}

pub enum Poll<T> {
    Ready(T),
    Pending,
}
```

- （参考）値を返すだけのFutureを自前で実装

```rust
use std::future::Future;
use std::pin::Pin;
use std::task::{Context, Poll};

pub struct ReturnFuture<T>(Option<T>);

impl<T> ReturnFuture<T> {
    pub fn new(t: T) -> Self {
        Self(Some(t))
    }
}

impl<T> Future for ReturnFuture<T>
where
    T: Unpin,
{
    type Output = T;
    fn poll(self: Pin<&mut Self>, _: &mut Context) -> Poll<Self::Output> {
        Poll::Ready(
            self.get_mut()
                .0
                .take()
                .expect("A future should never be polled after it returns Ready"),
        )
    }
}
```

## 利用クレートfutures::future

### join

- `join`関数は二つの`Future`を引数にとり、非同期実行可能な、つまり新たな`Future`を作ります。

```rust
// a: impl Future<OutPut = i32>
let a = async { 1 };
// b: impl Future<OutPut = ()>
let b = async { print!("hello!") };

// joined: Join<impl Future<Output = i32>, impl Future<Output = ()>>
let joined = futures::future::join(a, b);
// result: (i32, ())
let result = joined.await;
asert_eq!(result.0, 1)
```

- `join`関数は`Join`オブジェクトを構築します。
- `Join`オブジェクトは、マクロによって`Future`をImplする形で作られています。
  - `join`にはjoin~join5があり、それぞれ与える`future`の数によって利用する`join`が異なります。各返却値である`Join`オブジェクトを冗長に実装しない目的で、マクロによる実装がされています。

```rust
// https://docs.rs/futures-util/0.3.24/src/futures_util/future/join.rs.html#111
pub fn join<Fut1, Fut2>(future1: Fut1, future2: Fut2) -> Join<Fut1, Fut2>
where
    Fut1: Future,
    Fut2: Future,
{
    let f = Join::new(future1, future2);
    assert_future::<(Fut1::Output, Fut2::Output), _>(f)
}

// https://docs.rs/futures-util/0.3.24/src/futures_util/future/join.rs.html#46
impl<$($Fut: Future),*> Future for $Join<$($Fut),*> {
    type Output = ($($Fut::Output),*);
    fn poll(
        self: Pin<&mut Self>, cx: &mut Context<'_>
    ) -> Poll<Self::Output> {
        let mut all_done = true;
        let mut futures = self.project();
        $(
            all_done &= futures.$Fut.as_mut().poll(cx).is_ready();
        )*
        if all_done {
            Poll::Ready(($(futures.$Fut.take_output().unwrap()), *))
        } else {
            Poll::Pending
        }
    }
}
```



## tonicとactix_webの並列ランナー実装

### 
- `futures::future`クレートの`join`により、`actix-web`の`future`と`tonic`の`future`を同時実行させます。

```rust
pub mod runner_actix_web;
pub mod runner_tonic;

use crate::error::server_error::ActixWebTonicError;
use futures::future::Future;
use runner_actix_web::actix_main;
use runner_tonic::tokio_main;
use std::io::Error as AError;
use tonic::transport::Error as TError;

pub async fn async_main(
    actix_future: impl Future<Output = Result<(), AError>>,
    tonic_future: impl Future<Output = Result<(), TError>>,
) -> Result<(), ActixWebTonicError> {
    let r_actix = actix_main(actix_future);
    let r_tokio = tokio_main(tonic_future);

    let r = futures::future::join(r_actix, r_tokio).await;
    match r {
        (Ok(_), Ok(_)) => Ok(()),
        _ => Err(ActixWebTonicError::Either {
            actix: r.0,
            tonic: r.1,
        }),
    }
}
```