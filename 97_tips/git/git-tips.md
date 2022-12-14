## 初期リポジトリとローカルリポジトリの紐づけ

- リモートにて任意のリポジトリ作成
- `$ git remote add origin リモートURL`
- `$ git push -f origin main`

※branch 名称が master の場合、`$ git branch -M main`にて変更しておく

## リモートで削除されているブランチをローカルでも削除

- そもそもfetchの時点で削除する
  - `$ git fetch --prune`
- dry-runにて対象を確認
  - `$ git remote prune origin --dry-run`
- prune
  - `$ git remote prune origin`

## リモートリポジトリを手元のブランチに取得

- fetch
  - `$ git fetch origin feature/hogehoge`
- switch
  - `$ git checkout feature/hogehoge`

## APIコールしてIssueの取得
- 全件取得する例

`$ curl -u ":username" -H "Accept: application/vnd.github+json" -H "Authorization: Bearer hogehoge" "https://api.github.com/repos/ORG/REPO/issues?state=all&per_page=100&page=1" | jq -r '["number","title","html_url","state"], (.[] | [.number,.title,.html_url,.state]) | @csv' > issues_all_page1.csv`


