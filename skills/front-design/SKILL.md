---
name: front-design
description: 前端设计与部署技能，用于创建和部署静态网页、可视化界面等。
---

# Front Design

## 适用场景

当需要创建、设计或部署网页界面时使用，包括：
- 数据可视化页面
- 仪表板 (Dashboard)
- 静态展示页面
- 交互式前端应用

## 使用步骤

1. 在 `/root/clawd/www/` 目录下创建项目文件夹
2. 编写 HTML、CSS、JavaScript 文件
3. 使用 `scripts/deploy.sh` 部署到本地服务器
4. 返回可访问的 URL

## 项目结构

```
/root/clawd/www/
├── project-name/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── assets/
```

## 部署

运行部署脚本：
```bash
bash /root/clawd/skills/front-design/scripts/deploy.sh <project-name>
```

部署后可通过以下 URL 访问：
- `http://<host-ip>:8080/<project-name>/`

## 技术栈

- HTML5
- CSS3 (支持 Flexbox, Grid)
- Vanilla JavaScript (ES6+)
- 可选：Tailwind CSS (通过 CDN)
- 可选：Chart.js (数据可视化)
- 可选：Marked.js (Markdown 渲染)

## 示例

创建一个简单的仪表板：
```bash
mkdir -p /root/clawd/www/dashboard
# 编写文件...
bash /root/clawd/skills/front-design/scripts/deploy.sh dashboard
```
