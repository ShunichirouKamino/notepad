# blog

<!-- @import "[TOC]" {cmd="toc" depthFrom=1 depthTo=6 orderedList=false} -->

<!-- code_chunk_output -->

- [blog](#blog)
- [GKE](#gke)
- [AWS](#aws)
- [k8s](#k8s)
- [マイクロサービス](#マイクロサービス)
- [CI/CD](#cicd)
- [Other](#other)

<!-- /code_chunk_output -->

# GKE

- [Autopilot](https://medium.com/google-cloud-jp/gke-autopilot-87f8458ccf74)

# AWS

- [AWS のグローバル IP の空間はインターネットなのか？](https://tech.nri-net.com/entry/2021/05/10/085654#:~:text=%E3%81%84%E3%81%84%E3%81%88%E3%80%82,%E3%83%8D%E3%83%83%E3%83%88%E3%83%AF%E3%83%BC%E3%82%AF%E3%82%92%E4%BD%BF%E7%94%A8%E3%81%97%E3%81%BE%E3%81%99%E3%80%82)

# k8s

- [Istio - ZOZOTOWN](https://techblog.zozo.com/entry/zozotown-istio-production-ready?amp=1&__twitter_impression=true)

# マイクロサービス

- [AWS Startup ブログ](https://aws.amazon.com/jp/blogs/startup/techblog-microservices-introduction/)

# CI/CD

- [GitHub Actions ワークフローコマンド](https://docs.github.com/ja/actions/reference/workflow-commands-for-github-actions)
  - 後続ステップに値を渡したい際に`set-output`コマンドを利用
    - `echo "::set-output name=NAME::VALUE"`にて後続に渡す値を指定
    - set-output が属するブロックには、必ず任意の id 要素として、`id: ANY`を指定
    - 利用する際は、`${{ steps.ANY.outputs.NAME }}`にて`VALUE`を取り出すことが可能

# Other

- [Marp](https://zenn.dev/gakin/articles/set_up_marp_on_github_actions)
- [公開鍵暗号と電子署名の基礎知識](https://qiita.com/kunichiko/items/ef5efdb41611d6cf7775)
- [使用中グローバルIPアドレス確認](https://www.cman.jp/network/support/go_access.cgi)
