"""
整合第三方平台价格到products.json
读取 thirdparty_prices.json，更新 products.json 中的Best Buy、eBay、Walmart价格
"""

import json
import os
from datetime import datetime


def integrate_thirdparty_prices():
    """整合第三方平台价格"""

    print("\n" + "="*70)
    print("🔧 整合第三方平台价格数据")
    print("="*70)

    # 读取第三方平台价格
    thirdparty_file = '../data/thirdparty_prices.json'
    products_file = '../data/products.json'

    # 检查文件是否存在
    if not os.path.exists(thirdparty_file):
        print(f"⚠️  第三方价格文件不存在: {thirdparty_file}")
        print("   Playwright爬虫可能还未运行，跳过整合")
        return False

    # 读取第三方价格
    print(f"\n📖 读取第三方价格: {thirdparty_file}")
    with open(thirdparty_file, 'r', encoding='utf-8') as f:
        thirdparty_data = json.load(f)

    scraped_products = thirdparty_data.get('products', [])
    print(f"✅ 找到 {len(scraped_products)} 个产品的第三方价格")
    print(f"   成功率: {thirdparty_data.get('success_rate', 'N/A')}")

    # 读取产品数据
    if not os.path.exists(products_file):
        print(f"❌ 产品数据文件不存在: {products_file}")
        return False

    print(f"\n📖 读取产品数据: {products_file}")
    with open(products_file, 'r', encoding='utf-8') as f:
        dashboard_data = json.load(f)

    products = dashboard_data.get('products', [])
    print(f"✅ 找到 {len(products)} 个产品")

    # 创建价格映射（品牌+产品名 → 价格和URL）
    price_map = {}
    for item in scraped_products:
        key = f"{item['brand']}_{item['name']}"
        price_map[key] = {
            'prices': item['prices'],
            'urls': item.get('urls', {})
        }

    print(f"\n🔄 开始整合第三方平台价格和URL...")
    updated_count = 0

    # 更新产品数据
    for product in products:
        brand = product.get('brand', '')
        name = product.get('name', '')
        key = f"{brand}_{name}"

        if key in price_map:
            data = price_map[key]
            prices_data = data['prices']
            urls_data = data['urls']

            # 更新Best Buy价格和URL
            if prices_data.get('bestbuy') and 'channels' in product:
                if 'bestbuy' not in product['channels']:
                    product['channels']['bestbuy'] = {}

                old_price = product['channels'].get('bestbuy', {}).get('price')
                new_price = prices_data['bestbuy']

                product['channels']['bestbuy']['price'] = new_price
                product['channels']['bestbuy']['confidence'] = 'VERIFIED_PLAYWRIGHT'
                product['channels']['bestbuy']['price_source'] = 'Playwright Scraper - Direct URL'

                # 更新URL（重要！用于点击跳转）
                if urls_data.get('bestbuy'):
                    product['channels']['bestbuy']['url'] = urls_data['bestbuy']

                print(f"  ✅ {brand} {name} - Best Buy: ${old_price} → ${new_price}")
                updated_count += 1

            # 更新eBay价格和URL
            if prices_data.get('ebay') and 'channels' in product and 'ebay' in product['channels']:
                old_price = product['channels']['ebay'].get('price')
                new_price = prices_data['ebay']

                product['channels']['ebay']['price'] = new_price
                product['channels']['ebay']['confidence'] = 'VERIFIED_PLAYWRIGHT'
                product['channels']['ebay']['price_source'] = 'Playwright Scraper - Direct URL'

                # 更新URL（重要！用于点击跳转）
                if urls_data.get('ebay'):
                    product['channels']['ebay']['url'] = urls_data['ebay']

                print(f"  ✅ {brand} {name} - eBay: ${old_price} → ${new_price}")

            # 更新Walmart价格（如果有）
            if prices_data.get('walmart') and 'channels' in product and 'walmart' in product['channels']:
                old_price = product['channels']['walmart'].get('price')
                new_price = prices_data['walmart']

                product['channels']['walmart']['price'] = new_price
                product['channels']['walmart']['confidence'] = 'VERIFIED_PLAYWRIGHT'
                product['channels']['walmart']['price_source'] = 'Playwright Scraper'

                print(f"  ✅ {brand} {name} - Walmart: ${old_price} → ${new_price}")

    print(f"\n✅ 更新了 {updated_count} 个产品的第三方平台价格")

    # 更新last_update时间
    dashboard_data['last_update'] = datetime.now().isoformat()

    # 保存更新后的数据
    print(f"\n💾 保存更新后的数据到: {products_file}")
    with open(products_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

    print("\n" + "="*70)
    print("✅ 第三方平台价格整合完成！")
    print("="*70)
    print()

    return True


if __name__ == "__main__":
    success = integrate_thirdparty_prices()
    exit(0 if success else 1)
