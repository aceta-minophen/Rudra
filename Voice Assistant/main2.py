from __future__ import print_function
import datetime
from heapq import merge
from sqlite3 import Time
from tkinter.messagebox import YES
from typing import Any, List
import speech_recognition as sr
import pyttsx3
import wikipedia
import requests
import pyjokes
from urllib.request import urlopen
import json
import datetime
import time
from playsound import playsound
from pywikihow import search_wikihow
import webbrowser as web
import pytz
#import spotipy
from google_apis import Create_Service
#from spotipy import oauth2
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase import Firebase

SCOPES = ['https://www.googleapis.com/auth/calendar',
          'https://www.googleapis.com/auth/calendar.events']
DAYS = ["monday", "tuesday", "wednesday",
        "thursday", "friday", "saturday", "sunday"]
MONTHS = ["january", "february", "march", "april", "may", "june",
          "july", "august", "september", "october", "november", "december"]
DAY_EXTENTIONS = ["rd", "th", "st", "nd"]
client_file = 'Credentials.json'
API_NAME = 'calendar'
API_VERSION = 'v3'
cred = credentials.Certificate(
    'rudra-x-firebase-adminsdk-e2s77-2a7119b4c9.json')

firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://rudra-x-default-rtdb.firebaseio.com/'
})

engine = pyttsx3.init()
voices = engine.getProperty('voices')

config = {
    "apiKey": "AIzaSyA3sxz8LTLgtvdkvBAaLvZO7gBLqzuLM_A",
    "authDomain": "rudra-x.firebaseapp.com",
    "databaseURL": "https://rudra-x-default-rtdb.firebaseio.com/",
    "storageBucket": "rudra-x.appspot.com"
}
firebase = Firebase(config)
db1 = firebase.database()

ref = db.reference('Computer Vision/Action Recognition/Drinking Water')
value = ref.get()
refEat = db.reference('Computer Vision/Action Recognition/Eating Food')
valueEat = refEat.get()
refExp = db.reference('Computer Vision/Expression Detection')
valueExp = refExp.get()
refMealLike = db1.child('Meal Suggestion/Liked meals/')
valueMealLike = refMealLike.get()
refMealPrev = db.reference('Meal Suggestion/Previous meals')
valueMealPrev = refMealPrev.get()
refMealSuggestLog = db.reference('Meal Suggestion/Food log/')
valueMealLog = refMealSuggestLog.get()


def AddEvent():
    service = Create_Service(client_file, API_NAME, API_VERSION, SCOPES)
    response = service.events().quickAdd(
        calendarId='primary',
        text="rudra meeting at 3pm").execute()
    speak("  event   added  ")


def NewsFromBBC():

    query_params = {
        "source": "bbc-news",
        "sortBy": "top",
        "apiKey": "f8fa80f2816f417f8db3ed3b73305f44"
    }
    main_url = " https://newsapi.org/v1/articles"

    res = requests.get(main_url, params=query_params)
    open_bbc_page = res.json()

    article = open_bbc_page["articles"]

    results = []

    for ar in article:
        results.append(ar["title"])

    for i in range(len(results)):
        print(i + 1, results[i])

    speak(results)


def authenticate_google():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    return service


def get_events(day, service):

    date = datetime.datetime.combine(day, datetime.datetime.min.time())
    end_date = datetime.datetime.combine(day, datetime.datetime.max.time())
    utc = pytz.UTC
    date = date.astimezone(utc)
    end_date = end_date.astimezone(utc)

    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(), timeMax=end_date.isoformat(),
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        speak('No upcoming events found.')

    else:
        speak(f"you have {len(events)} events on this day.")

        # Prints the start and name of the next 10 events
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
        start_time = str(start.split("T")[1].split("+")[0])

        if int(start_time.split(":")[0]) < 12:
            start_time = start_time + "am"
        else:
            start_time = str(int(start_time.split(":")[0])-12)
            start_time = start_time + "pm"

        speak(event["summary"] + " at " + start_time)


def get_date(query):
    query = query.lower()
    today = datetime.date.today()

    if query.count("today") > 0:
        return today

    day = -1
    day_of_week = -1
    month = -1
    year = today.year

    for word in query.split():
        if word in MONTHS:
            month = MONTHS.index(word) + 1
        elif word in DAYS:
            day_of_week = DAYS.index(word)
        elif word.isdigit():
            day = int(word)
        else:
            for ext in DAY_EXTENTIONS:
                found = word.find(ext)
                if found > 0:
                    try:
                        day = int(word[:found])
                    except:
                        pass

    if month < today.month and month != -1:
        year = year+1
    if day < today.day and month == -1 and day != -1:
        month = today.month + 1
    if month == -1 and day == -1 and day_of_week != -1:
        current_day_of_week = today.weekday()  # 0-6
        dif = day_of_week - current_day_of_week

        if dif < 0:
            dif += 7
            if query.count("next") >= 1:
                dif += 7

        return today + datetime.timedelta(dif)
    if month == -1 or day == -1:
        return None
    return datetime.date(month=month, day=day, year=year)


def MusicFromSpotify():
    username = 'hw8sspurqbiei21c3pkx62n2s'
    clientID = '1d5fc82690934924867ee9617bee42a5'
    clientSecret = '46c70ba6cb924692b5710fb1d73d345c'
    redirectURI = 'https://open.spotify.com/'
    oauth_object = oauth2.SpotifyOAuth(clientID, clientSecret, redirectURI)
    token_dict = oauth_object.get_access_token()
    token = token_dict['access_token']
    spotifyObject = spotipy.Spotify(auth=token)
    user = spotifyObject.current_user()
    print(json.dumps(user, sort_keys=True, indent=4))
    while True:
        # print("Welcome, "+ user['display_name'])
        # print("0 - Exit")
        # print("1 - Search for a Song")
        speak("What song will you like to listen?")
        #searchQuery = takeCommand()
        # if choice == 1:
        # Get the Song Name.
        searchQuery = input("Enter Song Name: ")
        # Search for the Song.
        searchResults = spotifyObject.search(searchQuery, 1, 0, "track")
        # Get required data from JSON response.
        tracks_dict = searchResults['tracks']
        tracks_items = tracks_dict['items']
        song = tracks_items[0]['external_urls']['spotify']
        # Open the Song in Web Browser
        # playsound(song)
        web.open(song)
        print('Song has opened in your browser.')


def Water_Log():
    count = value["Waterlog"]
    speak("Are you drinking water?")
    reac = takeCommand()
    if(reac == "yes"):
        ref.update({'Confirmed': True})
        ref.update({'Waterlog': count+1})
        speak("Great, this will help you stay hydrated")
        ref.update({'Detected': False})


def EatingFood():
    speak('nice to have meal')
    hr = int(datetime.datetime.now().hour)
    if(6 < hr < 10):
        refEatBreak = db.reference(
            'Computer Vision/Action Recognition/Eating Food/Food log/Breakfast')
        speak("Are you having your breakfast?")
        react = takeCommand()
        if(react == "yes"):
            refEat.update({'Confirmed': True})
            refEatBreak.update({'Done': True})
            speak("what are you eating?")
            meal = takeCommand()
            refEatBreak.update({'Meal': meal})
            speak("How would you rate it on the scale of 1 to 10")
            ans = takeCommand()
            refMealSuggestLog.update({'rating1': ans})
            count = valueMealLog["meal_num"]
            refMealSuggestLog.update({'meal_num': count+1})
            speak("I hope you are having something light in your breakfast, Hope you enjoy it while taking care of yourself")
            refEat.update({'Detected': False})
    elif(12 < hr < 15):
        refEatLunch = db.reference(
            'Computer Vision/Action Recognition/Eating Food/Food log/Lunch')
        speak("Are you having your lunch?")
        react = takeCommand()
        if(react == "yes"):
            refEat.update({'Confirmed': True})
            refEatLunch.update({'Done': True})
            speak("I hope you are having something light in your lunch, Hope you enjoy it while taking care of yourself")
            refEat.update({'Detected': False})
    elif(19 < hr < 21):
        refEatDinner = db.reference(
            'Computer Vision/Action Recognition/Eating Food/Food log/Dinner')
        speak("Are you having your dinner?")
        react = takeCommand()
        if(react == "yes"):
            refEat.update({'Confirmed': True})
            refEatDinner.update({'Done': True})
            speak("I hope you are having something light in your dinner, Hope you enjoy it while taking care of yourself")
            refEat.update({'Detected': False})
    else:
        speak("Good, you should not keep your stomach empty. haha")


def ExpressionRecogHappy():

    speak("You seem happy, is there anything speacial?")
    react = takeCommand()
    if(react == "yes"):
        speak("Great")
        refExp.update({'Happy': False})
    elif(react == "no"):
        speak("It's good to be happy")
        refExp.update({'Happy': False})


def ExpressionRecogSad():

    speak("Is there something bothering you?")
    react = takeCommand()
    if(react == "yes"):
        speak("It's ok, everything will be fine")
        refExp.update({'Happy': False})
    elif(react == "no"):
        speak("Nice, if there is anyything, you can share it with me")
        refExp.update({'Happy': False})

# TODO


def MealSuggestLike():
    sort = query.replace("food like", "")
    speak(f"you want to eat something like {sort}?")
    refMealLike.update({'meal1': sort})
    # react = takeCommand()
    # if(react == "yes"):
    speak("okay let me see")
    result = refMealLike.child("meal1").get().val()
    # result=result1.val()
    print(result)


# def MealSuggestPrevious():
#     speak("let me check your previous meal")
#     new1 = valueMealPrev["meal1"]
#     new2 = valueMealPrev["meal2"]
#     speak(f"according to your previous meal i will recommend you to have {new1} or {new2} now")


def speak(audio):

    engine.say(audio)
    engine.runAndWait()


def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour < 9:
        speak("Good Morning friend. How are you feeling today?",)

    elif hour >= 12 and hour < 16:
        speak(
            "Good Afternoon. I am sure you achieved the targets of the day. You still have some time to complete your tasks.")

    elif hour >= 16 and hour < 18:
        speak("Good evening. It's time to wrap up the things and plan for some fun time.")

    elif hour >= 18 and hour < 20:
        speak("Good evening. Take your dinner and go out for a walk.")

    elif hour >= 20:
        speak("Good night my friend. How was your day today?")

    else:
        speak("hey")


def My_Location():
    ip_add = requests.get('https://api.ifify.org').text
    url = 'https://get.geojs.io/v1/ip/geo/' + ip_add + '.json'
    geo = requests.get(url)
    geo_d = geo.json()
    state = geo_d(['city'])
    country = geo_d(['country'])
    region = geo_d(['region'])
    speak(f"you are now in {state, country, region}")


def takeCommand():
    r = sr.Microphone()
    #my_mic = sr.Microphone(device_index=1)
    with sr.Microphone() as source:
        print("Listening...")
        r = sr.Recognizer()
        r.pause_threshold = 0.5
        r.adjust_for_ambient_noise(source, duration=5)
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        speak(audio)
        print(f"User said: {query}\n")

    except Exception as e:

        print("Say that again")
        return "none"
    return query


if __name__ == "__main__":
    wishMe()
    while True:

        query = takeCommand().lower()

        if 'wikipedia' in query:
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            speak(results)

        elif 'joke' in query:
            speak("here's a joke")
            speak(pyjokes.get_joke())

        elif 'how are you' in query:
            speak("I am fine, Thank you")
            speak("How are you?")

        elif 'i am fine' in query or "i am good" in query:
            speak("It's good to know that you are doing fine")

        elif 'it was good' in query:
            speak('great')

        elif 'not so good' in query or 'it was okay' in query:
            speak('not an issue..., hope you enjoy it next time')

        elif 'music' in query or "song" in query or 'play' in query:
            MusicFromSpotify()

        elif 'stop' in query:
            speak("ok, will stop")

        elif 'read' in query:
            speak("what kind of book will you prefer")

        elif 'thank you' in query:
            speak("Not a problem, I am here if you need me")

        elif 'what should i have in breakfast' in query:
            speak("according to your last meal i would suggest")

        elif 'podcast' in query:
            speak("which podcast will you like to listen")

        elif "don't listen" in query or "stop listening" in query:
            speak("for how much time you want me to stop from listening commands")
            a = int(takeCommand())
            time.sleep(a)

        elif "remember that" in query or "add event" in query:
            AddEvent()

        elif "did I tell you to remember something for me" in query or "what do i have" in query or "what am i doing" in query or "do i have something scheduled" in query or "schedule" in query:
            SERVICE = authenticate_google()
            date = get_date(query)
            if date:
                get_events(date, SERVICE)
            else:
                speak("I didn't quite get that")

        elif "alarm" in query:
            speak("at what time you want to set the alarm")
            time = takeCommand()

            while True:
                Time_Ac = datetime.datetime.now()
                now = Time_Ac.strftime("%H%M%S")

                if now == time:
                    speak("Time to wake up sir")
                    playsound('abc.mp3')
                    speak("alarm closed")
                elif now > time:
                    break

        elif 'news' in query:
            NewsFromBBC()

        elif "weather" in query:

            api_key = "31af4f2a83bb0ce586f8e374b220d047"

            base_url = "http://api.openweathermap.org/data/2.5/weather?"

            # speak(" City name ")
            # print("City name : ")
            # city_name = takeCommand()
            city_name = input("Enter city name")

            complete_url = base_url + "appid=" + api_key + "&q=" + city_name

            response = requests.get(complete_url)

            x = response.json()

            if x["cod"] != "404":

                y = x["main"]

                current_temperature = y["temp"]

                current_pressure = y["pressure"]

                current_humidiy = y["humidity"]

                z = x["weather"]

                weather_description = z[0]["description"]

                print(" Temperature (in kelvin unit) = " +
                      str(current_temperature) +
                      "\n atmospheric pressure (in hPa unit) = " +
                      str(current_pressure) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))

            else:
                print(" City Not Found ")

        elif "how to" in query:
            speak("let me see")
            op = query.replace("rudra", "")
            max_result = 1
            how_to_func = search_wikihow(op, max_result)
            assert len(how_to_func) == 1
            # how_to_func[0].print()
            speak(how_to_func[0].summary)

        elif "what is my location" in query:
            My_Location()

        elif "feeling low" in query or "feeling a bit low" in query:
            speak("what will you prefer to lift your mood, music or jokes?")

        elif "what is your name" in query:
            speak("I am Rudra")

        elif "what do you do?" in query:
            speak("I am here to help you and take care of your needs")

        elif "why do you follow me?" in query:
            speak("because i want to be your friend. I enjoy your company")

        elif "add to my liked meals" in query:
            speak(f"updated your liked meals")

        elif(value["Detected"] == True):
            Water_Log()

        elif(valueEat["Detected"] == True):
            EatingFood()

        elif(valueExp["Happy"] == True):
            ExpressionRecogHappy()

        elif(valueExp["Upset"] == True):
            ExpressionRecogSad()

        elif "food like" in query or "something to eat like" in query:
            MealSuggestLike()
