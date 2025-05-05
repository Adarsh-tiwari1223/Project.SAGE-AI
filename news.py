import requests

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
            print(f"Error fetching news: {e}")
            return []

    def read_news(self):
        """Fetch news and speak each headline consecutively."""
        articles = self.fetch_news()
        if not articles:
            print("No articles to display.")
            return

        print(f"\nFound {len(articles)} news articles. Reading now...")
        
        # Read each news headline one by one
        for i, article in enumerate(articles, 1):
            title = article.get('title', 'No Title Available')
            print(f"\nNews {i}: {title}")
            self.speak(title)  # This will now wait for each speech to complete



