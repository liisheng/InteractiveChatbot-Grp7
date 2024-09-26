import openai
import pyttsx3
import speech_recognition as sr
import time
from gtts import gTTS

openai.api_key = "ENTER KEY"

# Initialise the text-to-speech engine
engine = pyttsx3.init()

def transcribe_audio_to_text(filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(filename) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except Exception as e:
        print(f"Unknown error: {e}")

# Use OpenAI to generate a response
def generate_response(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        max_tokens=4000,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return response["choices"][0]["message"]["content"]

def speak_text(text):
    engine.say(text)
    engine.runAndWait()

def main():
    while True:
        # Wait for the user to start the operation using keyword "Yes"
        print("Say 'Yes' to start recording your question...")
        with sr.Microphone() as source:
            recognizer = sr.Recognizer()
            audio = recognizer.listen(source)
            try:
                transcription = recognizer.recognize_google(audio)
                if transcription.lower() == "yes":
                    # Proceed to record user's question
                    filename = "input.wav"
                    print("Please tell me your question...")
                    with sr.Microphone() as source:
                        recognizer = sr.Recognizer()
                        source.pause_threshold = 1
                        audio = recognizer.listen(source, phrase_time_limit=None, timeout=None)
                        with open(filename, "wb") as f:
                            f.write(audio.get_wav_data())
                    
                    # Transcribe audio to text
                    text = transcribe_audio_to_text(filename)
                    if text:
                        print(f"Your question: {text}")

                        # Generate response using GPT
                        response = generate_response(text)
                        print(f"Bot's answer: {response}")

                        # Read out the answer generated
                        speak_text(response)

            except Exception as e:
                print(f"An error has occurred: {e}")

if __name__ == "__main__":
    main()