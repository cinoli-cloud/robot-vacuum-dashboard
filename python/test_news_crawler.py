"""
快速测试新闻爬虫
无需API密钥，使用Google News RSS
"""

from auto_news_fetcher import MultiSourceNewsFetcher
import json

def test_crawler():
    print("\n" + "="*70)
    print("🧪 测试新闻爬虫（使用免费的Google News RSS）")
    print("="*70)

    # 创建爬虫实例
    fetcher = MultiSourceNewsFetcher()

    # 测试单个品牌
    print("\n📝 测试1: 获取Eufy品牌新闻...")
    eufy_news = fetcher.fetch_brand_news('Eufy')

    print(f"\n✅ 成功获取 {len(eufy_news)} 条Eufy新闻:")
    for idx, news in enumerate(eufy_news, 1):
        print(f"\n  [{idx}] {news['title']}")
        print(f"      来源: {news['source']}")
        print(f"      日期: {news['date']}")
        print(f"      URL: {news['url'][:80]}...")

    # 测试所有品牌
    print("\n" + "="*70)
    print("📝 测试2: 获取所有品牌新闻...")
    print("="*70)

    all_news = fetcher.fetch_all_brands()

    # 统计
    brand_counts = {}
    for news in all_news:
        brand = news['brand']
        brand_counts[brand] = brand_counts.get(brand, 0) + 1

    print("\n📊 统计结果:")
    for brand, count in sorted(brand_counts.items()):
        status = "✅" if count >= 5 else "⚠️ "
        print(f"  {status} {brand}: {count} 条新闻")

    print(f"\n✅ 总计: {len(all_news)} 条新闻")

    # 保存示例
    print("\n💾 保存示例新闻到 test_news_output.json")
    with open('test_news_output.json', 'w', encoding='utf-8') as f:
json.dump({
            'total': len(all_news),
            'by_brand': brand_counts,
            'sample_news': all_news[:5]
        }, f, indent=2, ensure_ascii=False)

    print("\n" + "="*70)
    if len(all_news) >= 40:
        print("✅ 测试成功！新闻爬虫工作正常！")
    else:
        print(f"⚠️  警告: 只获取到 {len(all_news)} 条新闻（预期40条）")
        print("   这可能是临时的网络问题，可以重试")
    print("="*70)
    print()

if __name__ == "__main__":
    test_crawler()
