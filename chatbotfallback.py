
import openai  # Importing the OpenAI library to interact with the GPT-3.5-turbo model
import speech_recognition as sr  # Importing the SpeechRecognition library to handle voice input
import time  # Importing the time library to add delays between actions

# Set up your OpenAI API key
openai.api_key = ''  # OpenAI API key

# get chatbot response using GPT-3.5-turbo
def get_chatbot_response(user_input):
    # Create a chat completion using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # gpt model(can change)
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},  # Define the assistant's role and initial behavior
            {"role": "user", "content": user_input}  # Pass the user's input to the model
        ]
    )
    # Return the reply
    return response['choices'][0]['message']['content']

# Function to get voice input from the user, with a fallback mechanism(if their mic quality too bad it will switch to text by default)
def get_voice_input():
    recognizer = sr.Recognizer()  # Initialize the recognizer for speech recognition
    with sr.Microphone() as source:  # Use the default microphone as the audio source
        print("Listening...")  # Show that the program is listening for voice input
        audio = recognizer.listen(source)  # Capture the audio input

        try:
            print("Recognizing...")  # Show that the program is processing/understanding the audio input
            text = recognizer.recognize_google(audio)  # Use Google's speech recognition service to convert audio to text
            print(f"You said: {text}")  # Print the recognized text
            return text  # Return the recognized text
        except sr.UnknownValueError:
            print("Sorry, I didn't catch that. Switching to text input mode.")  
            return "switch"  # Automatically switch to text input mode on failure
        except sr.RequestError as e:
            print("Speech recognition service is unavailable. Switching to text input mode.")  # switch to text input if there is a service error
            return "switch"

# Main function to select and switch between input methods
def main():
    input_mode = "text"  # default = use text input

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
            print("Say 'switch' to switch to text input.")
            user_input = get_voice_input()  # Get voice input from the user
            
            if user_input.lower() == "switch":  # Automatically switch to text mode if voice input fails
                input_mode = "text"
                print("Switched to text input.")
                continue
            elif user_input.lower() == "exit":
                print("Chatbot: Goodbye!")  # Exit the program if the user says 'exit'
                break

        chatbot_reply = get_chatbot_response(user_input)  # Get the chatbot's response to the user's input
        print(f"Chatbot: {chatbot_reply}")
        time.sleep(1)  # add a delay to so we dont hit rate limits

if __name__ == "__main__":
    main()  # Run the main function 
