import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import openai
import datetime
import random
import cv2
import numpy as np
from Replys import *

recognizer = sr.Recognizer()
MICROPHONE_INDEX = 1


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def say(audio):
    
    engine.say(audio)
    engine.runAndWait()
    rate = engine.getProperty('rate')   # Get the current rate
    engine.setProperty('rate', rate - 10)  # Adjust rate for slower speech

def listen():
    with sr.Microphone(device_index=MICROPHONE_INDEX) as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10)
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError:
            print("Could not request results from Google Speech Recognition service")
        return ""

def face_recognition_system():
# Load the pre-trained Haar Cascade XML file for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Initialize the recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load your trained model
    recognizer.read('trainer/trainer.yml')

    authorized_labels = [1]  # Replace with your actual authorized labels

# Open a video capture
    cap = cv2.VideoCapture(0)  # Use 0 for the default webcam

    while True:
    # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        access_granted = False

        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Get the face region
            face = gray[y:y+h, x:x+w]

            # Predict the label of the face
            label, confidence = recognizer.predict(face)
            
            # Display the label
            cv2.putText(frame, f'Label: {label}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Check if the label is authorized
            if label in authorized_labels:
                access_granted = True
                break

        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Grant access if authorized face is detected
        if access_granted:
            print("Access Granted. Welcome to Jarvis!")
            # Add code to grant access to Jarvis here
            os.system("taskkill /f /im Python.exe")
            break
        else:
            # Exit if no authorized face is detected
            if cv2.waitKey(10) & 0xFF == ord('q'):
                print("Access Denied. Exiting...")
                os.system("taskkill /f /im Python.exe")
                break

if __name__ == '__main__':
    print('Welcome to Jarvis Sir')
    say("Welcome to Jarvis Sir'")

    face_recognition_system()

    while True:
        print("Listening...")
        query = listen()
        # todo: Add more sites
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"],]
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])
        # todo: Add a feature to play a specific song
        if "open music" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")

        elif "hello" in query:
            say(random.choice(Hello))

        elif "how can I help you" in query:
            say(random.choice(answers_1))

        elif "what can you do" in query:
            say(random.choice(answers_2))

        elif "what is your name" in query:
            say(random.choice(answers_3))

        elif "how are you" in query:
            say(random.choice(answers_4))

        elif "where are you from" in query:
            say(random.choice(answers_5))

        elif "what is the weather like today" in query:
            say(random.choice(answers_6))

        elif "can you set a reminder" in query:
            say(random.choice(answers_7))

        elif "what is the time" in query:
            say(random.choice(answers_8))
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir time is {hour} {min}")

        elif "tell me a joke" in query:
            say(random.choice(answers_9))

        elif "can you play music" in query:
            say(random.choice(answers_10))

        elif "can you make a call" in query:
            say(random.choice(answers_11))

        elif "what is your purpose" in query:
            say(random.choice(answers_12))

        elif "how do you work" in query:
            say(random.choice(answers_13))

        elif "can you translate this" in query:
            say(random.choice(answers_14))

        elif "what is AI" in query:
            say(random.choice(answers_15))

        elif "what languages can you speak" in query:
            say(random.choice(answers_16))

        elif "can you help me with my homework" in query:
            say(random.choice(answers_17))

        elif "what is the meaning of life" in query:
            say(random.choice(answers_18))

        elif "what are you" in query:
            say(random.choice(answers_19))

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "Jarvis Quit".lower() in query.lower():
            exit()

        elif "reset chat".lower() in query.lower():
            chatStr = ""

        else:
            say("")




        # say(query)