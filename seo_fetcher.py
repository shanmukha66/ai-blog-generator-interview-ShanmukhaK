import random

# Mock SEO data for demonstration purposes
MOCK_SEO_DATA = {
    "wireless earbuds": {
        "search_volume": 165000,
        "keyword_difficulty": 72,
        "avg_cpc": 1.45
    },
    "gaming laptop": {
        "search_volume": 135000,
        "keyword_difficulty": 68,
        "avg_cpc": 2.10
    },
    "mechanical keyboard": {
        "search_volume": 110000,
        "keyword_difficulty": 65,
        "avg_cpc": 1.75
    },
    "gaming mouse": {
        "search_volume": 145000,
        "keyword_difficulty": 70,
        "avg_cpc": 1.95
    },
    "gaming headset": {
        "search_volume": 155000,
        "keyword_difficulty": 71,
        "avg_cpc": 1.85
    }
}

def get_seo_metrics(keyword: str) -> dict:
    """
    Get SEO metrics for a given keyword. If the keyword isn't in our mock data,
    generate reasonable random values.
    """
    if keyword.lower() in MOCK_SEO_DATA:
        return MOCK_SEO_DATA[keyword.lower()]
    
    # Generate mock data for unknown keywords
    return {
        "search_volume": random.randint(1000, 200000),
        "keyword_difficulty": random.randint(20, 80),
        "avg_cpc": round(random.uniform(0.5, 3.0), 2)
    }

def get_related_keywords(keyword: str) -> list:
    """
    Get a list of related keywords for the main keyword.
    This is a simplified mock implementation.
    """
    base_keywords = [
        f"best {keyword}",
        f"{keyword} reviews",
        f"top {keyword}",
        f"{keyword} comparison",
        f"affordable {keyword}"
    ]
    return base_keywords 