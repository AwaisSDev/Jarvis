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
from datetime import datetime

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

import time
def get_time():
    # Get the current time
    now = datetime.now()

    # Format the time in 12-hour format with AM/PM
    formatted_time = now.strftime("%I %M %p").lstrip('0')

    return formatted_time
def get_time2():
    # Get the current time
    now = datetime.now()

    # Format the time in 12-hour format with AM/PM
    formatted_time = now.strftime("%I:%M %p")

    return formatted_time
def face_recognition_system():
    say("Recognizing face")
    # Load the pre-trained Haar Cascade XML file for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # Initialize the recognizer
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    # Load your trained model
    recognizer.read('Jarvis/trainer/trainer.yml')

    authorized_labels = [1]  # Replace with your actual authorized labels
    confidence_threshold = 50  # Adjust based on your model's performance
    face_change_time_limit = 15  # Time in seconds

    # Open a video capture
    cap = cv2.VideoCapture(0)  # Use 0 for the default webcam

    access_granted = False
    last_authorized_time = time.time()  # Time when the last authorized face was detected

    while not access_granted:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Convert frame to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Detect faces
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        authorized_face_detected = False

        for (x, y, w, h) in faces:
            # Draw a rectangle around the face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            
            # Get the face region
            face = gray[y:y+h, x:x+w]

            # Predict the label of the face
            label, confidence = recognizer.predict(face)
            
            # Display the label and confidence
            cv2.putText(frame, f'Label: {label} - Confidence: {confidence:.2f}', (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
            
            # Check if the label is authorized and confidence is below the threshold
            if label in authorized_labels and confidence < confidence_threshold:
                authorized_face_detected = True
                access_granted = True
                t = (f"Access Granted. Welcome Sir, the time is", get_time())
                print(f"Access Granted. Welcome Sir the time is",get_time2())
                say(t)
                break

        if not authorized_face_detected:
            # Check if a different face has been detected for more than the time limit
            if time.time() - last_authorized_time > face_change_time_limit:
                print("Access Denied. Exiting due to different face detected.")
                say("Access Denied. Exiting due to different face detected.")
                cap.release()
                cv2.destroyAllWindows()
                exit()

        # Update the last authorized time if an authorized face is detected
        if authorized_face_detected:
            last_authorized_time = time.time()

        # Display the resulting frame
        cv2.imshow('Face Recognition', frame)

        # Exit if user presses 'q'
        if cv2.waitKey(10) & 0xFF == ord('q'):
            print("Access Denied. Exiting...")
            say("Access Denied. Exiting...")
            cap.release()
            cv2.destroyAllWindows()
            exit()

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    print('Welcome to Jarvis')
    say("Welcome to Jarvis")

    face_recognition_system()

    while True:
        try:
            print("Listening...")
            query = listen()
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
   
        except sr.WaitTimeoutError:
            # Handle the timeout error and continue listening
            print("listening")
            continue