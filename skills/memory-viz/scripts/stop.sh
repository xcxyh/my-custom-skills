#!/bin/bash

# Memory Viz Stop Script
# 停止记忆可视化服务

echo "🛑 停止记忆可视化服务..."

# 查找并停止进程
if pgrep -f "node.*server.js" > /dev/null; then
    pkill -f "node.*server.js"
    sleep 1

    # 再次检查
    if pgrep -f "node.*server.js" > /dev/null; then
        echo "⚠️  服务仍在运行，尝试强制停止..."
        pkill -9 -f "node.*server.js"
        sleep 1
    fi

    if ! pgrep -f "node.*server.js" > /dev/null; then
        echo "✅ 服务已停止"
    else
        echo "❌ 无法停止服务"
        exit 1
    fi
else
    echo "⚠️️  服务未运行"
fi
