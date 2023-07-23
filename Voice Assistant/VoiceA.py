import openai
import os
import speech_recognition as sr
import pyttsx3
import datetime
import webrtcvad


# Set up the API key (either by setting the environment variable or using the 'api_key' parameter)
# os.environ["OPENAI_API_KEY"] = "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"

# Function to interact with the virtual assistant
def talk_to_va(prompt):
    openai.api_key = os.environ["OPENAI_API_KEY"]  # If using environment variable

    # Send the user's prompt and get the VA's response
    response = openai.Completion.create(
        engine="text-davinci-002",  # Specify the engine (GPT-3.5)
        prompt=prompt,
        max_tokens=150  # Set the maximum number of tokens in the response
    )

    # Extract the VA's response from the API response
    va_response = response["choices"][0]["text"].strip()
    return va_response

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty("rate", 150)
    engine.say(text)
    engine.runAndWait()

def get_greeting():
    current_time = datetime.datetime.now()
    hour = current_time.hour

    if 5 <= hour < 12:
        return "Good morning!"
    elif 12 <= hour < 17:
        return "Good afternoon!"
    else:
        return "Good evening!"

def is_speech(audio_data, sample_rate):
    vad = webrtcvad.Vad()
    vad.set_mode(3)  # Aggressive mode for better detection
    frames = [audio_data[i:i + 320] for i in range(0, len(audio_data), 320)]  # 320 bytes per frame (10 ms at 32 kHz)
    return any(vad.is_speech(frame, sample_rate) for frame in frames)

# Virtual Assistant conversation loop
speak(get_greeting())
speak("How can I assist you?")
user_prompt = ""

while True:
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("You: Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source, timeout=120)  # Set the timeout to 2 minutes (120 seconds)

    try:
    
            user_prompt = recognizer.recognize_google(audio).lower()
            print(f"You: {user_prompt}")

    
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        continue

    except sr.RequestError:
        speak("There was an issue with the speech recognition service.")
        continue

    if user_prompt == "exit, bye":
        speak("Take Care....Goodbye!")
        break

    # Append user's prompt to the ongoing conversation with the VA
    conversation = f"You: {user_prompt}\nVirtual Assistant: "

    # Get the VA's response based on the conversation
    va_response = talk_to_va(conversation)
    print(f"Virtual Assistant: {va_response}")

