from utils.seo_fetcher import get_metrics

def test_seo_fetcher():
    # Test with a sample keyword
    keyword = "example"
    metrics = get_metrics(keyword)
    
    # Verify that all required fields are present and have correct types
    assert isinstance(metrics.search_volume, int), "search_volume should be an integer"
    assert isinstance(metrics.keyword_difficulty, float), "keyword_difficulty should be a float"
    assert isinstance(metrics.avg_cpc, float), "avg_cpc should be a float"
    
    # Verify value ranges
    assert 1000 <= metrics.search_volume <= 50000, "search_volume out of expected range"
    assert 0 <= metrics.keyword_difficulty <= 100, "keyword_difficulty out of expected range"
    assert 0.5 <= metrics.avg_cpc <= 10.0, "avg_cpc out of expected range"
    
    print("✅ All tests passed!")
    print(f"\nResults for keyword '{keyword}':")
    print(f"Search Volume: {metrics.search_volume}")
    print(f"Keyword Difficulty: {metrics.keyword_difficulty:.1f}")
    print(f"Average CPC: ${metrics.avg_cpc:.2f}")

if __name__ == "__main__":
    test_seo_fetcher() 