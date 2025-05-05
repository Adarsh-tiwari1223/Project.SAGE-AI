from flask import Flask, request, jsonify, render_template
from main import processCommand
from flask_cors import CORS
import asyncio
from Weather import WeatherFetcher
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS if frontend is separate
weather_fetcher = WeatherFetcher()


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
        
        if "weather" in message.lower():
            try:
                # Extract city name from message
                city = message.lower().replace("weather", "").replace("in", "").strip()
                if not city:
                    return jsonify({'response': "Please specify a city. For example: 'weather in London'"})
                
                # Run the async weather function
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(weather_fetcher.get_weather(city))
                loop.close()
                return jsonify({'response': response})
            except Exception as e:
                logger.error(f"Weather error: {str(e)}")
                return jsonify({'response': f"Error fetching weather: {str(e)}"})
        
        response = processCommand(message)
        logger.debug(f"Command response: {response}")
        return jsonify({'response': response})
        
    except Exception as e:
        logger.error(f"General error: {str(e)}")
        return jsonify({'response': f"Error processing request: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)
