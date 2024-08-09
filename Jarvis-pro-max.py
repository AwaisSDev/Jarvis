# -*- coding: utf-8 -*-

import sys
import threading
import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import datetime
import random
import uuid
import smtplib
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from groq import Groq
from PyQt5 import QtCore, QtGui, QtWidgets

# Initialize the recognizer and text-to-speech engine
recognizer = sr.Recognizer()
MICROPHONE_INDEX = 1
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

mode = "text"  # Set default mode to text
bypass_words = ["!", "$", "^", "&", "*", "/", "asteras", "😊"]
known_face_encodings = []
known_face_names = []

history = []  # Initialize history

def say(audio, speed_adjustment=0):
    # Handle specific replacements for pronunciation
    replacements = {
        "Awais": "ah-WASS",  # Pronunciation replacement
        # Add more replacements as needed
    }

    for old_word, new_word in replacements.items():
        audio = audio.replace(old_word, new_word)

    sentences = audio.split(". ")
    for sentence in sentences:
        words = sentence.split()
        filtered_words = [word for word in words if word.lower() not in bypass_words]
        filtered_sentence = " ".join(filtered_words)

        if filtered_sentence:
            #engine.say(filtered_sentence)
           # engine.runAndWait()
            #rate = engine.getProperty('rate')
           # new_rate = rate + speed_adjustment
           # engine.setProperty('rate', new_rate)
            tts_thread = threading.Thread(target=run_tts, args=(filtered_sentence, speed_adjustment))
            tts_thread.start()
        else:
            print(f"Bypassed sentence: {sentence}")

def run_tts(text, speed_adjustment):
    engine = pyttsx3.init('sapi5')
    rate = engine.getProperty('rate')
    new_rate = rate + speed_adjustment
    engine.setProperty('rate', new_rate)
    engine.say(text)
    engine.runAndWait()

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

def send_email(subject, body, to_email):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    from_email = 'mawais9171@gmail.com'
    password = 'ipau ainb zjjt ajmk'

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        print('Email sent successfully!')
        say('Email sent successfully!')
    except Exception as e:
        print(f'Error: {e}')
        say(f'Error: {e}')
    finally:
        server.quit()

def face_recognition():
    video_capture = cv2.VideoCapture(0)  # Use the default camera

    while True:
        ret, frame = video_capture.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        rgb_frame = frame[:, :, ::-1]  # Convert BGR to RGB

        # Find all face locations and encodings in the frame
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)

        # Display the resulting image
        cv2.imshow('Video', frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

def create_program_file(code):
    filename = f"generated_program_{uuid.uuid4().hex}.py"
    with open(filename, "w") as file:
        file.write(code)
    print(f"Program created: {filename}")

def extract_code(response_text):
    print(response_text)
    lines = response_text.split("\n")
    code_lines = []
    in_code_block = False
    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            code_lines.append(line)
    return "\n".join(code_lines)

def process_query(query):
    if not query.strip():  # Check if query is empty or just whitespace
        say("The query cannot be empty. Please provide a valid command.")
        return ""

    api_key = os.environ.get("GROQ_API_KEY")
    if api_key is None:
        raise ValueError("GROQ_API_KEY environment variable not set")

    client = Groq(api_key=api_key)
    model = "mixtral-8x7b-32768"

    # Check the context for relevant previous queries
    relevant_context = ""
    if history:
        last_query = history[-1]['query']
        last_response = history[-1]['response']
        relevant_context = f"Earlier you asked about '{last_query}', and I responded with '{last_response}'. "

    if "send email" in query.lower():
        say("Who is the recipient of the email?")
        to_email = listen() if mode == "listening" else input("Enter the recipient email address: ")
        
        say("What is the subject of the email?")
        subject = listen() if mode == "listening" else input("Enter the subject of the email: ")
        
        say("What is the body of the email?")
        body = listen() if mode == "listening" else input("Enter the body of the email: ")
        
        if to_email and subject and body:
            send_email(subject, body, to_email)
        else:
            say("Sorry, I didn't catch that. Please try again.")
        return ""

    elif "make me a program" in query.lower():
        say("What should the program be about?")
        if mode == "listening":
            description = listen()
        else:
            description = input("Enter the program description: ")
        if description:
            prompt = f"{relevant_context}Generate a Python program that {description}"
            try:
                chat_completion = client.chat.completions.create(
                    messages=[{"role": "user", "content": prompt}],
                    model=model,
                )
                response_text = chat_completion.choices[0].message.content
                code = extract_code(response_text)
                create_program_file(code)
                return response_text  # Return response text for history
            except Exception as e:
                print(f"An error occurred: {e}")
                say("An error occurred while generating the program.")
                return ""
        else:
            say("Sorry, I didn't catch that. Please try again.")
            return ""
    else:
        try:
            prompt = f"{relevant_context}{query}"
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=model,
            )
            response_text = chat_completion.choices[0].message.content
            MAX_LENGTH = 300  # Shortened for brevity

            # Define your replacements here
            replacements = {
                "trained by Groq.": "trained by Awais",
                "trained by Groq": "trained by Awais",
                # Add more replacements as needed
            }

            # Apply replacements
            for old_word, new_word in replacements.items():
                response_text = response_text.replace(old_word, new_word)

            brief_response = response_text[:MAX_LENGTH] + '...' if len(response_text) > MAX_LENGTH else response_text

            print(brief_response)
            say(brief_response)
            return brief_response  # Return brief response for history
        except Exception as e:
            print(f"An error occurred: {e}")
            say("An error occurred while processing your query.")
            return ""

def update_history(query, response):
    history.append({"query": query, "response": response})
    

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1689, 1045)

        # Set frameless window
        MainWindow.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Full-screen background image
        self.backgroundLabel = QtWidgets.QLabel(self.centralwidget)
        self.backgroundLabel.setGeometry(QtCore.QRect(0, 0, MainWindow.width(), MainWindow.height()))
        self.backgroundLabel.setText("")
        self.backgroundLabel.setPixmap(QtGui.QPixmap("F:/images/HD-wallpaper-black-solid-plain-colors-dark-color-screen.jpg"))
        self.backgroundLabel.setScaledContents(True)
        self.backgroundLabel.setObjectName("backgroundLabel")

        # Create custom title bar
        self.customTitleBar = QtWidgets.QWidget(self.centralwidget)
        self.customTitleBar.setGeometry(QtCore.QRect(0, 0, MainWindow.width(), 30))
        self.customTitleBar.setStyleSheet("""
            background-color: rgba(0, 0, 0, 0.5);
        """)
        self.customTitleBar.setObjectName("customTitleBar")

        # Add minimize, maximize, and close buttons
        self.minimizeButton = QtWidgets.QPushButton(self.customTitleBar)
        self.maximizeButton = QtWidgets.QPushButton(self.customTitleBar)
        self.closeButton = QtWidgets.QPushButton(self.customTitleBar)

        # Load icon images
        self.minimizeIcon = QtGui.QIcon("F:/images/3.png")
        self.maximizeIcon = QtGui.QIcon("F:/images/1.png")
        self.closeIcon = QtGui.QIcon("F:/images/2.png")

        # Set icons
        self.minimizeButton.setIcon(self.minimizeIcon)
        self.maximizeButton.setIcon(self.maximizeIcon)
        self.closeButton.setIcon(self.closeIcon)

        # Style buttons
        self.minimizeButton.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                border: none;
                border-radius: 15px;  # Circular shape
                font-size: 16px;
                width: 90px;
                height: 90px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)
        self.maximizeButton.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                border: none;
                border-radius: 15px;  # Circular shape
                font-size: 16px;
                width: 90px;
                height: 90px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: lightgray;
            }
        """)
        self.closeButton.setStyleSheet("""
            QPushButton {
                background-color: red;
                color: white;
                border: none;
                border-radius: 15px;  # Circular shape
                font-size: 16px;
                width: 90px;
                height: 90px;
                padding: 0;
            }
            QPushButton:hover {
                background-color: darkred;
            }
        """)

        # Layout for buttons
        buttonLayout = QtWidgets.QHBoxLayout()
        buttonLayout.addStretch()
        buttonLayout.addWidget(self.minimizeButton)
        buttonLayout.addWidget(self.closeButton)
        buttonLayout.setContentsMargins(0, 0, 0, 0)
        buttonLayout.setSpacing(0)
        self.customTitleBar.setLayout(buttonLayout)

        # Connect buttons to functionality
        self.minimizeButton.clicked.connect(MainWindow.showMinimized)
        self.maximizeButton.clicked.connect(self.toggle_maximize_window)
        self.closeButton.clicked.connect(MainWindow.close)

        # Additional content
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(440, 40, 800, 600))
        self.label_3.setText("")
        self.label_3.setScaledContents(True)
        self.label_3.setObjectName("label_3")

        self.movie = QtGui.QMovie("F:/images/circle.gif")
        self.label_3.setMovie(self.movie)
        self.movie.start()

        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(500, 950, 600, 50))
        self.textEdit.setObjectName("textEdit")
        self.textEdit.setStyleSheet("""
            QTextEdit {
                font-size: 18px;
                border: 2px solid gray;
                border-radius: 5px;
                padding: 5px;
                background-color: rgba(255, 255, 255, 0.8);
            }
        """)

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1120, 950, 100, 50))
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setText("Submit")
        self.pushButton.clicked.connect(self.on_click)
        self.pushButton.setStyleSheet("""
            QPushButton {
                background-color: gray;
                color: white;
                border: none;
                padding: 10px;
                font-size: 16px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: white;
                color: gray;
            }
        """)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Jarvis"))

    def toggle_maximize_window(self):
        if MainWindow.isMaximized():
            MainWindow.showNormal()
        else:
            MainWindow.showMaximized()

    def on_click(self):
        command = self.textEdit.toPlainText()
        self.process_command(command)

    def process_command(self, command_text):
        response = process_query(command_text)
        update_history(command_text, response)
        self.textEdit.clear()

    def say(self, audio):
        tts_thread = threading.Thread(target=run_tts, args=(audio, 0))
        tts_thread.start()
class MainThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        self.say("Welcome to Jarvis")

    def say(self, audio):
        engine = pyttsx3.init()
        engine.say(audio)
        engine.runAndWait()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()

    startExecution = MainThread()
    startExecution.start()

    sys.exit(app.exec_())

#made by awais siddique