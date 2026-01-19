"""
Generate realistic demo data for the robot vacuum price dashboard
This includes current prices, historical data, forecasts, and news
"""

import json
import random
from datetime import datetime, timedelta
from config import BRANDS_CONFIG


def generate_realistic_price(base_price, variance=0.1):
    """Generate a realistic price with some variance"""
    variation = base_price * variance * (random.random() - 0.5) * 2
    return round(base_price + variation, 2)


def generate_price_change():
    """Generate a realistic price change percentage"""
    # 70% chance of no change, 20% increase, 10% decrease
    rand = random.random()
    if rand < 0.7:
        return 0
    elif rand < 0.9:
        return round(random.uniform(0.5, 8.0), 1)
    else:
        return round(random.uniform(-8.0, -0.5), 1)


def generate_current_prices():
    """Generate current prices for all products across all channels"""
    products = []

    # Base prices for different tiers
    price_tiers = {
        "premium": (900, 1500),
        "mid": (500, 900),
        "budget": (200, 500)
    }

    tier_mapping = {
        "iRobot": {"Roomba Combo j9+": "premium", "Roomba j7+": "mid", "Roomba i7+": "mid"},
        "Roborock": {"Roborock S8 Pro Ultra": "premium", "Roborock Q Revo": "mid", "Roborock S7 MaxV": "mid"},
        "Ecovacs": {"Deebot X2 Omni": "premium", "Deebot T30 Pro": "mid", "Deebot N8 Pro+": "budget"},
        "Dreame": {"Dreame X40 Ultra": "premium", "Dreame L10s Ultra": "mid", "Dreame L20 Ultra": "mid"},
        "Shark": {"Shark AI Ultra": "mid", "Shark Matrix Plus": "mid", "Shark IQ Robot": "budget"},
        "Eufy": {"Eufy X10 Pro Omni": "mid", "Eufy L60": "budget", "Eufy RoboVac X8": "budget"},
        "Narwal": {"Narwal Freo Z10": "premium", "Narwal Freo X Ultra": "premium", "Narwal T10": "mid"},
        "Dyson": {"Dyson 360 Vis Nav": "premium", "Dyson 360 Heurist": "premium"}
    }

    for brand, brand_info in BRANDS_CONFIG.items():
        for product in brand_info['products']:
            product_name = product['name']
            tier = tier_mapping.get(brand, {}).get(product_name, "mid")
            base_price = random.randint(*price_tiers[tier])

            # Generate prices for each channel
            official_price = base_price
            amazon_price = generate_realistic_price(base_price, 0.08)
            walmart_price = generate_realistic_price(base_price, 0.1)
            costco_available = random.random() > 0.6  # 40% availability at Costco
            costco_price = generate_realistic_price(base_price * 0.95, 0.05) if costco_available else 0
            ebay_price = generate_realistic_price(base_price * 0.92, 0.12)

            product_data = {
                "brand": brand,
                "name": product_name,
                "model": product['model'],
                "channels": {
                    "official": {
                        "price": official_price,
                        "change": generate_price_change(),
                        "available": True,
                        "url": brand_info['official_site']
                    },
                    "amazon": {
                        "price": amazon_price,
                        "change": generate_price_change(),
                        "available": True,
                        "url": f"https://amazon.com/s?k={product['amazon_search'].replace(' ', '+')}"
                    },
                    "walmart": {
                        "price": walmart_price,
                        "change": generate_price_change(),
                        "available": True,
                        "url": f"https://walmart.com/search?q={product['walmart_search'].replace(' ', '+')}"
                    },
                    "costco": {
                        "price": costco_price,
                        "change": generate_price_change() if costco_available else 0,
                        "available": costco_available,
                        "url": "https://costco.com"
                    },
                    "ebay": {
                        "price": ebay_price,
                        "change": generate_price_change(),
                        "available": True,
                        "url": f"https://ebay.com/sch/i.html?_nkw={product['amazon_search'].replace(' ', '+')}"
                    }
                }
            }

            products.append(product_data)

    return products


def generate_price_history(products, days=30):
    """Generate historical price data for the past N days"""
    history = {}
    dates = [(datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(days, -1, -1)]

    for brand in BRANDS_CONFIG.keys():
        brand_products = [p for p in products if p['brand'] == brand]
        if not brand_products:
            continue

        # Calculate average price for this brand
        avg_prices = []
        base_avg = sum([
            sum([ch['price'] for ch in p['channels'].values() if ch['available'] and ch['price'] > 0])
            / max(sum([1 for ch in p['channels'].values() if ch['available'] and ch['price'] > 0]), 1)
            for p in brand_products
        ]) / len(brand_products)

        # Generate historical trend
        for i, date in enumerate(dates):
            # Add some realistic fluctuation
            trend = base_avg + (random.random() - 0.5) * base_avg * 0.15
            seasonal = 10 * (1 + 0.5 * (i % 7) / 7)  # Weekly pattern
            price = round(trend + seasonal, 2)
            avg_prices.append(price)

        history[brand] = {
            "dates": dates,
            "prices": avg_prices
        }

    return history


def generate_price_forecast(price_history, days=7):
    """Generate price forecast for the next N days"""
    forecast = {}
    current_date = datetime.now()

    for brand, history in price_history.items():
        # Get last 7 days trend
        recent_prices = history['prices'][-7:]
        avg_recent = sum(recent_prices) / len(recent_prices)

        # Calculate trend
        trend = (recent_prices[-1] - recent_prices[0]) / 7

        # Generate forecast
        forecast_dates = [(current_date + timedelta(days=i)).strftime('%Y-%m-%d') for i in range(1, days + 1)]
        forecast_prices = []

        for i in range(days):
            # Projected price with some uncertainty
            projected = avg_recent + (trend * i) + random.uniform(-5, 5)
            forecast_prices.append(round(max(projected, 0), 2))

        forecast[brand] = {
            "dates": forecast_dates,
            "prices": forecast_prices
        }

    return forecast


def generate_brand_averages(products):
    """Calculate average price by brand"""
    averages = {}

    for brand in BRANDS_CONFIG.keys():
        brand_products = [p for p in products if p['brand'] == brand]
        if not brand_products:
            continue

        total = 0
        count = 0

        for product in brand_products:
            for channel in product['channels'].values():
                if channel['available'] and channel['price'] > 0:
                    total += channel['price']
                    count += 1

        if count > 0:
            averages[brand] = round(total / count, 2)
        else:
            averages[brand] = 0

    return averages


def generate_news():
    """Generate realistic news items for each brand"""
    news_templates = [
        {
            "title": "{brand} Announces New {model} with Advanced AI Navigation",
            "summary": "The latest robot vacuum from {brand} features cutting-edge AI technology for improved obstacle detection and navigation efficiency.",
            "source": "TechCrunch"
        },
        {
            "title": "{brand} Launches Holiday Sale: Up to 30% Off Select Models",
            "summary": "Consumers can save big on popular {brand} robot vacuum models during their winter promotion event.",
            "source": "RetailDive"
        },
        {
            "title": "Review: {brand} {model} Sets New Standard for Smart Home Cleaning",
            "summary": "Industry experts praise the {model} for its exceptional cleaning performance and innovative features.",
            "source": "CNET"
        },
        {
            "title": "{brand} Expands Distribution to Major Retailers",
            "summary": "{brand} announces partnership with leading retailers to make their products more accessible to consumers.",
            "source": "BusinessWire"
        },
        {
            "title": "Consumer Reports Ranks {brand} Among Top Robot Vacuum Brands",
            "summary": "Latest testing shows {brand} products excel in suction power, battery life, and navigation accuracy.",
            "source": "Consumer Reports"
        }
    ]

    all_news = []
    brands = list(BRANDS_CONFIG.keys())

    for brand in brands:
        # Generate 5 news items per brand
        for i in range(5):
            template = random.choice(news_templates)
            product = random.choice(BRANDS_CONFIG[brand]['products'])

            news_item = {
                "brand": brand,
                "title": template['title'].format(brand=brand, model=product['model']),
                "summary": template['summary'].format(brand=brand, model=product['model']),
                "source": template['source'],
                "date": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
                "url": f"https://example.com/news/{brand.lower()}-{i}"
            }

            all_news.append(news_item)

    # Sort by date (most recent first)
    all_news.sort(key=lambda x: x['date'], reverse=True)

    return all_news[:40]  # Return top 40 news items


def main():
    """Generate complete demo dataset"""
    print("Generating demo data for Robot Vacuum Price Dashboard...")

    # Generate current prices
    print("1/6 Generating current prices...")
    products = generate_current_prices()

    # Generate price history
    print("2/6 Generating price history...")
    price_history = generate_price_history(products, days=30)

    # Generate price forecast
    print("3/6 Generating price forecast...")
    price_forecast = generate_price_forecast(price_history, days=7)

    # Calculate brand averages
    print("4/6 Calculating brand averages...")
    brand_averages = generate_brand_averages(products)

    # Generate news
    print("5/6 Generating news items...")
    news = generate_news()

    # Compile complete dataset
    print("6/6 Compiling final dataset...")
    complete_data = {
        "lastUpdate": datetime.now().isoformat(),
        "products": products,
        "priceHistory": price_history,
        "priceForecast": price_forecast,
        "brandAverages": brand_averages,
        "news": news
    }

    # Save to file
    output_file = '../data/products.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(complete_data, f, indent=2, ensure_ascii=False)

    print(f"\n✓ Demo data generated successfully!")
    print(f"✓ Total products: {len(products)}")
    print(f"✓ Total news items: {len(news)}")
    print(f"✓ Data saved to: {output_file}")
    print(f"✓ Last updated: {complete_data['lastUpdate']}")


if __name__ == "__main__":
    main()
