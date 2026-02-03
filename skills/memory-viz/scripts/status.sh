#!/bin/bash

# Memory Viz Status Script
# 检查记忆可视化服务状态

WWW_DIR="/root/clawd/www/memory-viz"
PORT=3001

echo "📊 记忆可视化服务状态"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 检查进程
if pgrep -f "node.*server.js" > /dev/null; then
    PID=$(pgrep -f "node.*server.js" | head -1)
    echo "✅ 状态: 运行中"
    echo "🔢 PID: $PID"
    echo "🌐 访问地址: http://172.31.0.2:$PORT"
    echo "📁 项目目录: $WWW_DIR"

    # 检查日志
    if [ -f "$WWW_DIR/server.log" ]; then
        LOG_SIZE=$(wc -l < "$WWW_DIR/server.log")
        echo "📝 日志文件: $WWW_DIR/server.log ($LOG_SIZE 行)"
    fi

    # 测试 API
    if curl -s "http://localhost:$PORT/api/memory" > /dev/null 2>&1; then
        echo "🔗 API: 正常"
    else
        echo "🔗 API: 异常"
    fi
else
    echo "❌ 状态: 未运行"
    echo "📁 项目目录: $WWW_DIR"
    echo ""
    echo "提示：使用 'bash /root/clawd/skills/memory-viz/scripts/start.sh' 启动服务"
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
