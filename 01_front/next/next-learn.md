# Next 学習ノート

===

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [Next 学習ノート](#next-学習ノート)
  - [⭐ 用語の整理](#用語の整理)
    - [ビルド・デプロイ関連](#ビルドデプロイ関連)

<!-- /code_chunk_output -->

yarn 含めすべてグローバルインストール

```console
PS D:\workspace\my-hooks> $ npm -v
8.2.0
PS D:\workspace\my-hooks> $ node -v
v16.13.1
PS D:\workspace\my-hooks> $ yarn -v
1.22.17
```

以降の手順

- `npx create-react-app my-hooks --user-npm`
  - 初期 React アプリのテンプレを構築する。プロキシ下のみ`--user-npm`が必要
- `npm install @material-ui/core`
  - [material-ui](https://material-ui.com/ja/)のインストール
- `npm start`
  - [localhost:3000](localhost:3000)にアクセスすることで React アプリ起動

## ⭐ 用語の整理

### ビルド・デプロイ関連

- pm2
  エラーが発生した際に落ちる Node サーバを落ちないようにする。
  なお docker コンテナ内で利用するには docker コンテナ用に設計された`pm2-runtime`を利用することで、Node サーバの起動共にコンテナを起動し続ける。

**起動方法**

- `$ yarn add -D pm2`
- `$ pm2-runtime start pm2.config.json --env $ENV`

**pm2.config.json**

```json
{
  "name": "app",
  "script": "./node_modules/next/dist/bin/next",
  "args": ["start", "-p", "80"],
  "env_development": {
    "NODE_ENV": "dev"
  },
  "env_production": {
    "NODE_ENV": "prod"
  },
  "log-date-format": "YYYY-MM-DD HH:mm Z",
  "exp_backoff_restart_delay": 100
}
```
