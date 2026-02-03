---
name: memory-viz
description: 记忆可视化技能，提供街溜子记忆的实时 Web 可视化界面。
---

# Memory Viz

## 功能

提供街溜子记忆的实时 Web 可视化界面，可以：
- 查看所有记忆文件（Markdown 和 JSON）
- 实时统计数据（文件数、字数、大小、更新最后时间）
- 点击文件查看详细内容
- 自动刷新（每 30 秒）
- 精美的深色渐变界面

## 使用方法

### 启动可视化服务

```bash
bash /root/clawd/skills/memory-viz/scripts/start.sh
```

### 停止服务

```bash
bash /root/clawd/skills/memory-viz/scripts/stop.sh
```

### 检查服务状态

```bash
bash /root/clawd/skills/memory-viz/scripts/status.sh
```

## 访问地址

启动后，通过以下地址访问：

**本地访问：**
- http://localhost:3001
- http://127.0.0.1:3001

**内网访问：**
- http://172.31.0.2:3001

## 技术栈

- **后端：** Node.js + Express
- **前端：** HTML5 + Tailwind CSS + Vanilla JavaScript
- **Markdown 渲染：** Marked.js
- **自动刷新：** 每 30 秒

## 项目结构

```
/root/clawd/www/memory-viz/
├── index.html          # 前端页面
├── server.js           # 后端 API 服务器
├── package.json        # Node.js 依赖
└── server.log          # 服务器日志
```

## API 端点

- `GET /api/memory` - 获取所有记忆文件
- `GET /api/memory/:filename` - 获取单个文件内容
- `GET /api/memory-main` - 获取 MEMORY.md 内容

## 注意事项

- 服务默认运行在 3001 端口
- 需要安装 Node.js 和 npm
- 首次使用会自动安装依赖（express, cors）
- 服务会自动后台运行，日志写入 server.log

## 示例

```bash
# 启动服务
bash /root/clawd/skills/memory-viz/scripts/start.sh

# 检查状态
bash /root/clawd/skills/memory-viz/scripts/status.sh

# 访问
# 打开浏览器访问 http://172.31.0.2:3001
```
