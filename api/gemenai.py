import os
import logging
from google import genai

logger = logging.getLogger(__name__)

class Gemenai:
    def Genai(self, command):
        try:
            api_key = os.getenv('GOOGLE_API_KEY')
            if not api_key:
                return "Error: GOOGLE_API_KEY environment variable not set"
            client = genai.Client(api_key=api_key)
            response = client.models.generate_content(
                model="gemini-2.0-flash", contents=command
            )
            if response and response.text:
                return response.text
            else:
                return "No response from the server."
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            return None
