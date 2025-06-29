import speech_recognition as sr
import webbrowser
import pyttsx3
import api.musicLibrary as musicLibrary
import asyncio
import os
from dotenv import load_dotenv
from api.Gemini import Gemenai
from api.news import NewsSpeaker
from api.Weather import WeatherFetcher

# Load environment variables
try:
    load_dotenv()
except Exception as e:
    print(f"Warning: Could not load .env file: {e}")

recognizer = sr.Recognizer()
engine = pyttsx3.init()
weather_fetcher = WeatherFetcher()


def speak(text):
    engine.say(text)
    try:
        engine.runAndWait()
    except RuntimeError:
        pass


def aiProcess(command):
    g = Gemenai()
    return g.Genai(command)


def listen():
    """Listens for a voice command and returns it as text."""
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)  # Reduce noise
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=3)
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("I'm having trouble connecting to the voice service.")
            return None


async def get_weather_response(city):
    """Get weather response for a city."""
    return await weather_fetcher.get_weather(city)


def processCommand(c):
    if "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
        return "Opening YouTube..."
    elif "open google" in c.lower():
        webbrowser.open("https://google.co.in")
        return "Opening Google..."
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
            return f"Playing {song}..."
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


if __name__ == "__main__":
    speak("Initializing LUMEN...")
    
    while True:
        print("Waiting for wake word 'LUMEN'...")
        wake_word = listen()

        if wake_word == "LUMEN":
            speak("LUMEN activated. How can I assist?")
            command = listen()
            if command:
                print(f"Recognized Command: {command}")
                response = processCommand(command)
                print(response)
                speak(response)
