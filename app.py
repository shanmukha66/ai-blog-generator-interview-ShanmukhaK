import os
from flask import Flask, request, jsonify, render_template_string, send_from_directory, make_response
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
import json
from pathlib import Path
import markdown2

from ai_generator import generate_blog_post

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Create a directory for storing generated posts
POSTS_DIR = Path("generated_posts")
POSTS_DIR.mkdir(exist_ok=True)

# HTML template for the blog list page
BLOG_LIST_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>AI-Powered Blog Generator</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }
        .header {
            text-align: center;
            margin-bottom: 3rem;
            padding: 3rem 0;
            background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
            color: white;
            border-radius: 16px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .header h1 {
            font-size: 2.5rem;
            margin-bottom: 1rem;
            font-weight: 700;
        }
        .header p {
            font-size: 1.1rem;
            opacity: 0.9;
            max-width: 600px;
            margin: 0 auto 2rem;
        }
        .generate-form {
            max-width: 500px;
            margin: 0 auto;
            display: flex;
            gap: 0.5rem;
        }
        input[type="text"] {
            flex: 1;
            padding: 0.75rem 1rem;
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 8px;
            background: rgba(255, 255, 255, 0.1);
            color: white;
            font-size: 1rem;
        }
        input[type="text"]::placeholder {
            color: rgba(255, 255, 255, 0.6);
        }
        button {
            padding: 0.75rem 1.5rem;
            background: white;
            color: #6366f1;
            border: none;
            border-radius: 8px;
            font-weight: 600;
            font-size: 1rem;
            cursor: pointer;
            transition: all 0.2s;
        }
        button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        .section-title {
            font-size: 1.5rem;
            font-weight: 600;
            margin: 2rem 0 1rem;
            color: #1a1a1a;
        }
        .post-list {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            margin-top: 2rem;
        }
        .post-card {
            background: white;
            border-radius: 12px;
            overflow: hidden;
            transition: all 0.3s;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .post-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        .post-image {
            height: 200px;
            background: linear-gradient(45deg, #6366f1, #8b5cf6);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 3rem;
            font-weight: bold;
        }
        .post-content {
            padding: 1.5rem;
        }
        .post-title {
            color: #1a1a1a;
            text-decoration: none;
            font-size: 1.25rem;
            font-weight: 600;
            margin-bottom: 1rem;
            display: block;
        }
        .post-meta {
            font-size: 0.875rem;
            color: #666;
        }
        .meta-item {
            display: flex;
            align-items: center;
            margin-bottom: 0.5rem;
        }
        .meta-label {
            font-weight: 500;
            margin-right: 0.5rem;
            color: #4b5563;
        }
        .meta-value {
            color: #6366f1;
        }
        @media (max-width: 768px) {
            .container { padding: 1rem; }
            .header { padding: 2rem 1rem; margin-bottom: 2rem; }
            .post-list { gap: 1rem; }
            .generate-form { flex-direction: column; }
            button { width: 100%; }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>AI-Powered Blog Generator</h1>
            <p>Generate high-quality, SEO-optimized blog posts instantly using advanced AI technology.</p>
            <div class="generate-form">
                <input type="text" name="keyword" placeholder="Enter a topic (e.g., gaming laptop, smart home, fitness tech)">
                <button type="submit" onclick="generatePost()">Generate Post</button>
            </div>
        </div>
        {% if recent_posts %}
        <h2 class="section-title">Recently Viewed</h2>
        <div class="post-list">
            {% for post in recent_posts %}
            <div class="post-card">
                <div class="post-image">
                    {{ post.keyword[0]|upper }}
                </div>
                <div class="post-content">
                    <a href="/view/{{ post.filename }}" class="post-title">{{ post.title }}</a>
                    <div class="post-meta">
                        <div class="meta-item">
                            <span class="meta-label">Topic:</span>
                            <span class="meta-value">{{ post.keyword }}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Generated:</span>
                            <span class="meta-value">{{ post.date }}</span>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
        {% endif %}
        
        <h2 class="section-title">All Posts</h2>
        <div class="post-list">
            {% for post in posts %}
            <div class="post-card">
                <div class="post-image">
                    {{ post.keyword[0]|upper }}
                </div>
                <div class="post-content">
                    <a href="/view/{{ post.filename }}" class="post-title">{{ post.title }}</a>
                    <div class="post-meta">
                        <div class="meta-item">
                            <span class="meta-label">Topic:</span>
                            <span class="meta-value">{{ post.keyword }}</span>
                        </div>
                        <div class="meta-item">
                            <span class="meta-label">Generated:</span>
                            <span class="meta-value">{{ post.date }}</span>
                        </div>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>
    </div>
    <script>
        function generatePost() {
            const keyword = document.querySelector('input[name="keyword"]').value;
            if (keyword) {
                // Disable the button to prevent double submission
                const button = document.querySelector('button');
                button.disabled = true;
                button.textContent = 'Generating...';
                
                window.location.href = `/generate?keyword=${encodeURIComponent(keyword)}`;
            }
        }
        
        // Allow form submission with Enter key
        document.querySelector('input[name="keyword"]').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                generatePost();
            }
        });
    </script>
</body>
</html>
"""

# HTML template for individual blog posts
BLOG_POST_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Inter', sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        .back-link {
            display: inline-flex;
            align-items: center;
            color: #6366f1;
            text-decoration: none;
            font-weight: 500;
            margin-bottom: 2rem;
            transition: all 0.2s;
        }
        .back-link:hover {
            transform: translateX(-5px);
        }
        .back-link:before {
            content: '←';
            margin-right: 0.5rem;
        }
        .article {
            background: white;
            border-radius: 16px;
            padding: 2rem;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }
        .article-header {
            text-align: center;
            margin-bottom: 2rem;
            padding-bottom: 2rem;
            border-bottom: 1px solid #eee;
        }
        .article-title {
            font-size: 2.5rem;
            color: #1a1a1a;
            margin-bottom: 1rem;
            line-height: 1.2;
        }
        .meta {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1rem;
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 2rem 0;
        }
        .meta-item {
            text-align: center;
        }
        .meta-label {
            font-size: 0.875rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            color: #6b7280;
            margin-bottom: 0.25rem;
        }
        .meta-value {
            font-size: 1.25rem;
            font-weight: 600;
            color: #6366f1;
        }
        .content {
            font-size: 1.125rem;
            color: #374151;
        }
        .content h1 { font-size: 2rem; margin: 2rem 0 1rem; }
        .content h2 { font-size: 1.5rem; margin: 1.5rem 0 1rem; }
        .content h3 { font-size: 1.25rem; margin: 1.25rem 0 0.75rem; }
        .content p { margin-bottom: 1.25rem; }
        .content ul, .content ol { margin: 1rem 0; padding-left: 1.5rem; }
        .content li { margin-bottom: 0.5rem; }
        .content table {
            width: 100%;
            border-collapse: collapse;
            margin: 1.5rem 0;
        }
        .content th, .content td {
            border: 1px solid #e5e7eb;
            padding: 0.75rem;
            text-align: left;
        }
        .content th {
            background: #f8f9fa;
            font-weight: 600;
        }
        .content tr:nth-child(even) {
            background: #f8f9fa;
        }
        @media (max-width: 768px) {
            .container { padding: 1rem; }
            .article { padding: 1.5rem; }
            .article-title { font-size: 2rem; }
            .meta { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <div class="container">
        <a href="/" class="back-link">Back to all posts</a>
        <article class="article">
            <header class="article-header">
                <h1 class="article-title">{{ title }}</h1>
                <div class="meta">
                    <div class="meta-item">
                        <div class="meta-label">Topic</div>
                        <div class="meta-value">{{ keyword }}</div>
                    </div>
                    <div class="meta-item">
                        <div class="meta-label">Generated</div>
                        <div class="meta-value">{{ date }}</div>
                    </div>
                </div>
            </header>
            <div class="content">
                {{ content|safe }}
            </div>
        </article>
    </div>
</body>
</html>
"""

def get_post_data(filename):
    """Get post data from a file."""
    try:
        with open(POSTS_DIR / filename) as f:
            data = json.load(f)
            content = data.get('content', '')
            title = content.split('\n')[0].strip('# ') if content else data['keyword']
            return {
                'filename': filename,
                'title': title,
                'keyword': data['keyword'],
                'date': datetime.fromisoformat(data['generated_at']).strftime('%Y-%m-%d %H:%M:%S'),
                'content': content
            }
    except Exception as e:
        print(f"Error loading post {filename}: {str(e)}")
        return None

def get_recent_posts(recent_filenames):
    """Get data for recently viewed posts."""
    recent_posts = []
    for filename in recent_filenames:
        post_data = get_post_data(filename)
        if post_data:
            recent_posts.append(post_data)
    return recent_posts

@app.route('/')
def list_posts():
    """Display a list of all generated blog posts."""
    posts = []
    for file in POSTS_DIR.glob("*.json"):
        post_data = get_post_data(file.name)
        if post_data:
            posts.append(post_data)
    
    # Sort posts by date, newest first
    posts.sort(key=lambda x: x['date'], reverse=True)
    
    # Get recently viewed posts from cookie
    recent_filenames = request.cookies.get('recent_posts', '').split(',')
    recent_filenames = [f for f in recent_filenames if f]  # Remove empty strings
    recent_posts = get_recent_posts(recent_filenames[-5:])  # Get last 5 viewed posts
    
    return render_template_string(BLOG_LIST_TEMPLATE, posts=posts, recent_posts=recent_posts)

@app.route('/view/<filename>')
def view_post(filename):
    """Display a single blog post."""
    try:
        post_data = get_post_data(filename)
        if not post_data:
            return "Post not found", 404
            
        # Convert markdown content to HTML
        content_html = markdown2.markdown(post_data['content'])
        
        # Create response with the rendered template
        response = make_response(render_template_string(
            BLOG_POST_TEMPLATE,
            title=post_data['title'],
            keyword=post_data['keyword'],
            date=post_data['date'],
            content=content_html
        ))
        
        # Update recently viewed posts in cookie
        recent_posts = request.cookies.get('recent_posts', '').split(',')
        recent_posts = [f for f in recent_posts if f and f != filename]  # Remove empty strings and current file
        recent_posts.append(filename)  # Add current file to end
        recent_posts = recent_posts[-5:]  # Keep only last 5
        
        # Set cookie with 30-day expiration
        response.set_cookie('recent_posts', ','.join(recent_posts), max_age=30*24*60*60)
        
        return response
    except Exception as e:
        return f"Error loading post: {str(e)}", 404

@app.route('/generate', methods=['GET'])
def generate():
    """Generate a blog post for the given keyword."""
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword parameter is required"}), 400
    
    result = generate_blog_post(keyword)
    
    # Save the post
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{keyword.replace(' ', '_')}_{timestamp}.json"
    with open(POSTS_DIR / filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    # Redirect to the post page
    return view_post(filename)

if __name__ == '__main__':
    # Run on port 5001 instead of default 5000
    app.run(debug=True, port=5001) 