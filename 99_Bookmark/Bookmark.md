# blog

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [blog](#blog)
- [GKE](#gke)
- [AWS](#aws)
- [k8s](#k8s)
- [マイクロサービス](#マイクロサービス)
- [Java](#java)
- [CI/CD](#cicd)
- [フロントエンド](#フロントエンド)
- [Other](#other)

<!-- /code_chunk_output -->

# GKE

- [Autopilot](https://medium.com/google-cloud-jp/gke-autopilot-87f8458ccf74)
  - GKE 実行モードとして、Control Plain のみでなく Node もマネージドになるサービス。
  - Standard では Node 単位に課金されていたが、Pod 単位で課金となる。
  - Node 数は Pod のスケジューリングに合わせて自動でプロビジョニングされる。
  - サービスアカウントへの接続はできないが、デフォルトで Workload Identity が有効となっている。

# AWS

- [AWS のグローバル IP の空間はインターネットなのか？](https://tech.nri-net.com/entry/2021/05/10/085654#:~:text=%E3%81%84%E3%81%84%E3%81%88%E3%80%82,%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%BE%E3%81%99%E3%80%82)

# k8s

- [Istio - ZOZOTOWN](https://techblog.zozo.com/entry/zozotown-istio-production-ready?amp=1&__twitter_impression=true)
  - サービスメッシュ（マイクロサービスを実装する人が、ビジネスロジックに集中できることを目指す手法）を実現するフレームワーク Istio のプロダクションでの動作実績の紹介。
  - Envoy 等共通機能をサイドカーとしてどのように各 Pod に組み込んでいくか？や運用監視に利用するツールなどの紹介。
- [あなたの知らない Kubernetes の Service の仕組み](https://eng-blog.iij.ad.jp/archives/9998)
  - Service は、クラスタ内部通信のロードバランサに対して、Service から Pod のエンドポイントの通信経路を設定するためのリソースである。
  - 別の Pod からこの Service へアクセスするために、クラスタ内部権威 DNS に A レコードが追記される。つまり、ホスト名でアクセスが可能となる。
  - ヘッドレスサービスは、DNS の A レコードに登録される IP アドレスが Pod の IP アドレスそのものになるサービス提供形態。通常は Service に IP アドレスと Pod のホスト名が A レコードに登録されるため、Service の IP アドレスによってロードバランシングされる。
  - ヘッドレスサービスは、StatefulSet のように永続的なデータを保持したロードバランシングされたくないリソースへのアクセスに利用される。

# マイクロサービス

- [AWS Startup ブログ](https://aws.amazon.com/jp/blogs/startup/techblog-microservices-introduction/)

# Java

- [コンテナ時代における最新の Java&JVM 監視](https://b.chiroito.dev/entry/2021/06/23/163430)
  - k8s 上で動作する Java アプリの監視手法としては、Elasticsearch+Kibana や Prometheus+Grafana などが挙げられる。
  - Cryostat を利用して、コンテナ上で JFR を利用した監視をおこなう手法の紹介。

# CI/CD

- [GitHub Actions ワークフローコマンド](https://docs.github.com/ja/actions/reference/workflow-commands-for-github-actions)
  - 後続ステップに値を渡したい際に`set-output`コマンドを利用
    - `echo "::set-output name=NAME::VALUE"`にて後続に渡す値を指定
    - set-output が属するブロックには、必ず任意の id 要素として、`id: ANY`を指定
    - 利用する際は、`${{ steps.ANY.outputs.NAME }}`にて`VALUE`を取り出すことが可能

# フロントエンド

- [React の新しい状態管理ライブラリ「Recoil」とは？ Redux との違いを解説](https://ics.media/entry/210224/)
- [【LINE 証券 FrontEnd】Recoil を使って安全快適な状態管理を手に入れた話](https://engineering.linecorp.com/ja/blog/line-sec-frontend-using-recoil-to-get-a-safe-and-comfortable-state-management/)

  - これまでグローバルな状態管理について、Redux で行っていることが多かった。デメリットとして、グローバルな状態に対して非同期な処理の実装が複雑になることなどが課題となっていた。
  - Hook の登場、具体的には ContextAPI の登場により、useContext ＋ useState（useReducer）を利用することで、プレーンな React のみで Redux と同等の状態管理が行えるようになった。具体的には、トップコンポーネントからグローバルなコンテキストをプロバイドすることで、下位コンポーネントが階層を跨いでグローバルな状態にアクセスが可能となっていた。
  - ContextAPI は、あくまでツリーであるため、Context を変更してしまうとスコープ化にあるツリー下位のコンポーネント全てが再計算されてしまうデメリットがあった。
  - Recoil は facebook 製の状態管理ライブラリであり、状態を管理する「Atoms」と状態を変更する「Selectors」から成る。

- [Deno には WebAssembly がある](https://www.infoq.com/jp/articles/deno-loves-webassembly/)
  - Node.js では、複雑な npm, node_modules によるライブラリ管理があったが、これが不要に。自身のリポジトリに直接ライブラリを保有することがなくなる。
  - 同様に、package.json での複雑なバージョン管理も不要となる。
  - Node.js では外部ライブラリを複数の人が開発し、エコシステムとしては素晴らしいがディペンデンシーが複雑になる傾向に。Deno では標準ライブラリに多くの機能が実装されている。
  - TypeScript とも相性がいい。
  - asserts 機能も標準となるため、テストも簡単。

# Other

- [Marp](https://zenn.dev/gakin/articles/set_up_marp_on_github_actions)
  - マークダウンからパワポを作成するライブラリ
- [公開鍵暗号と電子署名の基礎知識](https://qiita.com/kunichiko/items/ef5efdb41611d6cf7775)
- [2021 年のエンジニア新人研修の講義資料を公開しました](https://blog.cybozu.io/entry/2021/07/20/100000)
  - Cybozu 新人研修資料 2021
- [Isoflow](https://isoflow.io/)
- [立体的な表現で見やすいネットワーク図がブラウザ上で作成できる「Isoflow」](https://gigazine.net/news/20210722-isoflow/)
  - 視覚的に理解しやすいアイソメトリック図を記載、共有ができるツール
  - 無料版では設置ノード 8 個・保存プロジェクトは 3 件の制約
- [使用中グローバル IP アドレス確認](https://www.cman.jp/network/support/go_access.cgi)
- [資料で使う技術/プロダクトロゴのリンク集](https://qiita.com/tkit/items/932316c5f5f7b162b61e)
- [material.io](https://material.io/)
