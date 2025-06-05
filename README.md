# AI Blog Generator

An intelligent blog content generation system that leverages AI to create engaging and informative blog posts. This project demonstrates the integration of Python and OpenAI's capabilities to streamline the content creation process.

## Project Structure

```
.
├── app.py              # Main application file
├── requirements.txt    # Python dependencies
├── .env               # Environment variables (not tracked in git)
├── templates/         # HTML templates
├── static/           # Static assets (CSS, JS, images)
└── utils/            # Utility functions
```

## Features (Planned)

- AI-powered blog content generation
- Topic suggestion system
- Content optimization
- Export functionality

## Tech Stack

- Python 3.8+
- Flask web framework
- OpenAI API
- SQLite database

## Setup

1. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key

4. Run the application:
   ```bash
   python app.py
   ```

## License

MIT License 