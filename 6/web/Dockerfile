FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
# それほど多くないが依存関係をrequirements.txtで管理
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# コンテナが使用するポートを明示するが、実際には使用時にcliやdockercomposeでも
# ポートを指定する必要がある。
EXPOSE 5000

CMD ["python", "app.py"]