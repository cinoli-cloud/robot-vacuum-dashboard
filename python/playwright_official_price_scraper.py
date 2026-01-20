"""
Playwright Official Price Scraper
自动爬取品牌官网的实时价格（支持JavaScript动态加载和Coupon处理）
支持：Roborock、Eufy
"""

import asyncio
import json
import re
from datetime import datetime
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class PlaywrightPriceScraper:
    """官网价格爬虫（使用Playwright）"""

    def __init__(self):
        # 产品URL配置（从飞书文档提取）
        self.products = {
            'Roborock': [
                {'name': 'Saros Z70', 'url': 'https://us.roborock.com/products/roborock-saros-z70'},
                {'name': 'Saros 10R', 'url': 'https://us.roborock.com/products/roborock-saros-10r'},
                {'name': 'Saros 10', 'url': 'https://us.roborock.com/products/roborock-saros-10'},
                {'name': 'Qrevo Curv 2 Flow', 'url': 'https://us.roborock.com/products/roborock-qrevo-curv-2-flow'},
                {'name': 'Qrevo CurvX', 'url': 'https://us.roborock.com/products/roborock-qrevo-curv-x'},
            ],
            'Eufy': [
                {'name': 'Omni S2', 'url': 'https://www.eufy.com/products/t2081111?variant=45474923249850'},
                {'name': 'Omni S1 Pro', 'url': 'https://www.eufy.com/products/t2080111?ref=navimenu_2_1_1_2_img'},
                {'name': 'X10 Pro Omni', 'url': 'https://www.eufy.com/products/t2351111?variant=43078499532986'},
                {'name': 'Omni E28', 'url': 'https://www.eufy.com/products/t2352111?ref=navimenu_2_1_1_1_img&variant=44777786867898'},
                {'name': 'Omni E25', 'url': 'https://www.eufy.com/products/t2353111?ref=navimenu_2_1_1_2_img&variant=44777910075578'},
                {'name': 'L60', 'url': 'https://www.eufy.com/products/t2277111?variant=42812301017274'},
                {'name': 'Omni C20', 'url': 'https://www.eufy.com/products/t2280111?ref=navimenu_2_1_1_1_img&variant=44222902993082'},
            ]
        }

    def extract_price_number(self, price_text):
        """从价格文本中提取数字"""
        if not price_text:
            return None
        # 移除$符号、逗号、空格
        price_str = price_text.replace('$', '').replace(',', '').replace(' ', '').strip()
        try:
            return float(price_str)
        except:
            return None

    async def scrape_roborock_price(self, page, product):
        """
        爬取Roborock官网价格
        规则：折后价是放大加粗的价格，划线价是原价
        """
        url = product['url']
        product_name = product['name']

        try:
            logger.info(f"  访问: {url}")

            # 访问产品页面
            await page.goto(url, wait_until='networkidle', timeout=30000)

            # 等待价格元素加载
            await page.wait_for_timeout(2000)

            # 策略1：查找价格元素（通常是大号加粗的价格）
            sale_price = None
            original_price = None

            # 尝试多种选择器找到折后价（放大加粗的价格）
            sale_price_selectors = [
                '.price--large',
                '.price-item--sale',
                '[class*="sale-price"]',
                '[class*="current-price"]',
                '.product-price .price',
                'span.money'
            ]

            for selector in sale_price_selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        price_text = await element.inner_text()
                        sale_price = self.extract_price_number(price_text)
                        if sale_price:
                            logger.info(f"    ✅ 找到折后价: ${sale_price}")
                            break
                except:
                    continue

            # 尝试找到原价（划线价格）
            original_price_selectors = [
                '.price--compare-at',
                '.price-item--regular',
                '[class*="compare-at-price"]',
                '[class*="original-price"]',
                's.money',
                'del.money'
            ]

            for selector in original_price_selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        price_text = await element.inner_text()
                        original_price = self.extract_price_number(price_text)
                        if original_price:
                            logger.info(f"    ✅ 找到原价: ${original_price}")
                            break
                except:
                    continue

            # 如果没找到划线价，说明没有折扣
            if sale_price and not original_price:
                original_price = sale_price

            return {
                'brand': 'Roborock',
                'product': product_name,
                'url': url,
                'sale_price': sale_price,
                'original_price': original_price,
                'has_discount': sale_price != original_price if (sale_price and original_price) else False,
                'discount_amount': (original_price - sale_price) if (sale_price and original_price) else 0,
                'success': sale_price is not None
            }

        except Exception as e:
            logger.error(f"    ❌ 爬取失败: {e}")
            return {
                'brand': 'Roborock',
                'product': product_name,
                'url': url,
                'sale_price': None,
                'original_price': None,
                'success': False,
                'error': str(e)
            }

    async def scrape_eufy_price(self, page, product):
        """
        爬取Eufy官网价格
        规则：需要勾选蓝色Coupon才能获取真实折后价
        """
        url = product['url']
        product_name = product['name']

        try:
            logger.info(f"  访问: {url}")

            # 访问产品页面
            await page.goto(url, wait_until='networkidle', timeout=30000)

            # 等待页面加载
            await page.wait_for_timeout(3000)

            # 策略1：查找Coupon checkbox并勾选
            coupon_checked = False
            try:
                # 查找Coupon checkbox
                coupon_selectors = [
                    'input[type="checkbox"][class*="coupon"]',
                    'input[type="checkbox"][class*="discount"]',
                    '.coupon-checkbox',
                    '[class*="coupon"] input[type="checkbox"]'
                ]

                for selector in coupon_selectors:
                    coupon = page.locator(selector).first
                    if await coupon.count() > 0:
                        # 检查是否已勾选
                        is_checked = await coupon.is_checked()
                        if not is_checked:
                            # 勾选Coupon
                            await coupon.click()
                            logger.info(f"    ✅ 已勾选Coupon")
                            coupon_checked = True
                            # 等待价格更新
                            await page.wait_for_timeout(1000)
                        break
            except Exception as e:
                logger.warning(f"    ⚠️  未找到Coupon: {e}")

            # 策略2：提取价格
            sale_price = None
            original_price = None
            coupon_amount = None

            # 查找折后价（显示的主要价格）
            sale_price_selectors = [
                '.product-price__price',
                '.price__sale .price-item--sale',
                '[class*="sale-price"]',
                '.price .money',
                '[data-product-price]'
            ]

            for selector in sale_price_selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        price_text = await element.inner_text()
                        sale_price = self.extract_price_number(price_text)
                        if sale_price:
                            logger.info(f"    ✅ 找到折后价: ${sale_price}")
                            break
                except:
                    continue

            # 查找原价
            original_price_selectors = [
                '.price__compare-at',
                '.price__regular',
                '[class*="compare-at"]',
                's.money',
                'del.money'
            ]

            for selector in original_price_selectors:
                try:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        price_text = await element.inner_text()
                        original_price = self.extract_price_number(price_text)
                        if original_price:
                            logger.info(f"    ✅ 找到原价: ${original_price}")
                            break
                except:
                    continue

            # 查找Coupon金额
            try:
                coupon_selectors = [
                    '[class*="coupon"] [class*="saving"]',
                    '[class*="save"] [class*="amount"]',
                    '.coupon-amount'
                ]
                for selector in coupon_selectors:
                    element = await page.locator(selector).first
                    if await element.count() > 0:
                        text = await element.inner_text()
                        # 提取Saving金额（如"Saving $350.00"）
                        match = re.search(r'\$?(\d+\.?\d*)', text)
                        if match:
                            coupon_amount = float(match.group(1))
                            logger.info(f"    ✅ Coupon金额: ${coupon_amount}")
                            break
            except:
                pass

            # 如果没找到原价但有coupon，计算原价
            if sale_price and coupon_amount and not original_price:
                original_price = sale_price + coupon_amount

            # 如果没有折扣
            if sale_price and not original_price:
                original_price = sale_price

            return {
                'brand': 'Eufy',
                'product': product_name,
                'url': url,
                'sale_price': sale_price,
                'original_price': original_price,
                'coupon_amount': coupon_amount,
                'coupon_applied': coupon_checked,
                'has_discount': sale_price != original_price if (sale_price and original_price) else False,
                'discount_amount': (original_price - sale_price) if (sale_price and original_price) else 0,
                'success': sale_price is not None
            }

        except Exception as e:
            logger.error(f"    ❌ 爬取失败: {e}")
            return {
                'brand': 'Eufy',
                'product': product_name,
                'url': url,
                'sale_price': None,
                'original_price': None,
                'success': False,
                'error': str(e)
            }

    async def scrape_all_prices(self):
        """爬取所有品牌的价格"""
        results = []

        async with async_playwright() as p:
            # 启动浏览器（无头模式）
            browser = await p.chromium.launch(headless=True)

            # 创建浏览器上下文
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                viewport={'width': 1920, 'height': 1080}
            )

            page = await context.new_page()

            logger.info("="*70)
            logger.info("🚀 开始爬取官网价格")
            logger.info("="*70)

            # 爬取Roborock
            logger.info(f"\n📍 爬取Roborock官网价格（{len(self.products['Roborock'])}个产品）")
            for idx, product in enumerate(self.products['Roborock'], 1):
                logger.info(f"\n[{idx}/{len(self.products['Roborock'])}] {product['name']}")
                result = await self.scrape_roborock_price(page, product)
                results.append(result)

                # 延迟，避免请求过快
                await asyncio.sleep(3)

            # 爬取Eufy
            logger.info(f"\n📍 爬取Eufy官网价格（{len(self.products['Eufy'])}个产品）")
            for idx, product in enumerate(self.products['Eufy'], 1):
                logger.info(f"\n[{idx}/{len(self.products['Eufy'])}] {product['name']}")
                result = await self.scrape_eufy_price(page, product)
                results.append(result)

                # 延迟
                await asyncio.sleep(3)

            await browser.close()

        return results

    def save_results(self, results, output_file='../data/official_prices.json'):
        """保存爬取结果到JSON文件"""
        data = {
            'last_update': datetime.now().isoformat(),
            'total_products': len(results),
            'successful': sum(1 for r in results if r['success']),
            'failed': sum(1 for r in results if not r['success']),
            'prices': results
        }

        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        logger.info(f"\n💾 结果已保存到: {output_file}")

    def print_summary(self, results):
        """打印爬取摘要"""
        logger.info("\n" + "="*70)
        logger.info("📊 爬取结果统计")
        logger.info("="*70)

        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]

        logger.info(f"\n✅ 成功: {len(successful)} 个")
        logger.info(f"❌ 失败: {len(failed)} 个")

        if successful:
            logger.info(f"\n💰 成功爬取的价格：")
            for r in successful:
                discount_info = f" (原价: ${r['original_price']}, 优惠: ${r['discount_amount']})" if r['has_discount'] else ""
                logger.info(f"  ✅ {r['brand']} {r['product']}: ${r['sale_price']}{discount_info}")

        if failed:
            logger.info(f"\n⚠️  失败的产品：")
            for r in failed:
                logger.info(f"  ❌ {r['brand']} {r['product']}: {r.get('error', 'Unknown error')}")


async def main():
    """主函数"""
    print("\n" + "="*70)
    print("🤖 Playwright官网价格爬虫")
    print("="*70)

    scraper = PlaywrightPriceScraper()

    # 爬取所有价格
    results = await scraper.scrape_all_prices()

    # 打印摘要
    scraper.print_summary(results)

    # 保存结果
    scraper.save_results(results)

    print("\n" + "="*70)
    print("✅ 爬取完成！")
    print("="*70)
    print()


if __name__ == "__main__":
    asyncio.run(main())
