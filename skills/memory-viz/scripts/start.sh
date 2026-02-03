#!/bin/bash

# Memory Viz Start Script
# 启动记忆可视化服务

WWW_DIR="/root/clawd/www/memory-viz"
PORT=3001

echo "🚀 启动记忆可视化服务..."

# 检查目录是否存在
if [ ! -d "$WWW_DIR" ]; then
    echo "❌ 错误：项目目录不存在: $WWW_DIR"
    exit 1
fi

# 检查是否已经运行
if pgrep -f "node.*server.js" > /dev/null; then
    echo "⚠️  服务已在运行中"
    bash /root/clawd/skills/memory-viz/scripts/status.sh
    exit 0
fi

# 检查依赖
if [ ! -d "$WWW_DIR/node_modules" ]; then
    echo "📦 安装依赖..."
    cd "$WWW_DIR" && npm install express cors --silent
fi

# 启动服务
cd "$WWW_DIR" && nohup node server.js > server.log 2>&1 &

# 等待服务启动
sleep 2

# 检查是否启动成功
if pgrep -f "node.*server.js" > /dev/null; then
    echo "✅ 服务启动成功！"
    echo ""
    echo "📁 项目目录: $WWW_DIR"
    echo "🌐 访问地址: http://172.31.0.2:$PORT"
    echo "📝 日志文件: $WWW_DIR/server.log"
    echo ""
    echo "提示：使用 'bash /root/clawd/skills/memory-viz/scripts/status.sh' 查看状态"
else
    echo "❌ 服务启动失败，请查看日志: $WWW_DIR/server.log"
    exit 1
fi
