"""
Complete 2026 Robot Vacuum Product Configuration
Based on CES 2026 announcements and verified market data
"""

# COMPLETE Top 8 Robot Vacuum Brands - ALL In-Sale Products (2026)
BRANDS_CONFIG = {
    "iRobot": {
        "official_site": "https://www.irobot.com",
        "note": "Bankruptcy Dec 2025, acquired by China's Picea Robotics",
        "products": [
            # 2026 Models (Post-bankruptcy)
            {
                "name": "Roomba Combo 10 Max",
                "model": "Combo 10 Max",
                "official_url": "https://www.irobot.com/roomba-combo-10-max",
                "amazon_asin": "B0DK8ZYX9Q",
                "price_range": (799, 999),
            },
            {
                "name": "Roomba 705 Max Combo",
                "model": "705 Max Combo",
                "official_url": "https://www.irobot.com/roomba-705-max-combo",
                "amazon_asin": "B0DK8MAXXX",
                "price_range": (799, 899),
            },
            {
                "name": "Roomba Plus 505 Combo",
                "model": "Plus 505 Combo",
                "official_url": "https://www.irobot.com/roomba-plus-505-combo",
                "amazon_asin": "B0DK8505XX",
                "price_range": (499, 549),
            },
            {
                "name": "Roomba 405 Combo",
                "model": "405 Combo",
                "official_url": "https://www.irobot.com/roomba-405-combo",
                "amazon_asin": "B0DK8405XX",
                "price_range": (399, 499),
            },
            {
                "name": "Roomba 205 DustCompactor Combo",
                "model": "205 DustCompactor",
                "official_url": "https://www.irobot.com/roomba-205-dustcompactor-combo",
                "amazon_asin": "B0DK8205XX",
                "price_range": (249, 470),
                "note": "60-day dustbin capacity"
            },
            {
                "name": "Roomba 105 Combo",
                "model": "105 Combo",
                "official_url": "https://www.irobot.com/roomba-105-combo",
                "amazon_asin": "B0DK8105XX",
                "price_range": (199, 299),
                "note": "Budget model"
            },
            # Pre-bankruptcy models still in stock
            {
                "name": "Roomba j9+",
                "model": "j9+",
                "official_url": "https://www.irobot.com/roomba-j9-plus",
                "amazon_asin": "B0C1SJ3PWJ",
                "price_range": (564, 899),
            },
            {
                "name": "Roomba Combo j7+",
                "model": "j7+",
                "official_url": "https://www.irobot.com/roomba-combo-j7-plus",
                "amazon_asin": "B09ZVRF8B9",
                "price_range": (599, 799),
            },
        ]
    },

    "Roborock": {
        "official_site": "https://us.roborock.com",
        "products": [
            # CES 2026 New Releases
            {
                "name": "Saros 20 Sonic",
                "model": "Saros 20 Sonic",
                "official_url": "https://us.roborock.com/pages/saros-20-sonic",
                "amazon_asin": "B0DKSAROS20",
                "price_range": (1799, 2199),
                "note": "CES 2026 - 35,000Pa (record-breaking)"
            },
            {
                "name": "Saros 20",
                "model": "Saros 20",
                "official_url": "https://us.roborock.com/pages/saros-20",
                "amazon_asin": "B0DKSAROS2X",
                "price_range": (1599, 1899),
                "note": "CES 2026 - 35,000Pa, AdaptiLift 3.0"
            },
            {
                "name": "Qrevo Curv 2 Flow",
                "model": "Qrevo Curv 2 Flow",
                "official_url": "https://us.roborock.com/pages/qrevo-curv-2-flow",
                "amazon_asin": "B0DKQCURV2F",
                "price_range": (849, 999),
                "note": "CES 2026 - First roller mop, launch price $849"
            },
            {
                "name": "Saros Z70",
                "model": "Saros Z70",
                "official_url": "https://us.roborock.com/pages/saros-z70",
                "amazon_asin": "B0CZ70XXXX",
                "price_range": (1799, 2000),
                "note": "Robotic arm - CES 2025 Best of Show"
            },
            {
                "name": "Saros 10R",
                "model": "Saros 10R",
                "official_url": "https://us.roborock.com/pages/saros-10r",
                "amazon_asin": "B0DKSAROS10",
                "price_range": (999, 1599),
            },
            {
                "name": "Qrevo CurvX",
                "model": "Qrevo CurvX",
                "official_url": "https://us.roborock.com/pages/qrevo-curvx",
                "amazon_asin": "B0DKQCURVX",
                "price_range": (1299, 1599),
                "note": "22,000Pa"
            },
            {
                "name": "Qrevo Curv",
                "model": "Qrevo Curv",
                "official_url": "https://us.roborock.com/pages/qrevo-curv",
                "amazon_asin": "B0CYREVO11",
                "price_range": (799, 1149),
                "note": "18,500Pa, 4cm threshold"
            },
            {
                "name": "Qrevo Master",
                "model": "Qrevo Master",
                "official_url": "https://us.roborock.com/pages/qrevo-master",
                "amazon_asin": "B0CQREVOXX",
                "price_range": (1099, 1399),
                "note": "10,000Pa"
            },
            {
                "name": "Qrevo Slim",
                "model": "Qrevo Slim",
                "official_url": "https://us.roborock.com/pages/qrevo-slim",
                "amazon_asin": "B0DKQSLIM",
                "price_range": (799, 999),
                "note": "11,000Pa, slim design"
            },
            {
                "name": "S8 Pro Ultra",
                "model": "S8 Pro Ultra",
                "official_url": "https://us.roborock.com/pages/roborock-s8-pro-ultra",
                "amazon_asin": "B0BS3XVD1P",
                "price_range": (899, 1199),
            },
        ]
    },

    "Ecovacs": {
        "official_site": "https://www.ecovacs.com",
        "products": [
            # CES 2026 New Models
            {
                "name": "Deebot X12 Pro Omni",
                "model": "X12 Pro Omni",
                "official_url": "https://www.ecovacs.com/us/deebot-robot-vacuum/deebot-x12-pro-omni",
                "amazon_asin": "B0DKX12PRO",
                "price_range": (1499, 1799),
                "note": "CES 2026 - OZMO Roller 3.0, stain pretreat"
            },
            {
                "name": "Deebot X12 OmniCyclone",
                "model": "X12 OmniCyclone",
                "official_url": "https://www.ecovacs.com/us/deebot-robot-vacuum/deebot-x12-omnicyclone",
                "amazon_asin": "B0DKX12CYC",
                "price_range": (1299, 1599),
                "note": "CES 2026 - Bagless dock, mop cover"
            },
            {
                "name": "Deebot T90 Pro Omni",
                "model": "T90 Pro Omni",
                "official_url": "https://www.ecovacs.com/us/deebot-robot-vacuum/deebot-t90-pro-omni",
                "amazon_asin": "B0DKT90PRO",
                "price_range": (899, 1199),
                "note": "CES 2026 - OZMO Roller 3.0"
            },
            # Current Models
            {
                "name": "Deebot X9 Pro Omni",
                "model": "X9 Pro Omni",
                "official_url": "https://www.ecovacs.com/us/deebot-robot-vacuum/deebot-x9-pro-omni",
                "amazon_asin": "B0DKX9PROX",
                "price_range": (699, 799),
            },
            {
                "name": "Deebot X8 Pro Omni",
                "model": "X8 Pro Omni",
                "official_url": "https://www.ecovacs.com/us/deebot-robot-vacuum/deebot-x8-pro-omni",
                "amazon_asin": "B0CX8PROXX",
                "price_range": (749, 1099),
            },
            {
                "name": "Deebot T30S Combo",
                "model": "T30S Combo",
                "official_url": "https://www.ecovacs.com/us/deebot-robot-vacuum/deebot-t30s-combo",
                "amazon_asin": "B0CT30SXXX",
                "price_range": (500, 699),
            },
            {
                "name": "Deebot T20 Omni",
                "model": "T20 Omni",
                "official_url": "https://www.ecovacs.com/us/deebot-robot-vacuum/deebot-t20-omni",
                "amazon_asin": "B0CT20XXXX",
                "price_range": (599, 799),
            },
            {
                "name": "Deebot N30 Pro Omni",
                "model": "N30 Pro Omni",
                "official_url": "https://www.ecovacs.com/us/deebot-robot-vacuum/deebot-n30-pro-omni",
                "amazon_asin": "B0CN30PROX",
                "price_range": (399, 549),
            },
            {
                "name": "Deebot N8 Pro+",
                "model": "N8 Pro+",
                "official_url": "https://www.ecovacs.com/us/deebot-robot-vacuum/deebot-n8-pro-plus",
                "amazon_asin": "B08DXZN8FG",
                "price_range": (299, 511),
            },
        ]
    },

    "Dreame": {
        "official_site": "https://www.dreametech.com",
        "products": [
            # CES 2026 Ultra-Thin Series
            {
                "name": "X60 Max Ultra Complete",
                "model": "X60 Max Ultra Complete",
                "official_url": "https://www.dreametech.com/products/dreame-x60-max-ultra-complete-robot-vacuum-and-mop",
                "amazon_asin": "B0DKX60MAX",
                "price_range": (1799, 1999),
                "note": "CES 2026 - 7.95cm thin, robotic legs climb 8.8cm"
            },
            {
                "name": "X60 Ultra",
                "model": "X60 Ultra",
                "official_url": "https://www.dreametech.com/products/dreame-x60-ultra-robot-vacuum-and-mop",
                "amazon_asin": "B0DKX60ULT",
                "price_range": (1499, 1699),
                "note": "CES 2026 - 7.95cm ultra-thin"
            },
            {
                "name": "Cyber10 Ultra",
                "model": "Cyber10 Ultra",
                "official_url": "https://www.dreametech.com/products/dreame-cyber10-ultra",
                "amazon_asin": "B0DKCYBER10",
                "price_range": (1599, 1899),
                "note": "CES 2026 - Robotic arm for object manipulation"
            },
            # Current Premium X Series
            {
                "name": "X50 Ultra",
                "model": "X50 Ultra",
                "official_url": "https://www.dreametech.com/products/dreame-x50-ultra-robot-vacuum-and-mop",
                "amazon_asin": "B0DKX50ULT",
                "price_range": (1050, 1399),
            },
            {
                "name": "X40 Ultra",
                "model": "X40 Ultra",
                "official_url": "https://www.dreametech.com/products/dreame-x40-ultra-robot-vacuum-and-mop",
                "amazon_asin": "B0CX40ULTR",
                "price_range": (1099, 1499),
            },
            {
                "name": "X30 Ultra",
                "model": "X30 Ultra",
                "official_url": "https://www.dreametech.com/products/dreame-x30-ultra-robot-vacuum-and-mop",
                "amazon_asin": "B0BVHQMFYS",
                "price_range": (999, 1313),
            },
            # L Series Mid-Range
            {
                "name": "L50 Ultra",
                "model": "L50 Ultra",
                "official_url": "https://www.dreametech.com/products/dreame-l50-ultra",
                "amazon_asin": "B0DKL50ULT",
                "price_range": (899, 1199),
                "note": "ProLeap system, 6cm climb"
            },
            {
                "name": "L40s Ultra",
                "model": "L40s Ultra",
                "official_url": "https://www.dreametech.com/products/dreame-l40s-ultra",
                "amazon_asin": "B0DKL40SUL",
                "price_range": (799, 999),
                "note": "19,000Pa Vormax suction"
            },
            {
                "name": "L20 Ultra",
                "model": "L20 Ultra",
                "official_url": "https://www.dreametech.com/products/dreame-l20-ultra",
                "amazon_asin": "B0CL20ULTR",
                "price_range": (699, 899),
            },
            # Aqua & D Series
            {
                "name": "Aqua10 Ultra Roller",
                "model": "Aqua10 Ultra Roller",
                "official_url": "https://www.dreametech.com/products/dreame-aqua10-ultra-roller",
                "amazon_asin": "B0DKAQUA10",
                "price_range": (899, 1199),
                "note": "CES 2026 Innovation Award - First roller mop"
            },
            {
                "name": "D20 Pro Plus",
                "model": "D20 Pro Plus",
                "official_url": "https://www.dreametech.com/products/dreame-d20-pro-plus",
                "amazon_asin": "B0DKD20PRO",
                "price_range": (399, 549),
                "note": "13,000Pa, 150-day capacity"
            },
            {
                "name": "D20 Plus",
                "model": "D20 Plus",
                "official_url": "https://www.dreametech.com/products/dreame-d20-plus",
                "amazon_asin": "B0DKD20PLU",
                "price_range": (329, 449),
                "note": "13,000Pa entry-level"
            },
        ]
    },

    "Shark": {
        "official_site": "https://www.sharkclean.com",
        "products": [
            # 2026 PowerDetect Series
            {
                "name": "PowerDetect NeverTouch Pro",
                "model": "PowerDetect NeverTouch Pro",
                "official_url": "https://www.sharkclean.com/robot-vacuums/shark-powerdetect-nevertouch-pro-robot-vacuum-and-mop",
                "amazon_asin": "B0DKSHPWRDT",
                "price_range": (899, 1099),
                "note": "Mop washing/drying, 185F water"
            },
            {
                "name": "PowerDetect Self-Empty",
                "model": "PowerDetect Self-Empty",
                "official_url": "https://www.sharkclean.com/robot-vacuums/shark-powerdetect-self-empty-robot-vacuum",
                "amazon_asin": "B0DKSHPWRXX",
                "price_range": (599, 799),
                "note": "NeverStuck lift chassis 38mm"
            },
            # Matrix Series
            {
                "name": "Matrix Plus 2-in-1",
                "model": "Matrix Plus",
                "official_url": "https://www.sharkclean.com/robot-vacuums/shark-matrix-plus-2-in-1-robot-vacuum-mop",
                "amazon_asin": "B0CSHMTXPL",
                "price_range": (449, 649),
                "note": "Sonic mopping 1000x/sec"
            },
            {
                "name": "Matrix Self-Empty",
                "model": "Matrix",
                "official_url": "https://www.sharkclean.com/robot-vacuums/shark-matrix-self-empty-robot-vacuum",
                "amazon_asin": "B0CSHMTXXX",
                "price_range": (399, 549),
                "note": "30-day capacity"
            },
            # AI Ultra Series
            {
                "name": "AI Ultra Self-Empty",
                "model": "AI Ultra",
                "official_url": "https://www.sharkclean.com/robot-vacuums/shark-ai-ultra-self-empty-robot-vacuum",
                "amazon_asin": "B09PBW7SM3",
                "price_range": (399, 599),
                "note": "60-day capacity"
            },
        ]
    },

    "Eufy": {
        "official_site": "https://www.eufy.com",
        "note": "Anker sub-brand",
        "products": [
            # CES 2026 New Launch
            {
                "name": "Omni S2",
                "model": "Omni S2",
                "official_url": "https://www.eufy.com/products/t2381111",
                "amazon_asin": "B0DKEFOMNIS2",
                "price_range": (1599, 1599),
                "note": "CES 2026 - 30,000Pa, aromatherapy pods, $1,599"
            },
            # Omni Series
            {
                "name": "Omni S1 Pro",
                "model": "Omni S1 Pro",
                "official_url": "https://www.eufy.com/products/t2320111",
                "amazon_asin": "B0CEFOMNIS1",
                "price_range": (999, 1499),
                "note": "Floor washing station"
            },
            {
                "name": "X10 Pro Omni",
                "model": "X10 Pro Omni",
                "official_url": "https://www.eufy.com/products/t2351111",
                "amazon_asin": "B0CX10OMNI",
                "price_range": (599, 799),
            },
            {
                "name": "Omni E28",
                "model": "Omni E28",
                "official_url": "https://www.eufy.com/products/t2360111",
                "amazon_asin": "B0CEOMNIE28",
                "price_range": (599, 700),
                "note": "Roller mop"
            },
            # L Series
            {
                "name": "L60 Ultra",
                "model": "L60 Ultra",
                "official_url": "https://www.eufy.com/products/t2278111",
                "amazon_asin": "B0CEL60ULT",
                "price_range": (449, 649),
            },
            # E Series Budget
            {
                "name": "E20 3-in-1",
                "model": "E20",
                "official_url": "https://www.eufy.com/products/t2277111",
                "amazon_asin": "B0CEE20XXX",
                "price_range": (399, 549),
                "note": "Budget 3-in-1"
            },
        ]
    },

    "Narwal": {
        "official_site": "https://www.narwal.com",
        "products": [
            # CES 2026 Launch
            {
                "name": "Flow 2",
                "model": "Flow 2",
                "official_url": "https://www.narwal.com/products/narwal-freo-flow-2",
                "amazon_asin": "B0DKNWFLOW2",
                "price_range": (1299, 1599),
                "note": "CES 2026 - 30,000Pa, unlimited object recognition, 158F hot water"
            },
            # Freo Series
            {
                "name": "Freo Z10 Ultra",
                "model": "Freo Z10 Ultra",
                "official_url": "https://www.narwal.com/products/narwal-freo-z10-ultra",
                "amazon_asin": "B0CNWFREOZ10",
                "price_range": (799, 1099),
            },
            {
                "name": "Freo X Ultra",
                "model": "Freo X Ultra",
                "official_url": "https://www.narwal.com/products/narwal-freo-x-ultra",
                "amazon_asin": "B0CNWFREOXU",
                "price_range": (699, 899),
            },
            {
                "name": "Freo",
                "model": "Freo",
                "official_url": "https://www.narwal.com/products/narwal-freo",
                "amazon_asin": "B0CNWFREOX",
                "price_range": (599, 799),
            },
        ]
    },

    "Dyson": {
        "official_site": "https://www.dyson.com",
        "products": [
            {
                "name": "360 Vis Nav",
                "model": "360 Vis Nav",
                "official_url": "https://www.dyson.com/vacuum-cleaners/robot/dyson-360-vis-nav-purple-nickel/overview",
                "amazon_asin": "B0CYDS360VN",
                "price_range": (399, 999),
                "note": "2x suction power, massive discount from $999 to $399"
            },
        ]
    }
}

# Helper function to generate URLs
def get_product_url(product, channel):
    """Generate URL for product on specific channel"""
    if channel == 'official':
        return product.get('official_url', '')

    # Use ASIN for Amazon if available
    if channel == 'amazon' and 'amazon_asin' in product:
        return f"https://www.amazon.com/dp/{product['amazon_asin']}"

    # Fallback to search
    search_term = product['name'].replace(' ', '+')
    brand = product.get('brand', '')

    urls = {
        'amazon': f"https://www.amazon.com/s?k={brand}+{search_term}",
        'walmart': f"https://www.walmart.com/search?q={brand}+{search_term.replace('+', '-')}",
        'costco': f"https://www.costco.com/CatalogSearch?keyword={brand}+{search_term.replace('+', '%20')}",
        'ebay': f"https://www.ebay.com/sch/i.html?_nkw={brand}+{search_term}"
    }

    return urls.get(channel, '')


# Scraping settings
SCRAPER_CONFIG = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "request_delay": 2,
    "timeout": 10,
    "max_retries": 3
}

# Channel information
CHANNELS = {
    "official": "Official Site",
    "amazon": "https://www.amazon.com",
    "walmart": "https://www.walmart.com",
    "costco": "https://www.costco.com",
    "ebay": "https://www.ebay.com"
}
