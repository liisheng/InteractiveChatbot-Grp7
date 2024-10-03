import openai
import os
import json
import requests
import logging
from datetime import datetime, timedelta
import dateparser
from langdetect import detect
import langid
from googletrans import Translator, LANGUAGES
<<<<<<< HEAD
from flask import Flask, request, jsonify
import threading
import speech_recognition as sr


# Initialize Flask app
app = Flask(__name__)
=======
>>>>>>> 14e137db455c210abe21ae29b11c5f13ff7ab2f3

# Set up your API keys and IDs directly in the code
OPENAI_API_KEY = 'your-openai-api-key'           # Replace with your OpenAI API key
TEAMUP_API_KEY = 'your-teamup-api-key'           # Replace with your Teamup API key
TEAMUP_CALENDAR_KEY = 'your-teamup-calendar-key' # Replace with your Teamup Calendar key
OPENWEATHERMAP_API_KEY = 'your-openweathermap-api-key'  # Replace with your OpenWeatherMap API key

# Initialize the OpenAI API key
openai.api_key = OPENAI_API_KEY

# Initialize the translator
translator = Translator()

# Set up logging
logging.basicConfig(level=logging.INFO, filename='chatbot_debug.log',
                    format='%(asctime)s:%(levelname)s:%(message)s')

# File to store conversation history
CONVERSATION_FILE = 'conversation_history.json'

# Timezone for Singapore
TIMEZONE = 'Asia/Singapore'

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
        json.dump(conversation_history, file, indent=4)

# Load the conversation history from the file (if it exists)
conversation_history = load_conversation_history()

# Initialize a global variable to track pending intents
pending_intent = None  # e.g., {'intent': 'weather', 'parameters': {'location': None}}

def translate_to_english(text, src_lang):
    """
    Translates the given text from the source language to English.
    """
<<<<<<< HEAD
    if not src_lang or src_lang not in LANGUAGES:
=======
    if src_lang not in LANGUAGES:
>>>>>>> 14e137db455c210abe21ae29b11c5f13ff7ab2f3
        print(f"Translation error: '{src_lang}' is not a valid source language.")
        return text
    try:
        return translator.translate(text, src=src_lang, dest='en').text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

def translate_to_target_language(text, target_lang):
    """
    Translates the given text from English to the target language.
    """
<<<<<<< HEAD
    if not target_lang or target_lang not in LANGUAGES:
=======
    if target_lang not in LANGUAGES:
>>>>>>> 14e137db455c210abe21ae29b11c5f13ff7ab2f3
        print(f"Translation error: '{target_lang}' is not a valid target language.")
        return text
    try:
        return translator.translate(text, src='en', dest=target_lang).text
    except Exception as e:
        print(f"Translation failed: {e}")
        return text

def detect_language(user_input):
    """
    Detects the language of the user's input using langdetect and langid.
    """
    try:
        language_langdetect = detect(user_input)
    except:
        language_langdetect = "und"

    language_langid, confidence = langid.classify(user_input)

    print(f"langid detected: {language_langid} with confidence {confidence}")

    if confidence > 5.0:  # Adjusted threshold for higher confidence
        return language_langid
    elif language_langdetect == language_langid and language_langdetect != "und":
        return language_langdetect

    return "undetermined"
<<<<<<< HEAD

def detect_intent(user_input):
    """
    Uses GPT-3.5-turbo to detect the intent of the user's input.
    """
    # Define a fixed set of intents
    predefined_intents = ["weather", "news", "joke", "greeting", "farewell",
                          "create_event", "delete_event", "retrieve_events", "general"]

    # Enhanced prompt with few-shot examples and explicit instruction
    prompt = (
        f"You are an assistant that extracts the intent and parameters from user input. "
        f"Please output a JSON object with keys 'intent' and 'parameters'. "
        f"The 'intent' should be one of {predefined_intents}. "
        f"The 'parameters' should be a dictionary of extracted parameters.\n\n"
        f"Example:\n"
        f"User Input: \"What's the weather in New York?\"\n"
        f"Output: {{\"intent\": \"weather\", \"parameters\": {{\"location\": \"New York\"}}}}\n\n"
        f"User Input: \"Schedule a meeting with John tomorrow at 2 PM.\"\n"
        f"Output: {{\"intent\": \"create_event\", \"parameters\": {{\"event_title\": \"Meeting with John\", \"date\": \"tomorrow\", \"time\": \"2 PM\"}}}}\n\n"
        f"User Input: \"Delete my dentist appointment on Thursday.\"\n"
        f"Output: {{\"intent\": \"delete_event\", \"parameters\": {{\"event_title\": \"Dentist appointment\", \"date\": \"Thursday\"}}}}\n\n"
        f"User Input: \"What events do I have next week?\"\n"
        f"Output: {{\"intent\": \"retrieve_events\", \"parameters\": {{\"date_range\": \"next week\"}}}}\n\n"
        f"User Input: \"Tell me a joke.\"\n"
        f"Output: {{\"intent\": \"joke\", \"parameters\": {{}}}}\n\n"
        f"User Input: \"Hi there!\"\n"
        f"Output: {{\"intent\": \"greeting\", \"parameters\": {{}}}}\n\n"
        f"User Input: \"Goodbye!\"\n"
        f"Output: {{\"intent\": \"farewell\", \"parameters\": {{}}}}\n\n"
        f"User Input: \"{user_input}\"\n"
        f"Output:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts intents and parameters from user input."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0,
            top_p=1,
            n=1,
            stop=None
        )

        reply = response['choices'][0]['message']['content'].strip()

        # Parse the JSON response
        try:
            response_data = json.loads(reply)
            intent = response_data.get('intent', 'general')
            parameters = response_data.get('parameters', {})
        except json.JSONDecodeError:
            # If parsing fails, default to general intent
            intent = 'general'
            parameters = {}

        # Validate intent against predefined intents
        if intent not in predefined_intents:
            intent = "general"

        return intent, parameters

    except Exception as e:
        print(f"Error detecting intent: {e}")
        return "general", {}

def get_weather(location):
    """
    Fetches weather information for the specified location using OpenWeatherMap's API.
    """
    api_key = OPENWEATHERMAP_API_KEY  # Your OpenWeatherMap API key
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        # Determine chance of rain based on 'rain' data
        if 'rain' in data and '1h' in data['rain']:
            chance_of_rain = f"{data['rain']['1h']} mm in the last hour."
        else:
            chance_of_rain = "No rain expected in the next hour."
        return f"The weather in {location} is currently {weather_description} with a temperature of {temperature}°C, humidity at {humidity}%, and {chance_of_rain}"
    except requests.exceptions.HTTPError:
        return f"Sorry, I couldn't find weather information for '{location}'. Please check the location name and try again."
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "Sorry, I couldn't fetch the weather information right now."

def parse_datetime(date_str, time_str=None):
    """
    Parses natural language date and time strings into ISO 8601 format without microseconds.
    """
    combined_str = f"{date_str} {time_str}" if time_str else date_str
    dt = dateparser.parse(
        combined_str,
        settings={'TIMEZONE': TIMEZONE, 'RETURN_AS_TIMEZONE_AWARE': True}
    )
    if dt:
        # Format the datetime without microseconds
        return dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    else:
        return None

def get_subcalendar_ids():
    """
    Retrieves the list of subcalendar IDs from the Teamup Calendar.
    """
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_KEY}/subcalendars"
    headers = {
        "Content-Type": "application/json",
        "Teamup-Token": TEAMUP_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            subcalendars = response.json().get('subcalendars', [])
            if not subcalendars:
                print("No subcalendars found.")
                return []
            else:
                # Return a list of subcalendar IDs
                return [subcalendar['id'] for subcalendar in subcalendars]
        else:
            print(f"Failed to retrieve subcalendars: {response.text}")
            return []
    except Exception as e:
        print(f"Error retrieving subcalendars: {e}")
        return []

def schedule_event(event_details):
    """
    Schedules an event using the Teamup Calendar API.
    """
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_KEY}/events"
    headers = {
        "Content-Type": "application/json",
        "Teamup-Token": TEAMUP_API_KEY
    }
    event_title = event_details.get('event_title', 'No Title')
    date_str = event_details.get('date')
    time_str = event_details.get('time')
    end_time_str = event_details.get('end_time')

    start_datetime = parse_datetime(date_str, time_str)
    if not start_datetime:
        return "Sorry, I couldn't understand the date and time. Please try again."

    if end_time_str:
        end_datetime = parse_datetime(date_str, end_time_str)
        if not end_datetime:
            # Assume 1-hour duration if end time parsing fails
            dt = datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S%z')
            dt += timedelta(hours=1)
            end_datetime = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    else:
        # Assume 1-hour duration if end time is not provided
        dt = datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S%z')
        dt += timedelta(hours=1)
        end_datetime = dt.strftime('%Y-%m-%dT%H:%M:%S%z')

    # Get subcalendar IDs
    subcalendar_ids = get_subcalendar_ids()
    if not subcalendar_ids:
        return "Failed to retrieve subcalendar IDs."

    data = {
        "subcalendar_id": subcalendar_ids[0],  # Use the first subcalendar ID
        "title": event_title,
        "start_dt": start_datetime,
        "end_dt": end_datetime,
        "all_day": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            return f"Event '{event_title}' scheduled successfully."
        else:
            return f"Failed to schedule event: {response.text}"
    except Exception as e:
        print(f"Error scheduling event: {e}")
        return "Sorry, I couldn't schedule the event."

def delete_event(event_details):
    """
    Deletes an event using the Teamup Calendar API.
    """
    event_title = event_details.get('event_title')
    date_str = event_details.get('date')

    # Fetch events to find matching ones
    events = retrieve_events({'date_range': date_str})

    if isinstance(events, str):
        # An error message was returned
        return events

    matching_events = [event for event in events if event['title'] == event_title]

    if not matching_events:
        return f"No event found with the title '{event_title}'."
    else:
        for event in matching_events:
            event_id = event['id']
            url = f"https://api.teamup.com/{TEAMUP_CALENDAR_KEY}/events/{event_id}"
            headers = {
                "Content-Type": "application/json",
                "Teamup-Token": TEAMUP_API_KEY
            }
            try:
                response = requests.delete(url, headers=headers)
                if response.status_code != 204:
                    return f"Failed to delete event: {response.text}"
            except Exception as e:
                print(f"Error deleting event: {e}")
                return "Sorry, I couldn't delete the event."
        return f"Event(s) titled '{event_title}' have been deleted."

def retrieve_events(parameters):
    """
    Retrieves events using the Teamup Calendar API.
    """
    date_range = parameters.get('date_range', 'today')

    start_dt = parse_datetime(date_range)
    if not start_dt:
        return "Sorry, I couldn't understand the date range. Please try again."

    # Default to 7 days if no end date is provided
    dt = datetime.strptime(start_dt, '%Y-%m-%dT%H:%M:%S%z')
    end_dt = (dt + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S%z')

    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_KEY}/events"
    headers = {
        "Content-Type": "application/json",
        "Teamup-Token": TEAMUP_API_KEY
    }
    params = {
        "startDate": start_dt[:10],
        "endDate": end_dt[:10]
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            events = response.json().get('events', [])
            if not events:
                return "No events found."
            else:
                # Return the list of events
                return events
        else:
            return f"Failed to retrieve events: {response.text}"
    except Exception as e:
        print(f"Error retrieving events: {e}")
        return "Sorry, I couldn't retrieve events."
    

# Flask API route for receiving user input
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data.get('message')
    
    if not user_input:
        return jsonify({"error": "Message is required"}), 400
    
    # Detect the language of the user input
    language = data.get('language', 'en')

    # Get the chatbot's response
    chatbot_reply = get_chatbot_response(user_input, language)
    
    return jsonify({
        "response": chatbot_reply,
        "language": language
    })


# Flask API route for voice input
@app.route('/voice-chat', methods=['POST'])
def voice_chat():
    stop_event = threading.Event()
    recognizer = sr.Recognizer()
    
    # For simplicity, this assumes voice input has already been recorded and converted to text
    audio_file = request.files.get('audio')
    if audio_file:
        audio_path = 'temp.wav'
        audio_file.save(audio_path)

        with sr.AudioFile(audio_path) as source:
            audio = recognizer.record(source)
            try:
                text = recognizer.recognize_google(audio)
                language = detect_language(text)
                chatbot_reply = get_chatbot_response(text, language)
                return jsonify({"response": chatbot_reply, "language": language})
            except Exception as e:
                return jsonify({"error": f"Voice recognition failed: {e}"}), 500
    else:
        return jsonify({"error": "Audio file is required"}), 400


def get_chatbot_response(user_input, language):
    """
    Processes the user's input to generate an appropriate chatbot response.
    """
    global pending_intent  # Access the global variable
    global conversation_history  # Access the global conversation history

    # Translate user input to English if necessary
    if language != 'en' and language != 'undetermined':
        user_input = translate_to_english(user_input, language)

    # Detect intent and parameters
    intent, params = detect_intent(user_input)

    print(f"Detected intent: {intent} with parameters: {params}")

    if intent == "weather":
        location = params.get("location")
        if location:
            weather_info = get_weather(location)
            if language != 'en' and language != "undetermined":
                weather_info = translate_to_target_language(weather_info, language)
            pending_intent = None  # Reset pending intent if it was set
            return weather_info
        else:
            # Set pending intent to wait for location
            pending_intent = {'intent': 'weather', 'parameters': {'location': None}}
            prompt = "Sure, I can help with the weather. Could you please specify the location?"
            if language != 'en' and language != "undetermined":
                prompt = translate_to_target_language(prompt, language)
            return prompt

    elif intent == "create_event":
        response = schedule_event(params)
        if language != 'en' and language != "undetermined":
            response = translate_to_target_language(response, language)
        return response

    elif intent == "delete_event":
        response = delete_event(params)
        if language != 'en' and language != "undetermined":
            response = translate_to_target_language(response, language)
        return response

    elif intent == "retrieve_events":
        events = retrieve_events(params)
        if isinstance(events, str):
            # An error message was returned
            response = events
        else:
            # Format the list of events
            if not events:
                response = "No events found."
            else:
                event_list = ""
                for event in events:
                    event_title = event.get('title', 'No Title')
                    event_start_str = event.get('start_dt', 'Unknown Start Time')

                    # Parse the event_start_str into a datetime object
                    try:
                        event_start = datetime.strptime(event_start_str, "%Y-%m-%dT%H:%M:%S%z")
                        # Format the datetime according to the desired format
                        formatted_start = event_start.strftime("%d %m %Y, %A, %I:%M %p")
                    except ValueError:
                        formatted_start = event_start_str  # If parsing fails, use the original string

                    event_list += f"- {event_title} on {formatted_start}\n"
                response = event_list
        if language != 'en' and language != "undetermined":
            response = translate_to_target_language(response, language)
        return response

    elif intent == "joke":
        # Fetch a joke using GPT-3.5-turbo
        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation_history
            )
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return "Sorry, I couldn't get a response."

        assistant_response = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": assistant_response})

        # Save the updated conversation history
        save_conversation_history(conversation_history)

        # Translate the response back to the user's language if necessary
        if language != 'en' and language != "undetermined":
            assistant_response = translate_to_target_language(assistant_response, language)

        return assistant_response

    elif intent == "general":
        if language != 'en' and language != "undetermined":
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

        # Translate the response back to the user's language if necessary
        if language != 'en' and language != "undetermined":
            assistant_response = translate_to_target_language(assistant_response, language)

        return assistant_response

    else:
        # If intent is not recognized, default to general
        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation_history
            )
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return "Sorry, I couldn't get a response."

        assistant_response = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": assistant_response})

        save_conversation_history(conversation_history)

        if language != 'en' and language != "undetermined":
            assistant_response = translate_to_target_language(assistant_response, language)

        return assistant_response


def main():
    """
    The main function to run the chatbot in a terminal.
=======

def detect_intent(user_input):
    """
    Uses GPT-3.5-turbo to detect the intent of the user's input.
    """
    # Define a fixed set of intents
    predefined_intents = ["weather", "news", "joke", "greeting", "farewell",
                          "create_event", "delete_event", "retrieve_events", "general"]

    # Enhanced prompt with few-shot examples and explicit instruction
    prompt = (
        f"You are an assistant that extracts the intent and parameters from user input. "
        f"Please output a JSON object with keys 'intent' and 'parameters'. "
        f"The 'intent' should be one of {predefined_intents}. "
        f"The 'parameters' should be a dictionary of extracted parameters.\n\n"
        f"Example:\n"
        f"User Input: \"What's the weather in New York?\"\n"
        f"Output: {{\"intent\": \"weather\", \"parameters\": {{\"location\": \"New York\"}}}}\n\n"
        f"User Input: \"Schedule a meeting with John tomorrow at 2 PM.\"\n"
        f"Output: {{\"intent\": \"create_event\", \"parameters\": {{\"event_title\": \"Meeting with John\", \"date\": \"tomorrow\", \"time\": \"2 PM\"}}}}\n\n"
        f"User Input: \"Delete my dentist appointment on Thursday.\"\n"
        f"Output: {{\"intent\": \"delete_event\", \"parameters\": {{\"event_title\": \"Dentist appointment\", \"date\": \"Thursday\"}}}}\n\n"
        f"User Input: \"What events do I have next week?\"\n"
        f"Output: {{\"intent\": \"retrieve_events\", \"parameters\": {{\"date_range\": \"next week\"}}}}\n\n"
        f"User Input: \"Tell me a joke.\"\n"
        f"Output: {{\"intent\": \"joke\", \"parameters\": {{}}}}\n\n"
        f"User Input: \"Hi there!\"\n"
        f"Output: {{\"intent\": \"greeting\", \"parameters\": {{}}}}\n\n"
        f"User Input: \"Goodbye!\"\n"
        f"Output: {{\"intent\": \"farewell\", \"parameters\": {{}}}}\n\n"
        f"User Input: \"{user_input}\"\n"
        f"Output:"
    )

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that extracts intents and parameters from user input."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0,
            top_p=1,
            n=1,
            stop=None
        )

        reply = response['choices'][0]['message']['content'].strip()

        # Parse the JSON response
        try:
            response_data = json.loads(reply)
            intent = response_data.get('intent', 'general')
            parameters = response_data.get('parameters', {})
        except json.JSONDecodeError:
            # If parsing fails, default to general intent
            intent = 'general'
            parameters = {}

        # Validate intent against predefined intents
        if intent not in predefined_intents:
            intent = "general"

        return intent, parameters

    except Exception as e:
        print(f"Error detecting intent: {e}")
        return "general", {}

def get_weather(location):
    """
    Fetches weather information for the specified location using OpenWeatherMap's API.
    """
    api_key = OPENWEATHERMAP_API_KEY  # Your OpenWeatherMap API key
    base_url = 'http://api.openweathermap.org/data/2.5/weather'
    params = {
        'q': location,
        'appid': api_key,
        'units': 'metric'
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        humidity = data['main']['humidity']
        # Determine chance of rain based on 'rain' data
        if 'rain' in data and '1h' in data['rain']:
            chance_of_rain = f"{data['rain']['1h']} mm in the last hour."
        else:
            chance_of_rain = "No rain expected in the next hour."
        return f"The weather in {location} is currently {weather_description} with a temperature of {temperature}°C, humidity at {humidity}%, and {chance_of_rain}"
    except requests.exceptions.HTTPError:
        return f"Sorry, I couldn't find weather information for '{location}'. Please check the location name and try again."
    except Exception as e:
        print(f"Error fetching weather data: {e}")
        return "Sorry, I couldn't fetch the weather information right now."

def parse_datetime(date_str, time_str=None):
    """
    Parses natural language date and time strings into ISO 8601 format without microseconds.
    """
    combined_str = f"{date_str} {time_str}" if time_str else date_str
    dt = dateparser.parse(
        combined_str,
        settings={'TIMEZONE': TIMEZONE, 'RETURN_AS_TIMEZONE_AWARE': True}
    )
    if dt:
        # Format the datetime without microseconds
        return dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    else:
        return None

def get_subcalendar_ids():
    """
    Retrieves the list of subcalendar IDs from the Teamup Calendar.
    """
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_KEY}/subcalendars"
    headers = {
        "Content-Type": "application/json",
        "Teamup-Token": TEAMUP_API_KEY
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            subcalendars = response.json().get('subcalendars', [])
            if not subcalendars:
                print("No subcalendars found.")
                return []
            else:
                # Return a list of subcalendar IDs
                return [subcalendar['id'] for subcalendar in subcalendars]
        else:
            print(f"Failed to retrieve subcalendars: {response.text}")
            return []
    except Exception as e:
        print(f"Error retrieving subcalendars: {e}")
        return []

def schedule_event(event_details):
    """
    Schedules an event using the Teamup Calendar API.
    """
    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_KEY}/events"
    headers = {
        "Content-Type": "application/json",
        "Teamup-Token": TEAMUP_API_KEY
    }
    event_title = event_details.get('event_title', 'No Title')
    date_str = event_details.get('date')
    time_str = event_details.get('time')
    end_time_str = event_details.get('end_time')

    start_datetime = parse_datetime(date_str, time_str)
    if not start_datetime:
        return "Sorry, I couldn't understand the date and time. Please try again."

    if end_time_str:
        end_datetime = parse_datetime(date_str, end_time_str)
        if not end_datetime:
            # Assume 1-hour duration if end time parsing fails
            dt = datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S%z')
            dt += timedelta(hours=1)
            end_datetime = dt.strftime('%Y-%m-%dT%H:%M:%S%z')
    else:
        # Assume 1-hour duration if end time is not provided
        dt = datetime.strptime(start_datetime, '%Y-%m-%dT%H:%M:%S%z')
        dt += timedelta(hours=1)
        end_datetime = dt.strftime('%Y-%m-%dT%H:%M:%S%z')

    # Get subcalendar IDs
    subcalendar_ids = get_subcalendar_ids()
    if not subcalendar_ids:
        return "Failed to retrieve subcalendar IDs."

    data = {
        "subcalendar_id": subcalendar_ids[0],  # Use the first subcalendar ID
        "title": event_title,
        "start_dt": start_datetime,
        "end_dt": end_datetime,
        "all_day": False
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 201:
            return f"Event '{event_title}' scheduled successfully."
        else:
            return f"Failed to schedule event: {response.text}"
    except Exception as e:
        print(f"Error scheduling event: {e}")
        return "Sorry, I couldn't schedule the event."

def delete_event(event_details):
    """
    Deletes an event using the Teamup Calendar API.
    """
    event_title = event_details.get('event_title')
    date_str = event_details.get('date')

    # Fetch events to find matching ones
    events = retrieve_events({'date_range': date_str})

    if isinstance(events, str):
        # An error message was returned
        return events

    matching_events = [event for event in events if event['title'] == event_title]

    if not matching_events:
        return f"No event found with the title '{event_title}'."
    else:
        for event in matching_events:
            event_id = event['id']
            url = f"https://api.teamup.com/{TEAMUP_CALENDAR_KEY}/events/{event_id}"
            headers = {
                "Content-Type": "application/json",
                "Teamup-Token": TEAMUP_API_KEY
            }
            try:
                response = requests.delete(url, headers=headers)
                if response.status_code != 204:
                    return f"Failed to delete event: {response.text}"
            except Exception as e:
                print(f"Error deleting event: {e}")
                return "Sorry, I couldn't delete the event."
        return f"Event(s) titled '{event_title}' have been deleted."

def retrieve_events(parameters):
    """
    Retrieves events using the Teamup Calendar API.
    """
    date_range = parameters.get('date_range', 'today')

    start_dt = parse_datetime(date_range)
    if not start_dt:
        return "Sorry, I couldn't understand the date range. Please try again."

    # Default to 7 days if no end date is provided
    dt = datetime.strptime(start_dt, '%Y-%m-%dT%H:%M:%S%z')
    end_dt = (dt + timedelta(days=7)).strftime('%Y-%m-%dT%H:%M:%S%z')

    url = f"https://api.teamup.com/{TEAMUP_CALENDAR_KEY}/events"
    headers = {
        "Content-Type": "application/json",
        "Teamup-Token": TEAMUP_API_KEY
    }
    params = {
        "startDate": start_dt[:10],
        "endDate": end_dt[:10]
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            events = response.json().get('events', [])
            if not events:
                return "No events found."
            else:
                # Return the list of events
                return events
        else:
            return f"Failed to retrieve events: {response.text}"
    except Exception as e:
        print(f"Error retrieving events: {e}")
        return "Sorry, I couldn't retrieve events."

def get_chatbot_response(user_input, language):
    """
    Processes the user's input to generate an appropriate chatbot response.
    """
    global pending_intent  # Access the global variable
    global conversation_history  # Access the global conversation history

    # Translate user input to English if necessary
    if language != 'en' and language != 'undetermined':
        user_input = translate_to_english(user_input, language)

    # Detect intent and parameters
    intent, params = detect_intent(user_input)

    print(f"Detected intent: {intent} with parameters: {params}")

    if intent == "weather":
        location = params.get("location")
        if location:
            weather_info = get_weather(location)
            if language != 'en' and language != "undetermined":
                weather_info = translate_to_target_language(weather_info, language)
            pending_intent = None  # Reset pending intent if it was set
            return weather_info
        else:
            # Set pending intent to wait for location
            pending_intent = {'intent': 'weather', 'parameters': {'location': None}}
            prompt = "Sure, I can help with the weather. Could you please specify the location?"
            if language != 'en' and language != "undetermined":
                prompt = translate_to_target_language(prompt, language)
            return prompt

    elif intent == "create_event":
        response = schedule_event(params)
        if language != 'en' and language != "undetermined":
            response = translate_to_target_language(response, language)
        return response

    elif intent == "delete_event":
        response = delete_event(params)
        if language != 'en' and language != "undetermined":
            response = translate_to_target_language(response, language)
        return response

    elif intent == "retrieve_events":
        events = retrieve_events(params)
        if isinstance(events, str):
            # An error message was returned
            response = events
        else:
            # Format the list of events
            if not events:
                response = "No events found."
            else:
                event_list = ""
                for event in events:
                    event_title = event.get('title', 'No Title')
                    event_start_str = event.get('start_dt', 'Unknown Start Time')

                    # Parse the event_start_str into a datetime object
                    try:
                        event_start = datetime.strptime(event_start_str, "%Y-%m-%dT%H:%M:%S%z")
                        # Format the datetime according to the desired format
                        formatted_start = event_start.strftime("%d %m %Y, %A, %I:%M %p")
                    except ValueError:
                        formatted_start = event_start_str  # If parsing fails, use the original string

                    event_list += f"- {event_title} on {formatted_start}\n"
                response = event_list
        if language != 'en' and language != "undetermined":
            response = translate_to_target_language(response, language)
        return response

    elif intent == "joke":
        # Fetch a joke using GPT-3.5-turbo
        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation_history
            )
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return "Sorry, I couldn't get a response."

        assistant_response = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": assistant_response})

        # Save the updated conversation history
        save_conversation_history(conversation_history)

        # Translate the response back to the user's language if necessary
        if language != 'en' and language != "undetermined":
            assistant_response = translate_to_target_language(assistant_response, language)

        return assistant_response

    elif intent == "general":
        if language != 'en' and language != "undetermined":
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

        # Translate the response back to the user's language if necessary
        if language != 'en' and language != "undetermined":
            assistant_response = translate_to_target_language(assistant_response, language)

        return assistant_response

    else:
        # If intent is not recognized, default to general
        conversation_history.append({"role": "user", "content": user_input})

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=conversation_history
            )
        except Exception as e:
            print(f"Error communicating with OpenAI: {e}")
            return "Sorry, I couldn't get a response."

        assistant_response = response['choices'][0]['message']['content']
        conversation_history.append({"role": "assistant", "content": assistant_response})

        save_conversation_history(conversation_history)

        if language != 'en' and language != "undetermined":
            assistant_response = translate_to_target_language(assistant_response, language)

        return assistant_response

def main():
    """
    The main function to run the chatbot.
>>>>>>> 14e137db455c210abe21ae29b11c5f13ff7ab2f3
    """
    global pending_intent  # Access the global variable
    print("Welcome to the Interactive Chatbot!")
    print("Type 'exit' to quit the chatbot.")

    while True:
        user_input = input("You: ")

        if user_input.lower() == "exit":
            print("Chatbot: Goodbye!")
            break

        if len(user_input.strip()) < 4:
            language = 'en'
        else:
            language = detect_language(user_input)

        print(f"Detected language: {language}")

        if user_input:
            chatbot_reply = get_chatbot_response(user_input, language)
            print(f"Chatbot: {chatbot_reply}")


if __name__ == "__main__":
<<<<<<< HEAD
    # Run Flask in a separate thread if we want to handle API requests
    flask_thread = threading.Thread(target=lambda: app.run(debug=True, use_reloader=False, ))
    flask_thread.start()
    # Start the interactive chatbot in the main thread
    main()
=======
    main()

>>>>>>> 14e137db455c210abe21ae29b11c5f13ff7ab2f3
