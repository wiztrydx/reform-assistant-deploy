# リフォーム提案アシスタント - 独自デプロイ版

Manusウォーターマークなしで独自サーバーにデプロイできるバージョンです。

## 🚀 クイックスタート

### 1. 環境変数の設定

```bash
cp .env.example .env
# .envファイルを編集してAPIキーを設定
```

### 2. Dockerでの起動

```bash
# ビルドと起動
docker-compose up --build

# バックグラウンドで起動
docker-compose up -d --build
```

### 3. アクセス

ブラウザで `http://localhost:5000` にアクセス

## 📦 各種ホスティングサービスでのデプロイ

### Vercel (推奨)

1. GitHubリポジトリにプッシュ
2. Vercelでリポジトリを連携
3. 環境変数 `ANTHROPIC_API_KEY` を設定
4. デプロイ

### Netlify

1. GitHubリポジトリにプッシュ
2. Netlifyでリポジトリを連携
3. ビルドコマンド: `pip install -r requirements.txt`
4. 公開ディレクトリ: `src/static`
5. 環境変数 `ANTHROPIC_API_KEY` を設定

### Railway

1. GitHubリポジトリにプッシュ
2. Railwayでリポジトリを連携
3. 環境変数 `ANTHROPIC_API_KEY` を設定
4. 自動デプロイ

### Render

1. GitHubリポジトリにプッシュ
2. Renderでリポジトリを連携
3. サービスタイプ: Web Service
4. ビルドコマンド: `pip install -r requirements.txt`
5. 開始コマンド: `python src/main.py`
6. 環境変数 `ANTHROPIC_API_KEY` を設定

### AWS EC2

```bash
# EC2インスタンスにSSH接続
ssh -i your-key.pem ubuntu@your-ec2-ip

# Dockerのインストール
sudo apt update
sudo apt install docker.io docker-compose -y
sudo systemctl start docker
sudo systemctl enable docker

# プロジェクトのクローン
git clone your-repository-url
cd reform-assistant-deploy

# 環境変数の設定
cp .env.example .env
nano .env  # APIキーを設定

# 起動
sudo docker-compose up -d --build
```

### Google Cloud Run

```bash
# Google Cloud SDKの設定
gcloud auth login
gcloud config set project your-project-id

# コンテナのビルドとプッシュ
gcloud builds submit --tag gcr.io/your-project-id/reform-assistant

# デプロイ
gcloud run deploy reform-assistant \
  --image gcr.io/your-project-id/reform-assistant \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your-api-key
```

## 🔧 カスタマイズ

### フロントエンドの変更

1. `reform-assistant-frontend` ディレクトリで変更を行う
2. ビルド: `pnpm run build`
3. ビルド済みファイルを `src/static/` にコピー

### バックエンドの変更

`src/` ディレクトリ内のPythonファイルを直接編集

## 📁 プロジェクト構成

```
reform-assistant-deploy/
├── Dockerfile              # Dockerコンテナ設定
├── docker-compose.yml      # Docker Compose設定
├── requirements.txt        # Python依存関係
├── .env.example           # 環境変数サンプル
├── src/
│   ├── main.py            # メインアプリケーション
│   ├── routes/            # APIルート
│   │   └── chat.py        # チャット機能
│   └── static/            # フロントエンドファイル
│       ├── index.html
│       ├── assets/
│       └── ...
└── README.md
```

## 🔒 セキュリティ

- APIキーは環境変数で管理
- HTTPS通信を推奨
- 定期的なセキュリティアップデート

## 🆘 トラブルシューティング

### ポート5000が使用中の場合

`docker-compose.yml` の `ports` を変更:
```yaml
ports:
  - "8080:5000"  # 8080ポートでアクセス
```

### APIキーエラー

1. `.env` ファイルの確認
2. 環境変数の設定確認
3. APIキーの有効性確認

## 📞 サポート

技術的な問題が発生した場合は、GitHubのIssuesでお知らせください。

