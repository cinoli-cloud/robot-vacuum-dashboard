"""
独立的新闻更新脚本
只更新新闻部分，不影响价格数据
读取现有的 products.json，只更新 news 字段
"""

import json
import os
from auto_news_fetcher import MultiSourceNewsFetcher
from datetime import datetime


def update_news_in_json():
    """只更新JSON文件中的新闻数据"""

    print("\n" + "="*70)
    print("📰 开始更新品牌新闻")
    print("="*70)

    # 读取现有数据
    data_file = '../data/products.json'

    try:
        with open(data_file, 'r', encoding='utf-8') as f:
            dashboard_data = json.load(f)
        print(f"✅ 读取现有数据文件成功")
    except FileNotFoundError:
        print(f"❌ 找不到数据文件: {data_file}")
        print("⚠️  请先运行 generate_with_real_prices.py 生成初始数据")
        return False

    # 获取最新新闻
    print("\n🚀 开始爬取最新品牌新闻...")
    fetcher = MultiSourceNewsFetcher()
    new_news = fetcher.fetch_all_brands()

    # 如果爬取失败，使用备用新闻
    if len(new_news) == 0:
        print("⚠️  新闻爬取失败，使用备用新闻数据")
        from real_news_generator import generate_real_brand_news
        new_news = generate_real_brand_news()

    # 更新新闻数据
    dashboard_data['news'] = new_news
    dashboard_data['last_update'] = datetime.now().isoformat()

    # 更新元数据（安全方式）
    if 'metadata' in dashboard_data:
        if 'data_sources' not in dashboard_data['metadata']:
            dashboard_data['metadata']['data_sources'] = {}
        dashboard_data['metadata']['data_sources']['news'] = "Auto-crawled from Google News RSS"

    # 保存回文件
    print(f"\n💾 保存更新后的数据到: {data_file}")
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

    print("\n" + "="*70)
    print("✅ 新闻更新完成！")
    print("="*70)

    # 统计
    brand_counts = {}
    for news in new_news:
        brand = news['brand']
        brand_counts[brand] = brand_counts.get(brand, 0) + 1

    print("\n📊 新闻统计:")
    for brand, count in sorted(brand_counts.items()):
        status = "✅" if count >= 5 else "⚠️ "
        print(f"  {status} {brand}: {count} 条")

    print(f"\n✅ 总计: {len(new_news)} 条新闻")
    print()

    return True


if __name__ == "__main__":
    success = update_news_in_json()
    exit(0 if success else 1)
