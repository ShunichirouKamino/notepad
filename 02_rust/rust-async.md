# Rust 非同期生理

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

```

```
