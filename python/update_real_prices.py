"""
Real-time price update utility
Helps manually update verified prices from official sources
"""

import json
from datetime import datetime


class PriceUpdater:
    """Tool for updating real verified prices"""

    def __init__(self, database_file='real_prices_database.py', data_file='../data/products.json'):
        self.database_file = database_file
        self.data_file = data_file

        # Load current data
        with open(data_file, 'r') as f:
            self.data = json.load(f)

    def display_current_prices(self, brand=None):
        """Display current prices in the system"""
        print("=" * 70)
        print("当前系统价格")
        print("=" * 70)

        products = self.data['products']
        if brand:
            products = [p for p in products if p['brand'] == brand]

        for p in products:
            print(f"\n{p['brand']} - {p['name']}")
            print(f"  官网: ${p['channels']['official']['price']:.2f}")
            if p['channels']['amazon']['available']:
                print(f"  Amazon: ${p['channels']['amazon']['price']:.2f}")
            if 'price_source' in p['channels']['official']:
                print(f"  来源: {p['channels']['official']['price_source']}")

    def update_price_interactive(self):
        """Interactive price update tool"""
        print("\n" + "=" * 70)
        print("价格更新工具")
        print("=" * 70)
        print("\n请输入要更新的产品信息:\n")

        brand = input("品牌 (如: Eufy): ").strip()
        product_name = input("产品名称 (如: Omni S2): ").strip()
        channel = input("渠道 (official/amazon/walmart/costco/ebay): ").strip().lower()
        new_price = input("新价格 (如: 1599.99): ").strip()
        source = input("价格来源 (如: Official website): ").strip()

        try:
            new_price = float(new_price)
        except ValueError:
            print("\n❌ 价格格式错误")
            return

        # Find product
        found = False
        for p in self.data['products']:
            if p['brand'] == brand and product_name in p['name']:
                old_price = p['channels'][channel]['price']

                # Update price
                p['channels'][channel]['price'] = new_price
                p['channels'][channel]['price_source'] = source
                p['channels'][channel]['confidence'] = 'MANUALLY_VERIFIED'
                p['channels'][channel]['last_updated'] = datetime.now().isoformat()

                print(f"\n✓ 价格已更新:")
                print(f"  产品: {p['brand']} {p['name']}")
                print(f"  渠道: {channel}")
                print(f"  旧价格: ${old_price:.2f}")
                print(f"  新价格: ${new_price:.2f}")
                print(f"  来源: {source}")

                found = True
                break

        if not found:
            print(f"\n❌ 未找到产品: {brand} {product_name}")
            return

        # Save
        save = input("\n是否保存更改? (y/n): ").strip().lower()
        if save == 'y':
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)
            print("\n✓ 更改已保存到", self.data_file)
        else:
            print("\n✗ 更改未保存")

    def batch_update_from_file(self, update_file):
        """Batch update prices from JSON file"""
        print("\n批量更新功能 - 从文件导入")
        print(f"文件: {update_file}")

        try:
            with open(update_file, 'r') as f:
                updates = json.load(f)

            count = 0
            for update in updates:
                brand = update['brand']
                product_name = update['product']
                channel = update['channel']
                new_price = update['price']
                source = update.get('source', 'Batch update')

                # Find and update
                for p in self.data['products']:
                    if p['brand'] == brand and product_name in p['name']:
                        p['channels'][channel]['price'] = new_price
                        p['channels'][channel]['price_source'] = source
                        p['channels'][channel]['confidence'] = 'MANUALLY_VERIFIED'
                        count += 1
                        print(f"✓ Updated: {brand} {product_name} - {channel}: ${new_price}")
                        break

            # Save
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=2, ensure_ascii=False)

            print(f"\n✓ 批量更新完成: {count} 个价格已更新")

        except Exception as e:
            print(f"\n❌ 错误: {e}")

    def generate_price_update_template(self, output_file='price_updates_template.json'):
        """Generate a template file for batch updates"""
        template = [
            {
                "brand": "Eufy",
                "product": "Omni S2",
                "channel": "official",
                "price": 1599.99,
                "source": "Official website",
                "notes": "Verified from eufy.com/products/t2081111"
            },
            {
                "brand": "Roborock",
                "product": "Qrevo Curv 2 Flow",
                "channel": "official",
                "price": 849.99,
                "source": "Official CES 2026 announcement",
                "notes": "Launch price Jan 19, 2026"
            }
        ]

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(template, f, indent=2, ensure_ascii=False)

        print(f"✓ 模板已生成: {output_file}")
        print("\n编辑此文件后，运行:")
        print(f"  python update_real_prices.py --batch {output_file}")


def main():
    """Interactive price update tool"""
    updater = PriceUpdater()

    print("\n" + "=" * 70)
    print("Robot Vacuum Price Update Tool")
    print("=" * 70)
    print("\n选项:")
    print("  1) 查看当前价格")
    print("  2) 交互式更新单个价格")
    print("  3) 生成批量更新模板")
    print("  4) 查看Eufy产品价格")
    print("  0) 退出")

    choice = input("\n请选择 (0-4): ").strip()

    if choice == '1':
        updater.display_current_prices()
    elif choice == '2':
        updater.update_price_interactive()
    elif choice == '3':
        updater.generate_price_update_template()
    elif choice == '4':
        updater.display_current_prices(brand='Eufy')
    else:
        print("退出")


if __name__ == "__main__":
    main()
