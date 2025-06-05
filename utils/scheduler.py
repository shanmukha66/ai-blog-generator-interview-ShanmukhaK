from datetime import datetime
import os
from .seo_fetcher import get_metrics
from .ai_generator import generate_blog_content

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
            # Create blogs directory if it doesn't exist
            os.makedirs('blogs', exist_ok=True)
            
            # Generate filename with today's date
            today = datetime.now().strftime('%Y-%m-%d')
            filename = f"blogs/blog_{today}.md"
            
            # Prepare the content with metadata
            content = f"""---
title: {blog.title}
date: {today}
keyword: {keyword}
meta_description: {blog.meta_description}
search_volume: {metrics.search_volume}
keyword_difficulty: {metrics.keyword_difficulty:.1f}
avg_cpc: ${metrics.avg_cpc:.2f}
---

{blog.content}
"""
            
            # Save to file
            with open(filename, 'w') as f:
                f.write(content)
            
            print(f"✅ Daily blog generated successfully: {filename}")
            return True
        else:
            print("❌ Failed to generate blog content")
            return False
            
    except Exception as e:
        print(f"❌ Error generating daily blog: {str(e)}")
        return False 