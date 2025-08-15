# Vercelでのデプロイガイド

## 🌟 Vercel（推奨）

Vercelは最も簡単で高速なデプロイ方法です。

### 前提条件

- GitHubアカウント
- Vercelアカウント（無料）
- Claude APIキー

### 手順

#### 1. GitHubリポジトリの準備

```bash
# 新しいリポジトリを作成
git init
git add .
git commit -m "Initial commit"

# GitHubにプッシュ
git remote add origin https://github.com/yourusername/reform-assistant.git
git push -u origin main
```

#### 2. Vercelでのプロジェクト作成

1. [Vercel](https://vercel.com)にログイン
2. 「New Project」をクリック
3. GitHubリポジトリを選択
4. 「Import」をクリック

#### 3. ビルド設定

**Framework Preset**: Other
**Root Directory**: `./`
**Build Command**: `pip install -r requirements.txt`
**Output Directory**: `src/static`
**Install Command**: `pip install -r requirements.txt`

#### 4. 環境変数の設定

「Environment Variables」セクションで以下を追加:

- **Name**: `ANTHROPIC_API_KEY`
- **Value**: `sk-ant-your-api-key-here`

#### 5. デプロイ

「Deploy」ボタンをクリックして完了！

### カスタムドメインの設定

1. Vercelダッシュボードでプロジェクトを選択
2. 「Settings」→「Domains」
3. カスタムドメインを追加

### 自動デプロイ

GitHubにプッシュするたびに自動的にデプロイされます。

### トラブルシューティング

**ビルドエラーが発生する場合:**
- `requirements.txt` の内容を確認
- Python バージョンを確認（3.11推奨）

**APIが動作しない場合:**
- 環境変数 `ANTHROPIC_API_KEY` が正しく設定されているか確認
- APIキーの有効性を確認

