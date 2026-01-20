"""
Automatic News Fetcher - Multi-source News Crawler
每日自动获取8个品牌的最新资讯（每个品牌至少5条）
支持多个数据源：NewsAPI、Google News RSS、Bing News
"""

import os
import json
import requests
import feedparser
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import time
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class MultiSourceNewsFetcher:
    """多源新闻获取器"""

    def __init__(self):
        # API密钥（从环境变量读取）
        self.newsapi_key = os.getenv('NEWSAPI_KEY', '')
        self.bing_api_key = os.getenv('BING_NEWS_API_KEY', '')

        # 每个品牌获取的新闻数量（可配置）
        self.news_per_brand = int(os.getenv('NEWS_PER_BRAND', '10'))

        # 品牌列表
        self.brands = [
            'Eufy', 'Roborock', 'Dreame', 'Ecovacs',
            'Shark', 'Narwal', 'iRobot', 'Dyson'
        ]

        # 搜索关键词（品牌 + robot vacuum）
        self.search_keywords = {
            'Eufy': 'Eufy robot vacuum',
            'Roborock': 'Roborock robot vacuum',
            'Dreame': 'Dreame robot vacuum',
            'Ecovacs': 'Ecovacs Deebot robot vacuum',
            'Shark': 'Shark robot vacuum',
            'Narwal': 'Narwal robot vacuum',
            'iRobot': 'iRobot Roomba',
            'Dyson': 'Dyson robot vacuum'
        }

        # 排除的域名（品牌官网）
        self.excluded_domains = [
            'eufy.com', 'eufylife.com',
            'roborock.com', 'us.roborock.com',
            'dreame.com', 'dreametech.com',
            'ecovacs.com',
            'sharkclean.com', 'sharkninja.com',
            'narwal.com',
            'irobot.com',
            'dyson.com',
            'anker.com', 'ankermake.com'  # Eufy母公司
        ]

        # 优先的科技媒体来源
        self.preferred_sources = [
            'CNET', 'Tom\'s Guide', 'The Verge', 'TechCrunch',
            'Engadget', 'Android Authority', 'Digital Trends',
            'PCMag', 'TechRadar', 'Mashable', 'Wired',
            'The Guardian', 'Forbes', 'BBC', 'CNN',
            'Vacuum Wars', 'Robot Reviews'
        ]

    def is_excluded_url(self, url):
        """检查URL是否来自品牌官网（需要排除）"""
        url_lower = url.lower()
        for domain in self.excluded_domains:
            if domain in url_lower:
                return True
        return False

    def is_preferred_source(self, source_name):
        """检查是否是优先的科技媒体"""
        for preferred in self.preferred_sources:
            if preferred.lower() in source_name.lower():
                return True
        return False

    def fetch_from_newsapi(self, brand, keyword):
        """
        从 NewsAPI.org 获取新闻
        免费版：100次请求/天
        文档：https://newsapi.org/docs
        """
        if not self.newsapi_key:
            logger.warning("NewsAPI key not configured")
            return []

        try:
            # 清理关键词
            clean_keyword = keyword.strip().replace('\t', ' ').replace('\n', ' ')

            url = "https://newsapi.org/v2/everything"
            params = {
                'apiKey': self.newsapi_key,
                'q': clean_keyword,
                'language': 'en',
                'sortBy': 'publishedAt',
                'pageSize': min(self.news_per_brand * 2, 100),  # 获取更多以便过滤
                'from': (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
            }

            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('articles', [])

                news_list = []
                for article in articles:
                    article_url = article.get('url', '')
                    source_name = article.get('source', {}).get('name', '')

                    # 跳过官网新闻
                    if self.is_excluded_url(article_url):
                        continue

                    news_list.append({
                        'brand': brand,
                        'title': article.get('title', ''),
                        'summary': article.get('description', '')[:200] + '...',
                        'source': source_name,
                        'url': article_url,
                        'date': article.get('publishedAt', '')[:10],
                        'image': article.get('urlToImage', ''),
                        'is_preferred': self.is_preferred_source(source_name)
                    })

                    # 获取足够数量后停止
                    if len(news_list) >= self.news_per_brand:
                        break

                logger.info(f"✅ NewsAPI: {brand} - {len(news_list)} articles")
                return news_list

            elif response.status_code == 429:
                logger.warning(f"NewsAPI rate limit reached")
                return []

        except Exception as e:
            logger.error(f"NewsAPI error for {brand}: {e}")

        return []

    def extract_real_url_from_google(self, google_url):
        """
        从Google News重定向链接中提取真实URL
        方法1：Base64解码
        方法2：HTTP请求跟随重定向
        """
        import base64
        import re

        # 如果不是Google News重定向链接，直接返回
        if 'news.google.com/rss/articles/' not in google_url:
            return google_url

        # 方法1：Base64解码提取真实URL
        try:
            # 提取编码部分 (CBMi... 或 CAIi...)
            match = re.search(r'/articles/(CBMi[A-Za-z0-9_-]+|CAIi[A-Za-z0-9_-]+)', google_url)
            if match:
                encoded = match.group(1)
                # 去掉前缀 (CBMi 或 CAIi)
                encoded_data = encoded[4:]

                # Base64解码
                try:
                    # 添加padding
                    padding = (4 - len(encoded_data) % 4) % 4
                    encoded_data += '=' * padding

                    decoded = base64.urlsafe_b64decode(encoded_data)
                    decoded_str = decoded.decode('utf-8', errors='ignore')

                    # 查找http链接（改进的正则）
                    url_match = re.search(r'https?://[a-zA-Z0-9\-._~:/?#\[\]@!$&\'()*+,;=%]+', decoded_str)
                    if url_match:
                        real_url = url_match.group(0)
                        # 清理URL末尾的特殊字符
                        real_url = re.sub(r'[\x00-\x1f]+.*$', '', real_url)
                        # 移除末尾的垃圾字符
                        real_url = real_url.rstrip('\x00\x01\x02\x03\x08\x10\x12')
                        logger.info(f"✅ Base64解码成功: {real_url[:60]}...")
                        return real_url
                except Exception as decode_error:
                    logger.debug(f"Base64解码失败: {decode_error}")
        except Exception as e:
            logger.debug(f"Base64方法失败: {e}")

        # 方法2：HTTP请求跟随重定向（备用方案）
        try:
            logger.info(f"尝试HTTP重定向跟踪...")
            response = requests.head(google_url, allow_redirects=True, timeout=5)
            if response.url and response.url != google_url:
                logger.info(f"✅ HTTP重定向成功: {response.url[:60]}...")
                return response.url
        except Exception as e:
            logger.debug(f"HTTP重定向失败: {e}")

        # 如果两种方法都失败，返回原URL
        logger.warning(f"⚠️  URL解析失败，使用原始链接: {google_url[:60]}...")
        return google_url

    def fetch_from_google_news_rss(self, brand, keyword):
        """
        从 Google News RSS 获取新闻
        完全免费，无需API密钥
        """
        try:
            # 清理关键词：移除非ASCII字符、制表符、换行符
            import urllib.parse
            clean_keyword = keyword.strip().replace('\t', ' ').replace('\n', ' ')
            # URL编码
            encoded_keyword = urllib.parse.quote(clean_keyword)

            # Google News RSS URL
            rss_url = f"https://news.google.com/rss/search?q={encoded_keyword}&hl=en-US&gl=US&ceid=US:en"

            # 解析RSS
            feed = feedparser.parse(rss_url)

            news_list = []
            for entry in feed.entries:
                entry_url = entry.get('link', '')

                # 跳过官网新闻
                if self.is_excluded_url(entry_url):
                    continue

                # 提取发布日期
                pub_date = entry.get('published', '')
                try:
                    date_obj = datetime.strptime(pub_date, '%a, %d %b %Y %H:%M:%S %Z')
                    formatted_date = date_obj.strftime('%Y-%m-%d')
                except:
                    formatted_date = datetime.now().strftime('%Y-%m-%d')

                # 尝试从title中提取真实来源
                title = entry.get('title', '')
                source_name = 'Google News'
                if ' - ' in title:
                    # Google News的标题格式通常是 "标题 - 来源"
                    source_name = title.split(' - ')[-1].strip()

                # 清理和验证URL
                clean_url = entry_url.strip()
                # 确保URL是完整的http/https链接
                if not clean_url.startswith('http'):
                    logger.warning(f"Invalid URL for {brand}: {clean_url}")
                    continue

                # 提取Google News重定向中的真实URL
                real_url = self.extract_real_url_from_google(clean_url)

                # 确保URL不是GitHub代码链接
                if 'github.com' in real_url.lower() and '/blob/' in real_url.lower():
                    logger.warning(f"Skipping GitHub code URL: {real_url}")
                    continue

                news_list.append({
                    'brand': brand,
                    'title': title.split(' - ')[0] if ' - ' in title else title,  # 移除来源部分
                    'summary': entry.get('summary', '')[:200] + '...',
                    'source': source_name,
                    'url': real_url,  # 使用提取的真实URL
                    'date': formatted_date,
                    'image': '',
                    'is_preferred': self.is_preferred_source(source_name)
                })

                # 获取足够数量后停止
                if len(news_list) >= self.news_per_brand:
                    break

            logger.info(f"✅ Google News RSS: {brand} - {len(news_list)} articles")
            return news_list

        except Exception as e:
            logger.error(f"Google News RSS error for {brand}: {e}")

        return []

    def fetch_from_bing_news(self, brand, keyword):
        """
        从 Bing News API 获取新闻
        免费版：3000次/月
        """
        if not self.bing_api_key:
            logger.warning("Bing News API key not configured")
            return []

        try:
            # 清理关键词
            clean_keyword = keyword.strip().replace('\t', ' ').replace('\n', ' ')

            url = "https://api.bing.microsoft.com/v7.0/news/search"
            headers = {'Ocp-Apim-Subscription-Key': self.bing_api_key}
            params = {
                'q': clean_keyword,
                'count': self.news_per_brand,
                'mkt': 'en-US',
                'freshness': 'Month'
            }

            response = requests.get(url, headers=headers, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = data.get('value', [])

                news_list = []
                for article in articles:
                    article_url = article.get('url', '')
                    source_name = article.get('provider', [{}])[0].get('name', 'Bing News')

                    # 跳过官网新闻
                    if self.is_excluded_url(article_url):
                        continue

                    news_list.append({
                        'brand': brand,
                        'title': article.get('name', ''),
                        'summary': article.get('description', '')[:200] + '...',
                        'source': source_name,
                        'url': article_url,
                        'date': article.get('datePublished', '')[:10],
                        'image': article.get('image', {}).get('thumbnail', {}).get('contentUrl', ''),
                        'is_preferred': self.is_preferred_source(source_name)
                    })

                    # 获取足够数量后停止
                    if len(news_list) >= self.news_per_brand:
                        break

                logger.info(f"✅ Bing News: {brand} - {len(news_list)} articles")
                return news_list

        except Exception as e:
            logger.error(f"Bing News error for {brand}: {e}")

        return []

    def fetch_brand_news(self, brand):
        """
        为单个品牌获取新闻（尝试多个数据源）
        优先级：NewsAPI → Google News RSS → Bing News
        """
        keyword = self.search_keywords.get(brand, f'{brand} robot vacuum')
        news_list = []

        # 尝试 NewsAPI
        if self.newsapi_key:
            news_list = self.fetch_from_newsapi(brand, keyword)
            if len(news_list) >= self.news_per_brand:
                return news_list

        # 备选：Google News RSS（免费）
        google_news = self.fetch_from_google_news_rss(brand, keyword)
        news_list.extend(google_news)
        if len(news_list) >= self.news_per_brand:
            return news_list[:self.news_per_brand]

        # 备选：Bing News
        if self.bing_api_key and len(news_list) < self.news_per_brand:
            bing_news = self.fetch_from_bing_news(brand, keyword)
            news_list.extend(bing_news)

        # 去重（根据URL）
        seen_urls = set()
        unique_news = []
        for news in news_list:
            if news['url'] not in seen_urls:
                seen_urls.add(news['url'])
                unique_news.append(news)

        # 优先排序：优先媒体的新闻排在前面
        unique_news.sort(key=lambda x: (
            not x.get('is_preferred', False),  # 优先媒体排前面（False < True，取反后True < False）
            x.get('date', '')  # 按日期降序
        ), reverse=True)

        return unique_news[:self.news_per_brand]  # 返回配置的数量

    def fetch_all_brands(self):
        """获取所有品牌的新闻"""
        all_news = []

        logger.info("="*70)
        logger.info("🚀 开始获取品牌新闻")
        logger.info("="*70)

        for idx, brand in enumerate(self.brands, 1):
            logger.info(f"\n[{idx}/{len(self.brands)}] 获取 {brand} 新闻...")

            brand_news = self.fetch_brand_news(brand)
            all_news.extend(brand_news)

            logger.info(f"    ✅ 获取到 {len(brand_news)} 条新闻")

            # 避免频繁请求
            if idx < len(self.brands):
                time.sleep(2)

        logger.info("\n" + "="*70)
        logger.info(f"✅ 总计获取 {len(all_news)} 条新闻")
        logger.info("="*70)

        return all_news

    def save_to_json(self, news_data, output_file='../data/latest_news.json'):
        """保存新闻到JSON文件"""
        data = {
            'last_update': datetime.now().isoformat(),
            'total_news': len(news_data),
            'news': news_data
        }

        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"\n💾 新闻数据已保存到: {output_file}")


def main():
    """主函数"""
    print("\n" + "="*70)
    print("📰 机器人吸尘器品牌新闻自动抓取器")
    print("="*70)

    # 检查API配置
    newsapi_key = os.getenv('NEWSAPI_KEY')
    bing_key = os.getenv('BING_NEWS_API_KEY')

    print("\n🔑 API配置检查:")
    print(f"  NewsAPI: {'✅ 已配置' if newsapi_key else '⚠️  未配置（将使用Google News RSS）'}")
    print(f"  Bing News: {'✅ 已配置' if bing_key else '⚠️  未配置'}")

    if not newsapi_key and not bing_key:
        print("\n💡 提示: 未配置任何API密钥，将使用免费的Google News RSS")
        print("   Google News RSS完全免费，但可能获取速度较慢")

    # 创建爬虫实例
    fetcher = MultiSourceNewsFetcher()

    # 获取所有新闻
    all_news = fetcher.fetch_all_brands()

    # 保存到文件
    fetcher.save_to_json(all_news)

    # 统计每个品牌的新闻数量
    print("\n📊 品牌新闻统计:")
    brand_counts = {}
    for news in all_news:
        brand = news['brand']
        brand_counts[brand] = brand_counts.get(brand, 0) + 1

    for brand, count in sorted(brand_counts.items()):
        status = "✅" if count >= 5 else "⚠️ "
        print(f"  {status} {brand}: {count} 条")

    print("\n" + "="*70)
    print("✅ 新闻抓取完成！")
    print("="*70)
    print()


if __name__ == "__main__":
    main()
