import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import datetime
import random
import cv2
import numpy as np
from Replys import *
from datetime import datetime
import google.generativeai as genai
import PIL.Image
from googletrans import Translator

recognizer = sr.Recognizer()
MICROPHONE_INDEX = 1

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

mode = "listening"

def say(audio, speed_adjustment=0):
    engine.say(audio)
    engine.runAndWait()
    rate = engine.getProperty('rate')   # Get the current rate
    new_rate = rate + speed_adjustment
    engine.setProperty('rate', new_rate)  # Adjust rate for slower speech

def listen():
    with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio, language='en-pk')
            print(f"You said: {text}")
            return text

        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
        return ""

def process_query(query):

    api_key = os.environ.get("API_KEY")
    if api_key is None:
        raise ValueError("API_KEY environment variable not set")

    genai.configure(api_key=api_key)

    model = genai.GenerativeModel(model_name="gemini-1.5-flash")
    response = model.generate_content(query)

    MAX_LENGTH = 500  # Adjust this value as needed

    # Provide a brief description if the response is too long
    if len(response.text) > MAX_LENGTH:
        brief_response = response.text[:MAX_LENGTH] + '...'  # Truncate and add ellipsis
    else:
        brief_response = response.text

    print(brief_response)
    say(brief_response)

    # Add more sites
    sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
    for site in sites:
        if f"Open {site[0]}".lower() in query.lower():
            say(f"Opening {site[0]} sir...")
            webbrowser.open(site[1])

    # Add a feature to play a specific song
    if "open music" in query:
        musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
        os.system(f"open {musicPath}")

    elif "what is the time" in query:
        say(random.choice(answers_8))
        hour = datetime.datetime.now().strftime("%H")
        min = datetime.datetime.now().strftime("%M")
        say(f"Sir time is {hour} {min}")

    elif "open facetime".lower() in query.lower():
        os.system(f"open /System/Applications/FaceTime.app")

    elif "open pass".lower() in query.lower():
        os.system(f"open /Applications/Passky.app")

    elif "Jarvis Quit".lower() in query.lower():
        exit()

    elif "reset chat".lower() in query.lower():
        chatStr = ""

if __name__ == '__main__':
    print('Welcome to Jarvis')
    say("Welcome to Jarvis")

    while True:
        try:
            if mode == "listening":
                query = listen()
            else:
                query = input("Enter your command: ")

            if "switch to text mode" in query.lower():
                mode = "text"
                print("Switched to text mode.")
                say("Switched to text mode.")

            elif "switch to listening mode" in query.lower():
                mode = "listening"
                print("Switched to listening mode.")
                say("Switched to listening mode.")

            else:
                process_query(query)

        except sr.WaitTimeoutError:
            # Handle the timeout error and continue listening
            print("Listening...")
            continue