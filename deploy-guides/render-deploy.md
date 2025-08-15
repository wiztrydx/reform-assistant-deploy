# Renderでのデプロイガイド

## 🎨 Render

Renderは使いやすく信頼性の高いクラウドプラットフォームです。

### 前提条件

- GitHubアカウント
- Renderアカウント（無料枠あり）
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

#### 2. Renderでのサービス作成

1. [Render](https://render.com)にログイン
2. 「New」→「Web Service」をクリック
3. GitHubリポジトリを選択
4. 「Connect」をクリック

#### 3. サービス設定

**基本設定:**
- **Name**: `reform-assistant`
- **Region**: `Oregon (US West)`
- **Branch**: `main`
- **Runtime**: `Docker`

**ビルド設定:**
- **Build Command**: 自動検出（Dockerfileを使用）
- **Start Command**: 自動検出

#### 4. 環境変数の設定

「Environment」セクションで以下を追加:

```
ANTHROPIC_API_KEY=sk-ant-your-api-key-here
```

#### 5. デプロイ

「Create Web Service」をクリックしてデプロイ開始！

### 料金プラン

- **Free Plan**: 
  - 750時間/月まで無料
  - 512MB RAM
  - 自動スリープ機能

- **Starter Plan**: 月7ドル
  - 常時稼働
  - 1GB RAM

### 特徴

- 自動SSL証明書
- 継続的デプロイ
- 簡単なスケーリング
- PostgreSQL、Redis対応

### カスタムドメインの設定

1. 「Settings」→「Custom Domains」
2. ドメインを追加
3. DNS設定を更新

### トラブルシューティング

**ビルドが失敗する場合:**
- Dockerfileの構文を確認
- ログを確認（Renderダッシュボード）

**アプリが503エラーを返す場合:**
- ポート設定を確認（5000番ポート）
- 環境変数の設定を確認

**無料プランでスリープする場合:**
- 有料プランにアップグレード
- または定期的なヘルスチェックを設定

