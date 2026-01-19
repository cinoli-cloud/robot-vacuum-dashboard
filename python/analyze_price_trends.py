"""
Price trend analysis tool
Analyze historical data and provide insights
"""

import json
import statistics
from datetime import datetime
from collections import defaultdict


class PriceTrendAnalyzer:
    """Analyze price trends and provide actionable insights"""

    def __init__(self, data_file='../data/products.json'):
        with open(data_file, 'r') as f:
            self.data = json.load(f)

    def analyze_brand_performance(self):
        """Analyze price competitiveness by brand"""
        print("\n" + "=" * 60)
        print("品牌价格竞争力分析")
        print("=" * 60)

        brand_stats = {}

        for product in self.data['products']:
            brand = product['brand']
            if brand not in brand_stats:
                brand_stats[brand] = {
                    'prices': [],
                    'changes': [],
                    'product_count': 0
                }

            brand_stats[brand]['product_count'] += 1

            for channel in product['channels'].values():
                if channel['available'] and channel['price'] > 0:
                    brand_stats[brand]['prices'].append(channel['price'])
                    if channel['change'] != 0:
                        brand_stats[brand]['changes'].append(channel['change'])

        # Print analysis
        for brand in sorted(brand_stats.keys()):
            stats = brand_stats[brand]
            if not stats['prices']:
                continue

            avg_price = statistics.mean(stats['prices'])
            min_price = min(stats['prices'])
            max_price = max(stats['prices'])

            avg_change = statistics.mean(stats['changes']) if stats['changes'] else 0

            print(f"\n{brand}:")
            print(f"  产品数量: {stats['product_count']}")
            print(f"  平均价格: ${avg_price:.2f}")
            print(f"  价格区间: ${min_price:.2f} - ${max_price:.2f}")
            print(f"  平均变化: {avg_change:+.1f}%")

            # Price positioning
            if avg_price > 1000:
                print(f"  市场定位: 高端市场 💎")
            elif avg_price > 600:
                print(f"  市场定位: 中高端市场 ⭐")
            else:
                print(f"  市场定位: 大众市场 ✓")

    def find_best_deals(self, top_n=10):
        """Find products with the best price across channels"""
        print("\n" + "=" * 60)
        print(f"最优惠产品 TOP {top_n}")
        print("=" * 60)

        deals = []

        for product in self.data['products']:
            prices = []
            for channel_name, channel in product['channels'].items():
                if channel['available'] and channel['price'] > 0:
                    prices.append((channel['price'], channel_name))

            if len(prices) >= 2:
                prices.sort()
                lowest = prices[0]
                avg_price = sum(p[0] for p in prices) / len(prices)
                discount_pct = ((avg_price - lowest[0]) / avg_price) * 100

                if discount_pct > 0:
                    deals.append({
                        'brand': product['brand'],
                        'product': product['name'],
                        'lowest_price': lowest[0],
                        'channel': lowest[1],
                        'avg_price': avg_price,
                        'discount': discount_pct
                    })

        # Sort by discount percentage
        deals.sort(key=lambda x: x['discount'], reverse=True)

        for i, deal in enumerate(deals[:top_n], 1):
            print(f"\n{i}. {deal['brand']} - {deal['product']}")
            print(f"   最低价: ${deal['lowest_price']:.2f} ({deal['channel']})")
            print(f"   平均价:${deal['avg_price']:.2f}")
            print(f"   优惠幅度: {deal['discount']:.1f}% 💰")

    def identify_price_changes(self):
        """Identify significant price changes"""
        print("\n" + "=" * 60)
        print("显著价格变化")
        print("=" * 60)

        increases = []
        decreases = []

        for product in self.data['products']:
            for channel_name, channel in product['channels'].items():
                if channel['available'] and channel['change'] != 0:
                    change_data = {
                        'brand': product['brand'],
                        'product': product['name'],
                        'channel': channel_name,
                        'price': channel['price'],
                        'change': channel['change']
                    }

                    if channel['change'] > 0:
                        increases.append(change_data)
                    else:
                        decreases.append(change_data)

        # Show top increases
        if increases:
            increases.sort(key=lambda x: x['change'], reverse=True)
            print("\n📈 价格上涨 TOP 5:")
            for item in increases[:5]:
                print(f"  • {item['brand']} {item['product']}")
                print(f"    {item['channel']}: ${item['price']:.2f} (+{item['change']:.1f}%)")

        # Show top decreases
        if decreases:
            decreases.sort(key=lambda x: x['change'])
            print("\n📉 价格下降 TOP 5:")
            for item in decreases[:5]:
                print(f"  • {item['brand']} {item['product']}")
                print(f"    {item['channel']}: ${item['price']:.2f} ({item['change']:.1f}%)")

    def channel_comparison(self):
        """Compare average prices across channels"""
        print("\n" + "=" * 60)
        print("渠道价格对比")
        print("=" * 60)

        channel_stats = defaultdict(lambda: {'prices': [], 'count': 0})

        for product in self.data['products']:
            for channel_name, channel in product['channels'].items():
                if channel['available'] and channel['price'] > 0:
                    channel_stats[channel_name]['prices'].append(channel['price'])
                    channel_stats[channel_name]['count'] += 1

        channel_averages = []
        for channel, stats in channel_stats.items():
            if stats['prices']:
                avg = statistics.mean(stats['prices'])
                channel_averages.append((channel, avg, stats['count']))

        channel_averages.sort(key=lambda x: x[1])

        print("\n各渠道平均价格（从低到高）:")
        for channel, avg, count in channel_averages:
            print(f"  {channel.capitalize():12} ${avg:8.2f}  ({count} 产品)")

    def generate_report(self):
        """Generate comprehensive analysis report"""
        print("\n" + "=" * 70)
        print("竞品价格分析报告")
        print(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        # Brand performance
        self.analyze_brand_performance()

        # Channel comparison
        self.channel_comparison()

        # Best deals
        self.find_best_deals(top_n=10)

        # Price changes
        self.identify_price_changes()

        print("\n" + "=" * 70)
        print("报告生成完成")
        print("=" * 70)


def main():
    """Generate analysis report"""
    analyzer = PriceTrendAnalyzer()
    analyzer.generate_report()


if __name__ == "__main__":
    main()
