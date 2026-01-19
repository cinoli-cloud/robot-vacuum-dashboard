"""
New Products Tagging
Based on CES 2026 announcements and 2026 launches
"""

# Products that should be tagged as NEW (CES 2026 or Jan 2026 launches)
NEW_PRODUCTS_2026 = {
    "Eufy": [
        "Omni S2",  # CES 2026 Innovation Honoree, Launch Jan 20
    ],
    "Roborock": [
        "Saros 20 Sonic",  # CES 2026 - 35,000Pa record
        "Saros 20",  # CES 2026
        "Qrevo Curv 2 Flow",  # CES 2026 - Launch Jan 19
        "Saros Z70",  # CES 2025 Best of Show (still new in 2026)
    ],
    "Ecovacs": [
        "X12 Pro Omni",  # CES 2026
        "X12 OmniCyclone",  # CES 2026 Innovation Award
        "T90 Pro Omni",  # CES 2026
    ],
    "Dreame": [
        "X60 Max Ultra Complete",  # CES 2026 - Ultra thin
        "X60 Ultra",  # CES 2026
        "Cyber10 Ultra",  # CES 2026 - Robotic arm
        "Aqua10 Ultra Roller",  # CES 2026 Innovation Award
    ],
    "Narwal": [
        "Flow 2",  # CES 2026 - NarMind Pro AI
    ],
    "Shark": [],  # No new CES 2026 products
    "iRobot": [],  # Bankruptcy - no new products
    "Dyson": [],  # No new products announced
}

def is_new_product(brand, product_name):
    """Check if product should be tagged as NEW"""
    if brand not in NEW_PRODUCTS_2026:
        return False

    new_list = NEW_PRODUCTS_2026[brand]

    # Check if product name contains any of the new products
    for new_product in new_list:
        if new_product in product_name:
            return True

    return False

def get_new_product_note(brand, product_name):
    """Get NEW product note"""
    if not is_new_product(brand, product_name):
        return ""

    # CES 2026 specific notes
    ces_notes = {
        "Eufy Omni S2": "CES 2026 Innovation Honoree - Launch Jan 20, 2026",
        "Roborock Saros 20 Sonic": "CES 2026 - 35,000Pa record-breaking suction",
        "Roborock Saros 20": "CES 2026 - 35,000Pa with AdaptiLift 3.0",
        "Roborock Qrevo Curv 2 Flow": "CES 2026 - First roller mop, Launch Jan 19",
        "Roborock Saros Z70": "CES 2025 Best of Show - Mechanical arm",
        "Ecovacs X12 Pro Omni": "CES 2026 - OZMO Roller 3.0",
        "Ecovacs X12 OmniCyclone": "CES 2026 Innovation Award",
        "Ecovacs T90 Pro Omni": "CES 2026 - Advanced mopping",
        "Dreame X60 Max Ultra Complete": "CES 2026 - 7.95cm ultra-thin with robotic legs",
        "Dreame X60 Ultra": "CES 2026 - 7.95cm ultra-thin design",
        "Dreame Cyber10 Ultra": "CES 2026 - Robotic arm technology",
        "Dreame Aqua10 Ultra Roller": "CES 2026 Innovation Award",
        "Narwal Flow 2": "CES 2026 - 30,000Pa with unlimited object recognition",
    }

    # Find matching note
    for key, note in ces_notes.items():
        if key in f"{brand} {product_name}":
            return note

    return "NEW 2026"
