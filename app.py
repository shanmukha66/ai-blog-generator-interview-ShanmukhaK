import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
import json
from pathlib import Path

from ai_generator import generate_blog_post

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Create a directory for storing generated posts
POSTS_DIR = Path("generated_posts")
POSTS_DIR.mkdir(exist_ok=True)

def generate_daily_post():
    """Generate a blog post for the daily keyword and save it to disk."""
    daily_keyword = os.getenv("DAILY_KEYWORD", "wireless earbuds")
    result = generate_blog_post(daily_keyword)
    
    # Create filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = POSTS_DIR / f"{daily_keyword.replace(' ', '_')}_{timestamp}.json"
    
    # Save the result
    with open(filename, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"Generated daily post for '{daily_keyword}' saved to {filename}")
    return filename

# Set up the scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    generate_daily_post,
    'cron',
    hour=0,  # Run at midnight
    minute=0,
    id='daily_post_generator'
)
scheduler.start()

@app.route('/generate', methods=['GET'])
def generate():
    """Generate a blog post for the given keyword."""
    keyword = request.args.get('keyword')
    if not keyword:
        return jsonify({"error": "Keyword parameter is required"}), 400
    
    result = generate_blog_post(keyword)
    return jsonify(result)

@app.route('/health', methods=['GET'])
def health_check():
    """Detailed health check endpoint."""
    try:
        # Get scheduler status
        scheduler_status = {
            "running": scheduler.running,
            "jobs": [
                {
                    "id": job.id,
                    "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                    "trigger": str(job.trigger)
                }
                for job in scheduler.get_jobs()
            ]
        }
        
        # Get latest generated post
        latest_post = None
        if POSTS_DIR.exists():
            posts = list(POSTS_DIR.glob("*.json"))
            if posts:
                latest_post = str(max(posts, key=lambda x: x.stat().st_mtime))
        
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "scheduler": scheduler_status,
            "storage": {
                "posts_directory": str(POSTS_DIR),
                "latest_post": latest_post,
                "total_posts": len(list(POSTS_DIR.glob("*.json"))) if POSTS_DIR.exists() else 0
            },
            "environment": {
                "daily_keyword": os.getenv("DAILY_KEYWORD", "wireless earbuds"),
                "api_configured": bool(os.getenv("GROQ_API_KEY"))
            }
        })
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }), 500

if __name__ == '__main__':
    # Generate an initial post on startup
    generate_daily_post()
    app.run(debug=True) 