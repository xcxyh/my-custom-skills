# Clawdbot Memory Visualization Plugin

## 简介

这是一个 Clawdbot 插件，用于在 Control UI 中可视化街溜子的记忆文件。

## 功能

- 📊 实时统计记忆文件数量、字数、大小
- 📝 查看 Markdown 和 JSON 文件内容
- 🔄 自动刷新（每 30 秒）
- 🎨 精美的深色渐变界面

## 安装

### 方法 1：作为独立服务运行

```bash
cd /root/clawd/plugins/memory-viz-plugin
npm install
npm start
```

访问：http://localhost:3001

### 方法 2：集成到 Clawdbot Control UI

1. 将插件目录复制到 Clawdbot plugins 目录：
```bash
cp -r /root/clawd/plugins/memory-viz-plugin /usr/lib/node_modules/clawdbot/plugins/
```

2. 重启 Clawdbot Gateway：
```bash
clawdbot gateway restart
```

3. 打开 Control UI：
```bash
clawdbot dashboard
```

## 配置

在 `clawdbot.plugin.json` 中可以配置：

- `enabled`: 是否启用（默认 true）
- `autoRefresh`: 自动刷新间隔秒数（默认 30）
- `port`: 服务端口（默认 3001）

## API 端点

- `GET /api/memory` - 获取所有记忆文件
- `GET /api/memory/:filename` - 获取单个文件
- `GET /api/memory-main` - 获取 MEMORY.md
- `GET /health` - 健康检查

## 环境变量

- `MEMORY_VIZ_PORT`: 服务端口（默认 3001）
- `MEMORY_DIR`: 记忆目录（默认 /root/clawd/memory）
- `WORKSPACE_DIR`: 工作空间目录（默认 /root/clawd）

## 开发

```bash
# 安装依赖
npm install

# 启动开发服务器
npm start

# 在另一个终端测试
curl http://localhost:3001/health
curl http://localhost:3001/api/memory
```

## 许可证

MIT
