from flask import Flask, jsonify, request
from dotenv import load_dotenv
from utils.seo_fetcher import get_metrics
from utils.ai_generator import generate_blog_content
from utils.scheduler import generate_daily_blog
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
import os

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Initialize scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(
    func=generate_daily_blog,
    trigger=CronTrigger(hour=9, minute=0),  # Run at 09:00 every day
    id='daily_blog_generator',
    name='Generate daily blog post',
    replace_existing=True
)
scheduler.start()

@app.route('/')
def home():
    return jsonify({
        "message": "Welcome to AI Blog Generator API",
        "endpoints": {
            "generate": "/generate?keyword=your+keyword",
        },
        "scheduler_info": {
            "next_run": scheduler.get_job('daily_blog_generator').next_run_time.strftime('%Y-%m-%d %H:%M:%S')
        }
    })

@app.route('/generate', methods=['GET', 'POST'])
def generate_blog():
    # Get keyword from query parameters or JSON body
    if request.method == 'GET':
        keyword = request.args.get('keyword')
    else:  # POST
        keyword = request.json.get('keyword') if request.json else None
    
    if not keyword:
        return jsonify({
            "error": "Missing required parameter: keyword"
        }), 400
    
    try:
        # Get SEO metrics for the keyword
        metrics = get_metrics(keyword)
        
        # Generate blog content using the metrics
        blog = generate_blog_content(
            keyword=keyword,
            search_volume=metrics.search_volume,
            keyword_difficulty=metrics.keyword_difficulty,
            avg_cpc=metrics.avg_cpc
        )
        
        if not blog:
            return jsonify({
                "error": "Failed to generate blog content"
            }), 500
        
        # Return the combined response
        return jsonify({
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
            }
        })
        
    except Exception as e:
        return jsonify({
            "error": f"An error occurred: {str(e)}"
        }), 500

@app.route('/generate-now', methods=['POST'])
def generate_now():
    """Endpoint to trigger blog generation immediately"""
    success = generate_daily_blog()
    return jsonify({
        "status": "success" if success else "error",
        "message": "Blog generation completed" if success else "Failed to generate blog"
    })

# Shutdown scheduler when app stops
def shutdown_scheduler():
    scheduler.shutdown()

app.teardown_appcontext(lambda _: shutdown_scheduler())

if __name__ == '__main__':
    # Use port 5001 to avoid conflicts with AirPlay on macOS
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port) 