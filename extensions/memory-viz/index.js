/**
 * Memory Visualization Plugin for Clawdbot
 * Provides real-time visualization of memory files
 */

import fs from 'node:fs';
import path from 'node:path';

// Resolve workspace directory
const WORKSPACE_DIR = process.env.CLAWDBOT_WORKSPACE || '/root/clawd';
const MEMORY_DIR = path.join(WORKSPACE_DIR, 'memory');

// Content types
const CONTENT_TYPES = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'application/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.md': 'text/markdown; charset=utf-8',
};

// Ensure memory directory exists
if (!fs.existsSync(MEMORY_DIR)) {
  try {
    fs.mkdirSync(MEMORY_DIR, { recursive: true });
  } catch (err) {
    // Ignore errors
  }
}

/**
 * Format file size
 */
function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  return (bytes / (1024 * 1024)).toFixed(1) + ' MB';
}

/**
 * Get content type for file extension
 */
function getContentType(filename) {
  const ext = path.extname(filename).toLowerCase();
  return CONTENT_TYPES[ext] || 'application/octet-stream';
}

/**
 * List memory files
 */
function listMemoryFiles() {
  try {
    if (!fs.existsSync(MEMORY_DIR)) {
      return [];
    }

    const files = fs.readdirSync(MEMORY_DIR, { withFileTypes: true });
    return files
      .filter(f => f.isFile() && (f.name.endsWith('.md') || f.name.endsWith('.json')))
      .map(f => {
        const filePath = path.join(MEMORY_DIR, f.name);
        const stats = fs.statSync(filePath);
        return {
          name: f.name,
          size: stats.size,
          modified: stats.mtime,
          type: f.name.endsWith('.json') ? 'json' : 'markdown',
        };
      })
      .sort((a, b) => b.modified - a.modified);
  } catch (err) {
    console.error('[memory-viz] Error listing files:', err);
    return [];
  }
}

/**
 * Read file content
 */
function readFile(filename) {
  try {
    const filePath = path.join(MEMORY_DIR, filename);
    
    // Security check: ensure file is in memory directory
    const resolvedPath = path.resolve(filePath);
    const resolvedMemoryDir = path.resolve(MEMORY_DIR);
    
    if (!resolvedPath.startsWith(resolvedMemoryDir)) {
      return { error: 'Invalid file path' };
    }

    if (!fs.existsSync(resolvedPath)) {
      return { error: 'File not found' };
    }

    const content = fs.readFileSync(resolvedPath, 'utf-8');
    const stats = fs.statSync(resolvedPath);

    return {
      name: filename,
      size: stats.size,
      modified: stats.mtime,
      type: filename.endsWith('.json') ? 'json' : 'markdown',
      content,
    };
  } catch (err) {
    console.error('[memory-viz] Error reading file:', err);
    return { error: 'Failed to read file' };
  }
}

/**
 * Serve static file from plugin directory
 */
function serveStaticFile(filename, res) {
  try {
    const pluginDir = path.dirname(import.meta.url.replace('file://', ''));
    const filePath = path.join(pluginDir, 'public', filename);

    if (!fs.existsSync(filePath)) {
      res.statusCode = 404;
      res.end('Not Found');
      return;
    }

    const content = fs.readFileSync(filePath);
    const contentType = getContentType(filename);

    res.statusCode = 200;
    res.setHeader('Content-Type', contentType);
    res.setHeader('Cache-Control', 'no-cache');
    res.end(content);
  } catch (err) {
    console.error('[memory-viz] Error serving static file:', err);
    res.statusCode = 500;
    res.end('Internal Server Error');
  }
}

/**
 * Main HTTP handler
 */
export async function handleRequest(req, res) {
  const url = new URL(req.url || '/', 'http://localhost');
  const pathname = url.pathname;

  // Serve static assets
  if (pathname === '/memory' || pathname === '/memory/') {
    serveStaticFile('index.html', res);
    return true;
  }

  if (pathname.startsWith('/memory/assets/')) {
    const filename = pathname.slice('/memory/assets/'.length);
    serveStaticFile('assets/' + filename, res);
    return true;
  }

  // API: List files
  if (pathname === '/memory/api/files' || pathname === '/memory/api/memory') {
    const files = listMemoryFiles();
    res.statusCode = 200;
    res.setHeader('Content-Type', 'application/json; charset=utf-8');
    res.setHeader('Cache-Control', 'no-cache');
    res.end(JSON.stringify({ success: true, files }));
    return true;
  }

  // API: Get single file
  if (pathname.startsWith('/memory/api/memory/')) {
    const filename = pathname.slice('/memory/api/memory/'.length);
    const file = readFile(filename);
    
    if (file.error) {
      res.statusCode = 404;
      res.setHeader('Content-Type', 'application/json; charset=utf-8');
      res.end(JSON.stringify({ success: false, error: file.error }));
    } else {
      res.statusCode = 200;
      res.setHeader('Content-Type', 'application/json; charset=utf-8');
      res.setHeader('Cache-Control', 'no-cache');
      res.end(JSON.stringify({ success: true, file }));
    }
    return true;
  }

  // Not handled
  return false;
}

/**
 * Plugin registration
 */
export function register(api) {
  const { log, registerPluginHttpRoute } = api;

  log.info('[memory-viz] Plugin loaded');
  log.info('[memory-viz] Memory directory:', MEMORY_DIR);
  log.info('[memory-viz] Access at: http://localhost:18789/memory');

  // Register HTTP routes
  registerPluginHttpRoute({
    path: '/memory',
    handler: handleRequest,
    plugin: 'memory-viz',
  });

  registerPluginHttpRoute({
    path: '/memory/*',
    handler: handleRequest,
    plugin: 'memory-viz',
    fallbackPath: '/memory',
  });
}
