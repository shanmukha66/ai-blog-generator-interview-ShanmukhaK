from flask import Flask, jsonify, request, render_template
from dotenv import load_dotenv
from utils.seo_fetcher import get_metrics
from utils.ai_generator import generate_blog_content
from utils.scheduler import generate_daily_blog
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from flask_cors import CORS
import os
import atexit
import json
from datetime import datetime
import subprocess
from crontab import CronTab

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Ensure output directories exist
GENERATED_CONTENT_DIR = "generated_content"
os.makedirs(GENERATED_CONTENT_DIR, exist_ok=True)

# Initialize scheduler and crontab
scheduler = None
cron = CronTab(user=True)

# Clean up any existing cron jobs on startup
for job in cron:
    if 'generate_daily.sh' in str(job):
        cron.remove(job)
cron.write()

def init_scheduler():
    global scheduler
    if scheduler is None:
        scheduler = BackgroundScheduler()
        scheduler.start()

# Initialize scheduler when app starts
init_scheduler()

def save_generated_content(keyword, metrics, blog):
    """Save the generated content to a JSON file"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"blog_{timestamp}.json"
    filepath = os.path.join(GENERATED_CONTENT_DIR, filename)
    
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
        "generated_at": timestamp
    }
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    return filename

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scheduler')
def scheduler_view():
    return render_template('scheduler.html')

@app.route('/api/jobs', methods=['GET'])
def get_jobs():
    jobs = []
    for job in cron:
        if 'generate_daily.sh' in str(job):
            # Extract keyword from comment
            keyword = job.comment.split('_')[1] if '_' in job.comment else 'Unknown Topic'
            schedule = ' '.join(str(job.slices).split(' ')[:4])  # Only take minute, hour, day, month
            jobs.append({
                'id': job.comment,
                'schedule': schedule,
                'command': str(job),
                'enabled': job.is_enabled(),
                'keyword': keyword
            })
    return jsonify(jobs)

@app.route('/api/jobs', methods=['POST'])
def create_job():
    data = request.json
    keyword = data.get('keyword')
    minute = data.get('minute')
    hour = data.get('hour')
    day = data.get('day')
    month = data.get('month')
    
    if not all([keyword, minute, hour, day, month]):
        return jsonify({'error': 'Missing required fields'}), 400
    
    job_id = f"blog_{keyword}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    # Create the cron job with the keyword in the command
    job = cron.new(
        command=f'cd "{os.getcwd()}" && ./generate_daily.sh "{keyword}" >> /tmp/blog_generator.log 2>&1',
        comment=job_id
    )
    
    # Set the schedule (without day of week)
    job.setall(minute, hour, day, month, '*')
    
    # Save the crontab
    cron.write()
    
    return jsonify({
        'id': job_id,
        'schedule': ' '.join(str(job.slices).split(' ')[:4]),  # Only take minute, hour, day, month
        'command': str(job),
        'enabled': job.is_enabled(),
        'keyword': keyword
    })

@app.route('/api/jobs/<job_id>', methods=['DELETE'])
def delete_job(job_id):
    for job in cron:
        if job.comment == job_id:
            cron.remove(job)
            cron.write()
            return jsonify({'status': 'success'})
    return jsonify({'status': 'error', 'message': 'Job not found'}), 404

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
        
        # Save the generated content
        saved_filename = save_generated_content(keyword, metrics, blog)
        
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
            },
            "saved_to": saved_filename
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

def cleanup_jobs():
    """Remove all blog generation cron jobs when the server stops"""
    for job in cron:
        if 'generate_daily.sh' in str(job):
            cron.remove(job)
    cron.write()

def shutdown_scheduler():
    global scheduler
    if scheduler:
        try:
            scheduler.shutdown()
        except Exception:
            pass  # Ignore any shutdown errors
        scheduler = None
    cleanup_jobs()

# Register the shutdown functions to be called on exit
atexit.register(shutdown_scheduler)
atexit.register(cleanup_jobs)

if __name__ == '__main__':
    # Use port 5001 to avoid conflicts with AirPlay on macOS
    port = int(os.getenv('PORT', 5001))
    app.run(debug=True, host='0.0.0.0', port=port) 