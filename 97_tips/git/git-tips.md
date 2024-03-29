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
 
## 手元のファイルが更新済みである場合
以下エラーが出る。
> Please move or remove them before you merge.

- 作業ファイルをリセットしたい場合
  - `$ git clean -fd'
- 作業ファイルをリストアしたい場合
  - `$ git restore filename`
 
もしくはstash

## リモートリポジトリを手元のブランチに取得

- fetch
  - `$ git fetch origin feature/hogehoge`
- switch
  - `$ git checkout feature/hogehoge`

## APIコールしてIssueの取得
- 全件取得する例

`$ curl -u ":username" -H "Accept: application/vnd.github+json" -H "Authorization: Bearer hogehoge" "https://api.github.com/repos/ORG/REPO/issues?state=all&per_page=100&page=1" | jq -r '["number","title","html_url","state"], (.[] | [.number,.title,.html_url,.state]) | @csv' > issues_all_page1.csv`

## 初期リポジトリ作成からの流れ

- GUI上でリポジトリ作成
- ローカルで以下手順
  - $ git init
  - $ git add .
  - $ git commit -m 'first commit'
  - $ git remote add origin https://追加したいリポジトリ名
  - $ git push -u origin main

※originが存在してしまうと、以下エラー。

```
error: remote origin already exists.
```

- 以下コマンドで解消できる。
  - `$ git remote rm origin`

※初期リポジトリでREADMEを追加していると、pullを促された後に以下エラー。


```
fatal: refusing to merge unrelated histories
```

- 以下コマンドで解消できる。これは、自分のコミットログとは関係ないコミットを取り込むオプション。
  - `$ git merge --allow-unrelated-histories origin/main`
