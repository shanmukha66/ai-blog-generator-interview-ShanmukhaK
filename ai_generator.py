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
    return f"""You are an expert content writer and SEO specialist. Create a comprehensive, engaging, and highly detailed blog post about {keyword}. The post should be informative, well-researched, and valuable to readers.

Key Requirements:
1. Write in a professional yet conversational tone
2. Include current trends and industry insights
3. Back claims with data and expert opinions
4. Optimize for both readers and search engines
5. Structure content for easy reading and scanning

SEO Metrics to Consider:
- Monthly Search Volume: {seo_metrics['search_volume']}
- Keyword Difficulty: {seo_metrics['keyword_difficulty']}
- Target Keywords: {keyword}, {', '.join(related_keywords)}

Content Structure:
1. Start with an attention-grabbing headline that includes the main keyword
2. Write an engaging introduction that:
   - Hooks the reader immediately
   - States the value proposition
   - Previews what readers will learn
3. Include 4-5 main sections with descriptive subheadings
4. For each section:
   - Start with a clear topic sentence
   - Include specific examples and details
   - Back claims with data or expert insights
   - End with a mini-conclusion or takeaway
5. Add practical tips, comparisons, or case studies where relevant
6. Include product recommendations naturally using {{AFF_LINK_1}}, {{AFF_LINK_2}}, and {{AFF_LINK_3}}
7. End with a strong conclusion and clear call-to-action

Additional Requirements:
- Use bullet points and lists for better readability
- Include relevant statistics and data points
- Add expert quotes or industry insights where applicable
- Use transition sentences between sections
- Maintain a consistent voice throughout
- Format in proper Markdown with clear hierarchy

Make the content detailed, actionable, and valuable enough that readers would want to bookmark it and share it with others. Focus on providing genuine value while naturally incorporating SEO elements."""

def generate_default_content(keyword: str) -> str:
    """Generate a default blog post when API is not available."""
    return f"""# The Ultimate Guide to {keyword.title()}

## Introduction

Welcome to our comprehensive guide about {keyword}. In this article, we'll explore everything you need to know about this topic, from basic concepts to advanced tips and recommendations.

## What to Look for in {keyword.title()}

When considering {keyword}, there are several key factors to keep in mind:

* Quality and performance
* Value for money
* User experience
* Reliability and durability

## Top Recommendations

Here are our top picks for {keyword}:

1. Premium Option: [Check out our top recommendation]({{AFF_LINK_1}})
2. Best Value: [Great balance of features and price]({{AFF_LINK_2}})
3. Budget Pick: [Excellent for cost-conscious buyers]({{AFF_LINK_3}})

## Expert Tips and Advice

To make the most of your {keyword} experience:

* Do thorough research before making a decision
* Compare different options
* Read user reviews and expert opinions
* Consider your specific needs and use cases

## Conclusion

Whether you're new to {keyword} or looking to upgrade, we hope this guide has helped you make an informed decision. Ready to explore your options? Check out our [top recommendation]({{AFF_LINK_1}}) to get started!
"""

def generate_blog_post(keyword: str) -> dict:
    """
    Generate a complete blog post for the given keyword using Groq,
    including SEO metrics and affiliate links.
    """
    # Get SEO metrics and related keywords
    seo_metrics = get_seo_metrics(keyword)
    related_keywords = get_related_keywords(keyword)
    
    try:
        # Get API key
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            raise ValueError("GROQ_API_KEY not found in environment variables")

        # Initialize Groq client
        client = Groq(api_key=api_key)
        
        # Generate the blog post content
        prompt = create_blog_post_prompt(keyword, seo_metrics, related_keywords)
        
        response = client.chat.completions.create(
            model="meta-llama/llama-4-scout-17b-16e-instruct",
            messages=[
                {
                    "role": "system",
                    "content": """You are an expert content writer and SEO specialist with years of experience in creating viral blog posts. 
                    Your content is known for being:
                    - Deeply researched and informative
                    - Engaging and well-structured
                    - Rich in practical examples and insights
                    - Optimized for both readers and search engines
                    - Written in a professional yet conversational tone
                    
                    Always strive to create content that provides genuine value and establishes authority in the topic."""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.8,  # Increased for more creativity while maintaining coherence
            max_tokens=4000,  # Maximum length for detailed content
            top_p=0.95,      # Maintain high quality while allowing some variation
            stream=False
        )
        
        # Get the generated content
        content = response.choices[0].message.content
        
    except Exception as e:
        print(f"Error generating content with Groq API: {str(e)}")
        # Use default content if API fails
        content = generate_default_content(keyword)
    
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