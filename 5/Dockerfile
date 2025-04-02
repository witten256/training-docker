# ビルドステージ
FROM golang:latest AS builder

WORKDIR /app

COPY ./app /app/

# goモジュールを初期化し、必要なライブラリをインストール、ソースをコンパイル
RUN go mod init hello-app && \
    go get github.com/gin-gonic/gin && \
    go build -o hello-app

# 実行ステージ
FROM alpine:latest

RUN apk add --no-cache libc6-compat

WORKDIR /root/

COPY --from=builder /app/hello-app .

CMD ["./hello-app"]
