from neuralintents import GenericAssistant
import speech_recognition
import pyttsx3 as tts
import sys


recognizer = speech_recognition.Recognizer()

speaker = tts.init()
speaker.setProperty('rate', 150)

todo_list = ['Go shopping', 'Clean room', 'Record Video']


def create_note():
    global recognizer

    speaker.say("What do you want to write on your note?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                note = recognizer.recognize_google(audio)
                note = note.lower()

                speaker.say("Choose a filename!")
                speaker.runAndWait()

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                filename = recognizer.recognize_google(audio)
                filename = filename.lower()

            with open(filename, 'a') as f:
                f.write(note)
                done = True
                speaker.say(f"I successfully created the note {filename}")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand you! Please try again")
            speaker.runAndWait()


def add_todo():
    global recognizer

    speaker.say("What todo do you want to add?")
    speaker.runAndWait()

    done = False

    while not done:
        try:

            with speech_recognition.Microphone() as mic:

                recognizer.adjust_for_ambient_noise(mic, duration=0.2)
                audio = recognizer.listen(mic)

                item = recognizer.recognize_google(audio)
                item = item.lower()

                todo_list.append(item)
                done = True

                speaker.say(f"I added {item} to the todo list!")
                speaker.runAndWait()

        except speech_recognition.UnknownValueError:
            recognizer = speech_recognition.Recognizer()
            speaker.say("I did not understand. Please try again")
            speaker.runAndWait()


def show_todo():

    speaker.say("The item on your todo list are the following")
    for item in todo_list:
        speaker.say(item)
    speaker.runAndWait()


def hello():
    speaker.say("Hello, what can I do for you?")
    speaker.runAndWait()


def quit():
    speaker.say("Bye")
    speaker.runAndWait()
    sys.exit(0)


Mapping = {
    "greeting": hello,
    "create_note": create_note,
    "add_todo": add_todo,
    "show_todo": show_todo,
    "exit": quit
}

assistant = GenericAssistant('intents.json', intent_methods=Mapping)
assistant.train_model()

while True:

    try:
        with speech_recognition.Microphone() as mic:

            recognizer.adjust_for_ambient_noise(mic, duration=0.2)
            audio = recognizer.listen(mic)

            message = recognizer.listen(mic)
            message = message.lower()

        assistant.request(message)
    except speech_recognition.UnknownValueError:
        recognizer = speech_recognition.Recognizer()
