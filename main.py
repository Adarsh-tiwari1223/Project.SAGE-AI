import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
import sys
from google import genai
from gemenai import Gemenai
from news import NewsSpeaker
from newsdataapi import NewsDataApiClient

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "pub_7718740c4bb47ca5e0f8c705a798cf2f1a3f2"


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


def processCommand(c):
    if "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open google" in c.lower():
        webbrowser.open("https://google.co.in")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ", 1)[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
        else:
            speak(f"Sorry, I couldn't find {song} in the library.")
    elif "news" in c.lower():
        try:
            news_speaker = NewsSpeaker(newsapi)
            news_speaker.read_news()
            print("All news has been read. Do you need anything else?")
            speak("All news has been read. Do you need anything else?")
            # Wait for user response after news
            response = listen()
            if response:
                processCommand(response)
            else:
                print("No response received. Returning to wake word detection.")
        except Exception as e:
            speak("Error fetching news.")
            print("Error fetching news:", e)
    elif c.lower() in ["stop", "exit", "goodbye"]:
        speak("Goodbye! Have a great day!")
        sys.exit()
    else:
        output = aiProcess(c)
        print(output)
        speak(output)


if __name__ == "__main__":
    speak("Initializing Jarvis...")
    
    while True:
        print("Waiting for wake word 'Jarvis'...")
        wake_word = listen()

        if wake_word == "jarvis":
            speak("Jarvis activated. How can I assist?")
            command = listen()
            if command:
                print(f"Recognized Command: {command}")
                processCommand(command)
