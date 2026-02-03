#!/usr/bin/env python3
"""
AI Daily Digest - Fetch and summarize hot AI events from multiple sources
Sources:
1. HackerNews
2. GitHub Trending AI
3. AI资讯日报 (GitHub Pages)
"""

import requests
import json
import sys
from datetime import datetime, timedelta
from typing import List, Dict, Any

class AIDailyDigest:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        })
    
    def fetch_hackernews(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Fetch top AI/ML stories from HackerNews"""
        try:
            # Get top stories
            top_stories_url = "https://hacker-news.firebaseio.com/v0/topstories.json"
            response = self.session.get(top_stories_url, timeout=10)
            response.raise_for_status()
            top_stories = response.json()[:100]  # Get top 100
            
            ai_stories = []
            ai_keywords = ['ai', 'artificial intelligence', 'machine learning', 'ml', 'deep learning', 
                          'neural network', 'llm', 'gpt', 'chatgpt', 'openai', 'anthropic', 
                          'claude', 'gemini', 'stable diffusion', 'midjourney', 'generative']
            
            for story_id in top_stories:
                if len(ai_stories) >= limit:
                    break
                    
                try:
                    story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
                    story_response = self.session.get(story_url, timeout=5)
                    story_response.raise_for_status()
                    story = story_response.json()
                    
                    if not story or 'title' not in story:
                        continue
                    
                    title = story.get('title', '').lower()
                    text = story.get('text', '').lower() if story.get('text') else ''
                    
                    # Check if story is AI-related
                    content_to_check = title + ' ' + text
                    if any(keyword in content_to_check for keyword in ai_keywords):
                        ai_stories.append({
                            'title': story.get('title'),
                            'url': story.get('url'),
                            'score': story.get('score', 0),
                            'by': story.get('by', 'unknown'),
                            'time': datetime.fromtimestamp(story.get('time', 0)),
                            'descendants': story.get('descendants', 0)
                        })
                except Exception as e:
                    print(f"Error processing story {story_id}: {e}", file=sys.stderr)
                    continue
            
            return sorted(ai_stories, key=lambda x: x['score'], reverse=True)
            
        except Exception as e:
            print(f"Error fetching HackerNews: {e}", file=sys.stderr)
            return []
    
    def fetch_github_trending(self, limit: int = 8) -> List[Dict[str, Any]]:
        """Fetch trending AI repositories from GitHub"""
        try:
            # GitHub Trending AI page
            url = "https://github.com/trending/ai"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            # Simple HTML parsing (GitHub's structure)
            content = response.text
            repos = []
            
            # Look for repository articles
            import re
            repo_pattern = r'<article[^>]*>.*?<h2[^>]*>\s*<a[^>]*href="/([^"]+)"[^>]*>(.*?)</a>.*?</h2>.*?<p[^>]*>(.*?)</p>.*?<div[^>]*class="[^"]*f6[^"]*"[^>]*>.*?<span[^>]*>.*?([\d,]+).*?</span>.*?<span[^>]*>.*?([\d,]+).*?</span>'
            
            matches = re.findall(repo_pattern, content, re.DOTALL)
            
            for match in matches[:limit]:
                repo_path, name_desc, description, stars, forks = match
                
                # Clean up HTML tags and whitespace
                name_desc = re.sub(r'<[^>]+>', '', name_desc).strip()
                description = re.sub(r'<[^>]+>', '', description).strip()
                
                repos.append({
                    'name': name_desc,
                    'full_name': repo_path,
                    'url': f"https://github.com/{repo_path}",
                    'description': description,
                    'stars': stars.strip(),
                    'forks': forks.strip()
                })
            
            return repos
            
        except Exception as e:
            print(f"Error fetching GitHub Trending: {e}", file=sys.stderr)
            return []
    
    def fetch_product_hunt_ai(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Fetch AI products from Product Hunt"""
        try:
            # Product Hunt tech category often has AI products
            url = "https://www.producthunt.com/"
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            content = response.text
            import re
            
            # Look for product information
            products = []
            ai_keywords = ['ai', 'gpt', 'llm', 'machine learning', 'neural', 'artificial intelligence']
            
            # Try to extract product info (simplified pattern)
            product_pattern = r'class="[^"]*styles_title[^"]*"[^>]*>([^<]+)</'
            name_matches = re.findall(product_pattern, content)
            
            for name in name_matches[:20]:  # Check more products
                name_lower = name.lower()
                if any(keyword in name_lower for keyword in ai_keywords):
                    products.append({
                        'name': name.strip(),
                        'tagline': 'AI Product',
                        'url': 'https://www.producthunt.com/'
                    })
                    if len(products) >= limit:
                        break
            
            return products[:limit]
            
        except Exception as e:
            print(f"Error fetching Product Hunt: {e}", file=sys.stderr)
            return []
    
    def generate_digest(self) -> str:
        """Generate the daily digest report"""
        print("Fetching AI Daily Digest...", file=sys.stderr)
        
        # Fetch all sources
        hackernews = self.fetch_hackernews(limit=8)
        github_trending = self.fetch_github_trending(limit=6)
        
        # Generate report
        report = []
        report.append("🤖 AI Daily Digest - " + datetime.now().strftime("%Y-%m-%d"))
        report.append("=" * 50)
        
        # Product Hunt AI Products
        product_hunt = self.fetch_product_hunt_ai(limit=5)
        if product_hunt:
            report.append("\n🚀 Product Hunt AI 产品")
            report.append("-" * 30)
            for i, product in enumerate(product_hunt, 1):
                report.append(f"{i}. {product['name']}")
                report.append(f"   🔗 {product['url']}")
                report.append("")
        
        # HackerNews AI Stories
        if hackernews:
            report.append("\n🔥 HackerNews 热门AI话题")
            report.append("-" * 30)
            for i, story in enumerate(hackernews[:5], 1):
                title = story['title']
                url = story['url'] or f"https://news.ycombinator.com/item?id={story.get('id', '')}"
                score = story['score']
                comments = story['descendants']
                # 添加简短摘要（如果有文本内容）
                summary = ""
                if story.get('text'):
                    # 清理HTML标签并截断
                    import re
                    text = re.sub(r'<[^>]+>', '', story['text'])
                    if len(text) > 150:
                        summary = text[:150] + "..."
                    elif text:
                        summary = text
                
                report.append(f"{i}. {title}")
                if summary:
                    report.append(f"   📝 {summary}")
                report.append(f"   👍 {score} | 💬 {comments} comments")
                report.append(f"   🔗 {url}")
                report.append("")
        
        # GitHub Trending AI
        if github_trending:
            report.append("\n⭐ GitHub Trending AI 项目")
            report.append("-" * 30)
            for i, repo in enumerate(github_trending, 1):
                name = repo['name']
                desc = repo['description'][:100] + "..." if len(repo['description']) > 100 else repo['description']
                stars = repo['stars']
                report.append(f"{i}. {name}")
                if desc:
                    report.append(f"   📝 {desc}")
                report.append(f"   ⭐ {stars} | 🔗 {repo['url']}")
                report.append("")
        
        # Footer
        report.append("\n" + "=" * 50)
        report.append("💡 数据来源: HackerNews + GitHub Trending AI + AI资讯日报")
        report.append("🕒 更新时间: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        
        return "\n".join(report)

def main():
    digest = AIDailyDigest()
    report = digest.generate_digest()
    print(report)

if __name__ == "__main__":
    main()
