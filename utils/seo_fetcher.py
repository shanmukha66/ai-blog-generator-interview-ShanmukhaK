import random

class SEOMetrics:
    def __init__(self, search_volume: int, keyword_difficulty: float, avg_cpc: float):
        self.search_volume = search_volume
        self.keyword_difficulty = keyword_difficulty
        self.avg_cpc = avg_cpc

    def __repr__(self):
        return (f"SEOMetrics(search_volume={self.search_volume}, "
                f"keyword_difficulty={self.keyword_difficulty:.1f}, "
                f"avg_cpc=${self.avg_cpc:.2f})")

def get_metrics(keyword: str) -> SEOMetrics:
    """
    Mock function to return SEO metrics for a given keyword.
    In a real implementation, this would call an actual SEO API service.
    
    Args:
        keyword (str): The keyword to analyze
        
    Returns:
        SEOMetrics: Object containing search volume, keyword difficulty, and average CPC
    """
    # Mock data generation with some randomization
    search_volume = random.randint(1000, 50000)
    keyword_difficulty = random.uniform(0, 100)
    avg_cpc = random.uniform(0.5, 10.0)
    
    return SEOMetrics(
        search_volume=search_volume,
        keyword_difficulty=keyword_difficulty,
        avg_cpc=avg_cpc
    )

# Example usage
if __name__ == "__main__":
    test_keywords = ["digital marketing", "python programming", "machine learning"]
    
    print("Testing SEO Metrics Fetcher:")
    print("-" * 50)
    for keyword in test_keywords:
        metrics = get_metrics(keyword)
        print(f"Keyword: {keyword}")
        print(f"Metrics: {metrics}")
        print("-" * 50) 