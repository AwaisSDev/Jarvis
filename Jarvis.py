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
bypass_words = ["!", "$", "^", "&", "*", "/", "asteras", "😊"]

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
            try:
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text'):
                    code = extract_code(response.text)
                    create_program_file(code)
                    return response.text  # Return response text for history
                else:
                    say("Failed to generate program. Please try again.")
                    return ""
            except Exception as e:
                print(f"An error occurred: {e}")
                say("An error occurred while generating the program.")
                return ""
        else:
            say("Sorry, I didn't catch that. Please try again.")
            return ""
    elif "create me a program" in query.lower():
        say("What should the program be about?")
        if mode == "listening":
            description = listen()
        else:
            description = input("Enter the program description: ")
        if description:
            prompt = f"Generate a Python program that {description}"
            try:
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text'):
                    code = extract_code(response.text)
                    create_program_file(code)
                    return response.text  # Return response text for history
                else:
                    say("Failed to generate program. Please try again.")
                    return ""
            except Exception as e:
                print(f"An error occurred: {e}")
                say("An error occurred while generating the program.")
                return ""
        else:
            say("Sorry, I didn't catch that. Please try again.")
            return ""
    elif "please create me a program" in query.lower():
        say("What should the program be about?")
        if mode == "listening":
            description = listen()
        else:
            description = input("Enter the program description: ")
        if description:
            prompt = f"Generate a Python program that {description}"
            try:
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text'):
                    code = extract_code(response.text)
                    create_program_file(code)
                    return response.text  # Return response text for history
                else:
                    say("Failed to generate program. Please try again.")
                    return ""
            except Exception as e:
                print(f"An error occurred: {e}")
                say("An error occurred while generating the program.")
                return ""
        else:
            say("Sorry, I didn't catch that. Please try again.")
            return ""
    elif "please create me a program again" in query.lower():
        say("What should the program be about?")
        if mode == "listening":
            description = listen()
        else:
            description = input("Enter the program description: ")
        if description:
            prompt = f"Generate a Python program that {description}"
            try:
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text'):
                    code = extract_code(response.text)
                    create_program_file(code)
                    return response.text  # Return response text for history
                else:
                    say("Failed to generate program. Please try again.")
                    return ""
            except Exception as e:
                print(f"An error occurred: {e}")
                say("An error occurred while generating the program.")
                return ""
        else:
            say("Sorry, I didn't catch that. Please try again.")
            return ""
    elif "create me program" in query.lower():
        say("What should the program be about?")
        if mode == "listening":
            description = listen()
        else:
            description = input("Enter the program description: ")
        if description:
            prompt = f"Generate a Python program that {description}"
            try:
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text'):
                    code = extract_code(response.text)
                    create_program_file(code)
                    return response.text  # Return response text for history
                else:
                    say("Failed to generate program. Please try again.")
                    return ""
            except Exception as e:
                print(f"An error occurred: {e}")
                say("An error occurred while generating the program.")
                return ""
        else:
            say("Sorry, I didn't catch that. Please try again.")
            return ""
    elif "create me program again" in query.lower():
        say("What should the program be about?")
        if mode == "listening":
            description = listen()
        else:
            description = input("Enter the program description: ")
        if description:
            prompt = f"Generate a Python program that {description}"
            try:
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text'):
                    code = extract_code(response.text)
                    create_program_file(code)
                    return response.text  # Return response text for history
                else:
                    say("Failed to generate program. Please try again.")
                    return ""
            except Exception as e:
                print(f"An error occurred: {e}")
                say("An error occurred while generating the program.")
                return ""
        else:
            say("Sorry, I didn't catch that. Please try again.")
            return ""
    elif "please create me program again" in query.lower():
        say("What should the program be about?")
        if mode == "listening":
            description = listen()
        else:
            description = input("Enter the program description: ")
        if description:
            prompt = f"Generate a Python program that {description}"
            try:
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text'):
                    code = extract_code(response.text)
                    create_program_file(code)
                    return response.text  # Return response text for history
                else:
                    say("Failed to generate program. Please try again.")
                    return ""
            except Exception as e:
                print(f"An error occurred: {e}")
                say("An error occurred while generating the program.")
                return ""
        else:
            say("Sorry, I didn't catch that. Please try again.")
            return ""
    elif "create a program" in query.lower():
        say("What should the program be about?")
        if mode == "listening":
            description = listen()
        else:
            description = input("Enter the program description: ")
        if description:
            prompt = f"Generate a Python program that {description}"
            try:
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text'):
                    code = extract_code(response.text)
                    create_program_file(code)
                    return response.text  # Return response text for history
                else:
                    say("Failed to generate program. Please try again.")
                    return ""
            except Exception as e:
                print(f"An error occurred: {e}")
                say("An error occurred while generating the program.")
                return ""
        else:
            say("Sorry, I didn't catch that. Please try again.")
            return ""
    elif "what question did i ask before" in query.lower():
        if history:
            last_entry = history[-1]
            last_query = last_entry["query"]
            last_response = last_entry["response"]
            say(f"You previously asked: {last_query}. I responded with: {last_response}")
        else:
            say("No previous questions found.")
        return ""
    else:
        try:
            response = model.generate_content(query)
            if response and hasattr(response, 'text'):
                MAX_LENGTH = 2000  # Shortened for brevity

                # Define your replacements here
                replacements = {
                    "trained by Google.": "trained by Awais",
                    "trained by Google": "trained by Awais",
                    # Add more replacements as needed
                }

                # Apply replacements
                response_text = response.text
                for old_word, new_word in replacements.items():
                    response_text = response_text.replace(old_word, new_word)

                brief_response = response_text[:MAX_LENGTH] + '...' if len(response_text) > MAX_LENGTH else response_text

                print(brief_response)
                say(brief_response)
                return brief_response  # Return brief response for history
            else:
                say("Failed to process your query. Please try again.")
                return ""
        except Exception as e:
            print(f"An error occurred: {e}")
            say("An error occurred while processing your query.")
            return ""
 # Return brief response for history

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

            elif "what question did i ask before" in query.lower():
                if history:
                    last_entry = history[-1]
                    last_query = last_entry["query"]
                    last_response = last_entry["response"]
                    say(f"You previously asked: {last_query}. I responded with: {last_response}")
                else:
                    say("No previous questions found.")

            else:
                response_text = process_query(query)
                update_history(query, response_text)

        except sr.WaitTimeoutError:
            print("Listening...")
            continue
