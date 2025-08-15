# Railway デプロイ手順

## 前提条件
- GitHubアカウント
- Railwayアカウント（https://railway.app でサインアップ）
- Anthropic APIキー（https://console.anthropic.com/settings/keys）

## デプロイ手順

### 1. GitHubリポジトリの準備

```bash
# 変更をコミット
git add .
git commit -m "Add Railway deployment configuration"

# GitHubにプッシュ（リポジトリを作成済みの場合）
git push origin main
```

### 2. Railwayでのデプロイ

1. [Railway](https://railway.app) にログイン

2. 「New Project」をクリック

3. 「Deploy from GitHub repo」を選択

4. GitHubアカウントを連携し、リポジトリを選択

5. 環境変数の設定：
   - プロジェクトダッシュボードで「Variables」タブをクリック
   - 「Add Variable」をクリック
   - 以下を追加：
     - Key: `ANTHROPIC_API_KEY`
     - Value: あなたのAnthropicAPIキー
   - 「Add Variable」をクリック

6. デプロイが自動的に開始されます

### 3. アプリケーションへのアクセス

1. デプロイ完了後、「Settings」タブに移動

2. 「Domains」セクションで「Generate Domain」をクリック

3. 生成されたURLでアプリケーションにアクセス可能

## カスタムドメイン（オプション）

1. 「Settings」→「Domains」
2. 「Add Custom Domain」をクリック
3. ドメインを入力し、DNSレコードを設定

## 自動デプロイ

GitHubのmainブランチにプッシュすると自動的にデプロイされます。

## トラブルシューティング

### デプロイが失敗する場合

1. ログを確認：
   - Railwayダッシュボードで「Deployments」タブ
   - 失敗したデプロイをクリック
   - ログを確認

2. よくある問題：
   - APIキーが設定されていない → 環境変数を確認
   - ポートエラー → RailwayはPORT環境変数を自動設定
   - ビルドエラー → requirements.txtを確認

### アプリケーションが起動しない場合

1. 環境変数 `ANTHROPIC_API_KEY` が正しく設定されているか確認
2. Procfileが正しく設定されているか確認
3. ログでエラーメッセージを確認

## 料金

- Railwayは月$5の無料枠があります
- 詳細: https://railway.app/pricing

## サポート

問題が発生した場合：
1. Railway Discord: https://discord.gg/railway
2. Railway Docs: https://docs.railway.app/