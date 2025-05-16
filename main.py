import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import asyncio
from gemenai import Gemenai
from news import NewsSpeaker
from Weather import WeatherFetcher
import wave


recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "pub_7718740c4bb47ca5e0f8c705a798cf2f1a3f2"
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
            # Using WAV format instead of AIFF
            audio = recognizer.listen(source, timeout=4, phrase_time_limit=3)
            # Save audio to WAV file temporarily
            with wave.open('temp_audio.wav', 'wb') as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(44100)
                wav_file.writeframes(audio.get_wav_data())
            return recognizer.recognize_google(audio).lower()
        except sr.UnknownValueError:
            return None
        except sr.RequestError:
            speak("I'm having trouble connecting to the voice service.")
            return None
        finally:
            # Clean up temporary file
            try:
                import os
                if os.path.exists('temp_audio.wav'):
                    os.remove('temp_audio.wav')
            except:
                pass


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
            news_speaker = NewsSpeaker(newsapi)
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
    speak("Initializing SAGE...")
    
    while True:
        print("Waiting for wake word 'SAGE'...")
        wake_word = listen()

        if wake_word == "SAGE":
            speak("SAGE activated. How can I assist?")
            command = listen()
            if command:
                print(f"Recognized Command: {command}")
                response = processCommand(command)
                print(response)
                speak(response)
