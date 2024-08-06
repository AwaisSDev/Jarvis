import pyttsx3
import speech_recognition as sr
import os
import webbrowser
import datetime
import random
import uuid
import google.generativeai as genai

recognizer = sr.Recognizer()
MICROPHONE_INDEX = 1

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

mode = "text"  # Set default mode to text
bypass_words = ["!", "$", "^", "&", "*", "/", "asteras","","","","",""]

history = []  # Initialize history

def say(audio, speed_adjustment=0):
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

def create_program_file(code):
    filename = f"generated_program_{uuid.uuid4().hex}.py"
    with open(filename, "w") as file:
        file.write(code)
    print(f"Program created: {filename}")
    say(f"Program created: {filename}")

def extract_code(response_text):
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

    api_key = os.environ.get("API_KEY")
    if api_key is None:
        raise ValueError("API_KEY environment variable not set")

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(model_name="gemini-1.5-flash")

    if "make me a program" in query.lower():
        say("What should the program be about?")
        if mode == "listening":
            description = listen()
        else:
            description = input("Enter the program description: ")
        if description:
            prompt = f"Generate a Python program that {description}"
            response = model.generate_content(prompt)
            code = extract_code(response.text)
            create_program_file(code)
            return response.text  # Return response text for history
        else:
            say("Sorry, I didn't catch that. Please try again.")
            return ""
    else:
        response = model.generate_content(query)
        MAX_LENGTH = 200  # Shortened for brevity

        brief_response = response.text[:MAX_LENGTH] + '...' if len(response.text) > MAX_LENGTH else response.text

        print(brief_response)
        say(brief_response)
        return brief_response  # Return brief response for history

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
                print("Enter your command (multi-line input allowed, end with an empty line):")
                lines = []
                while True:
                    line = input().strip()
                    if not line:
                        break
                    lines.append(line)
                query = "\n".join(lines)

            if not query:  # Skip empty input
                continue

            if query.lower() == "history":
                for entry in history:
                    print(f"Query: {entry['query']}")
                    print(f"Response: {entry['response']}")
            elif "switch to text mode" in query.lower():
                mode = "text"
                print("Switched to text mode.")
                say("Switched to text mode.")

            elif "switch to listening mode" in query.lower():
                mode = "listening"
                print("Switched to listening mode.")
                say("Switched to listening mode.")

            else:
                response_text = process_query(query)
                update_history(query, response_text)

        except sr.WaitTimeoutError:
            print("Listening...")
            continue
