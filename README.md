# AI Blog Generator

An automated blog content generator that creates SEO-optimized blog posts based on provided keywords. The application uses OpenAI's API for content generation and provides SEO metrics for the target keywords.

## Features

- 🤖 AI-powered blog content generation
- 📊 SEO metrics for keywords (search volume, difficulty, CPC)
- 🎯 Automated affiliate link integration
- 📱 Responsive web interface
- ⏰ Automated daily content generation
- 💾 JSON-based content storage

## Project Structure

```
ai-blog-generator/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── generate_daily.sh      # Cron job script
├── .env                   # Environment variables
├── static/               # Static assets
│   ├── style.css         # CSS styles
│   └── script.js         # Frontend JavaScript
├── templates/            # HTML templates
│   └── index.html        # Main web interface
├── utils/                # Python modules
│   ├── ai_generator.py   # OpenAI integration
│   ├── seo_fetcher.py    # SEO metrics fetcher
│   └── scheduler.py      # Scheduling utilities
└── generated_content/    # Generated blog posts
    └── blog_*.json       # Generated content files
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

The server will start on `http://localhost:5001` (Port 5001 is used to avoid conflicts with AirPlay on macOS).

### Using the Web Interface

1. Open `http://localhost:5001` in your browser
2. Enter a keyword in the input field
3. Click "Generate Blog Post"
4. View the generated content, including:
   - Blog title
   - Meta description
   - SEO metrics
   - Full blog content with affiliate links

## API Documentation

### Generate Endpoint

**Endpoint**: `/generate`
**Method**: GET
**Parameters**:
- `keyword` (required): The target keyword for blog generation
  - Example: `/generate?keyword=wireless+earbuds`

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
    "saved_to": "blog_20240605_123456.json"
}
```

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
curl "http://localhost:5001/generate?keyword=your+keyword"
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
   - Check if port 5001 is available
   - Ensure virtual environment is activated
   - Verify all dependencies are installed

3. **Cron Job Not Running**
   - Check `/tmp/blog_generator.log` for errors
   - Verify script permissions (should be executable)
   - Ensure paths in crontab are absolute

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