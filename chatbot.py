import openai  # Importing the OpenAI library to interact with the GPT-3.5-turbo model
import speech_recognition as sr  # Importing the SpeechRecognition library to handle voice input
import os  # Importing the os library to handle file operations
import json  # Importing the json library to handle JSON data
import threading  # Importing threading to handle simultaneous input
from langdetect import detect
import langid
import logging
from googletrans import Translator, LANGUAGES
translator = Translator()

# Set up your OpenAI API key


# File to store conversation history
CONVERSATION_FILE = 'conversation_history.json'

# Load conversation history from a file
def load_conversation_history():
    if os.path.exists(CONVERSATION_FILE):
        with open(CONVERSATION_FILE, 'r') as file:
            return json.load(file)
    else:
        return [{"role": "system", "content": "You are a helpful assistant."}]

# Save conversation history to a file
def save_conversation_history(conversation_history):
    with open(CONVERSATION_FILE, 'w') as file:
        json.dump(conversation_history, file)

# Load the conversation history from the file (if it exists)
conversation_history = load_conversation_history()

def translate_to_english(text, src_lang):
    translator = Translator()
    # Check if the detected source language is valid in googletrans
    if src_lang not in LANGUAGES:
        print(f"Translation error: '{src_lang}' is not a valid source language.")
        return text  # Return the original text if the language is invalid
    try:
        return translator.translate(text, src=src_lang, dest='en').text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text  # Return the original text if translation fails

def translate_to_target_language(text, target_lang):
    translator = Translator()
    # Check if the target language is valid in googletrans
    if target_lang not in LANGUAGES:
        print(f"Translation error: '{target_lang}' is not a valid target language.")
        return text  # Return the original text if the language is invalid
    try:
        return translator.translate(text, src='en', dest=target_lang).text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text  # Return the original text if translation fails

# get chatbot response using GPT-3.5-turbo
def get_chatbot_response(user_input, language):
    # Skip translation if language is undetermined
    if language != 'en' and language != 'undetermined':
        user_input = translate_to_english(user_input, language)
    
    # Append the user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    try:
        # Create a chat completion using the OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=conversation_history
        )
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        return "Sorry, I couldn't get a response."

    # Append the assistant's response to the conversation history
    assistant_response = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": assistant_response})

    # Save the updated conversation history
    save_conversation_history(conversation_history)

    # Skip translation if language is undetermined
    if language != 'en' and language != 'undetermined':
        assistant_response = translate_to_target_language(assistant_response, language)

    # Return the reply
    return assistant_response

# Function to get voice input from the user, with a fallback mechanism
def get_voice_input(stop_event):
    recognizer = sr.Recognizer()  # Initialize the recognizer for speech recognition
    with sr.Microphone() as source:  # Use the default microphone as the audio source
        print("Listening...")  # Show that the program is listening for voice input
        while not stop_event.is_set():
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=5)  # Capture the audio input
                print("Recognizing...")  # Show that the program is processing/understanding the audio input
                text = recognizer.recognize_google(audio)  # Use Google's speech recognition service to convert audio to text
                print(f"You said: {text}")  # Print the recognized text

                # Detect language of the spoken text
                language_langdetect = detect(text)
                language_langid, _ = langid.classify(text)
                language = language_langid if language_langid == language_langdetect else "undetermined"
                
                print(f"Detected language: {language}")  # Output the detected language
                
                return text, language  # Return the recognized text and detected language
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that. Please try again.")
            except sr.RequestError as e:
                print("Speech recognition service is unavailable. Switching to text input mode.")
                return "switch", "undetermined"
            

def detect_language(user_input):
    # Detect language using langdetect and langid
    language_langdetect = detect(user_input)
    language_langid, confidence = langid.classify(user_input)
    
    print(f"langid detected: {language_langid} with confidence {confidence}")  # Print confidence level

    if confidence > 5:  # If langid confidence is high enough, return that language
        return language_langid
    elif language_langdetect == language_langid:  # else if langid and langdetect agrees upon a detected language, use that one
        return language_langdetect

    return "undetermined"  # If confidence is low and they don't agree, return 'undetermined'

# Main function to select and switch between input methods
def main():
    input_mode = "text"  # default = use text input
    stop_event = threading.Event()

    print("Welcome to the Interactive Chatbot!")
    print("You can switch between text and voice input anytime by typing 'switch'.")

    while True:
        if input_mode == "text":
            user_input = input("You: ")  # ask the user for text input      
            
            if len(user_input.strip()) < 4:  # Handle short inputs (like "hello") as English (This is to ensure short inputs are not falsely classified)
                language = 'en'
            else:
                language = detect_language(user_input)  # Detect language of text input
            
            print(f"Detected language: {language}")  # Output the detected language
            
            if user_input.lower() == "switch":
                input_mode = "voice"  # Switch to voice input mode if the user types 'switch'
                print("Switched to voice input.")
                continue
            elif user_input.lower() == "exit":
                print("Chatbot: Goodbye!")  # Exit the program if the user types 'exit'
                break

        elif input_mode == "voice":
            stop_event.clear()
            voice_thread = threading.Thread(target=lambda: get_voice_input(stop_event))
            voice_thread.start()

            while voice_thread.is_alive():
                user_input = input("You (text override): ")
                if user_input.lower() == "switch":
                    input_mode = "text"  # Switch to text input mode if the user types 'switch'
                    print("Switched to text input.")
                    stop_event.set()
                    voice_thread.join()
                    break
                elif user_input.lower() == "exit":
                    print("Chatbot: Goodbye!")  # Exit the program if the user types 'exit'
                    stop_event.set()
                    voice_thread.join()
                    return

            voice_thread.join()  # Ensure the voice thread has finished

        if user_input and user_input.lower() != "switch":
            # Pass both user_input and language to get_chatbot_response
            chatbot_reply = get_chatbot_response(user_input, language)
            print(f"Chatbot: {chatbot_reply}")

if __name__ == "__main__":
    main()
