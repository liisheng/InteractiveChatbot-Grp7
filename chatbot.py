import openai
import speech_recognition as sr
import time
import os
import json

# Set up your OpenAI API key
openai.api_key = ''#<- api key here

# File to store conversation history
CONVERSATION_FILE = 'conversation_history.json'

# Function to load conversation history from a file
# If the file doesn't exist, it returns a default message
def load_conversation_history():
    if os.path.exists(CONVERSATION_FILE):
        # Load the conversation history from a JSON file
        with open(CONVERSATION_FILE, 'r') as file:
            return json.load(file)
    else:
        # Return an initial message if there's no saved history
        return [{"role": "system", "content": "You are a helpful assistant."}]

# Function to save the conversation history to a file after each interaction
def save_conversation_history(conversation_history):
    with open(CONVERSATION_FILE, 'w') as file:
        json.dump(conversation_history, file)

# Load the conversation history when the chatbot starts
conversation_history = load_conversation_history()

# Function to get chatbot response using GPT-3.5-turbo API
def get_chatbot_response(user_input):
    # Append the user's input to the conversation history
    conversation_history.append({"role": "user", "content": user_input})

    # Send the conversation history (including user's input) to GPT-3.5-turbo
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=conversation_history
    )

    # Extract the chatbot's response from the API response
    chatbot_message = response['choices'][0]['message']['content']

    # Append the chatbot's response to the conversation history
    conversation_history.append({"role": "assistant", "content": chatbot_message})

    # Save the updated conversation history to the file
    save_conversation_history(conversation_history)

    return chatbot_message

# Function to get voice input from the user using the microphone
def get_voice_input():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)  # Listen for user input through the mic

        try:
            # Use Google's speech recognition to convert audio to text
            print("Recognizing...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            # Handle cases where the speech was not recognized
            print("Sorry, I didn't catch that.")
            return None
        except sr.RequestError as e:
            # Handle errors with the speech recognition service
            print("Speech recognition service is unavailable.")
            return None

# Main function to manage the chatbot and handle input methods (text/voice)
def main():
    input_mode = "text"  # Default input mode is text

    print("Welcome to the Interactive Chatbot with Fallback!")
    print("I will remember our previous conversation across sessions.")
    print("You can switch between text and voice input anytime by typing 'switch'.")

    # Main interaction loop
    while True:
        if input_mode == "text":
            # Get user input in text mode
            user_input = input("You: ")
            if user_input.lower() == "switch":
                # Switch to voice input mode
                input_mode = "voice"
                print("Switched to voice input.")
                continue
            elif user_input.lower() == "exit":
                # Exit the conversation
                print("Chatbot: Goodbye!")
                break

        elif input_mode == "voice":
            # Get voice input from the user in voice mode
            print("Say 'switch' to switch to text input.")
            user_input = get_voice_input()
            if user_input is None:
                continue
            if user_input.lower() == "switch":
                # Switch back to text input mode
                input_mode = "text"
                print("Switched to text input.")
                continue
            elif user_input.lower() == "exit":
                # Exit the conversation
                print("Chatbot: Goodbye!")
                break

        # Get chatbot response from GPT-3.5-turbo API
        chatbot_reply = get_chatbot_response(user_input)
        print(f"Chatbot: {chatbot_reply}")
        time.sleep(1)  # Short delay to prevent overwhelming the API with requests

if __name__ == "__main__":
    main()
