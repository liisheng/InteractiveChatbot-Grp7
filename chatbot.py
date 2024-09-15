import openai  # Importing the OpenAI library to interact with the GPT-3.5-turbo model
import speech_recognition as sr  # Importing the SpeechRecognition library to handle voice input
import os  # Importing the os library to handle file operations
import json  # Importing the json library to handle JSON data
import threading  # Importing threading to handle simultaneous input

# Set up your OpenAI API key
openai.api_key = ''  # OpenAI API key

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

# get chatbot response using GPT-3.5-turbo
def get_chatbot_response(user_input):
    # Append the user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Create a chat completion using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # gpt model(can change)
        messages=conversation_history
    )

    # Append the assistant's response to the conversation history
    assistant_response = response['choices'][0]['message']['content']
    conversation_history.append({"role": "assistant", "content": assistant_response})

    # Save the updated conversation history
    save_conversation_history(conversation_history)

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
                return text  # Return the recognized text
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                print("Sorry, I didn't catch that. Please try again.")
            except sr.RequestError as e:
                print("Speech recognition service is unavailable. Switching to text input mode.")
                return "switch"

# Main function to select and switch between input methods
def main():
    input_mode = "text"  # default = use text input
    stop_event = threading.Event()

    print("Welcome to the Interactive Chatbot!")
    print("You can switch between text and voice input anytime by typing 'switch'.")

    while True:
        if input_mode == "text":
            user_input = input("You: ")  # ask the user for text input
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
            chatbot_reply = get_chatbot_response(user_input)
            print(f"Chatbot: {chatbot_reply}")

if __name__ == "__main__":
    main()
