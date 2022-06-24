## レビュー観点

### TypeScript

- ParseInt / ParseFloat を使わず、Number()を利用する。
  - http://nmi.jp/2022-02-03-dont-use-parseInt
- `+`オペランドの利用有無、Number()としたときに対象が str であるか


### AWS バッチ

- イベントの手動／定期自動実行についてはEventBridgeよりキック。
- 15分超える以下の場合LambdaではなくECS（Fargate）。AWS Batchは負荷がより大きい場合。
  - 設定自体は、例えばECSのタスクスケジュールで行い、実行結果はAmazon EventBridgeで確認するイメージ
- 依存関係制御が有る場合はStep Functions
- [AWS Step Functions が AWS SDK 統合で 200 を超える AWS のサービスのサポートを追加](https://aws.amazon.com/jp/about-aws/whats-new/2021/09/aws-step-functions-200-aws-sdk-integration/)
  - Lambdaを介して各AWSサービスを呼び出していた手間が不要になる
- [アップデート]Step Functions Workflow Studioがリリースされて、ワークフロー作成が簡単になりました](https://dev.classmethod.jp/articles/stepfunctions-workflow-designer/)
  - GUIによるワークフロー作成
