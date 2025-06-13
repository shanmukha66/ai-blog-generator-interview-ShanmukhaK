# AI Blog Generator

An automated blog content generator that creates SEO-optimized blog posts based on provided keywords. The application uses OpenAI's API for content generation and provides SEO metrics for the target keywords.

## 🎥 Demo Video

Watch the complete demonstration of the AI Blog Generator in action:
**[📺 YouTube Demo](https://youtu.be/k608Yada4rM?si=w7sGfg6SzS6k8_g4)**

## Features

- 🤖 AI-powered blog content generation using OpenAI GPT
- 📊 SEO metrics for keywords (search volume, difficulty, CPC)
- 🎯 Automated affiliate link integration
- 📱 Responsive web interface with modern UI
- ⏰ **NEW**: Advanced scheduling system with calendar view
- 📚 **NEW**: Complete blog management and tracking system
- 💾 JSON-based content storage with metadata
- 🔍 **NEW**: Search, filter, and view all generated blogs
- 📈 **NEW**: Statistics dashboard for blog analytics
- 🗓️ **NEW**: Cron job management through web interface

## Recent Updates (Latest Version)

### ✨ **Major Enhancements Added:**

1. **📅 Advanced Scheduler Interface**
   - Interactive calendar view for scheduling
   - Precise time scheduling (minute, hour, day, month)
   - Visual schedule management
   - Cron job creation and deletion

2. **📚 Complete Blog Management System**
   - Dedicated `/blogs` page for viewing all generated content
   - Filter blogs by type (scheduled vs manual)
   - Search blogs by keyword or title
   - Sort by date, keyword, or creation time
   - Statistics dashboard showing total, scheduled, manual, and today's blogs

3. **👁️ Enhanced Blog Viewing**
   - Modal popup for full blog content viewing
   - SEO metrics display for each blog
   - File size and creation time information
   - Delete functionality for blog management

4. **🔧 Improved Backend**
   - Separate tracking for scheduled vs manual blogs
   - Enhanced API endpoints for blog management
   - Better error handling and logging
   - Improved file naming conventions

5. **🎨 Better User Experience**
   - Modern card-based layout for blog display
   - Responsive design for all screen sizes
   - Loading states and error handling
   - Intuitive navigation between pages

## Project Structure

```
ai-blog-generator/
├── app.py                 # Main Flask application with enhanced API endpoints
├── requirements.txt       # Python dependencies
├── generate_daily.sh      # Cron job script for scheduled generation
├── .env                   # Environment variables (create this file)
├── static/               # Static assets
│   ├── style.css         # Enhanced CSS styles
│   └── script.js         # Frontend JavaScript
├── templates/            # HTML templates
│   ├── index.html        # Main blog generation interface
│   ├── scheduler.html    # NEW: Advanced scheduling interface
│   └── blogs.html        # NEW: Blog management and viewing page
├── utils/                # Python modules
│   ├── ai_generator.py   # OpenAI GPT integration
│   ├── seo_fetcher.py    # SEO metrics fetcher (mock data)
│   └── scheduler.py      # Enhanced scheduling utilities
└── generated_content/    # Generated blog posts
    ├── manual_blog_*.json     # Manually generated blogs
    └── scheduled_blog_*.json  # Scheduled blogs
```

## Prerequisites

- Python 3.13 or higher
- OpenAI API key
- macOS, Linux, or WSL (for cron functionality)
- Modern web browser

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd ai-blog-generator-interview-ShanmukhaK
```

### 2. Install Dependencies

Create and activate a virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

Install required packages:
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file in the root directory:
```env
OPENAI_API_KEY=your_openai_api_key_here
FLASK_APP=app.py
FLASK_ENV=development
PORT=5001
```

## Running the Application

### Start the Flask Server

```bash
python3 app.py
```

The server will start on `http://localhost:5000` by default. You can access:
- **Main Interface**: `http://localhost:5000/`
- **Scheduler**: `http://localhost:5000/scheduler`
- **Blog Management**: `http://localhost:5000/blogs`

### Using the Web Interface

#### 🏠 **Main Page** (`/`)
1. Open `http://localhost:5000` in your browser
2. Enter a keyword in the input field
3. Click "Generate Blog Post"
4. View the generated content, including:
   - Blog title and meta description
   - SEO metrics (search volume, difficulty, CPC)
   - Full blog content with affiliate link placeholders

#### ⏰ **Scheduler Page** (`/scheduler`)
1. Navigate to the Scheduler from the main menu
2. Fill in the scheduling form:
   - **Blog Topic/Keyword**: Your target keyword
   - **Time Settings**: Minute, hour, day, month
3. Click "Schedule Blog Generation"
4. View scheduled jobs in the calendar and list
5. Monitor job execution and delete jobs as needed

#### 📚 **Generated Blogs Page** (`/blogs`)
1. Navigate to "Generated Blogs" from the main menu
2. View all your generated blogs with:
   - **Statistics Dashboard**: Total, scheduled, manual, and today's blogs
   - **Filtering Options**: By type (scheduled/manual) and keyword search
   - **Sorting Options**: By date (newest/oldest) or keyword
3. Click "👁️ View" to see full blog content in a modal
4. Use "🗑️ Delete" to remove unwanted blogs
5. Use "🔄 Refresh" to update the blog list

## API Documentation

### Blog Generation Endpoints

#### Generate Blog
**Endpoint**: `/generate`  
**Methods**: GET, POST  
**Parameters**:
- `keyword` (required): The target keyword for blog generation

**Example**: `/generate?keyword=wireless+earbuds`

**Response Format**:
```json
{
    "keyword": "wireless earbuds",
    "seo_metrics": {
        "search_volume": 1000,
        "keyword_difficulty": 45.5,
        "avg_cpc": 2.50
    },
    "blog": {
        "title": "Blog post title",
        "meta_description": "SEO meta description",
        "content": "Full blog post content"
    },
    "saved_to": "manual_blog_20240605_123456.json"
}
```

### Blog Management Endpoints

#### Get All Blogs
**Endpoint**: `/api/blogs`  
**Method**: GET  
**Description**: Retrieve all generated blogs with metadata

#### Get Specific Blog
**Endpoint**: `/api/blogs/<filename>`  
**Method**: GET  
**Description**: Get details of a specific blog file

#### Delete Blog
**Endpoint**: `/api/blogs/<filename>`  
**Method**: DELETE  
**Description**: Delete a specific blog file

### Scheduling Endpoints

#### Get Scheduled Jobs
**Endpoint**: `/api/jobs`  
**Method**: GET  
**Description**: Retrieve all scheduled cron jobs

#### Create Scheduled Job
**Endpoint**: `/api/jobs`  
**Method**: POST  
**Body**:
```json
{
    "keyword": "target keyword",
    "minute": 0,
    "hour": 9,
    "day": 15,
    "month": 12
}
```

#### Delete Scheduled Job
**Endpoint**: `/api/jobs/<job_id>`  
**Method**: DELETE  
**Description**: Remove a scheduled job

## Automated Content Generation

### Setting up the Cron Job

1. Ensure the script is executable:
```bash
chmod +x generate_daily.sh
```

2. Add to crontab (runs daily at 9 AM):
```bash
crontab -e
```

Add the following line (the path will be automatically set during installation):
```
0 9 * * * cd "/path/to/ai-blog-generator-interview-ShanmukhaK" && ./generate_daily.sh >> /tmp/blog_generator.log 2>&1
```

### Generated Content

- All generated content is saved in the `generated_content` directory
- Files are named using the format: `blog_YYYYMMDD_HHMMSS.json`
- Each file contains:
  - Blog content
  - SEO metrics
  - Generation metadata
  - Timestamp

### Monitoring and Logs

- Web interface activity: Check the Flask application output
- Cron job execution: Check `/tmp/blog_generator.log`
- Generated content: Look in `generated_content/` directory

## Testing

### Manual Testing

1. Test the API endpoint:
```bash
curl "http://localhost:5000/generate?keyword=your+keyword"
```

2. Test the cron script:
```bash
./generate_daily.sh
```

3. Verify content generation:
```bash
ls -l generated_content/
```

### Automated Generation Testing

1. Check if cron job is installed:
```bash
crontab -l
```

2. Monitor the log file:
```bash
tail -f /tmp/blog_generator.log
```

## Troubleshooting

### Common Issues

1. **Python Command Not Found**
   - Use `python3` instead of `python`
   - Ensure Python 3.13+ is installed
   - Verify PATH includes Python installation

2. **Flask App Not Running**
   - Check if port 5000 is available
   - Ensure virtual environment is activated
   - Verify all dependencies are installed

3. **Cron Job Not Running**
   - Check `/tmp/blog_generator.log` for errors
   - Verify script permissions (should be executable)
   - Ensure paths in crontab are absolute
   - **macOS Users**: Grant Terminal full disk access in System Preferences

4. **Scheduled Blogs Not Appearing**
   - Check the `/blogs` page and filter by "Scheduled" type
   - Refresh the page to reload blog list
   - Verify Flask server is running when cron jobs execute
   - Check `generated_content/` directory for `scheduled_blog_*.json` files

5. **Blog Management Issues**
   - Clear browser cache if blogs don't load
   - Check browser console for JavaScript errors
   - Ensure all API endpoints are accessible
   - Verify file permissions in `generated_content/` directory

### Error Logs

- Application errors: Flask debug output
- Cron job errors: `/tmp/blog_generator.log`
- System errors: System log (`/var/log/syslog` or equivalent)

## Security Considerations

1. **API Keys**
   - Store in `.env` file
   - Never commit to version control
   - Rotate regularly

2. **File Permissions**
   - Keep `.env` readable only by application user
   - Ensure log files have appropriate permissions
   - Protect generated content directory

3. **Network Security**
   - Application runs on localhost by default
   - Implement authentication if exposing to network
   - Use HTTPS if deploying to production

## Maintenance

1. **Regular Tasks**
   - Monitor disk usage in `generated_content/`
   - Check log files for errors
   - Verify cron job execution

2. **Updates**
   - Keep dependencies updated
   - Monitor OpenAI API changes
   - Update affiliate links as needed

## Support

For issues and support:
1. Check the troubleshooting section
2. Review the logs
3. Contact the development team

## License

This project is licensed under the MIT License - see the LICENSE file for details. 