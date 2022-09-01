<!-- vscode-markdown-toc -->

- 1. [事前知識](#)
  - 1.1. [Future](#Future)
  - 1.2. [async](#async)
  - 1.3. [await](#await)
- 2. [利用クレート futures::future](#futures::future)
  - 2.1. [join](#join)
  - 2.2. [abortable](#abortable)
- 3. [tonic と actix_web の並列ランナー実装](#tonicactix_web)
  - 3.1. [①`futures::future`クレートの`join`により、`actix-web`の`future`と`tonic`の`future`を同時実行させます。](#futures::futurejoinactix-webfuturetonicfuture)
  - 3.2. [② 片方の future に対して SIGKILL の hook を実装し、abortable によるタスクキルを実現します。](#futureSIGKILLhookabortable)
  - 3.3. [③`tokio`ランタイムを構築し、仮想的な`#[tokio_main]`による非同期実行関数を実装します。](#tokiotokio_main)
- 4. [分からない](#-1)

<!-- vscode-markdown-toc-config
	numbering=true
	autoSave=true
	/vscode-markdown-toc-config -->
<!-- /vscode-markdown-toc -->1

# Rust 非同期整理

## 1. <a name=''></a>事前知識

### 1.1. <a name='Future'></a>Future

- `Future`trait は、非同期な関数を表します。JavaScript の`Promise`と似ていますが、処理の成功／失敗を内包しているわけではありません。
- `Future`trait を impl することで、自分で非同期なオブジェクトを実装することができます。
- `async`シンタックスは、任意の関数を`Future`でラップする、`Future`のシンタックスシュガーです。

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

- （参考）値を返すだけの Future を自前で実装

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

### 1.2. <a name='async'></a>async

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

### 1.3. <a name='await'></a>await

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
    - （結果並列になるので関係ないですが）実行順序は最初の引数の`Future`から実行されます。
    - 一度`learn_and_sing()`が実行されてしまったら、`learn_song()`が完了するまで別の`async`な処理（ここでは`dance()`）に入ることはできません。

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

## 2. <a name='futures::future'></a>利用クレート futures::future

### 2.1. <a name='join'></a>join

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
- `Join`オブジェクトは、マクロによって`Future`trait を Impl する形で作られています。
  - `join`には join~join5 があり、それぞれ与える`future`の数によって利用する`join`が異なります。各返却値である`Join`オブジェクトを冗長に実装しない目的で、マクロによる実装がされています。

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

### 2.2. <a name='abortable'></a>abortable

- `abortable`関数は、中断可能な`Future`を構築します。
- `abortable`関数は、1 つの`Future`を引数にとり、`Future`を`Abortable`オブジェクトに変換して返却します。
  - `Abortable`オブジェクトは、中断可能な`Future`です。
- `Abortable`オブジェクトは、`abortable`のもう一つの返り値である`abortHandle`によって、中断することが可能です。

```rust
use futures::future::{Abortable, Aborted};

let (abortable_future, aborter) = futures::future::abortable(future);
// abortableハンドラをabortさせる
aborter.abort();
// awaitで実行しても、既にabortしている
assert_eq!(abotable_future.await, Err(Aborted))
```

- abortable 関数では、`AbortHandle::new_pair()`により、ハンドラの登録に必要な`reg`変数が返却されます。
- `Abortable::new(future, reg)`により、既存の`future`と`reg`を用いてオブジェクト化することで、`handle`に対して既存の`future`が登録され、`abortable`になります。

```rust
// https://doc.servo.org/src/futures_util/future/abortable.rs.html#1
pub fn abortable<Fut>(future: Fut) -> (Abortable<Fut>, AbortHandle)
where
    Fut: Future,
{
    let (handle, reg) = AbortHandle::new_pair();
    let abortable = assert_future::<Result<Fut::Output, Aborted>, _>(Abortable::new(future, reg));
    (abortable, handle)
}
```

## 3. <a name='tonicactix_web'></a>tonic と actix_web の並列ランナー実装

- ①`futures::future`クレートの`join`により、`actix-web`の`future`と`tonic`の`future`を同時実行させます。
  - `actix-web`及び`tonic`の`Server`は、いずれも`Future`の形式で実装されています。つまり非同期実行可能です。
- ② 片方の future に対して SIGKILL の hook を実装し、abortable によるタスクキルを実現します。
- ③`tokio`ランタイムを構築し、仮想的な`#[tokio_main]`による非同期実行関数を実装します。

### 3.1. <a name='futures::futurejoinactix-webfuturetonicfuture'></a>①`futures::future`クレートの`join`により、`actix-web`の`future`と`tonic`の`future`を同時実行させます。

```rust
pub mod runner_tonic;

use crate::error::server_error::ActixWebTonicError;
use futures::future::Future;
use runner_tonic::tokio_main;
use std::io::Error as AError;
use tonic::transport::Error as TError;

pub async fn async_main(
    actix_future: impl Future<Output = Result<(), AError>>,
    tonic_future: impl Future<Output = Result<(), TError>>,
) -> Result<(), ActixWebTonicError> {
    // ②によりabort可能なFutureとするために、tokioのみ別Futureを構築する
    let abortable_tonic = abortable_future(tonic_future);

    // actix_web及び、abortableなtonicを並列実行する
    let r = futures::future::join(actix_future, abortable_tonic).await;
    // 双方がOKであれば問題無く、片方がエラーの場合は元のエラーを返す
    match r {
        (Ok(_), Ok(_)) => Ok(()),
        _ => Err(ActixWebTonicError::Either {
            actix: r.0,
            tonic: r.1,
        }),
    }
}
```

### 3.2. <a name='futureSIGKILLhookabortable'></a>② 片方の future に対して SIGKILL の hook を実装し、abortable によるタスクキルを実現します。

```rust
use futures::future::Future;
use tonic::transport::Error;

/// Pseudo-#[tokio::main] specialized for tonic
/// with SIGINT(CTRL+C) aborter injection.
pub async fn abortable_future(
    future: impl Future<Output = Result<(), Error>>,
) -> Result<(), Error> {
    let (f_abortable, aborter) = futures::future::abortable(future);

    // ここで(=kill=CTRL+C)でシグキル可能なようにhookするFutureを作成しています。
    // asyncコードブロックで利用されているmoveによってaborterの所有権が移動していますが、
    // aborterはその後利用しないためmove無くても問題無いです。
    // コードブロック外のスコープ変数を利用するため、便宜上moveを使ってます。
    let f_sigint = async move {
        tokio::signal::ctrl_c().await.unwrap();
        aborter.abort();
    };
    log::info!("Tonic runtime found; starting in Tonic runtime.");

    // let r: (Result<Result<(), Error>, Aborted>, ())
    let r = futures::future::join(f_abortable, f_sigint).await;

    // Ok(Err)の場合は、f_abortableがErrであることを示すため、Errとします。
    // それ以外の場合はOkなので、まとめて残余記法をしています。
    match r.0 {
        Ok(Err(e_tonic)) => Err(e_tonic),
        // Err(_) => Ok(()),
        // Ok(Ok(())) => Ok(()),
        _ => Ok(()),
    }
}
```

### 3.3. <a name='tokiotokio_main'></a>③`tokio`ランタイムを構築し、仮想的な`#[tokio_main]`による非同期実行関数を実装します。

tokio ランタイムをマクロを用いず自前で実装する。

- [how to run server by #[tokio::main]](https://github.com/actix/actix-web/issues/1283#issuecomment-886170802)
- [Rust の非同期ランタイム `#[tokio::main]`を深堀り](https://qiita.com/ryuma017/items/1f31f5441ed5df80f1cc)

```rust
// （参考）#[tokio_main]を付与したmainのマクロ展開後のコード

#![feature(prelude_import)]
#[prelude_import]
use std::prelude::rust_2021::*;
#[macro_use]
extern crate std;
use actix_web::{web, App, HttpServer, Responder};
async fn hello() -> impl Responder {
    "Hello, World!"
}
fn main() -> std::io::Result<()> {
    let body = async {
        HttpServer::new(|| App::new().route("/", web::get().to(hello)))
            .bind("127.0.0.1:8000")?
            .run()
            .await
    };
    #[allow(clippy::expect_used)]
    tokio::runtime::Builder::new_multi_thread()
        .enable_all()
        .build()
        .expect("Failed building the Runtime")
        .block_on(body)
}
```

```rust
// （参考）tokioランタイム用のスレッドを自前で構築する方法

fn main() {
    actix_web::rt::System::with_tokio_rt(|| {
        tokio::runtime::Builder::new_multi_thread()
            .enable_all()
            .worker_threads(8) // 8スレッド利用するtokioランタイム
            .thread_name("main-tokio")
            .build()
            .unwrap()
    })
    .block_on(async_main());
}
```

- 実際の実装

```rust
use futures::future::Future;
use std::io::Error as AError;
use tonic::transport::Error as TError;

use crate::{error::server_error::ActixWebTonicError, system::async_runner};

pub fn invoke(
    actix_future: impl Future<Output = Result<(), AError>>,
    tonic_future: impl Future<Output = Result<(), TError>>,
    tokio_worker_threads: usize,
) -> Result<(), ActixWebTonicError> {
    log::info!("actix-web and tonic futures will be start.");
    log::info!("(Note) Use **SIGINT(CTRL+C)** if you should stop the app.");
    log::info!("tokio worker threads=[{}]", tokio_worker_threads);

    // tokioのランタイムを構築し、そのランタイムの配下でactix_future及びtonic_futureを動かす
    // 結果block_onによりホールドされるFutureは、非同期でマルチで実行される
    actix_web::rt::System::with_tokio_rt(|| {
        tokio::runtime::Builder::new_multi_thread()
            .enable_all()
            .worker_threads(tokio_worker_threads)
            .thread_name("unaf::main::tokio")
            .build()
            .unwrap()
    })
    .block_on(async_runner::async_main(actix_future, tonic_future))?;

    log::info!("actix-web and tonic futures has been terminated.");
    Ok(())
}
```

## 4. <a name='-1'></a>分からない

- tokio ランタイムのスレッド数について
  - どの程度 tokio に与えればいいのか
  - actix-web から出力されるログに表示されるスレッド数が、物理コア数と同値
