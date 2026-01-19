"""
Main update script for the robot vacuum dashboard
This script orchestrates all data collection and processing
"""

import json
import logging
from datetime import datetime
import os
import sys

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('../data/update.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


def update_dashboard():
    """Main function to update all dashboard data"""
    logger.info("=" * 60)
    logger.info("DASHBOARD UPDATE STARTED")
    logger.info(f"Timestamp: {datetime.now().isoformat()}")
    logger.info("=" * 60)

    try:
        # Import the demo data generator
        # In production, you would use the real scrapers
        logger.info("Step 1/5: Generating price data...")
        from generate_demo_data import generate_current_prices, generate_price_history
        from generate_demo_data import generate_price_forecast, generate_brand_averages
        from generate_demo_data import generate_news

        # Generate current prices
        products = generate_current_prices()
        logger.info(f"✓ Generated data for {len(products)} products")

        # Generate price history
        logger.info("Step 2/5: Generating price history...")
        price_history = generate_price_history(products, days=30)
        logger.info(f"✓ Generated 30-day history for {len(price_history)} brands")

        # Generate price forecast
        logger.info("Step 3/5: Generating price forecast...")
        price_forecast = generate_price_forecast(price_history, days=7)
        logger.info(f"✓ Generated 7-day forecast for {len(price_forecast)} brands")

        # Calculate brand averages
        logger.info("Step 4/5: Calculating brand averages...")
        brand_averages = generate_brand_averages(products)
        logger.info(f"✓ Calculated averages for {len(brand_averages)} brands")

        # Generate news
        logger.info("Step 5/5: Generating news items...")
        news = generate_news()
        logger.info(f"✓ Generated {len(news)} news items")

        # Compile complete dataset
        logger.info("Compiling final dataset...")
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

        logger.info(f"✓ Data saved to {output_file}")
        logger.info("=" * 60)
        logger.info("DASHBOARD UPDATE COMPLETED SUCCESSFULLY")
        logger.info("=" * 60)

        return True

    except Exception as e:
        logger.error("=" * 60)
        logger.error(f"DASHBOARD UPDATE FAILED: {str(e)}")
        logger.error("=" * 60)
        raise


def main():
    """Entry point for manual updates"""
    try:
        success = update_dashboard()
        if success:
            print("\n✓ Dashboard updated successfully!")
            print(f"✓ Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            sys.exit(0)
        else:
            print("\n✗ Dashboard update failed!")
            sys.exit(1)

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
