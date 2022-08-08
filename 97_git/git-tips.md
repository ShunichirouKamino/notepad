## 初期リポジトリとローカルリポジトリの紐づけ

- リモートにて任意のリポジトリ作成
- `$ git remote add origin リモートURL`
- `$ git push -f origin main`

※branch 名称が master の場合、`$ git branch -M main`にて変更しておく

## リモートで削除されているブランチをローカルでも削除

- dry-runにて対象を確認
  - `$ git remote prune origin --dry-run`
- prune
  - `$ git remote prune origin`
