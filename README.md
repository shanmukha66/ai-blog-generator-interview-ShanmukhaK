# AI Blog Post Generator

This is a Flask-based application that generates SEO-optimized blog posts using Groq's deepseek-r1-distill-llama-70b model. It includes features for keyword research (mocked) and automated daily post generation.

## Features

- Generate blog posts from keywords via REST API
- Mock SEO metrics (search volume, keyword difficulty, CPC)
- Automated daily blog post generation
- Affiliate link placeholder integration
- Markdown-formatted output

## Prerequisites

- Python 3.8+
- Groq API key
- Virtual environment (recommended)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/ai-blog-generator-interview-yourname.git
   cd ai-blog-generator-interview-yourname
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the project root:
   ```
   GROQ_API_KEY=your_groq_api_key_here
   DAILY_KEYWORD=wireless earbuds
   FLASK_APP=app.py
   FLASK_ENV=development
   ```

## Usage

1. Start the Flask application:
   ```bash
   python app.py
   ```

2. Generate a blog post via API:
   ```bash
   curl "http://localhost:5000/generate?keyword=wireless%20earbuds"
   ```

3. Check application health:
   ```bash
   curl "http://localhost:5000/health"
   ```

## Automated Daily Posts

The application includes two options for automated daily post generation:

### 1. Built-in APScheduler (Default)
- Already configured in `app.py`
- Runs automatically at midnight (00:00)
- Saves posts to `generated_posts/` directory
- No additional setup required

### 2. Crontab Alternative
If you prefer using crontab:

1. Create a shell script `generate_daily.sh`:
   ```bash
   #!/bin/bash
   curl "http://localhost:5000/generate?keyword=wireless%20earbuds" > "$(date +%Y%m%d)_post.json"
   ```

2. Make it executable:
   ```bash
   chmod +x generate_daily.sh
   ```

3. Add to crontab (runs at midnight):
   ```bash
   0 0 * * * /path/to/generate_daily.sh
   ```

## Output Format

Generated posts are saved as JSON files containing:
- Keyword information
- SEO metrics
- Generated content (in Markdown)
- Affiliate links
- Timestamp

## Directory Structure

```
.
├── README.md
├── requirements.txt
├── app.py                 # Main Flask application
├── ai_generator.py        # OpenAI integration
├── seo_fetcher.py        # SEO metrics mock
├── generated_posts/      # Directory for saved posts
└── .env                  # Configuration (not in repo)
```

## Development

- The application uses mock SEO data for demonstration
- Affiliate links are generated as placeholders
- The AI model used is Groq's deepseek-r1-distill-llama-70b for high-quality content generation

## License

MIT 