# Memory Viz Plugin

街溜子记忆可视化插件 - 一个优雅的 Web 界面，用于查看和管理 Clawdbot 的记忆文件。

## ✨ 功能特性

- 📁 **文件浏览** - 查看 memory 目录下的所有文件
- 📝 **内容预览** - 支持 Markdown 和 JSON 格式
- 🔄 **实时更新** - 自动刷新，显示最新修改时间
- ✏️ **文件编辑** - 可编辑 AGENTS.md、TOOLS.md、SOUL.md、USER.md、IDENTITY.md、HEARTBEAT.md
- 🎨 **优雅界面** - 深色主题，与 Clawdbot Dashboard 风格一致

## 🚀 快速开始

### 环境要求

- Node.js >= 14
- npm 或 yarn

### 安装

```bash
# 克隆仓库
git clone https://github.com/xcxyh/memory-viz-skill.git
cd memory-viz-skill/www/memory-viz

# 安装依赖
npm install
```

### 运行

```bash
# 启动服务
node server.js

# 服务运行在 http://0.0.0.0:3001
```

### 通过 SSH 隧道访问

如果你在远程服务器上运行：

```bash
# 建立 SSH 隧道
ssh -N -L 3001:127.0.0.1:3001 root@your-server-ip

# 然后在本地浏览器访问
http://localhost:3001/
```

## 📖 使用说明

### 1. Memory 标签

查看 `/root/clawd/memory/` 目录下的所有文件：
- `.md` 文件 - 以 Markdown 格式显示
- `.json` 文件 - 以 JSON 格式显示
- 显示文件大小和最后修改时间

### 2. Clawd 标签

查看 Clawdbot 核心文件：
- **MEMORY.md** - 只读，长期记忆
- **AGENTS.md** - 可编辑，Agent 配置
- **TOOLS.md** - 可编辑，工具配置
- **SOUL.md** - 可编辑，灵魂配置
- **USER.md** - 可编辑，用户配置
- **IDENTITY.md** - 可编辑，身份配置
- **HEARTBEAT.md** - 可编辑，心跳配置

### 3. 编辑文件

在 Clawd 标签下：
1. 点击可编辑的文件
2. 点击 **✏️ Edit** 按钮
3. 修改内容
4. 点击 **💾 Save** 保存 或 **✖ Cancel** 取消

## 📁 项目结构

```
memory-viz-skill/
├── www/memory-viz/
│   ├── index.html      # 前端界面
│   ├── server.js        # 后端 API 服务
│   ├── package.json    # 项目依赖
│   └── server.log      # 服务日志
├── skills/memory-viz/   # Clawdbot Skill
└── README.md
```

## 🔧 API 接口

| 接口 | 方法 | 说明 |
|------|------|------|
| `/api/memory` | GET | 获取 memory 目录下所有文件 |
| `/api/memory/:filename` | GET | 获取单个文件内容 |
| `/api/memory-main` | GET | 获取 MEMORY.md 内容 |
| `/api/clawd` | GET | 获取 Clawdbot 核心文件列表 |
| `/api/clawd/:filename` | GET | 获取单个核心文件 |
| `/api/clawd/:filename` | PATCH | 更新核心文件（仅限可编辑的文件） |

## 🎯 运行环境

该插件已集成到 Clawdbot Dashboard，可以通过以下方式运行：

```bash
# 作为独立服务运行
cd /root/clawd/www/memory-viz
node server.js

# 或使用 Clawdbot skill
bash /root/clawd/skills/memory-viz/scripts/start.sh
```

## 📝 更新日志

### v1.1.0 (2026-02-03)
- ✨ 新增：显示文件最后修改时间
- ✨ 新增：支持编辑 Clawdbot 核心文件
- 🐛 修复：编辑后退出编辑模式的 bug

### v1.0.0 (2026-02-01)
- 🎉 初始版本
- 📁 文件浏览和预览功能
- 🔄 自动刷新
- 🎨 深色主题界面

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License
