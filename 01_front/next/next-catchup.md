# Next キャッチアップ資料

===

## 開発環境

README のバージョンよりも上げてますが動きました。

yarn 含めすべてグローバルインストール

```console
PS D:\workspace\my-hooks> $ npm -v
8.2.0
PS D:\workspace\my-hooks> $ node -v
v16.13.1
PS D:\workspace\my-hooks> $ yarn -v
1.22.17
```

## ランタイムツール

pm2 の docker コンテナ動作用ランタイム、[pm2-runtime](https://github.com/ISID/m-sherpa-frontend/blob/develop/docker/Sherpa_Frontend_Dockerfile#L49)

**起動方法**

- `$ yarn add -D pm2`
- `$ pm2-runtime start pm2.config.json --env $ENV`

[pm2.config.json](https://github.com/ISID/m-sherpa-frontend/blob/develop/pm2.config.json)

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

## ディレクトリ構成

## テスト

- テストツール
- テスト方法
  - 起動方法、デバッグ方法
  - サーバサイドどうしてる？モック？結合？

## API コール用のソース生成

## ルーティング

[next/router](https://github.com/ISID/m-sherpa-frontend/blob/develop/src/pages/[companyId]/faq/search/index.tsx#L10) 使ってそう。静的ページは[Link](https://nextjs.org/docs/api-reference/next/link) じゃない？

## エラーメッセージ

## datastore の利用有無

## 静的ページ

- 静的ページ利用箇所
- 静的ページ実装方法

## CSS フレームワーク

## フロントで管理する Enum

## その他分からん

- injectable てなに
- [server/config/saml.pem](https://github.com/ISID/m-sherpa-frontend#%E3%82%B5%E3%83%BC%E3%83%90%E3%82%B5%E3%82%A4%E3%83%89%E5%87%A6%E7%90%86%E3%81%AB%E9%96%A2%E3%81%99%E3%82%8B%E7%92%B0%E5%A2%83%E8%A8%AD%E5%AE%9A%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%AE%E9%85%8D%E7%BD%AE)の利用

## 参考

- [nextjs.org](https://nextjs.org/)
