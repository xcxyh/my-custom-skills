---
name: web-search
description: 使用火山引擎融合信息搜索API进行网络搜索，支持网页搜索、图片搜索和AI总结搜索
---

# Web Search Skill

使用火山引擎融合信息搜索API进行网络搜索，获取网页内容、图片信息或AI总结的搜索结果。

## API 配置

API Key 已配置在环境变量或配置文件中：
- **API URL**: `https://open.feedcoopapi.com/search_api/web_search`
- **认证方式**: Bearer Token (API Key)

## 搜索类型

支持三种搜索类型：

### 1. Web 搜索 (`web`)
返回搜索到的网页信息，包括标题、摘要、链接等。

**参数：**
- `query` (必填): 搜索关键词，1-100个字符
- `count` (可选): 返回条数，最多50条，默认10条
- `time_range` (可选): 时间范围
  - `OneDay`: 1天内
  - `OneWeek`: 1周内
  - `OneMonth`: 1月内
  - `OneYear`: 1年内
  - `YYYY-MM-DD..YYYY-MM-DD`: 自定义日期范围
- `sites` (可选): 指定搜索站点，多个用 `|` 分隔，最多5个
- `block_hosts` (可选): 屏蔽站点，多个用 `|` 分隔，最多5个

### 2. Web 总结搜索 (`web_summary`)
在网页搜索基础上，提供AI总结的搜索结果。

**参数：**
- `query` (必填): 搜索关键词
- `count` (可选): 返回条数，最多50条，默认10条
- `need_summary` (必填): 必须为 `true`
- 其他参数同 Web 搜索

### 3. 图片搜索 (`image`)
返回搜索到的图片信息。

**参数：**
- `query` (必填): 搜索关键词
- `count` (可选): 返回条数，最多5条，默认5条
- `image_shapes` (可选): 图片形状筛选
  - `横长方形`
  - `竖长方形`
  - `方形`
- `image_width_min/max`, `image_height_min/max`: 图片尺寸筛选

## 使用方法

### Web 搜索示例

```bash
curl -X POST "https://open.feedcoopapi.com/search_api/web_search" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "Query": "人工智能最新进展",
    "SearchType": "web",
    "Count": 10,
    "TimeRange": "OneMonth"
  }'
```

### Web 总结搜索示例

```bash
curl -X POST "https://open.feedcoopapi.com/search_api/web_search" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "Query": "北京旅游攻略",
    "SearchType": "web_summary",
    "Count": 5,
    "NeedSummary": true
  }'
```

### 图片搜索示例

```bash
curl -X POST "https://open.feedcoopapi.com/search_api/web_search" \
  -H "Authorization: Bearer YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "Query": "风景图片",
    "SearchType": "image",
    "Count": 3
  }'
```

## 返回结果结构

### Web 搜索结果
- `Title`: 标题
- `Url`: 链接
- `Snippet`: 简短摘要（约100字）
- `Summary`: AI总结摘要（约300-500字，仅 web_summary）
- `SiteName`: 站点名称
- `PublishTime`: 发布时间
- `AuthInfoDes`: 权威度描述

### 图片搜索结果
- `Title`: 标题
- `Image.Url`: 图片链接
- `Image.Width`, `Image.Height`: 图片尺寸
- `Image.Shape`: 图片形状

## 错误处理

常见错误码：
- `10400`: 参数错误
- `10402`: 搜索类型错误
- `10403`: 权限错误
- `10500`: 服务器内部错误

## 注意事项

1. API Key 需要在火山引擎控制台创建"融合信息搜索"的 API Key
2. 免费额度：web 搜索和 web_summary 各 5000 次免费调用
3. 默认限流：5 QPS
4. 查询长度限制：1-100 个字符
