# AWS EC2でのデプロイガイド

## ☁️ AWS EC2

AWS EC2で本格的なサーバー運用を行う方法です。

### 前提条件

- AWSアカウント
- SSH接続の基本知識
- Claude APIキー

### 手順

#### 1. EC2インスタンスの作成

1. AWS Management Consoleにログイン
2. EC2サービスを選択
3. 「Launch Instance」をクリック

**推奨設定:**
- **AMI**: Ubuntu Server 22.04 LTS
- **Instance Type**: t3.micro（無料枠）または t3.small
- **Security Group**: HTTP(80), HTTPS(443), SSH(22)を許可
- **Storage**: 20GB以上

#### 2. SSH接続

```bash
# キーペアを使用してSSH接続
ssh -i your-key.pem ubuntu@your-ec2-public-ip
```

#### 3. サーバーの初期設定

```bash
# システムアップデート
sudo apt update && sudo apt upgrade -y

# 必要なパッケージのインストール
sudo apt install -y docker.io docker-compose git nginx

# Dockerサービスの開始
sudo systemctl start docker
sudo systemctl enable docker

# ユーザーをdockerグループに追加
sudo usermod -aG docker ubuntu
```

#### 4. プロジェクトのデプロイ

```bash
# プロジェクトのクローン
git clone https://github.com/yourusername/reform-assistant.git
cd reform-assistant

# 環境変数の設定
cp .env.example .env
nano .env  # APIキーを設定

# Dockerでアプリケーションを起動
docker-compose up -d --build
```

#### 5. Nginxの設定（リバースプロキシ）

```bash
# Nginx設定ファイルを作成
sudo nano /etc/nginx/sites-available/reform-assistant
```

設定内容:
```nginx
server {
    listen 80;
    server_name your-domain.com;  # ドメインまたはIPアドレス

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# 設定を有効化
sudo ln -s /etc/nginx/sites-available/reform-assistant /etc/nginx/sites-enabled/
sudo nginx -t  # 設定テスト
sudo systemctl restart nginx
```

#### 6. SSL証明書の設定（Let's Encrypt）

```bash
# Certbotのインストール
sudo apt install -y certbot python3-certbot-nginx

# SSL証明書の取得
sudo certbot --nginx -d your-domain.com

# 自動更新の設定
sudo crontab -e
# 以下の行を追加:
# 0 12 * * * /usr/bin/certbot renew --quiet
```

### セキュリティ設定

#### ファイアウォールの設定

```bash
# UFWの有効化
sudo ufw enable

# 必要なポートを開放
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
```

#### 自動アップデート

```bash
# 自動セキュリティアップデートの設定
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

### 監視とメンテナンス

#### ログの確認

```bash
# アプリケーションログ
docker-compose logs -f

# Nginxログ
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

#### バックアップ

```bash
# データベースのバックアップ
docker-compose exec reform-assistant cp /app/src/database/app.db /app/backup/

# 定期バックアップの設定
sudo crontab -e
# 以下の行を追加:
# 0 2 * * * cd /home/ubuntu/reform-assistant && docker-compose exec reform-assistant cp /app/src/database/app.db /app/backup/backup-$(date +\%Y\%m\%d).db
```

### 料金目安

- **t3.micro**: 月約10ドル（無料枠利用時は無料）
- **t3.small**: 月約20ドル
- **ストレージ**: 20GB で月約2ドル

### トラブルシューティング

**アプリケーションが起動しない:**
```bash
docker-compose logs
```

**Nginxエラー:**
```bash
sudo nginx -t
sudo systemctl status nginx
```

**ポート接続エラー:**
- セキュリティグループの設定を確認
- UFWの設定を確認

