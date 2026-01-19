"""
Price alert system
Monitor price changes and send notifications
"""

import json
from datetime import datetime


class PriceAlertSystem:
    """Monitor prices and trigger alerts based on configured rules"""

    def __init__(self, data_file='../data/products.json', config_file='alert_config.json'):
        with open(data_file, 'r') as f:
            self.data = json.load(f)

        # Try to load alert configuration
        try:
            with open(config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            # Create default configuration
            self.config = {
                'enabled': True,
                'rules': [
                    {
                        'name': 'Large Price Drop',
                        'type': 'price_decrease',
                        'threshold': -5.0,  # -5% or more
                        'enabled': True
                    },
                    {
                        'name': 'Large Price Increase',
                        'type': 'price_increase',
                        'threshold': 5.0,  # +5% or more
                        'enabled': True
                    },
                    {
                        'name': 'New Low Price',
                        'type': 'price_below',
                        'threshold': 500,  # Below $500
                        'enabled': True
                    }
                ],
                'notification': {
                    'email': {
                        'enabled': False,
                        'recipients': ['your-email@example.com']
                    },
                    'slack': {
                        'enabled': False,
                        'webhook_url': 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'
                    }
                }
            }
            # Save default config
            with open(config_file, 'w') as f:
                json.dump(self.config, f, indent=2)

    def check_alerts(self):
        """Check all products against alert rules"""
        alerts = []

        if not self.config['enabled']:
            return alerts

        for product in self.data['products']:
            for channel_name, channel in product['channels'].items():
                if not channel['available']:
                    continue

                # Check each rule
                for rule in self.config['rules']:
                    if not rule['enabled']:
                        continue

                    alert = None

                    if rule['type'] == 'price_decrease':
                        if channel['change'] <= rule['threshold']:
                            alert = {
                                'type': 'Price Drop Alert',
                                'brand': product['brand'],
                                'product': product['name'],
                                'channel': channel_name,
                                'price': channel['price'],
                                'change': channel['change'],
                                'message': f"Price dropped by {abs(channel['change']):.1f}%"
                            }

                    elif rule['type'] == 'price_increase':
                        if channel['change'] >= rule['threshold']:
                            alert = {
                                'type': 'Price Increase Alert',
                                'brand': product['brand'],
                                'product': product['name'],
                                'channel': channel_name,
                                'price': channel['price'],
                                'change': channel['change'],
                                'message': f"Price increased by {channel['change']:.1f}%"
                            }

                    elif rule['type'] == 'price_below':
                        if channel['price'] > 0 and channel['price'] <= rule['threshold']:
                            alert = {
                                'type': 'Low Price Alert',
                                'brand': product['brand'],
                                'product': product['name'],
                                'channel': channel_name,
                                'price': channel['price'],
                                'change': channel['change'],
                                'message': f"Price is now ${channel['price']:.2f} (below ${rule['threshold']})"
                            }

                    if alert:
                        alerts.append(alert)

        return alerts

    def display_alerts(self):
        """Display all triggered alerts"""
        print("=" * 70)
        print("价格警报系统")
        print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)

        alerts = self.check_alerts()

        if not alerts:
            print("\n✓ 没有触发任何警报")
            print("\n当前警报规则:")
            for rule in self.config['rules']:
                status = "✓" if rule['enabled'] else "✗"
                print(f"  {status} {rule['name']}")
        else:
            print(f"\n🔔 发现 {len(alerts)} 个价格警报:\n")

            # Group by type
            by_type = {}
            for alert in alerts:
                alert_type = alert['type']
                if alert_type not in by_type:
                    by_type[alert_type] = []
                by_type[alert_type].append(alert)

            for alert_type, items in by_type.items():
                print(f"\n{alert_type} ({len(items)} 个):")
                for alert in items:
                    print(f"  • {alert['brand']} {alert['product']}")
                    print(f"    {alert['channel']}: ${alert['price']:.2f}")
                    print(f"    {alert['message']}")

        print("\n" + "=" * 70)

        # Show notification configuration
        print("\n通知设置:")
        email_status = "✓ 已启用" if self.config['notification']['email']['enabled'] else "✗ 未启用"
        slack_status = "✓ 已启用" if self.config['notification']['slack']['enabled'] else "✗ 未启用"
        print(f"  邮件通知: {email_status}")
        print(f"  Slack通知: {slack_status}")

        if self.config['notification']['email']['enabled']:
            print(f"  邮件接收人: {', '.join(self.config['notification']['email']['recipients'])}")

        print("\n配置文件: alert_config.json")
        print("=" * 70)

        return alerts

    def send_notifications(self, alerts):
        """Send notifications via configured channels"""
        if not alerts:
            return

        # Email notification
        if self.config['notification']['email']['enabled']:
            print("\n📧 发送邮件通知...")
            # In production, implement email sending here
            print("  (邮件通知功能需要配置 SMTP 服务器)")

        # Slack notification
        if self.config['notification']['slack']['enabled']:
            print("\n💬 发送Slack通知...")
            # In production, implement Slack webhook here
            print("  (Slack通知功能需要配置 Webhook URL)")


def main():
    """Run price alert check"""
    alert_system = PriceAlertSystem()
    alerts = alert_system.display_alerts()

    # Optionally send notifications
    if alerts:
        alert_system.send_notifications(alerts)


if __name__ == "__main__":
    main()
