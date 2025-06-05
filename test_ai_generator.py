from utils.ai_generator import generate_blog_content
from utils.seo_fetcher import get_metrics

def test_ai_generator():
    # Get SEO metrics for a test keyword
    keyword = "best productivity apps"
    metrics = get_metrics(keyword)
    
    # Generate blog content using the metrics
    blog = generate_blog_content(
        keyword=keyword,
        search_volume=metrics.search_volume,
        keyword_difficulty=metrics.keyword_difficulty,
        avg_cpc=metrics.avg_cpc
    )
    
    # Verify the generated content
    assert blog is not None, "Blog generation failed"
    assert blog.title, "Blog title is missing"
    assert blog.content, "Blog content is missing"
    assert blog.meta_description, "Meta description is missing"
    
    # Verify content structure
    assert "{{AFF_LINK_1}}" in blog.content, "Affiliate link placeholder is missing"
    assert "#" in blog.content, "Markdown headings are missing"
    
    # Print the results
    print("✅ Blog Generation Test Passed!")
    print("\nGenerated Blog Details:")
    print(f"Title: {blog.title}")
    print(f"Meta Description: {blog.meta_description}")
    print("\nContent Preview:")
    print("-" * 50)
    print(blog.content[:1000] + "...\n")
    print("-" * 50)
    print(f"Total content length: {len(blog.content)} characters")

if __name__ == "__main__":
    test_ai_generator() 