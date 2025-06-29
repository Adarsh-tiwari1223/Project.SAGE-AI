import python_weather
import asyncio

class WeatherFetcher:
    def __init__(self, unit=python_weather.METRIC):
        """Initialize the weather fetcher with the specified unit (default: Celsius)."""
        self.unit = unit

    async def get_weather(self, city: str) -> str:
        """Fetch weather for the specified city and return a formatted message."""
        try:
            async with python_weather.Client(unit=self.unit) as client:
                weather = await client.get(city)

                if weather:
                    return f"{city}'s weather is {weather.temperature}°C"
                else:
                    return f"Sorry, no weather data available for {city}"
        except Exception as e:
            return f"Error fetching weather: {e}"


