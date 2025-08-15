# Google Cloud Runでのデプロイガイド

## 🌐 Google Cloud Run

Google Cloud Runはサーバーレスでスケーラブルなコンテナプラットフォームです。

### 前提条件

- Google Cloudアカウント
- Google Cloud SDK（gcloud）
- Claude APIキー

### 手順

#### 1. Google Cloud SDKのセットアップ

```bash
# Google Cloud SDKのインストール（Ubuntu/Debian）
curl https://sdk.cloud.google.com | bash
exec -l $SHELL

# 認証
gcloud auth login

# プロジェクトの設定
gcloud config set project your-project-id

# 必要なAPIの有効化
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
```

#### 2. プロジェクトの準備

```bash
# プロジェクトディレクトリに移動
cd reform-assistant-deploy

# Cloud Build用の設定ファイルを作成
```

`cloudbuild.yaml` を作成:
```yaml
steps:
  # Docker イメージをビルド
  - name: 'gcr.io/cloud-builders/docker'
    args: ['build', '-t', 'gcr.io/$PROJECT_ID/reform-assistant', '.']
  
  # Container Registry にプッシュ
  - name: 'gcr.io/cloud-builders/docker'
    args: ['push', 'gcr.io/$PROJECT_ID/reform-assistant']
  
  # Cloud Run にデプロイ
  - name: 'gcr.io/cloud-builders/gcloud'
    args:
    - 'run'
    - 'deploy'
    - 'reform-assistant'
    - '--image'
    - 'gcr.io/$PROJECT_ID/reform-assistant'
    - '--region'
    - 'asia-northeast1'
    - '--platform'
    - 'managed'
    - '--allow-unauthenticated'
    - '--set-env-vars'
    - 'ANTHROPIC_API_KEY=$$ANTHROPIC_API_KEY'
    secretEnv: ['ANTHROPIC_API_KEY']

availableSecrets:
  secretManager:
  - versionName: projects/$PROJECT_ID/secrets/anthropic-api-key/versions/latest
    env: 'ANTHROPIC_API_KEY'
```

#### 3. Secret Managerでの環境変数設定

```bash
# APIキーをSecret Managerに保存
echo "sk-ant-your-api-key-here" | gcloud secrets create anthropic-api-key --data-file=-

# Cloud Buildサービスアカウントに権限を付与
gcloud secrets add-iam-policy-binding anthropic-api-key \
    --member="serviceAccount:$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')@cloudbuild.gserviceaccount.com" \
    --role="roles/secretmanager.secretAccessor"
```

#### 4. デプロイ

```bash
# Cloud Buildでビルドとデプロイを実行
gcloud builds submit --config cloudbuild.yaml
```

または手動でのデプロイ:

```bash
# イメージをビルドしてプッシュ
gcloud builds submit --tag gcr.io/your-project-id/reform-assistant

# Cloud Runにデプロイ
gcloud run deploy reform-assistant \
  --image gcr.io/your-project-id/reform-assistant \
  --platform managed \
  --region asia-northeast1 \
  --allow-unauthenticated \
  --set-env-vars ANTHROPIC_API_KEY=your-api-key
```

#### 5. カスタムドメインの設定

```bash
# ドメインマッピングの作成
gcloud run domain-mappings create \
  --service reform-assistant \
  --domain your-domain.com \
  --region asia-northeast1
```

### 料金

Cloud Runは使用量ベースの課金:
- **CPU**: vCPU時間あたり約0.000024ドル
- **メモリ**: GB時間あたり約0.0000025ドル
- **リクエスト**: 100万リクエストあたり0.40ドル
- **無料枠**: 月200万リクエスト、36万vCPU秒、72万GB秒

### 特徴

- **自動スケーリング**: 0から1000インスタンスまで
- **サーバーレス**: インフラ管理不要
- **高可用性**: 99.95%のSLA
- **グローバル**: 世界中のリージョンで利用可能

### 監視とログ

```bash
# ログの確認
gcloud run services logs read reform-assistant --region asia-northeast1

# リアルタイムログ
gcloud run services logs tail reform-assistant --region asia-northeast1
```

### CI/CDの設定

GitHub Actionsとの連携:

`.github/workflows/deploy.yml`:
```yaml
name: Deploy to Cloud Run

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    
    steps:
    - uses: actions/checkout@v2
    
    - id: 'auth'
      uses: 'google-github-actions/auth@v1'
      with:
        credentials_json: '${{ secrets.GCP_SA_KEY }}'
    
    - name: 'Set up Cloud SDK'
      uses: 'google-github-actions/setup-gcloud@v1'
    
    - name: 'Build and Deploy'
      run: |
        gcloud builds submit --config cloudbuild.yaml
```

### トラブルシューティング

**デプロイが失敗する場合:**
```bash
# ビルドログの確認
gcloud builds log [BUILD_ID]
```

**アプリケーションエラー:**
```bash
# サービスログの確認
gcloud run services logs read reform-assistant --region asia-northeast1 --limit 50
```

**権限エラー:**
- IAMロールの確認
- Secret Managerの権限確認

