import os
from groq import Groq
from datetime import datetime
import random
from dotenv import load_dotenv
from seo_fetcher import get_seo_metrics, get_related_keywords

# Load environment variables
load_dotenv()

# Get API key with error handling
api_key = os.getenv('GROQ_API_KEY')
if not api_key:
    raise ValueError("GROQ_API_KEY environment variable is not set. Please check your .env file.")

# Initialize Groq client
client = Groq(api_key=api_key)

def generate_affiliate_links(keyword: str, count: int = 3) -> list:
    """Generate mock affiliate links for the given keyword."""
    domains = ['amazon.com', 'bestbuy.com', 'walmart.com']
    return [
        f"https://{domain}/products/{keyword.replace(' ', '-')}-{i}"
        for i, domain in enumerate(domains[:count], 1)
    ]

def create_blog_post_prompt(keyword: str, seo_metrics: dict, related_keywords: list) -> str:
    """Create a detailed prompt for the AI to generate a blog post."""
    return f"""Write a comprehensive, SEO-optimized blog post about {keyword}. 
    Use the following metrics to inform the content:
    - Monthly Search Volume: {seo_metrics['search_volume']}
    - Keyword Difficulty: {seo_metrics['keyword_difficulty']}
    - Average CPC: ${seo_metrics['avg_cpc']}

    Related keywords to include: {', '.join(related_keywords)}

    The blog post should:
    1. Have a compelling title with the main keyword
    2. Include an introduction that hooks the reader
    3. Feature 3-5 main sections with subheadings
    4. Include {{AFF_LINK_1}}, {{AFF_LINK_2}}, and {{AFF_LINK_3}} naturally in the content
    5. End with a conclusion and call to action
    6. Be written in a conversational yet authoritative tone
    7. Be optimized for SEO while remaining engaging for readers

    Format the post in Markdown."""

def generate_blog_post(keyword: str) -> dict:
    """
    Generate a complete blog post for the given keyword using Groq,
    including SEO metrics and affiliate links.
    """
    # Get SEO metrics and related keywords
    seo_metrics = get_seo_metrics(keyword)
    related_keywords = get_related_keywords(keyword)
    
    # Generate the blog post content
    prompt = create_blog_post_prompt(keyword, seo_metrics, related_keywords)
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert content writer specializing in creating engaging, SEO-optimized blog posts."
                },
                {
                    "role": "user",
                    "content": [{"type": "text", "text": prompt}]
                }
            ],
            temperature=0.6,
            max_completion_tokens=4096,
            top_p=0.95,
            stream=False,
            stop=None
        )
        
        # Get the generated content
        content = response.choices[0].message.content
        
        # Generate and replace affiliate link placeholders
        affiliate_links = generate_affiliate_links(keyword)
        for i, link in enumerate(affiliate_links, 1):
            content = content.replace(f"{{{{AFF_LINK_{i}}}}}", link)
        
        # Create the response object
        result = {
            "keyword": keyword,
            "seo_metrics": seo_metrics,
            "content": content,
            "generated_at": datetime.now().isoformat(),
            "affiliate_links": affiliate_links
        }
        
        return result
    
    except Exception as e:
        return {
            "error": str(e),
            "keyword": keyword,
            "generated_at": datetime.now().isoformat()
        } 