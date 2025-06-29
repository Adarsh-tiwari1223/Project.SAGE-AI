# SAGE AI - Voice Assistant

A Python-based AI voice assistant with web interface capabilities.

## Features

- Voice command recognition
- AI-powered responses using Google Gemini
- Weather information
- News headlines
- Music playback
- Web browser control
- Web interface for text-based interaction

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the root directory with your API keys:
```
GOOGLE_API_KEY=your_google_api_key_here
NEWS_API_KEY=your_news_api_key_here
```

3. Run the application:
   - For voice interface: `python main.py`
   - For web interface: `python app.py`

## Project Structure

- `main.py` - Main voice assistant application
- `app.py` - Flask web server for web interface
- `api/` - API modules directory
  - `gemenai.py` - Google Gemini AI integration
  - `news.py` - News API integration
  - `Weather.py` - Weather API integration
  - `musicLibrary.py` - Music library configuration
- `templates/` - HTML templates
- `static/` - CSS and JavaScript files

## Recent Cleanup

The following unnecessary code has been removed:
- Unused `read_news()` method in `news.py`
- Unnecessary WAV file creation/deletion in voice recognition
- Duplicate weather handling logic in `app.py`
- Unused `styles.css` file in root directory
- Unused dependencies in `requirements.txt`
- Hardcoded API keys moved to environment variables
- Replaced print statements with proper logging
- Fixed file structure and import paths
- Removed unnecessary files (`.blackboxrules`, `vercel.jason`)

## Security

API keys are now stored in environment variables and the application will show appropriate error messages if they are not set.

## Deployment

The project includes `vercel.json` for deployment on Vercel platform. 