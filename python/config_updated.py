"""
Updated configuration with real 2026 product lineup
Based on CES 2026 and current market data
"""

# Top 8 Robot Vacuum Brands with REAL 2026 Products
BRANDS_CONFIG = {
    "iRobot": {
        "official_site": "https://www.irobot.com",
        "note": "Acquired by Picea Robotics in 2025",
        "products": [
            {
                "name": "Roomba Combo 10 Max",
                "model": "Combo 10 Max",
                "official_url": "https://www.irobot.com/roomba-combo-10-max",
                "amazon_search": "iRobot Roomba Combo 10 Max",
                "walmart_search": "iRobot Roomba Combo 10 Max",
            },
            {
                "name": "Roomba Max 700 Combo",
                "model": "Max 700 Combo",
                "official_url": "https://www.irobot.com/roomba-max-700",
                "amazon_search": "iRobot Roomba Max 700 Combo",
                "walmart_search": "iRobot Roomba Max 700",
            },
            {
                "name": "Roomba Plus 500 Combo",
                "model": "Plus 500 Combo",
                "official_url": "https://www.irobot.com/roomba-plus-500",
                "amazon_search": "iRobot Roomba Plus 500 Combo",
                "walmart_search": "iRobot Roomba Plus 500",
            },
            {
                "name": "Roomba 405 Combo",
                "model": "405 Combo",
                "official_url": "https://www.irobot.com/roomba-405",
                "amazon_search": "iRobot Roomba 405 Combo",
                "walmart_search": "iRobot Roomba 405",
            },
        ]
    },
    "Roborock": {
        "official_site": "https://us.roborock.com",
        "products": [
            {
                "name": "Saros 20 Sonic",
                "model": "Saros 20 Sonic",
                "official_url": "https://us.roborock.com/pages/saros-20-sonic",
                "amazon_search": "Roborock Saros 20 Sonic",
                "walmart_search": "Roborock Saros 20 Sonic",
                "note": "CES 2026 - 35,000Pa suction"
            },
            {
                "name": "Qrevo Curv 2 Flow",
                "model": "Qrevo Curv 2 Flow",
                "official_url": "https://us.roborock.com/pages/qrevo-curv-2-flow",
                "amazon_search": "Roborock Qrevo Curv 2 Flow",
                "walmart_search": "Roborock Qrevo Curv 2 Flow",
                "note": "CES 2026 - $999"
            },
            {
                "name": "Qrevo CurvX",
                "model": "Qrevo CurvX",
                "official_url": "https://us.roborock.com/pages/qrevo-curvx",
                "amazon_search": "Roborock Qrevo CurvX",
                "walmart_search": "Roborock Qrevo CurvX",
                "note": "22,000Pa suction"
            },
            {
                "name": "Saros Z70",
                "model": "Saros Z70",
                "official_url": "https://us.roborock.com/pages/saros-z70",
                "amazon_search": "Roborock Saros Z70",
                "walmart_search": "Roborock Saros Z70",
                "note": "Robotic arm model"
            },
            {
                "name": "S8 Pro Ultra",
                "model": "S8 Pro Ultra",
                "official_url": "https://us.roborock.com/pages/roborock-s8-pro-ultra",
                "amazon_search": "Roborock S8 Pro Ultra",
                "walmart_search": "Roborock S8 Pro Ultra",
            },
            {
                "name": "Qrevo Master",
                "model": "Qrevo Master",
                "official_url": "https://us.roborock.com/pages/qrevo-master",
                "amazon_search": "Roborock Qrevo Master",
                "walmart_search": "Roborock Qrevo Master",
            },
        ]
    },
    "Ecovacs": {
        "official_site": "https://www.ecovacs.com",
        "products": [
            {
                "name": "Deebot X12 Pro Omni",
                "model": "X12 Pro Omni",
                "official_url": "https://www.ecovacs.com/us/deebot-x12-pro-omni",
                "amazon_search": "Ecovacs Deebot X12 Pro Omni",
                "walmart_search": "Ecovacs Deebot X12 Pro Omni",
                "note": "CES 2026 - Advanced mopping"
            },
            {
                "name": "Deebot X11 OmniCyclone",
                "model": "X11 OmniCyclone",
                "official_url": "https://www.ecovacs.com/us/deebot-x11-omnicyclone",
                "amazon_search": "Ecovacs Deebot X11 OmniCyclone",
                "walmart_search": "Ecovacs Deebot X11",
                "note": "CES 2026 Innovation Honoree"
            },
            {
                "name": "Deebot T90 Pro Omni",
                "model": "T90 Pro Omni",
                "official_url": "https://www.ecovacs.com/us/deebot-t90-pro-omni",
                "amazon_search": "Ecovacs Deebot T90 Pro Omni",
                "walmart_search": "Ecovacs Deebot T90",
                "note": "CES 2026"
            },
            {
                "name": "Deebot T30C",
                "model": "T30C",
                "official_url": "https://www.ecovacs.com/us/deebot-t30c",
                "amazon_search": "Ecovacs Deebot T30C",
                "walmart_search": "Ecovacs Deebot T30C",
                "note": "Budget premium features"
            },
            {
                "name": "Deebot T20 Omni",
                "model": "T20 Omni",
                "official_url": "https://www.ecovacs.com/us/deebot-t20-omni",
                "amazon_search": "Ecovacs Deebot T20 Omni",
                "walmart_search": "Ecovacs Deebot T20 Omni",
            },
        ]
    },
    "Dreame": {
        "official_site": "https://www.dreametech.com",
        "products": [
            {
                "name": "X60 Max Ultra Complete",
                "model": "X60 Max Ultra Complete",
                "official_url": "https://www.dreametech.com/products/x60-max-ultra-complete",
                "amazon_search": "Dreame X60 Max Ultra Complete",
                "walmart_search": "Dreame X60 Max Ultra Complete",
                "note": "CES 2026 - 7.95cm thin, robotic legs"
            },
            {
                "name": "X60 Ultra",
                "model": "X60 Ultra",
                "official_url": "https://www.dreametech.com/products/x60-ultra",
                "amazon_search": "Dreame X60 Ultra",
                "walmart_search": "Dreame X60 Ultra",
                "note": "CES 2026 - Super thin 7.95cm"
            },
            {
                "name": "Cyber10 Ultra",
                "model": "Cyber10 Ultra",
                "official_url": "https://www.dreametech.com/products/cyber10-ultra",
                "amazon_search": "Dreame Cyber10 Ultra",
                "walmart_search": "Dreame Cyber10 Ultra",
                "note": "Robotic arm"
            },
            {
                "name": "X40 Ultra",
                "model": "X40 Ultra",
                "official_url": "https://www.dreametech.com/products/x40-ultra",
                "amazon_search": "Dreame X40 Ultra",
                "walmart_search": "Dreame X40 Ultra",
            },
            {
                "name": "L50 Ultra",
                "model": "L50 Ultra",
                "official_url": "https://www.dreametech.com/products/l50-ultra",
                "amazon_search": "Dreame L50 Ultra",
                "walmart_search": "Dreame L50 Ultra",
            },
            {
                "name": "Aqua10 Ultra Roller",
                "model": "Aqua10 Ultra Roller",
                "official_url": "https://www.dreametech.com/products/aqua10-ultra-roller",
                "amazon_search": "Dreame Aqua10 Ultra Roller",
                "walmart_search": "Dreame Aqua10 Ultra Roller",
                "note": "CES 2026 Innovation Honoree"
            },
        ]
    },
    "Shark": {
        "official_site": "https://www.sharkclean.com",
        "products": [
            {
                "name": "PowerDetect NeverTouch Pro",
                "model": "PowerDetect NeverTouch Pro",
                "official_url": "https://www.sharkclean.com/powerdetect-robot",
                "amazon_search": "Shark PowerDetect NeverTouch Pro",
                "walmart_search": "Shark PowerDetect NeverTouch Pro",
            },
            {
                "name": "Matrix Plus 2-in-1",
                "model": "Matrix Plus",
                "official_url": "https://www.sharkclean.com/matrix-plus",
                "amazon_search": "Shark Matrix Plus Robot Vacuum",
                "walmart_search": "Shark Matrix Plus",
            },
            {
                "name": "AI Ultra Self-Empty",
                "model": "AI Ultra",
                "official_url": "https://www.sharkclean.com/ai-ultra",
                "amazon_search": "Shark AI Ultra Robot Vacuum AV2501S",
                "walmart_search": "Shark AI Ultra",
            },
        ]
    },
    "Eufy": {
        "official_site": "https://www.eufy.com",
        "note": "Anker sub-brand",
        "products": [
            {
                "name": "Omni S2",
                "model": "Omni S2",
                "official_url": "https://www.eufy.com/robot-vacuum/omni-s2",
                "amazon_search": "Eufy Omni S2",
                "walmart_search": "Eufy Omni S2",
                "note": "CES 2026 - 30,000Pa, aromatherapy"
            },
            {
                "name": "X10 Pro Omni",
                "model": "X10 Pro Omni",
                "official_url": "https://www.eufy.com/robot-vacuum/x10-pro-omni",
                "amazon_search": "Eufy X10 Pro Omni",
                "walmart_search": "Eufy X10 Pro Omni",
            },
            {
                "name": "L60 Ultra",
                "model": "L60 Ultra",
                "official_url": "https://www.eufy.com/robot-vacuum/l60-ultra",
                "amazon_search": "Eufy L60 Ultra",
                "walmart_search": "Eufy L60",
            },
        ]
    },
    "Narwal": {
        "official_site": "https://www.narwal.com",
        "products": [
            {
                "name": "Flow 2",
                "model": "Flow 2",
                "official_url": "https://www.narwal.com/products/flow-2",
                "amazon_search": "Narwal Flow 2",
                "walmart_search": "Narwal Flow 2",
                "note": "CES 2026 - 30,000Pa, AI vision"
            },
            {
                "name": "Freo Z10 Ultra",
                "model": "Freo Z10 Ultra",
                "official_url": "https://www.narwal.com/products/freo-z10-ultra",
                "amazon_search": "Narwal Freo Z10 Ultra",
                "walmart_search": "Narwal Freo Z10",
            },
            {
                "name": "Freo X Ultra",
                "model": "Freo X Ultra",
                "official_url": "https://www.narwal.com/products/freo-x-ultra",
                "amazon_search": "Narwal Freo X Ultra",
                "walmart_search": "Narwal Freo X Ultra",
            },
        ]
    },
    "Dyson": {
        "official_site": "https://www.dyson.com",
        "products": [
            {
                "name": "360 Vis Nav",
                "model": "360 Vis Nav",
                "official_url": "https://www.dyson.com/vacuum-cleaners/robot/360-vis-nav",
                "amazon_search": "Dyson 360 Vis Nav Robot Vacuum",
                "walmart_search": "Dyson 360 Vis Nav",
                "note": "Most powerful suction - 2x others"
            },
        ]
    }
}

# Scraping settings (unchanged)
SCRAPER_CONFIG = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "request_delay": 2,
    "timeout": 10,
    "max_retries": 3
}

# Channel URLs
CHANNELS = {
    "official": "Official Site",
    "amazon": "https://www.amazon.com",
    "walmart": "https://www.walmart.com",
    "costco": "https://www.costco.com",
    "ebay": "https://www.ebay.com"
}
