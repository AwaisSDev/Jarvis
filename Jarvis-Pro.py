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
            engine.say(filtered_sentence)
            engine.runAndWait()
            rate = engine.getProperty('rate')
            new_rate = rate + speed_adjustment
            engine.setProperty('rate', new_rate)
        else:
            print(f"Bypassed sentence: {sentence}")

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
            prompt = f"Generate a Python program that {description}"
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
            chat_completion = client.chat.completions.create(
                messages=[{"role": "user", "content": query}],
                model=model,
            )
            response_text = chat_completion.choices[0].message.content
            MAX_LENGTH = 2000  # Shortened for brevity

            # Define your replacements here
            replacements = {
                "trained by Google.": "trained by Awais",
                "trained by Google": "trained by Awais",
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

if __name__ == '__main__':
    print('Welcome to Jarvis')
    say("Welcome to Jarvis")

    while True:
        try:
            if mode == "listening":
                query = listen()
            else:
                empty_lines = 0
                print("Enter your command (multi-line input allowed, end with two empty lines):")
                lines = []
                while empty_lines < 2:
                    line = input().strip()
                    if not line:
                        empty_lines += 1
                    else:
                        lines.append(line)
                        empty_lines = 0

                query = "\n".join(lines)

                if not query:  # Skip empty input
                    continue

            if query.lower() == "history":
                for entry in history:
                    print(f"Query: {entry['query']}")
                    print(f"Response: {entry['response']}")
            elif "tm" in query.lower():
                mode = "text"
                print("Switched to text mode.")
                say("Switched to text mode.")

            elif "lm" in query.lower():
                mode = "listening"
                print("Switched to listening mode.")
                say("Switched to listening mode.")
            
            elif query.lower() == "exit":
                say("Goodbye!")
                break

            elif query.lower().startswith("history"):
                for entry in history:
                    print(f"Query: {entry['query']}")
                    print(f"Response: {entry['response']}")

            else:
                response = process_query(query)
                if response:
                    update_history(query, response)

        except KeyboardInterrupt:
            print("\nInterrupted. Exiting...")
            say("Interrupted. Exiting...")
            break
