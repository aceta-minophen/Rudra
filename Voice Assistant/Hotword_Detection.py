import os
import speech_recognition as sr
import main4
import subprocess

def takeCommand1():
    r = sr.Microphone()
    #my_mic = sr.Microphone(device_index=1)
    with sr.Microphone() as source:
        print("Listening Hotword...")
        r = sr.Recognizer()
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration=5)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(audio)
        print(f"User said: {query}\n")

    except Exception as e:

        print("Say that again")
        return "none"
    return query.lower()


while True:
    wake_up = takeCommand1()
    
    if 'hey rudra' in wake_up or 'rudra' in wake_up:
        os.startfile('D:\\rudra\\main4.py')
        # exec(open("main4.py").read())
        # subprocess.call("python codes\main2.py", shell=True)
        # main2.wishMe()
        # os.system('python main4.py')

    else:
        print("nothing")
