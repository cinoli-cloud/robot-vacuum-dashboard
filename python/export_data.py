"""
Data export utility
Export dashboard data to CSV/Excel format
"""

import json
import csv
from datetime import datetime


class DataExporter:
    """Export price data to various formats"""

    def __init__(self, data_file='../data/products.json'):
        with open(data_file, 'r') as f:
            self.data = json.load(f)

    def export_to_csv(self, output_file='../data/price_export.csv'):
        """Export current prices to CSV"""
        print(f"正在导出数据到 CSV...")

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'Brand', 'Product', 'Model',
                'Official_Price', 'Official_Change',
                'Amazon_Price', 'Amazon_Change',
                'Walmart_Price', 'Walmart_Change',
                'Costco_Price', 'Costco_Change',
                'eBay_Price', 'eBay_Change',
                'Lowest_Price', 'Lowest_Channel',
                'Average_Price'
            ]

            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for product in self.data['products']:
                # Collect all valid prices
                prices = []
                for channel_name, channel in product['channels'].items():
                    if channel['available'] and channel['price'] > 0:
                        prices.append((channel['price'], channel_name))

                # Calculate lowest and average
                lowest_price = min(prices, key=lambda x: x[0]) if prices else (0, 'N/A')
                avg_price = sum(p[0] for p in prices) / len(prices) if prices else 0

                row = {
                    'Brand': product['brand'],
                    'Product': product['name'],
                    'Model': product['model'],
                    'Official_Price': product['channels']['official']['price'],
                    'Official_Change': product['channels']['official']['change'],
                    'Amazon_Price': product['channels']['amazon']['price'],
                    'Amazon_Change': product['channels']['amazon']['change'],
                    'Walmart_Price': product['channels']['walmart']['price'],
                    'Walmart_Change': product['channels']['walmart']['change'],
                    'Costco_Price': product['channels']['costco']['price'],
                    'Costco_Change': product['channels']['costco']['change'],
                    'eBay_Price': product['channels']['ebay']['price'],
                    'eBay_Change': product['channels']['ebay']['change'],
                    'Lowest_Price': lowest_price[0],
                    'Lowest_Channel': lowest_price[1],
                    'Average_Price': round(avg_price, 2)
                }

                writer.writerow(row)

        print(f"✓ CSV 导出完成: {output_file}")
        print(f"  共 {len(self.data['products'])} 个产品")

    def export_price_history_csv(self, output_file='../data/price_history_export.csv'):
        """Export price history to CSV"""
        print(f"正在导出价格历史到 CSV...")

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)

            # Write header
            header = ['Date'] + list(self.data['priceHistory'].keys())
            writer.writerow(header)

            # Get dates from first brand
            first_brand = list(self.data['priceHistory'].keys())[0]
            dates = self.data['priceHistory'][first_brand]['dates']

            # Write data rows
            for i, date in enumerate(dates):
                row = [date]
                for brand in self.data['priceHistory'].keys():
                    row.append(self.data['priceHistory'][brand]['prices'][i])
                writer.writerow(row)

        print(f"✓ 历史数据导出完成: {output_file}")
        print(f"  共 {len(dates)} 天的数据")

    def export_news_csv(self, output_file='../data/news_export.csv'):
        """Export news to CSV"""
        print(f"正在导出新闻数据到 CSV...")

        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Brand', 'Title', 'Summary', 'Source', 'Date', 'URL']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            for news_item in self.data['news']:
                writer.writerow({
                    'Brand': news_item['brand'],
                    'Title': news_item['title'],
                    'Summary': news_item['summary'],
                    'Source': news_item['source'],
                    'Date': news_item['date'][:10],
                    'URL': news_item['url']
                })

        print(f"✓ 新闻数据导出完成: {output_file}")
        print(f"  共 {len(self.data['news'])} 条新闻")

    def export_all(self):
        """Export all data to CSV files"""
        print("=" * 60)
        print("数据导出工具")
        print(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        # Export current prices
        self.export_to_csv()

        # Export price history
        self.export_price_history_csv()

        # Export news
        self.export_news_csv()

        print("=" * 60)
        print("✓ 所有数据导出完成")
        print("=" * 60)


def main():
    """Main export function"""
    exporter = DataExporter()
    exporter.export_all()


if __name__ == "__main__":
    main()
