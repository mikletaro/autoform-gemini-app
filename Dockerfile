# Playwright Python公式イメージ（最新の推奨タグにしてください）
FROM mcr.microsoft.com/playwright/python:v1.42.0-jammy

WORKDIR /app

# 必要なファイルをコピー
COPY requirements.txt requirements.txt
COPY . .

# 依存関係インストール
RUN pip install --no-cache-dir -r requirements.txt

# アプリ起動コマンド
CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--port=10000"]
