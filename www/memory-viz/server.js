const express = require('express');
const fs = require('fs').promises;
const path = require('path');
const cors = require('cors');

const app = express();
const PORT = 3001;
const MEMORY_DIR = '/root/clawd/memory';
const WWW_DIR = '/root/clawd/www/memory-viz';

app.use(cors());
app.use(express.json());

// 提供静态文件
app.use(express.static(WWW_DIR));

// 根路径重定向到 index.html
app.get('/', (req, res) => {
    res.sendFile(path.join(WWW_DIR, 'index.html'));
});

// 读取记忆目录
app.get('/api/memory', async (req, res) => {
    try {
        const files = await fs.readdir(MEMORY_DIR);
        const memoryFiles = [];

        for (const file of files) {
            const filePath = path.join(MEMORY_DIR, file);
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

// 读取单个文件
app.get('/api/memory/:filename', async (req, res) => {
    try {
        const filename = req.params.filename;
        const filePath = path.join(MEMORY_DIR, filename);

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

// 读取 MEMORY.md
app.get('/api/memory-main', async (req, res) => {
    try {
        const memoryPath = '/root/clawd/MEMORY.md';
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

// Clawd 核心文件配置
const CLAWD_DIR = '/root/clawd';
const CORE_FILES = [
    'AGENTS.md',
    'MEMORY.md',
    'SOUL.md',
    'TOOLS.md',
    'USER.md',
    'IDENTITY.md',
    'HEARTBEAT.md'
];

// 读取 Clawd 核心文件列表
app.get('/api/clawd', async (req, res) => {
    try {
        const files = [];

        for (const filename of CORE_FILES) {
            const filePath = path.join(CLAWD_DIR, filename);
            try {
                const stats = await fs.stat(filePath);
                if (stats.isFile()) {
                    const content = await fs.readFile(filePath, 'utf-8');
                    files.push({
                        name: filename,
                        type: 'markdown',
                        size: stats.size,
                        modified: stats.mtime,
                        content: content
                    });
                }
            } catch (e) {
                // 文件不存在则跳过
            }
        }

        // 按修改时间排序
        files.sort((a, b) => b.modified - a.modified);

        res.json({ success: true, files: files });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

// 读取单个 Clawd 核心文件
app.get('/api/clawd/:filename', async (req, res) => {
    try {
        const filename = req.params.filename;
        
        // 安全检查：只允许核心文件
        if (!CORE_FILES.includes(filename)) {
            return res.status(403).json({ success: false, error: 'File not allowed' });
        }
        
        const filePath = path.join(CLAWD_DIR, filename);
        const content = await fs.readFile(filePath, 'utf-8');
        const stats = await fs.stat(filePath);

        res.json({
            success: true,
            file: {
                name: filename,
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

// 更新 Clawd 核心文件（只允许部分文件）
app.patch('/api/clawd/:filename', async (req, res) => {
    try {
        const filename = req.params.filename;
        
        // 只允许修改这些文件
        const ALLOWED_EDIT_FILES = [
            'AGENTS.md',
            'TOOLS.md',
            'SOUL.md',
            'USER.md',
            'IDENTITY.md',
            'HEARTBEAT.md'
        ];
        
        if (!ALLOWED_EDIT_FILES.includes(filename)) {
            return res.status(403).json({ 
                success: false, 
                error: 'File is read-only or not allowed',
                allowedFiles: ALLOWED_EDIT_FILES
            });
        }
        
        const { content } = req.body;
        
        if (!content) {
            return res.status(400).json({ success: false, error: 'Content is required' });
        }
        
        const filePath = path.join(CLAWD_DIR, filename);
        await fs.writeFile(filePath, content, 'utf-8');

        res.json({
            success: true,
            message: 'File updated successfully',
            file: {
                name: filename,
                modified: new Date()
            }
        });
    } catch (error) {
        res.status(500).json({ success: false, error: error.message });
    }
});

app.listen(PORT, '0.0.0.0', () => {
    console.log(`🚀 Memory API server running on port ${PORT} (0.0.0.0)`);
});
