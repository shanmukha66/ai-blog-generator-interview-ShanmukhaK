from datetime import datetime
import os
import json
import sys
from .seo_fetcher import get_metrics
from .ai_generator import generate_blog_content

# Use the same directory as the web interface
GENERATED_CONTENT_DIR = "generated_content"
os.makedirs(GENERATED_CONTENT_DIR, exist_ok=True)

def generate_daily_blog(keyword=None):
    """
    Generate a daily blog post and save it to a file.
    This function will be called by the scheduler.
    """
    # Use provided keyword or default
    if not keyword:
        keyword = "wireless earbuds"  # Default fallback
    
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
            filename = f"scheduled_blog_{timestamp}.json"
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
                "generated_by": "scheduler",
                "scheduled_keyword": keyword,
                "generation_type": "scheduled"
            }
            
            # Save to file
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Scheduled blog generated successfully: {filepath}")
            print(f"📝 Keyword: {keyword}")
            print(f"📊 Search Volume: {metrics.search_volume}")
            print(f"🎯 Title: {blog.title}")
            return True
        else:
            print("❌ Failed to generate blog content")
            return False
            
    except Exception as e:
        print(f"❌ Error generating scheduled blog: {str(e)}")
        return False

# Command line interface for cron jobs
if __name__ == "__main__":
    keyword = sys.argv[1] if len(sys.argv) > 1 else None
    success = generate_daily_blog(keyword)
    sys.exit(0 if success else 1) 