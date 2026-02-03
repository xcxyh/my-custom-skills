#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
火山引擎融合信息搜索API客户端
支持 web、web_summary 和 image 三种搜索类型
"""

import os
import json
import sys
import argparse
from typing import Optional, List, Dict, Any


class VolcengineSearchClient:
    """火山引擎融合信息搜索API客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化客户端
        
        Args:
            api_key: API Key，如果不提供则从环境变量 VOLCENGINE_API_KEY 读取
        """
        self.api_key = api_key or os.environ.get("VOLCENGINE_API_KEY", "")
        self.base_url = "https://open.feedcoopapi.com/search_api/web_search"
        
        if not self.api_key:
            raise ValueError("API Key 未设置，请设置 VOLCENGINE_API_KEY 环境变量或传入 api_key 参数")
    
    def _parse_sse_response(self, response_text: str) -> Dict[str, Any]:
        """解析 SSE 流式响应，合并所有数据"""
        # 初始化结果结构
        result = {
            "ResponseMetadata": {},
            "Result": {
                "ResultCount": 0,
                "WebResults": [],
                "Choices": [],
                "ImageResults": None,
                "CardResults": None
            },
            "Usage": None
        }
        
        # 逐行解析 SSE 数据
        for line in response_text.strip().split('\n'):
            line = line.strip()
            if not line or line.startswith(':'):
                continue
            
            # 移除 "data:" 前缀
            if line.startswith('data:'):
                line = line[5:].strip()
            
            # 检查是否是结束标记
            if line == '[DONE]':
                break
            
            # 解析 JSON
            try:
                data = json.loads(line)
                
                # 合并 ResponseMetadata
                if "ResponseMetadata" in data:
                    result["ResponseMetadata"] = data["ResponseMetadata"]
                
                # 合并 Result
                if "Result" in data:
                    r = data["Result"]
                    
                    # 合并 WebResults（只在第一次出现时保留）
                    if "WebResults" in r and r["WebResults"] and not result["Result"]["WebResults"]:
                        result["Result"]["WebResults"] = r["WebResults"]
                        result["Result"]["ResultCount"] = r.get("ResultCount", 0)
                    
                    # 合并 Choices（累积）
                    if "Choices" in r and r["Choices"]:
                        if not result["Result"]["Choices"]:
                            result["Result"]["Choices"] = []
                        
                        for choice in r["Choices"]:
                            # 查找是否已存在相同 index 的 choice
                            existing = None
                            for c in result["Result"]["Choices"]:
                                if c.get("Index") == choice.get("Index"):
                                    existing = c
                                    break
                            
                            if existing:
                                # 累积 Delta 内容
                                if "Delta" in choice:
                                    if "Message" not in existing or existing["Message"] is None:
                                        existing["Message"] = {"role": "assistant", "content": ""}
                                    
                                    delta_content = choice["Delta"].get("Content", "")
                                    existing["Message"]["content"] += delta_content
                                
                                # 更新其他字段
                                if "FinishReason" in choice:
                                    existing["FinishReason"] = choice["FinishReason"]
                            else:
                                # 新增 choice
                                new_choice = choice.copy()
                                if "Delta" in new_choice:
                                    new_choice["Message"] = {
                                        "role": new_choice["Delta"].get("Role", "assistant"),
                                        "content": new_choice["Delta"].get("Content", "")
                                    }
                                    del new_choice["Delta"]
                                result["Result"]["Choices"].append(new_choice)
                    
                    # 合并 Usage（只在最后一次出现时保留）
                    if "Usage" in r and r["Usage"]:
                        result["Usage"] = r["Usage"]
                    
                    # 合并 ImageResults
                    if "ImageResults" in r and r["ImageResults"]:
                        result["Result"]["ImageResults"] = r["ImageResults"]
                    
                    # 合并 CardResults
                    if "CardResults" in r and r["CardResults"]:
                        result["Result"]["CardResults"] = r["CardResults"]
                    
                    # 合并其他字段
                    for key, value in r.items():
                        if key not in ["WebResults", "Choices", "Usage", "ImageResults", "CardResults"]:
                            result["Result"][key] = value
                            
            except json.JSONDecodeError:
                continue
        
        return result
    
    def search(
        self,
        query: str,
        search_type: str = "web",
        count: int = 10,
        time_range: Optional[str] = None,
        sites: Optional[str] = None,
        block_hosts: Optional[str] = None,
        need_summary: bool = False,
        image_shapes: Optional[List[str]] = None,
        image_width_min: Optional[int] = None,
        image_width_max: Optional[int] = None,
        image_height_min: Optional[int] = None,
        image_height_max: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        执行搜索请求
        
        Args:
            query: 搜索关键词，1-100个字符
            search_type: 搜索类型 (web/web_summary/image)
            count: 返回条数，web/web_summary最多50，image最多5
            time_range: 时间范围 (OneDay/OneWeek/OneMonth/OneYear/日期范围)
            sites: 指定搜索站点，用|分隔
            block_hosts: 屏蔽站点，用|分隔
            need_summary: 是否需要AI总结（仅web_summary有效）
            image_shapes: 图片形状筛选
            image_width_min/max: 图片宽度范围
            image_height_min/max: 图片高度范围
        
        Returns:
            API响应结果字典
        """
        # 构建请求体
        payload = {
            "Query": query[:100],  # 限制100字符
            "SearchType": search_type,
            "Count": count,
        }
        
        # 添加可选参数
        if time_range:
            payload["TimeRange"] = time_range
        
        if need_summary:
            payload["NeedSummary"] = True
        
        # 添加过滤条件
        filter_obj = {
            "NeedContent": False,
            "NeedUrl": True
        }
        
        if sites:
            filter_obj["Sites"] = sites
        
        if block_hosts:
            filter_obj["BlockHosts"] = block_hosts
        
        if image_shapes:
            filter_obj["ImageShapes"] = image_shapes
        
        if image_width_min is not None:
            filter_obj["ImageWidthMin"] = image_width_min
        
        if image_width_max is not None:
            filter_obj["ImageWidthMax"] = image_width_max
        
        if image_height_min is not None:
            filter_obj["ImageHeightMin"] = image_height_min
        
        if image_height_max is not None:
            filter_obj["ImageHeightMax"] = image_height_max
        
        if filter_obj:
            payload["Filter"] = filter_obj
        
        # 发送请求
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        try:
            import requests
            response = requests.post(self.base_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            
            # web_summary 返回 SSE 流式响应，需要特殊处理
            if search_type == "web_summary":
                return self._parse_sse_response(response.text)
            else:
                return response.json()
                
        except requests.exceptions.RequestException as e:
            return {
                "error": True,
                "message": str(e),
                "status_code": getattr(e.response, 'status_code', None)
            }
        except Exception as e:
            return {
                "error": True,
                "message": str(e)
            }
    
    def web_search(self, query: str, **kwargs) -> Dict[str, Any]:
        """网页搜索"""
        return self.search(query, search_type="web", **kwargs)
    
    def web_summary_search(self, query: str, **kwargs) -> Dict[str, Any]:
        """网页+AI总结搜索"""
        kwargs["need_summary"] = True
        return self.search(query, search_type="web_summary", **kwargs)
    
    def image_search(self, query: str, **kwargs) -> Dict[str, Any]:
        """图片搜索"""
        return self.search(query, search_type="image", **kwargs)
    
    def format_web_results(self, result: Dict[str, Any]) -> str:
        """格式化网页搜索结果为可读文本"""
        if result.get("error"):
            return f"搜索失败: {result.get('message', '未知错误')}"
        
        response_result = result.get("Result", {})
        web_results = response_result.get("WebResults", [])
        
        if not web_results:
            return "未找到相关结果"
        
        output = []
        output.append(f"找到 {response_result.get('ResultCount', 0)} 条结果\n")
        
        for i, item in enumerate(web_results, 1):
            title = item.get("Title", "无标题")
            url = item.get("Url", "")
            snippet = item.get("Snippet", "")
            site_name = item.get("SiteName", "")
            auth_info = item.get("AuthInfoDes", "")
            
            output.append(f"{i}. {title}")
            output.append(f"   来源: {site_name}")
            if snippet:
                output.append(f"   摘要: {snippet[:150]}...")
            if url:
                output.append(f"   链接: {url}")
            if auth_info:
                output.append(f"   权威: {auth_info}")
            output.append("")
        
        return "\n".join(output)
    
    def format_image_results(self, result: Dict[str, Any]) -> str:
        """格式化图片搜索结果为可读文本"""
        if result.get("error"):
            return f"搜索失败: {result.get('message', '未知错误')}"
        
        response_result = result.get("Result", {})
        image_results = response_result.get("ImageResults", [])
        
        if not image_results:
            return "未找到相关图片"
        
        output = []
        output.append(f"找到 {response_result.get('ResultCount', 0)} 张图片\n")
        
        for i, item in enumerate(image_results, 1):
            title = item.get("Title", "无标题")
            image_info = item.get("Image", {})
            image_url = image_info.get("Url", "")
            width = image_info.get("Width", 0)
            height = image_info.get("Height", 0)
            shape = image_info.get("Shape", "")
            
            output.append(f"{i}. {title}")
            output.append(f"   尺寸: {width}x{height} | {shape}")
            if image_url:
                output.append(f"   图片: {image_url}")
            output.append("")
        
        return "\n".join(output)
    
    def format_summary_results(self, result: Dict[str, Any]) -> str:
        """格式化总结搜索结果为可读文本"""
        if result.get("error"):
            return f"搜索失败: {result.get('message', '未知错误')}"
        
        response_result = result.get("Result", {})
        web_results = response_result.get("WebResults", [])
        choices = response_result.get("Choices", [])
        
        output = []
        
        # 显示搜索结果
        if web_results:
            output.append(f"找到 {response_result.get('ResultCount', 0)} 条参考来源\n")
            for i, item in enumerate(web_results[:3], 1):  # 只显示前3条
                title = item.get("Title", "无标题")
                url = item.get("Url", "")
                output.append(f"{i}. {title}")
                if url:
                    output.append(f"   {url}")
            output.append("")
        
        # 显示AI总结
        if choices:
            for choice in choices:
                message = choice.get("Message", {})
                content = message.get("content", "")
                if content:
                    output.append("AI 总结：")
                    output.append(content)
                    break
        
        # 如果没有总结但有搜索结果，显示完整摘要
        if not choices and web_results:
            for item in web_results:
                summary = item.get("Summary", "")
                if summary:
                    output.append("内容摘要：")
                    output.append(summary)
                    break
        
        return "\n".join(output)


def main():
    """命令行入口"""
    # 设置 UTF-8 输出编码
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    else:
        sys.stdout.reconfigure(encoding='utf-8')
    
    parser = argparse.ArgumentParser(description="火山引擎融合信息搜索API客户端")
    parser.add_argument("query", help="搜索关键词")
    parser.add_argument("-t", "--type", choices=["web", "web_summary", "image"], 
                       default="web", help="搜索类型")
    parser.add_argument("-c", "--count", type=int, default=10, help="返回条数")
    parser.add_argument("--time-range", help="时间范围")
    parser.add_argument("--sites", help="指定搜索站点")
    parser.add_argument("--block-hosts", help="屏蔽站点")
    parser.add_argument("--format", choices=["text", "json"], default="text", 
                       help="输出格式")
    parser.add_argument("--api-key", help="API Key（或使用环境变量VOLCENGINE_API_KEY）")
    
    args = parser.parse_args()
    
    # 创建客户端
    client = VolcengineSearchClient(api_key=args.api_key)
    
    # 执行搜索
    if args.type == "web":
        result = client.web_search(
            args.query,
            count=args.count,
            time_range=args.time_range,
            sites=args.sites,
            block_hosts=args.block_hosts
        )
        formatted = client.format_web_results(result)
    elif args.type == "web_summary":
        result = client.web_summary_search(
            args.query,
            count=args.count,
            time_range=args.time_range,
            sites=args.sites,
            block_hosts=args.block_hosts
        )
        formatted = client.format_summary_results(result)
    elif args.type == "image":
        result = client.image_search(
            args.query,
            count=args.count
        )
        formatted = client.format_image_results(result)
    
    # 输出结果
    if args.format == "json":
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(formatted)


if __name__ == "__main__":
    main()
