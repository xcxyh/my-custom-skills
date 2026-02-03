#!/bin/bash

# Front Design Deploy Script
# 部署静态网页到本地服务器

PROJECT_NAME="$1"
WWW_DIR="/root/clawd/www"
SERVER_DIR="/var/www/html"
PORT="8080"

if [ -z "$PROJECT_NAME" ]; then
    echo "Usage: $0 <project-name>"
    exit 1
fi

PROJECT_PATH="$WWW_DIR/$PROJECT_NAME"

if [ ! -d "$PROJECT_PATH" ]; then
    echo "Error: Project directory not found: $PROJECT_PATH"
    exit 1
fi

# 创建服务器目录
sudo mkdir -p "$SERVER_DIR"

# 复制项目到服务器目录
sudo cp -r "$PROJECT_PATH" "$SERVER_DIR/"

# 检查并启动简单的 HTTP 服务器
if ! pgrep -f "python3 -m http.server $PORT" > /dev/null; then
    echo "Starting HTTP server on port $PORT..."
    cd "$SERVER_DIR" && nohup python3 -m http.server $PORT > /dev/null 2>&1 &
    sleep 2
fi

# 获取本机 IP
IP=$(hostname -I | awk '{print $1}')

echo "✅ Deployment successful!"
echo "📁 Project: $PROJECT_NAME"
echo "🌐 URL: http://$IP:$PORT/$PROJECT_NAME/"
echo ""
echo "Note: If accessing from external network, ensure port $PORT is open."
