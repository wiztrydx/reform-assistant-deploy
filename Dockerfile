# Python 3.11をベースイメージとして使用
FROM python:3.11-slim

# 作業ディレクトリを設定
WORKDIR /app

# システムパッケージの更新とインストール
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Pythonの依存関係をコピーしてインストール
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションファイルをコピー
COPY src/ ./src/

# ポート5000を公開
EXPOSE 5000

# 環境変数を設定
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production

# アプリケーションを起動
CMD ["python", "src/main.py"]

