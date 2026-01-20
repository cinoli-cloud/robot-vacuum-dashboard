"""
测试Playwright价格爬虫
可以在本地运行测试，也可以只测试单个产品
"""

import asyncio
from playwright.async_api import async_playwright


async def test_single_product(brand, product_name, url):
    """测试单个产品的价格爬取"""
    print(f"\n{'='*70}")
    print(f"🧪 测试爬取: {brand} - {product_name}")
    print(f"{'='*70}")
    print(f"URL: {url}")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)  # 有头模式，可以看到浏览器
        context = await browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            viewport={'width': 1920, 'height': 1080}
        )
        page = await context.new_page()

        try:
            # 访问页面
            await page.goto(url, wait_until='networkidle', timeout=30000)
            print(f"\n✅ 页面加载成功")

            # 等待价格元素
            await page.wait_for_timeout(3000)

            # 截图（调试用）
            screenshot_path = f'screenshot_{brand}_{product_name}.png'.replace(' ', '_')
            await page.screenshot(path=screenshot_path)
            print(f"✅ 截图保存: {screenshot_path}")

            # 打印页面HTML（调试用）
            print(f"\n🔍 查找价格元素...")

            # 尝试查找所有可能的价格元素
            price_selectors = [
                '.price',
                '.product-price',
                '[class*="price"]',
                '.money',
                '[data-product-price]'
            ]

            for selector in price_selectors:
                elements = await page.locator(selector).all()
                if elements:
                    print(f"\n找到 {len(elements)} 个元素匹配 '{selector}':")
                    for i, elem in enumerate(elements[:5], 1):  # 只显示前5个
                        text = await elem.inner_text()
                        print(f"  [{i}] {text}")

        except Exception as e:
            print(f"\n❌ 测试失败: {e}")

        finally:
            await browser.close()


async def test_roborock():
    """测试Roborock产品"""
    await test_single_product(
        brand='Roborock',
        product_name='Saros Z70',
        url='https://us.roborock.com/products/roborock-saros-z70'
    )


async def test_eufy():
    """测试Eufy产品"""
    await test_single_product(
        brand='Eufy',
        product_name='Omni S2',
        url='https://www.eufy.com/products/t2081111?variant=45474923249850'
    )


if __name__ == "__main__":
    print("\n🧪 Playwright价格爬虫测试工具")
    print("\n选择测试：")
    print("1. 测试Roborock（Saros Z70）")
    print("2. 测试Eufy（Omni S2）")

    choice = input("\n请输入选择（1或2）：").strip()

    if choice == '1':
        asyncio.run(test_roborock())
    elif choice == '2':
        asyncio.run(test_eufy())
    else:
        print("无效选择")
