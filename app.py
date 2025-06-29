import os
import asyncio
from flask import Flask, request, jsonify, render_template
import logging
from dotenv import load_dotenv
from api.gemenai import Gemenai
from api.news import NewsSpeaker
from api.Weather import WeatherFetcher
import api.musicLibrary as musicLibrary

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')

# Initialize services
weather_fetcher = WeatherFetcher()

def aiProcess(command):
    g = Gemenai()
    return g.Genai(command)

async def get_weather_response(city):
    """Get weather response for a city."""
    return await weather_fetcher.get_weather(city)

def processCommand(c):
    if "open youtube" in c.lower():
        return "YouTube would open in a browser environment. In web mode, you can visit https://youtube.com"
    elif "open google" in c.lower():
        return "Google would open in a browser environment. In web mode, you can visit https://google.co.in"
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = musicLibrary.music.get(song)
        if link:
            return f"Playing {song}... You can visit: {link}"
        else:
            return f"Sorry, I couldn't find {song} in the library."
    elif "news" in c.lower():
        try:
            news_api_key = os.getenv("NEWS_API_KEY")
            if not news_api_key:
                return "News API key not set. Please configure NEWS_API_KEY in your environment."

            news_speaker = NewsSpeaker(news_api_key)
            articles = news_speaker.fetch_news()
            if articles:
                # Format the news response for the web interface
                response = "📰 Latest News Headlines:\n\n"
                for i, article in enumerate(articles, 1):
                    title = article.get('title', 'No Title Available')
                    response += f"{i}. {title}\n"
                return response
            else:
                return "Sorry, I couldn't fetch the news at the moment."
        except Exception as e:
            return f"Error fetching news: {str(e)}"
    elif "weather" in c.lower():
        try:
            # Extract city name from command
            city = c.lower().replace("weather", "").replace("in", "").strip()
            if not city:
                return "Please specify a city. For example: 'weather in London'"

            # Run the async weather function
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(get_weather_response(city))
            loop.close()
            return response
        except Exception as e:
            return f"Error fetching weather: {str(e)}"
    elif c.lower() in ["stop", "exit", "goodbye","close"]:
        return "Goodbye! Have a great day!"
    else:
        output = aiProcess(c)
        return output

# Route to render index.html
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    try:
        data = request.get_json()
        if not data:
            logger.error("No JSON data received")
            return jsonify({'response': "Error: No data received"}), 400
            
        message = data.get('message', '')
        if not message:
            logger.error("No message in request")
            return jsonify({'response': "Error: No message provided"}), 400
        
        logger.debug(f"Received message: {message}")
        
        response = processCommand(message)
        logger.debug(f"Command response: {response}")
        return jsonify({'response': response})
        
    except Exception as e:
        logger.error(f"General error: {str(e)}")
        return jsonify({'response': f"Error processing request: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
