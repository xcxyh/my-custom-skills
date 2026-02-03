const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const cors = require('cors');

// 配置
const CONFIG = {
  port: process.env.MEMORY_VIZ_PORT || 3001,
  memoryDir: process.env.MEMORY_DIR || '/root/clawd/memory',
  workspaceDir: process.env.WORKSPACE_DIR || '/root/clawd'
};

const app = express();

app.use(cors());
app.use(express.json());

// 静态文件服务（前端页面）
app.use(express.static(path.join(__dirname, 'public')));

// API: 获取所有记忆文件
app.get('/api/memory', async (req, res) => {
  try {
    const memoryDir = path.join(CONFIG.workspaceDir, 'memory');
    const files = await fs.readdir(memoryDir);
    const memoryFiles = [];

    for (const file of files) {
      const filePath = path.join(memoryDir, file);
      const stats = await fs.stat(filePath);

      if (stats.isFile() && (file.endsWith('.md') || file.endsWith('.json'))) {
        const content = await fs.readFile(filePath, 'utf-8');
        memoryFiles.push({
          name: file,
          type: file.endsWith('.json') ? 'json' : 'markdown',
          size: stats.size,
          modified: stats.mtime,
          content: content
        });
      }
    }

    // 按修改时间排序
    memoryFiles.sort((a, b) => b.modified - a.modified);

    res.json({ success: true, files: memoryFiles });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// API: 获取单个文件
app.get('/api/memory/:filename', async (req, res) => {
  try {
    const filename = req.params.filename;
    const memoryDir = path.join(CONFIG.workspaceDir, 'memory');
    const filePath = path.join(memoryDir, filename);

    const content = await fs.readFile(filePath, 'utf-8');
    const stats = await fs.stat(filePath);

    res.json({
      success: true,
      file: {
        name: filename,
        type: filename.endsWith('.json') ? 'json' : 'markdown',
        size: stats.size,
        modified: stats.mtime,
        content: content
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// API: 获取 MEMORY.md
app.get('/api/memory-main', async (req, res) => {
  try {
    const memoryPath = path.join(CONFIG.workspaceDir, 'MEMORY.md');
    const content = await fs.readFile(memoryPath, 'utf-8');
    const stats = await fs.stat(memoryPath);

    res.json({
      success: true,
      file: {
        name: 'MEMORY.md',
        type: 'markdown',
        size: stats.size,
        modified: stats.mtime,
        content: content
      }
    });
  } catch (error) {
    res.status(500).json({ success: false, error: error.message });
  }
});

// 健康检查
app.get('/health', (req, res) => {
  res.json({ status: 'ok', plugin: 'memory-viz', version: '1.0.0' });
});

// 启动服务器
if (require.main === module) {
  const server = app.listen(CONFIG.port, () => {
    console.log(`🚀 Memory Viz Plugin running on port ${CONFIG.port}`);
    console.log(`📁 Memory dir: ${path.join(CONFIG.workspaceDir, 'memory')}`);
    console.log(`🌐 URL: http://localhost:${CONFIG.port}`);
  });

  // 优雅关闭
  process.on('SIGTERM', () => {
    console.log('🛑 SIGTERM received, shutting down...');
    server.close(() => {
      console.log('✅ Server closed');
      process.exit(0);
    });
  });
}

module.exports = app;
