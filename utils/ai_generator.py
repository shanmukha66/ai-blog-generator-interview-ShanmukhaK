from typing import Dict, Optional
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI()  # Will automatically use OPENAI_API_KEY from environment

class BlogContent:
    def __init__(self, title: str, content: str, meta_description: str):
        self.title = title
        self.content = content
        self.meta_description = meta_description

    def __repr__(self):
        return f"BlogContent(title='{self.title}', content_length={len(self.content)} chars)"

def generate_blog_content(
    keyword: str,
    search_volume: int,
    keyword_difficulty: float,
    avg_cpc: float,
    tone: str = "professional"
) -> Optional[BlogContent]:
    """
    Generate blog content using OpenAI based on SEO metrics.
    
    Args:
        keyword: Main topic/keyword for the blog
        search_volume: Monthly search volume
        keyword_difficulty: SEO difficulty score (0-100)
        avg_cpc: Average cost per click
        tone: Desired tone of the content
        
    Returns:
        BlogContent object containing the generated content
    """
    
    # Construct the prompt template
    prompt = f"""
    Generate a comprehensive blog post about "{keyword}". 
    
    SEO Context:
    - Monthly Search Volume: {search_volume}
    - Keyword Difficulty: {keyword_difficulty:.1f}/100
    - Avg. CPC: ${avg_cpc:.2f}
    
    Requirements:
    1. Write in a {tone} tone
    2. Include a compelling title with the keyword
    3. Structure with H2 and H3 headings
    4. Add {{{{AFF_LINK_1}}}} placeholder where relevant product recommendations fit
    5. Include a meta description for SEO
    6. Use Markdown formatting
    7. Optimize for featured snippets
    8. Include a clear call-to-action
    
    Focus on providing valuable, actionable information while naturally incorporating the keyword.
    """

    try:
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert content writer and SEO specialist."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=2000
        )
        
        # Extract the generated content
        content = response.choices[0].message.content.strip()
        
        # Parse the content to extract title and meta description
        lines = content.split('\n')
        title = lines[0].replace('# ', '').strip()
        
        # Look for meta description in the content
        meta_description = ""
        for line in lines:
            if line.startswith('Meta Description:'):
                meta_description = line.replace('Meta Description:', '').strip()
                content = content.replace(line, '')  # Remove meta description from main content
                break
        
        return BlogContent(
            title=title,
            content=content,
            meta_description=meta_description or f"Comprehensive guide about {keyword} with expert insights and tips."
        )
        
    except Exception as e:
        print(f"Error generating blog content: {str(e)}")
        return None

# Example usage and testing
if __name__ == "__main__":
    # Test the generator with sample data
    test_keyword = "digital marketing strategies"
    blog = generate_blog_content(
        keyword=test_keyword,
        search_volume=25000,
        keyword_difficulty=65.5,
        avg_cpc=4.25,
        tone="professional"
    )
    
    if blog:
        print(f"Generated Blog Title: {blog.title}")
        print("\nMeta Description:")
        print(blog.meta_description)
        print("\nContent Preview (first 500 chars):")
        print(blog.content[:500] + "...") 