"""
整合Playwright爬取的官网价格到products.json
读取 official_prices.json，更新 products.json 中的官网价格
"""

import json
import os
from datetime import datetime


def integrate_official_prices():
    """整合官网价格"""

    print("\n" + "="*70)
    print("🔧 整合官网价格数据")
    print("="*70)

    # 读取Playwright爬取的官网价格
    official_prices_file = '../data/official_prices.json'
    products_file = '../data/products.json'

    # 检查官网价格文件是否存在
    if not os.path.exists(official_prices_file):
        print(f"⚠️  官网价格文件不存在: {official_prices_file}")
        print("   Playwright爬虫可能还未运行，跳过整合")
        return False

    # 读取官网价格
    print(f"\n📖 读取官网价格: {official_prices_file}")
    with open(official_prices_file, 'r', encoding='utf-8') as f:
        official_data = json.load(f)

    official_prices = official_data.get('prices', [])
    print(f"✅ 找到 {len(official_prices)} 个官网价格")

    # 读取产品数据
    if not os.path.exists(products_file):
        print(f"❌ 产品数据文件不存在: {products_file}")
        return False

    print(f"\n📖 读取产品数据: {products_file}")
    with open(products_file, 'r', encoding='utf-8') as f:
        dashboard_data = json.load(f)

    products = dashboard_data.get('products', [])
    print(f"✅ 找到 {len(products)} 个产品")

    # 创建官网价格映射
    price_map = {}
    for price_data in official_prices:
        if price_data['success']:
            key = f"{price_data['brand']}_{price_data['product']}"
            price_map[key] = price_data

    print(f"\n🔄 开始整合官网价格...")
    updated_count = 0

    # 更新产品数据
    for product in products:
        brand = product.get('brand', '')
        name = product.get('name', '')
        key = f"{brand}_{name}"

        if key in price_map:
            price_data = price_map[key]

            # 更新官网渠道的价格
            if 'channels' in product and 'official' in product['channels']:
                old_price = product['channels']['official'].get('price')
                new_price = price_data['sale_price']

                product['channels']['official']['price'] = new_price
                product['channels']['official']['confidence'] = 'VERIFIED_PLAYWRIGHT'
                product['channels']['official']['price_source'] = 'Playwright Scraper'

                # 更新MSRP（如果有原价）
                if price_data.get('original_price'):
                    product['msrp'] = price_data['original_price']

                updated_count += 1
                print(f"  ✅ {brand} {name}: ${old_price} → ${new_price}")

    print(f"\n✅ 更新了 {updated_count} 个产品的官网价格")

    # 更新last_update时间
    dashboard_data['last_update'] = datetime.now().isoformat()

    # 保存更新后的数据
    print(f"\n💾 保存更新后的数据到: {products_file}")
    with open(products_file, 'w', encoding='utf-8') as f:
        json.dump(dashboard_data, f, indent=2, ensure_ascii=False)

    print("\n" + "="*70)
    print("✅ 官网价格整合完成！")
    print("="*70)
    print()

    return True


if __name__ == "__main__":
    success = integrate_official_prices()
    exit(0 if success else 1)
