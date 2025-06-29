import requests
import logging

logger = logging.getLogger(__name__)

class NewsSpeaker:
    def __init__(self, api_key):
        self.api_key = api_key

    def fetch_news(self):
        """Fetch news articles using the newsdata.io API."""
        url = (
            f"https://newsdata.io/api/1/news?apikey={self.api_key}"
            f"&q=daily%20news&country=in&language=en&category=top"
        )
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data.get("results", [])
                return articles[:5]  # Limit to 5 articles for better experience
            else:
                return []
        except Exception as e:
            logger.error(f"Error fetching news: {e}")
            return []



