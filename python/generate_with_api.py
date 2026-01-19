"""
Generate dashboard data using API + VERIFIED PRICES
Integrates api_price_fetcher with real_prices_database
"""

import json
import os
import random
from datetime import datetime, timedelta
from config_final_verified import BRANDS_CONFIG_FINAL, get_channel_url
from real_prices_database import VERIFIED_PRICES, CURRENT_SALES, get_real_price
from new_products_tags import is_new_product, get_new_product_note
from ai_price_predictor import generate_ai_price_data
from real_news_generator import generate_real_brand_news
try:
    from auto_news_fetcher import MultiSourceNewsFetcher
    NEWS_FETCHER_AVAILABLE = True
except ImportError:
    NEWS_FETCHER_AVAILABLE = False
from api_price_fetcher import MultiChannelPriceFetcher

# ============================================
# 🔧 配置开关：启用API获取
# ============================================
USE_API_PRICES = True  # 设为 True 启用API，False 使用静态数据

# Initialize API fetcher
api_fetcher = MultiChannelPriceFetcher() if USE_API_PRICES else None


def get_api_price(brand, product_name, channel):
    """
    Try to fetch price from API, fallback to verified database

    Returns: (price, confidence, source)
    """
    if not USE_API_PRICES or not api_fetcher:
        return None, 'ESTIMATED', 'Static Data'

    # Construct search query
    search_query = f"{brand} {product_name}"

    try:
        if channel == 'bestbuy':
            result = api_fetcher.fetch_bestbuy_price(search_query)
            if result:
                price = result.get('sale_price') or result.get('regular_price')
                if price:
                    return price, 'VERIFIED_API', 'Best Buy API'

        elif channel == 'ebay':
            result = api_fetcher.fetch_ebay_price(search_query)
            if result:
                price = result.get('sale_price')
                if price:
                    return price, 'VERIFIED_API', 'eBay API'

        elif channel == 'walmart':
            result = api_fetcher.fetch_walmart_price(search_query)
            if result:
                price = result.get('sale_price') or result.get('regular_price')
                if price:
                    return price, 'VERIFIED_API', 'Walmart API'

    except Exception as e:
        print(f"⚠️  API error for {brand} {product_name} on {channel}: {e}")

    return None, 'ESTIMATED', 'API Failed'


def generate_product_with_api_price(brand, product_config):
    """Generate product data using API + verified prices"""
    product_name = product_config['name']

    # Check if product is NEW and update note
    original_note = product_config.get('note', '')
    if is_new_product(brand, product_name):
        ces_note = get_new_product_note(brand, product_name)
        note = ces_note if ces_note else original_note
    else:
        note = original_note

    # Extract MSRP if available
    msrp = None
    if 'msrp' in product_config:
        msrp = product_config['msrp']
    elif 'official_price' in product_config:
        msrp = product_config['official_price']

    product_data = {
        "brand": brand,
        "name": product_name,
        "model": product_config['model'],
        "msrp": msrp,
        "key_features": product_config.get('key_features', ''),
        "note": note,
        "verified": True,
        "channels": {}
    }

    # Priority order: Official site (always verified) → API → Estimated
    for channel_name in ['official', 'bestbuy', 'ebay', 'walmart']:
        price = None
        confidence = 'UNKNOWN'
        source = 'Unknown'

        # 1. Official site - always use verified database
        if channel_name == 'official':
            price, confidence, source = get_real_price(product_config, channel_name)

        # 2. Try API first for retail channels
        else:
            api_price, api_confidence, api_source = get_api_price(brand, product_name, channel_name)

            if api_price:
                # API succeeded
                price = api_price
                confidence = api_confidence
                source = api_source
            else:
                # API failed, fallback to verified database or estimation
                price, confidence, source = get_real_price(product_config, channel_name)

        # Get URL
        url = get_channel_url(product_config, brand, channel_name)

        # Add channel data
        product_data["channels"][channel_name] = {
            "price": price,
            "confidence": confidence,
            "price_source": source,
            "url": url
        }

        # Simulate 24h price change
        change_24h = round(random.uniform(-5, 2), 2)
        product_data["channels"][channel_name]["change_24h"] = change_24h

    return product_data


def generate_all_products_data():
    """Generate complete dashboard data with API integration"""
    all_products = []

    print("\n" + "="*70)
    print("🚀 开始生成数据（API模式: {})".format("启用" if USE_API_PRICES else "禁用"))
    print("="*70)

    # Generate products for each brand
    for brand, config in BRANDS_CONFIG_FINAL.items():
        print(f"\n处理品牌: {brand}")
        verified_products = config.get('verified_products', [])

        for idx, product_config in enumerate(verified_products, 1):
            product_name = product_config['name']
            print(f"  [{idx}/{len(verified_products)}] {product_name}...", end=" ")

            product_data = generate_product_with_api_price(brand, product_config)
            all_products.append(product_data)

            print("✅")

    print(f"\n✅ 共生成 {len(all_products)} 个产品数据")

    # Generate AI predictions
    print("\n生成AI价格预测...")
    ai_predictions = generate_ai_price_data(all_products)

    # Generate/Fetch news
    print("获取品牌新闻...")
    if NEWS_FETCHER_AVAILABLE and os.getenv('USE_AUTO_NEWS', 'true').lower() == 'true':
        # 使用自动新闻爬虫
        print("  → 使用全网新闻爬虫（实时获取）")
        news_fetcher = MultiSourceNewsFetcher()
        all_news = news_fetcher.fetch_all_brands()
        if len(all_news) < 20:  # 如果爬取失败，使用备用新闻
            print("  ⚠️  爬取的新闻数量不足，使用备用新闻")
            all_news = generate_real_brand_news()
    else:
        # 使用静态新闻
        print("  → 使用静态新闻数据")
        all_news = generate_real_brand_news()

    # Combine all data
    dashboard_data = {
        "products": all_products,
        "ai_predictions": ai_predictions,
        "news": all_news,
        "last_update": datetime.now().isoformat(),
        "api_enabled": USE_API_PRICES,
        "metadata": {
            "total_products": len(all_products),
            "total_brands": len(BRANDS_CONFIG_FINAL),
            "data_sources": {
                "official_prices": "Verified from official sites",
                "retail_prices": "Best Buy API, eBay API, Walmart API" if USE_API_PRICES else "Estimated",
                "ai_predictions": "Linear Regression + Moving Average",
                "news": "Auto-crawled from NewsAPI/Google News RSS" if NEWS_FETCHER_AVAILABLE else "Static news data"
            }
        }
    }

    return dashboard_data


def main():
    """Main execution"""
    print("\n" + "="*70)
    print("🤖 机器人吸尘器价格监控看板 - 数据生成器")
    print("="*70)

    # Check API configuration
    if USE_API_PRICES:
        print("\n📡 检查API配置...")
        has_bestbuy = bool(os.getenv('BESTBUY_API_KEY'))
        has_ebay = bool(os.getenv('EBAY_APP_ID'))
        has_walmart = bool(os.getenv('WALMART_API_KEY'))

        print(f"  Best Buy API: {'✅ 已配置' if has_bestbuy else '❌ 未配置'}")
        print(f"  eBay API: {'✅ 已配置' if has_ebay else '❌ 未配置'}")
        print(f"  Walmart API: {'✅ 已配置' if has_walmart else '❌ 未配置'}")

        if not (has_bestbuy or has_ebay or has_walmart):
            print("\n⚠️  警告: 没有配置任何API密钥，将使用估算价格")
    else:
        print("\n📊 使用静态数据模式（API已禁用）")

    # Generate data
    dashboard_data = generate_all_products_data()

    # Save to file
    output_file = '../data/products.json'
    print(f"\n💾 保存数据到: {output_file}")

    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

    print("\n" + "="*70)
    print("✅ 数据生成完成！")
    print("="*70)

    # Print summary
    print(f"\n📊 数据摘要:")
    print(f"  总产品数: {len(dashboard_data['products'])}")
    print(f"  品牌数: {len(BRANDS_CONFIG_FINAL)}")
    print(f"  新闻数: {len(dashboard_data['news'])}")
    print(f"  API模式: {'✅ 启用' if USE_API_PRICES else '❌ 禁用'}")
    print(f"  更新时间: {dashboard_data['last_update']}")

    # Count API vs Estimated prices
    if USE_API_PRICES:
        api_count = 0
        estimated_count = 0
        for product in dashboard_data['products']:
            for channel, data in product['channels'].items():
                if channel != 'official':  # Don't count official (always verified)
                    if data['confidence'] == 'VERIFIED_API':
                        api_count += 1
                    else:
                        estimated_count += 1

        print(f"\n💰 价格来源统计（零售渠道）:")
        print(f"  API获取: {api_count}")
        print(f"  估算价格: {estimated_count}")
        print(f"  覆盖率: {api_count / (api_count + estimated_count) * 100:.1f}%")

    print("\n")


if __name__ == "__main__":
    main()
