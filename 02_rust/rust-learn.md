# Rust 学習ノート

## コーディング

- Rust で変数はデフォルトで不変、Java のような final は不要。
  - 逆に、可変にする場合は`mut`を利用し、`let mut a = String::new();`のように宣言する。
- シャドウイング。既に宣言した変数に対して、再度変数名を再利用することが可能。型変換を行う際などによく利用する。

```rust
let mut guess = String::new();
io::stdin()
    .read_line(&mut guess)
    .expect("Failed to read line");
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

- [mutch 演算子](https://doc.rust-jp.rs/book-ja/ch06-02-match.html)。switch のような使い方が可能。全パターンの網羅をする必要が有り、ワイルドカード(\_)も利用可能

```rust
match guess.cmp(&secret_number) {
    Ordering::Less => println!("Too small!"),
    Ordering::Greater => println!("Too big!"),
    Ordering::Equal => {
        println!("You win!");
        break;
    }
}
```

- mutch によるパターンマッチング。以下の例では、parse の返り値`Result`型は、Ok もしくは Err の列挙型を返却する。Ok の場合の引数を guess に u32 型として返却。Err の場合は continue（ループの中で利用してる体）

```rust
let guess: u32 = match guess.trim().parse() {
    Ok(num) => num,
    Err(_) => continue,
};
```

- エラーハンドリングは、`Result`型の Enum を利用する。`try-catch`は無い。

```rust
pub enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

## パッケージ管理

- cargo によってパッケージ管理され、Cargo.toml, Cargo.lock にて依存ライブラリが記載される。
  - 依存ライブラリは、[crates.io](https://crates.io/)にて公開される。
- ビルドのタイプはバイナリ（bin）もしくはライブラリ（lib）となり、ビルドした一式のコンパイル単位をクレート（crate）と呼ぶ。
  - bin の場合は、`$ cargo new hello_world`もしくは`$ cargo init --bin hello_world`にてプロジェクトを作成する。
    - init の場合、引数に何も与えない場合はカレントディレクトリを root とみなす。

## 豆知識

- toml の由来は、`Tom's Obvious, Minimal Language`の略。[Tom Preston-Werner](https://twitter.com/mojombo)氏によって作成された。GitHub の共同創業者。

## 参考

- [The Rust Programming Language](https://doc.rust-lang.org/book/ch01-02-hello-world.html#anatomy-of-a-rust-program)
- [The Rust Programming Language 日本語版](https://doc.rust-jp.rs/book-ja/title-page.html)
