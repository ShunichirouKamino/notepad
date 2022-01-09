# Rust 学習ノート

## コーディング

- Rust で変数はデフォルトで不変、Java のような final は不要です。
  - 逆に、可変にする場合は`mut`を利用し、`let mut a = String::new();`のように宣言します。
- シャドウイング。既に宣言した変数に対して、再度変数名を再利用することが可能。型変換を行う際などに利用されます。。

```rust
let mut guess = String::new();
io::stdin()
    .read_line(&mut guess)
    .expect("Failed to read line");
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

- [mutch 演算子](https://doc.rust-jp.rs/book-ja/ch06-02-match.html)は、switch のような使い方が可能です。全パターンの網羅をする必要が有り、ワイルドカード(\_)も利用可能です。

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

- mutch によるパターンマッチング例です。以下の例では、parse の返り値`Result`型は、Ok もしくは Err の列挙型を返却します。Ok の場合の引数を guess に u32 型として返却します。Err の場合は continue（ループの中で利用してる体）を明示してます。

```rust
let guess: u32 = match guess.trim().parse() {
    Ok(num) => num,
    Err(_) => continue,
};
```

- エラーハンドリングは、`Result`型の Enum を利用します。

```rust
pub enum Result<T, E> {
    Ok(T),
    Err(E),
}
```

- [Rust -1.13](https://blog.rust-lang.org/2016/11/10/Rust-1.13.html)リリースで導入された`?`演算子 は、`Result`の複雑化を防ぐために導入されました。
  - `?`演算子は、`Result`を返す関数の中でしか利用できません。
  - `?`演算子は、`Result`型の後につけることで、`Ok`なら中の値の返却、`Err`なら即座に値を return します。

**これまでの書き方**

```rust
fn read_username_from_file() -> Result<String, io::Error> {
    let f = File::open("username.txt");

    let mut f = match f {
        Ok(file) => file,
        Err(e) => return Err(e),
    };

    let mut s = String::new();

    match f.read_to_string(&mut s) {
        Ok(_) => Ok(s),
        Err(e) => Err(e),
    }
}
```

- ## async/await が Rust 1.38.0 にてリリース。

## パッケージ管理

- cargo によってパッケージ管理され、Cargo.toml, Cargo.lock にて依存ライブラリが記載されます。
  - 依存ライブラリは、[crates.io](https://crates.io/)にて公開されます。
  - 公開されたライブラリに対するドキュメントは、[Docs.rs](https://docs.rs/)にて公開されます。
- ビルドのタイプはバイナリ（bin）もしくはライブラリ（lib）となり、ビルドした一式のコンパイル単位をクレート（crate）と呼びます。
  - bin の場合は、`$ cargo new hello_world`もしくは`$ cargo init --bin hello_world`にてプロジェクトを作成します。
    - init の場合、引数に何も与えない場合はカレントディレクトリを root とみなします。
- Cargo.lock は、lib クレートの場合は構成管理に含めませんが、バイナリクレートの場合は構成管理に含めます。（[参考：Cargo.toml と Cargo.lock](https://doc.rust-lang.org/cargo/guide/cargo-toml-vs-cargo-lock.html)）
  - lib クレートを利用するクレートにから見た際に、利用する lib クレートでのバージョンが固定されることで、他 lib クレートとのバージョンの競合が発生する可能性が有るためです。
- 利用者のフィーチャーフラグの利用方法。
  - フィーチャーフラグとは、コードを書き換えることなく動的にシステムの振る舞いを変更することができる開発手法を指します。
  - クレート内の特定の機能の有効／無効を切り替えることが可能です。
  - クレートによってはデフォルトでいくつかのフラグが有効になっていることも有るため、`default-features = false`を指定すると無効にできます。

**Cargo.toml**

```toml
[dependencies]
actix-web = { version = "4.0.0-beta.13", default-features = false }
```

- クレート作成者のフィーチャーフラグの利用方法。
  - 自作したクレートにフィーチャーフラグを設定する場合は、以下のように toml にフィーチャーフラグを設定します。
  - 以下のような設定で、`ja`フィーチャーフラグが有効な場合とそうでない場合で、依存先のクレートでの関数の振る舞いを動的にすることができます。

**Cargo.toml**

```tomol
[features]
default = []
ja = []
```

**lib.rs**

```rust
#[cfg(not(feature="ja"))]
pub fn hello() -> &'static str {
    "hello"
}
#[cfg(feature="ja")]
pub fn hello() -> &'static str {
    "こんにちは"
}
```

## トレインモデル

Rust では、コードの安全性に注意するため、リリースを以下の３バージョンに分けています。（[（参考）Nightly Rust](https://doc.rust-jp.rs/book-ja/appendix-07-nightly-rust.html)）

- Nightly
- Beta
- Stable

Nightly は毎日作られるリリースで、6 週間ごとに Beta に合流します。さらに 6 週間で、Beta が Stable に合流します。
Stable 版は、1.X の X 部分にあたるリリースとなります。

- 現時点のビルドバージョンの確認方法

```bash
$ rustup default
nightly-x86_64-pc-windows-msvc (default)
```

- デフォルトのビルドバージョンの変更方法

```bash
$ rustup default nightly
$ rustup update
```

## 豆知識

- toml の由来は、`Tom's Obvious, Minimal Language`の略です。[Tom Preston-Werner](https://twitter.com/mojombo)氏によって作成されました。GitHub の共同創業者。

## 参考

- [The Rust Programming Language](https://doc.rust-lang.org/book/ch01-02-hello-world.html#anatomy-of-a-rust-program)
- [The Rust Programming Language 日本語版](https://doc.rust-jp.rs/book-ja/title-page.html)
- [Qiita - Rust に影響を与えた言語たち](https://qiita.com/hinastory/items/e97d5459b9cda45758db)

## VScode での環境構築

- extention.json

```json
{
  "recommendations": ["matklad.rust-analyzer", "vadimcn.vscode-lldb"],
  "unwantedRecommendations": []
}
```

インストール後、`rust-analyzer`を動かすためには以下コンポーネントを追加します。

```bash
$ rustup component add rust-src
$ rustup component add rust-analysis
$ rustup component add rls
```
