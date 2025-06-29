import python_weather
import asyncio
import os

class WeatherFetcher:
    def __init__(self, unit=python_weather.METRIC):
        """Initialize the weather fetcher with the specified unit (default: Celsius)."""
        self.unit = unit

    async def get_weather(self, city: str) -> str:
        """Fetch weather for the specified city and return a formatted message."""
        try:
            # Set event loop policy for Windows compatibility
            if os.name == 'nt':
                asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
            
            async with python_weather.Client(unit=self.unit) as client:
                weather = await client.get(city)

                if weather:
                    return f"{city}'s weather is {weather.temperature}°C"
                else:
                    return f"Sorry, no weather data available for {city}"
        except Exception as e:
            return f"Error fetching weather: {e}"


