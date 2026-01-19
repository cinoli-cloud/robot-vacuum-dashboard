"""
Price scraper for robot vacuum products across multiple channels
"""

import requests
from bs4 import BeautifulSoup
import time
import json
import re
from datetime import datetime
from config import BRANDS_CONFIG, SCRAPER_CONFIG, CHANNELS
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class PriceScraper:
    """Scraper for collecting product prices from various channels"""

    def __init__(self):
        self.headers = {
            'User-Agent': SCRAPER_CONFIG['user_agent'],
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = requests.Session()
        self.session.headers.update(self.headers)

    def extract_price_from_text(self, text):
        """Extract price from text using regex"""
        if not text:
            return None

        # Look for patterns like $599.99, $599, etc.
        price_patterns = [
            r'\$\s*(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)',
            r'(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)\s*USD',
            r'USD\s*(\d{1,4}(?:,\d{3})*(?:\.\d{2})?)'
        ]

        for pattern in price_patterns:
            match = re.search(pattern, text)
            if match:
                price_str = match.group(1).replace(',', '')
                try:
                    return float(price_str)
                except ValueError:
                    continue

        return None

    def scrape_amazon(self, search_query):
        """Scrape price from Amazon (Demo implementation using search)"""
        try:
            logger.info(f"Searching Amazon for: {search_query}")

            # Note: In production, you would need to handle Amazon's anti-bot measures
            # This is a simplified demonstration
            url = f"{CHANNELS['amazon']}/s?k={search_query.replace(' ', '+')}"

            response = self.session.get(url, timeout=SCRAPER_CONFIG['timeout'])

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Look for price in search results
                price_elements = soup.find_all('span', class_='a-price-whole')

                if price_elements:
                    price_text = price_elements[0].text
                    price = self.extract_price_from_text(price_text)
                    if price:
                        logger.info(f"Found Amazon price: ${price}")
                        return price

            logger.warning(f"Could not find price on Amazon for {search_query}")
            return None

        except Exception as e:
            logger.error(f"Error scraping Amazon: {e}")
            return None

    def scrape_walmart(self, search_query):
        """Scrape price from Walmart (Demo implementation)"""
        try:
            logger.info(f"Searching Walmart for: {search_query}")

            url = f"{CHANNELS['walmart']}/search?q={search_query.replace(' ', '+')}"

            response = self.session.get(url, timeout=SCRAPER_CONFIG['timeout'])

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                # Look for price elements
                price_elements = soup.find_all('div', class_=re.compile(r'.*price.*', re.I))

                for element in price_elements[:5]:  # Check first 5 matches
                    price = self.extract_price_from_text(element.text)
                    if price and 100 < price < 3000:  # Reasonable price range
                        logger.info(f"Found Walmart price: ${price}")
                        return price

            logger.warning(f"Could not find price on Walmart for {search_query}")
            return None

        except Exception as e:
            logger.error(f"Error scraping Walmart: {e}")
            return None

    def scrape_costco(self, search_query):
        """Scrape price from Costco (Demo implementation)"""
        try:
            logger.info(f"Searching Costco for: {search_query}")

            # Costco requires membership for most products
            # This is a simplified demo
            url = f"{CHANNELS['costco']}/s?text={search_query.replace(' ', '%20')}"

            response = self.session.get(url, timeout=SCRAPER_CONFIG['timeout'])

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                price_text = soup.find('span', class_=re.compile(r'.*price.*', re.I))

                if price_text:
                    price = self.extract_price_from_text(price_text.text)
                    if price:
                        logger.info(f"Found Costco price: ${price}")
                        return price

            logger.warning(f"Could not find price on Costco for {search_query}")
            return None

        except Exception as e:
            logger.error(f"Error scraping Costco: {e}")
            return None

    def scrape_ebay(self, search_query):
        """Scrape price from eBay (Demo implementation)"""
        try:
            logger.info(f"Searching eBay for: {search_query}")

            url = f"{CHANNELS['ebay']}/sch/i.html?_nkw={search_query.replace(' ', '+')}"

            response = self.session.get(url, timeout=SCRAPER_CONFIG['timeout'])

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                price_element = soup.find('span', class_='s-item__price')

                if price_element:
                    price = self.extract_price_from_text(price_element.text)
                    if price:
                        logger.info(f"Found eBay price: ${price}")
                        return price

            logger.warning(f"Could not find price on eBay for {search_query}")
            return None

        except Exception as e:
            logger.error(f"Error scraping eBay: {e}")
            return None

    def scrape_official_site(self, brand, product_name):
        """Scrape price from official brand website (Demo implementation)"""
        try:
            logger.info(f"Searching official site for {brand} - {product_name}")

            # This would need custom logic for each brand's website structure
            # For now, return None (would be implemented per brand)

            logger.warning(f"Official site scraping not implemented for {brand}")
            return None

        except Exception as e:
            logger.error(f"Error scraping official site: {e}")
            return None

    def scrape_product(self, brand, product):
        """Scrape a single product across all channels"""
        logger.info(f"Scraping {brand} - {product['name']}")

        result = {
            "brand": brand,
            "name": product['name'],
            "model": product['model'],
            "channels": {
                "official": {"price": 0, "change": 0, "available": False},
                "amazon": {"price": 0, "change": 0, "available": False},
                "walmart": {"price": 0, "change": 0, "available": False},
                "costco": {"price": 0, "change": 0, "available": False},
                "ebay": {"price": 0, "change": 0, "available": False}
            }
        }

        # Scrape each channel
        channels_to_scrape = [
            ("amazon", lambda: self.scrape_amazon(product['amazon_search'])),
            ("walmart", lambda: self.scrape_walmart(product['walmart_search'])),
            ("costco", lambda: self.scrape_costco(product['amazon_search'])),
            ("ebay", lambda: self.scrape_ebay(product['amazon_search'])),
            ("official", lambda: self.scrape_official_site(brand, product['name']))
        ]

        for channel_name, scrape_func in channels_to_scrape:
            try:
                price = scrape_func()
                if price:
                    result["channels"][channel_name] = {
                        "price": price,
                        "change": 0,  # Will be calculated against historical data
                        "available": True
                    }

                # Respect rate limiting
                time.sleep(SCRAPER_CONFIG['request_delay'])

            except Exception as e:
                logger.error(f"Error scraping {channel_name} for {product['name']}: {e}")

        return result

    def scrape_all_products(self):
        """Scrape all products from all brands"""
        logger.info("Starting comprehensive scraping of all products")

        all_products = []

        for brand, brand_info in BRANDS_CONFIG.items():
            logger.info(f"Processing brand: {brand}")

            for product in brand_info['products']:
                try:
                    product_data = self.scrape_product(brand, product)
                    all_products.append(product_data)

                    # Add extra delay between products
                    time.sleep(SCRAPER_CONFIG['request_delay'])

                except Exception as e:
                    logger.error(f"Error processing {brand} - {product['name']}: {e}")
                    continue

        logger.info(f"Scraping complete. Collected data for {len(all_products)} products")
        return all_products


def main():
    """Main function to run the scraper"""
    scraper = PriceScraper()

    logger.info("=" * 50)
    logger.info("Robot Vacuum Price Scraper Started")
    logger.info("=" * 50)

    # Scrape all products
    products_data = scraper.scrape_all_products()

    # Save results
    output_file = '../data/scraped_prices.json'
    with open(output_file, 'w') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'products': products_data,
            'total_products': len(products_data)
        }, f, indent=2)

    logger.info(f"Results saved to {output_file}")
    logger.info("Scraping session completed")


if __name__ == "__main__":
    main()
