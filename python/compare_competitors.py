"""
Competitor Price Comparison Tool
Quick analysis of Eufy vs competitors
"""

import json
from collections import defaultdict


class CompetitorAnalyzer:
    """Analyze Eufy vs competitor pricing"""

    def __init__(self, data_file='../data/products.json'):
        with open(data_file, 'r') as f:
            self.data = json.load(f)

    def compare_eufy_vs_all(self):
        """Compare Eufy products against all competitors"""
        print("=" * 70)
        print("Eufy vs 竞品价格对比分析")
        print("=" * 70)

        eufy_products = [p for p in self.data['products'] if p['brand'] == 'Eufy']

        for eufy_p in eufy_products:
            print(f"\n{'─' * 70}")
            print(f"【Eufy {eufy_p['name']}】")
            print(f"{'─' * 70}")

            # Get Eufy price
            eufy_price = eufy_p['channels']['official']['price']
            print(f"\nEufy官网价: ${eufy_price:.2f}")

            if eufy_p['channels']['amazon']['available']:
                print(f"Eufy Amazon: ${eufy_p['channels']['amazon']['price']:.2f}")

            # Find similar priced competitors (±30%)
            price_min = eufy_price * 0.70
            price_max = eufy_price * 1.30

            print(f"\n同价位竞品 (${price_min:.0f} - ${price_max:.0f}):")

            competitors = []
            for p in self.data['products']:
                if p['brand'] == 'Eufy':
                    continue

                comp_price = p['channels']['official']['price']
                if price_min <= comp_price <= price_max:
                    competitors.append({
                        'brand': p['brand'],
                        'name': p['name'],
                        'price': comp_price,
                        'features': p.get('key_features', ''),
                        'amazon': p['channels']['amazon']['price'] if p['channels']['amazon']['available'] else 0
                    })

            # Sort by price
            competitors.sort(key=lambda x: x['price'])

            for comp in competitors[:8]:  # Top 8 competitors
                print(f"\n  • {comp['brand']} {comp['name']}")
                print(f"    官网: ${comp['price']:.2f}")
                if comp['amazon'] > 0:
                    print(f"    Amazon: ${comp['amazon']:.2f}")
                # Show key features (first 60 chars)
                features = comp['features'][:60] + '...' if len(comp['features']) > 60 else comp['features']
                if features:
                    print(f"    特性: {features}")

                # Price comparison
                diff = eufy_price - comp['price']
                if abs(diff) < 50:
                    print(f"    对比: 价格相当 (差${abs(diff):.2f})")
                elif diff > 0:
                    print(f"    对比: Eufy贵${diff:.2f} ⚠️")
                else:
                    print(f"    对比: Eufy便宜${abs(diff):.2f} ✅")

    def find_best_deals(self):
        """Find products with best prices across all brands"""
        print("\n" + "=" * 70)
        print("全市场最佳价格 TOP 10")
        print("=" * 70)

        deals = []
        for p in self.data['products']:
            prices = []
            for channel_name, channel in p['channels'].items():
                if channel['available'] and channel['price'] > 0:
                    prices.append((channel['price'], channel_name))

            if len(prices) >= 2:
                prices.sort()
                lowest = prices[0]
                highest = prices[-1]
                savings = highest[0] - lowest[0]

                if savings > 50:  # Meaningful savings
                    deals.append({
                        'brand': p['brand'],
                        'product': p['name'],
                        'lowest_price': lowest[0],
                        'lowest_channel': lowest[1],
                        'highest_price': highest[0],
                        'savings': savings,
                        'savings_pct': (savings / highest[0]) * 100
                    })

        deals.sort(key=lambda x: x['savings'], reverse=True)

        for i, deal in enumerate(deals[:10], 1):
            print(f"\n{i}. {deal['brand']} {deal['product']}")
            print(f"   最低价: ${deal['lowest_price']:.2f} ({deal['lowest_channel']})")
            print(f"   最高价: ${deal['highest_price']:.2f}")
            print(f"   可省: ${deal['savings']:.2f} ({deal['savings_pct']:.1f}%)")

    def eufy_competitive_position(self):
        """Analyze Eufy's competitive positioning"""
        print("\n" + "=" * 70)
        print("Eufy市场竞争力分析")
        print("=" * 70)

        eufy_products = [p for p in self.data['products'] if p['brand'] == 'Eufy']
        all_products = self.data['products']

        # Calculate Eufy average
        eufy_prices = []
        for p in eufy_products:
            for ch in p['channels'].values():
                if ch['available'] and ch['price'] > 0:
                    eufy_prices.append(ch['price'])

        eufy_avg = sum(eufy_prices) / len(eufy_prices) if eufy_prices else 0

        # Compare with each brand
        print(f"\nEufy平均价格: ${eufy_avg:.2f}")
        print("\n与竞品对比:")

        for brand in ['Roborock', 'Dreame', 'Ecovacs', 'Shark', 'Narwal', 'iRobot', 'Dyson']:
            brand_products = [p for p in all_products if p['brand'] == brand]
            if not brand_products:
                continue

            brand_prices = []
            for p in brand_products:
                for ch in p['channels'].values():
                    if ch['available'] and ch['price'] > 0:
                        brand_prices.append(ch['price'])

            if brand_prices:
                brand_avg = sum(brand_prices) / len(brand_prices)
                diff = eufy_avg - brand_avg
                pct = (diff / brand_avg) * 100 if brand_avg > 0 else 0

                symbol = "✅" if diff < 0 else "⚠️"
                comparison = f"Eufy便宜${abs(diff):.2f} ({abs(pct):.1f}%)" if diff < 0 else f"Eufy贵${diff:.2f} ({pct:.1f}%)"

                print(f"  {symbol} {brand:12} 平均${brand_avg:.2f}  → {comparison}")

    def show_verified_prices(self):
        """Show all verified prices with sources"""
        print("\n" + "=" * 70)
        print("已验证价格清单")
        print("=" * 70)

        verified_count = 0
        for p in self.data['products']:
            has_verified = False
            for channel_name, ch in p['channels'].items():
                if ch.get('confidence') in ['VERIFIED', 'VERIFIED_SALE'] and ch['available']:
                    if not has_verified:
                        print(f"\n{p['brand']} {p['name']}:")
                        has_verified = True

                    source = ch.get('price_source', 'Unknown')
                    confidence = ch.get('confidence', '')
                    print(f"  ✓ {channel_name.capitalize()}: ${ch['price']:.2f}")
                    print(f"    来源: {source}")
                    print(f"    可信度: {confidence}")
                    verified_count += 1

        print(f"\n总计: {verified_count} 个已验证价格")


def main():
    """Run competitor analysis"""
    analyzer = CompetitorAnalyzer()

    print("\n" + "=" * 70)
    print("竞品价格对比工具")
    print("=" * 70)
    print("\n选项:")
    print("  1) Eufy vs 所有竞品对比")
    print("  2) 查找全市场最佳价格")
    print("  3) Eufy市场竞争力分析")
    print("  4) 查看所有已验证价格")
    print("  0) 退出")

    choice = input("\n请选择 (0-4): ").strip()

    if choice == '1':
        analyzer.compare_eufy_vs_all()
    elif choice == '2':
        analyzer.find_best_deals()
    elif choice == '3':
        analyzer.eufy_competitive_position()
    elif choice == '4':
        analyzer.show_verified_prices()
    else:
        print("退出")


if __name__ == "__main__":
    main()
