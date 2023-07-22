import openai
import os
import speech_recognition as sr
import pyttsx3

# Set up the API key (either by setting the environment variable or using the 'api_key' parameter)
os.environ["OPENAI_API_KEY"] = "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"

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


# Virtual Assistant conversation loop
print("Virtual Assistant: Hello! How can I assist you today?")
user_prompt = ""

while True:

    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
            print("You: Listening...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

    try:
            user_prompt = recognizer.recognize_google(audio).lower()
            print(f"You: {user_prompt}")
            # speak("Hello, this is a test.")
    except sr.UnknownValueError:
            print("You: Sorry, I couldn't understand that.")
            continue
    except sr.RequestError:
            print("You: There was an issue with the speech recognition service.")
            continue

    if user_prompt == "exit":
            print("Virtual Assistant: Goodbye!")
            break

        # Append user's prompt to the ongoing conversation with the VA
    conversation = f"You: {user_prompt}\nVirtual Assistant: "

        # Get the VA's response based on the conversation
    va_response = talk_to_va(conversation)
    print(f"Virtual Assistant: {va_response}")

        # Convert VA's response to speech and play it
    speak(va_response)
