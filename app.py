import os
import importlib.util

from flask import Flask, request, jsonify, render_template
import logging
from dotenv import load_dotenv

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

# Import the deployment version of main
spec = importlib.util.spec_from_file_location("main_deploy", "main-deploy.py")
main_deploy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(main_deploy)
processCommand = main_deploy.processCommand

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')


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
