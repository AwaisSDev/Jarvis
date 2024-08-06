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
bypass_words = ["!", "$", "^", "&", "*","**", "/", "asteras"]

def say(audio, speed_adjustment=0):
    sentences = audio.split(". ")
    for sentence in sentences:
        # Remove bypassed words from the sentence
        words = sentence.split()
        filtered_words = [word for word in words if word.lower() not in bypass_words]
        filtered_sentence = " ".join(filtered_words)
        
        if filtered_sentence:
            engine.say(filtered_sentence)
            engine.runAndWait()
            rate = engine.getProperty('rate')  # Get the current rate
            new_rate = rate + speed_adjustment
            engine.setProperty('rate', new_rate)  # Adjust rate for slower speech
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
    filename = f"generated_program_{uuid.uuid4().hex}.py"  # Generate a unique filename
    with open(filename, "w") as file:
        file.write(code)
    print(f"Program created: {filename}")
    say(f"Program created: {filename}")

def extract_code(response_text):
    """Extracts code from the AI response."""
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
        else:
            say("Sorry, I didn't catch that. Please try again.")
    else:
        response = model.generate_content(query)
        MAX_LENGTH = 500  # Adjust this value as needed

        if len(response.text) > MAX_LENGTH:
            brief_response = response.text[:MAX_LENGTH] + '...'  # Truncate and add ellipsis
        else:
            brief_response = response.text

        print(brief_response)
        say(brief_response)

        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "open music" in query:
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")

        elif "what is the time" in query:
            hour = datetime.datetime.now().strftime("%H")
            min = datetime.datetime.now().strftime("%M")
            say(f"Sir, the time is {hour}:{min}")

        elif "open facetime".lower() in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        elif "open pass".lower() in query.lower():
            os.system(f"open /Applications/Passky.app")

        elif "jarvis quit".lower() in query.lower():
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
            print("Listening...")
            continue
