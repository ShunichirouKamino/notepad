# Rust 学習ノート

# 重要ポイント

- Rust で変数はデフォルトで不変、Java のような final は不要
  - 逆に、可変にする場合は`mut`を利用し、`let mut a = String::new();`のように宣言する。
- シャドウイング。既に宣言した変数に対して、再度変数名を再利用することが可能。型変換を行う際などによく利用する。

```rust
let mut guess = String::new();
io::stdin()
    .read_line(&mut guess)
    .expect("Failed to read line");
let guess: u32 = guess.trim().parse().expect("Please type a number!");
```

# 参考

- ![The Rust Programming Language](https://doc.rust-lang.org/book/ch01-02-hello-world.html#anatomy-of-a-rust-program)

```

```
