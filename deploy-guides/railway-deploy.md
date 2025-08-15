# Railwayでのデプロイガイド

## 🚂 Railway

Railwayは簡単で高性能なクラウドプラットフォームです。

### 前提条件

- GitHubアカウント
- Railwayアカウント（無料枠あり）
- Claude APIキー

### 手順

#### 1. GitHubリポジトリの準備

```bash
# リポジトリをGitHubにプッシュ
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/yourusername/reform-assistant.git
git push -u origin main
```

#### 2. Railwayでのプロジェクト作成

1. [Railway](https://railway.app)にログイン
2. 「New Project」をクリック
3. 「Deploy from GitHub repo」を選択
4. リポジトリを選択

#### 3. 環境変数の設定

1. プロジェクトダッシュボードで「Variables」タブをクリック
2. 以下の環境変数を追加:

```
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
PORT=5000
```

#### 4. 自動デプロイ

Railwayが自動的にDockerfileを検出してデプロイします。

#### 5. カスタムドメインの設定（オプション）

1. 「Settings」→「Domains」
2. カスタムドメインを追加

### 料金

- **Starter Plan**: 月5ドルまで無料
- **Developer Plan**: 月20ドル

### 特徴

- 自動スケーリング
- 高速デプロイ
- 簡単な環境変数管理
- PostgreSQL、Redis等のアドオン対応

### トラブルシューティング

**デプロイが失敗する場合:**
- Dockerfileの構文を確認
- ポート設定を確認（5000番ポート）

**アプリが起動しない場合:**
- ログを確認（Railwayダッシュボード）
- 環境変数の設定を確認

