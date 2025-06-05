# MIRRALISM V2 Docker環境
FROM python:3.9-slim

# システム依存関係のインストール
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 作業ディレクトリ設定
WORKDIR /app

# 依存関係のインストール（キャッシュ効率化）
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# アプリケーションコードコピー
COPY . .

# 環境変数設定
ENV PYTHONPATH=/app
ENV MIRRALISM_ENV=docker

# デフォルトコマンド（CI/CD用）
CMD ["python3", "-m", "pytest", "tests/", "-v", "--tb=short"]
