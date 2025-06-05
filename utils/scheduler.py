from datetime import datetime
import os
import json
from .seo_fetcher import get_metrics
from .ai_generator import generate_blog_content

# Use the same directory as the web interface
GENERATED_CONTENT_DIR = "generated_content"
os.makedirs(GENERATED_CONTENT_DIR, exist_ok=True)

def generate_daily_blog():
    """
    Generate a daily blog post and save it to a file.
    This function will be called by the scheduler.
    """
    # Predefined keyword for daily blog
    keyword = "wireless earbuds"
    
    try:
        # Get SEO metrics
        metrics = get_metrics(keyword)
        
        # Generate blog content
        blog = generate_blog_content(
            keyword=keyword,
            search_volume=metrics.search_volume,
            keyword_difficulty=metrics.keyword_difficulty,
            avg_cpc=metrics.avg_cpc
        )
        
        if blog:
            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"blog_{timestamp}.json"
            filepath = os.path.join(GENERATED_CONTENT_DIR, filename)
            
            # Prepare the content
            content = {
                "keyword": keyword,
                "seo_metrics": {
                    "search_volume": metrics.search_volume,
                    "keyword_difficulty": round(metrics.keyword_difficulty, 1),
                    "avg_cpc": round(metrics.avg_cpc, 2)
                },
                "blog": {
                    "title": blog.title,
                    "meta_description": blog.meta_description,
                    "content": blog.content
                },
                "generated_at": timestamp,
                "generated_by": "scheduler"
            }
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Daily blog generated successfully: {filepath}")
            return True
        else:
            print("❌ Failed to generate blog content")
            return False
            
    except Exception as e:
        print(f"❌ Error generating daily blog: {str(e)}")
        return False 