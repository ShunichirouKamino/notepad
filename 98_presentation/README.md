# Marp 利用 TIPS

## 必要なもの

- [Marp for VS Code](https://marketplace.visualstudio.com/items?itemName=marp-team.marp-vscode)
  - VSCode MARKETPLACE よりインストール

## 操作

- preview

  - マークダウンファイルを右クリックし、Open Preview を選択

- build
  - [marpteam/marp-cli](https://hub.docker.com/r/marpteam/marp-cli/)にて提供される marp 公式 Docker イメージを利用
  - ビルド時基本構文
    - `docker run --rm --init -v $PWD:/home/marp/app/ -e LANG=$LANG marpteam/marp-cli slide.md --pdf`
    -
