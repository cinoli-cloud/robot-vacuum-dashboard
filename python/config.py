"""
Configuration file for robot vacuum price scraper
"""

# Top 8 Robot Vacuum Brands and their flagship products
BRANDS_CONFIG = {
    "iRobot": {
        "official_site": "https://www.irobot.com",
        "products": [
            {
                "name": "Roomba Combo j9+",
                "model": "j9+",
                "amazon_search": "iRobot Roomba Combo j9+",
                "walmart_search": "iRobot Roomba j9+",
            },
            {
                "name": "Roomba j7+",
                "model": "j7+",
                "amazon_search": "iRobot Roomba j7+",
                "walmart_search": "iRobot Roomba j7+",
            },
            {
                "name": "Roomba i7+",
                "model": "i7+",
                "amazon_search": "iRobot Roomba i7+",
                "walmart_search": "iRobot Roomba i7+",
            }
        ]
    },
    "Roborock": {
        "official_site": "https://us.roborock.com",
        "products": [
            {
                "name": "Roborock S8 Pro Ultra",
                "model": "S8 Pro Ultra",
                "amazon_search": "Roborock S8 Pro Ultra",
                "walmart_search": "Roborock S8 Pro Ultra",
            },
            {
                "name": "Roborock Q Revo",
                "model": "Q Revo",
                "amazon_search": "Roborock Q Revo",
                "walmart_search": "Roborock Q Revo",
            },
            {
                "name": "Roborock S7 MaxV",
                "model": "S7 MaxV",
                "amazon_search": "Roborock S7 MaxV",
                "walmart_search": "Roborock S7 MaxV",
            }
        ]
    },
    "Ecovacs": {
        "official_site": "https://www.ecovacs.com",
        "products": [
            {
                "name": "Deebot X2 Omni",
                "model": "X2 Omni",
                "amazon_search": "Ecovacs Deebot X2 Omni",
                "walmart_search": "Ecovacs Deebot X2 Omni",
            },
            {
                "name": "Deebot T30 Pro",
                "model": "T30 Pro",
                "amazon_search": "Ecovacs Deebot T30 Pro",
                "walmart_search": "Ecovacs Deebot T30 Pro",
            },
            {
                "name": "Deebot N8 Pro+",
                "model": "N8 Pro+",
                "amazon_search": "Ecovacs Deebot N8 Pro+",
                "walmart_search": "Ecovacs Deebot N8 Pro+",
            }
        ]
    },
    "Dreame": {
        "official_site": "https://www.dreametech.com",
        "products": [
            {
                "name": "Dreame X40 Ultra",
                "model": "X40 Ultra",
                "amazon_search": "Dreame X40 Ultra",
                "walmart_search": "Dreame X40 Ultra",
            },
            {
                "name": "Dreame L10s Ultra",
                "model": "L10s Ultra",
                "amazon_search": "Dreame L10s Ultra",
                "walmart_search": "Dreame L10s Ultra",
            },
            {
                "name": "Dreame L20 Ultra",
                "model": "L20 Ultra",
                "amazon_search": "Dreame L20 Ultra",
                "walmart_search": "Dreame L20 Ultra",
            }
        ]
    },
    "Shark": {
        "official_site": "https://www.sharkclean.com",
        "products": [
            {
                "name": "Shark AI Ultra",
                "model": "AI Ultra",
                "amazon_search": "Shark AI Ultra Robot Vacuum",
                "walmart_search": "Shark AI Ultra",
            },
            {
                "name": "Shark Matrix Plus",
                "model": "Matrix Plus",
                "amazon_search": "Shark Matrix Plus Robot Vacuum",
                "walmart_search": "Shark Matrix Plus",
            },
            {
                "name": "Shark IQ Robot",
                "model": "IQ Robot",
                "amazon_search": "Shark IQ Robot Vacuum",
                "walmart_search": "Shark IQ Robot",
            }
        ]
    },
    "Eufy": {
        "official_site": "https://www.eufy.com",
        "products": [
            {
                "name": "Eufy X10 Pro Omni",
                "model": "X10 Pro Omni",
                "amazon_search": "Eufy X10 Pro Omni",
                "walmart_search": "Eufy X10 Pro Omni",
            },
            {
                "name": "Eufy L60",
                "model": "L60",
                "amazon_search": "Eufy L60 Robot Vacuum",
                "walmart_search": "Eufy L60",
            },
            {
                "name": "Eufy RoboVac X8",
                "model": "X8",
                "amazon_search": "Eufy RoboVac X8",
                "walmart_search": "Eufy RoboVac X8",
            }
        ]
    },
    "Narwal": {
        "official_site": "https://www.narwal.com",
        "products": [
            {
                "name": "Narwal Freo Z10",
                "model": "Freo Z10",
                "amazon_search": "Narwal Freo Z10",
                "walmart_search": "Narwal Freo Z10",
            },
            {
                "name": "Narwal Freo X Ultra",
                "model": "Freo X Ultra",
                "amazon_search": "Narwal Freo X Ultra",
                "walmart_search": "Narwal Freo X Ultra",
            },
            {
                "name": "Narwal T10",
                "model": "T10",
                "amazon_search": "Narwal T10 Robot Vacuum",
                "walmart_search": "Narwal T10",
            }
        ]
    },
    "Dyson": {
        "official_site": "https://www.dyson.com",
        "products": [
            {
                "name": "Dyson 360 Vis Nav",
                "model": "360 Vis Nav",
                "amazon_search": "Dyson 360 Vis Nav",
                "walmart_search": "Dyson 360 Vis Nav",
            },
            {
                "name": "Dyson 360 Heurist",
                "model": "360 Heurist",
                "amazon_search": "Dyson 360 Heurist",
                "walmart_search": "Dyson 360 Heurist",
            }
        ]
    }
}

# Scraping settings
SCRAPER_CONFIG = {
    "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "request_delay": 2,  # seconds between requests
    "timeout": 10,  # seconds
    "max_retries": 3
}

# Channel URLs
CHANNELS = {
    "amazon": "https://www.amazon.com",
    "walmart": "https://www.walmart.com",
    "costco": "https://www.costco.com",
    "ebay": "https://www.ebay.com"
}
