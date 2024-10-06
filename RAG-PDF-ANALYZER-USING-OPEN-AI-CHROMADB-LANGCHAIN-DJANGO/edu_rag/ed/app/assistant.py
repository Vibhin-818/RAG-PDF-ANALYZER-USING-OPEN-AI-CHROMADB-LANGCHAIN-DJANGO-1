# assistant.py
import webbrowser
import wikipedia
import pyttsx3
import speech_recognition as sr
import datetime
import os
import pywhatkit as kit
import sys
from requests import get
import pyjokes
import smtplib

# Initialize the voice engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)

def speak(audio):
    engine.say(audio)
    print(audio)
    engine.runAndWait()

def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Listening...')
        r.pause_threshold = 1
        audio = r.listen(source, timeout=7, phrase_time_limit=6)
    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-US')
        print(f"User said: {query}")
    except Exception as e:
        speak("Say that again please")
        return "none"
    return query

def wish():
    hour = int(datetime.datetime.now().hour)
    if hour >= 0 and hour <= 12:
        speak("Good morning")
    elif hour > 12 and hour < 18:
        speak("Good afternoon")
    else:
        speak("Good evening")
    speak("I am Jarvis, sir. Please tell me how can I help you.")

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('your_email@gmail.com', 'your_password')
    server.sendmail('your_email@gmail.com', to, content)
    server.close()

def jarvis(query):
    if "hello jarvis" in query:
        speak("Hello sir")
    elif "open notepad" in query:
        npath = "C:\\Users\\saivi\\Desktop\\Notepad.txt"
        os.startfile(npath)
    elif "open chrome" in query:
        wpath = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        os.startfile(wpath)
    elif "open command prompt" in query:
        os.system("start cmd")
    elif "play movie" in query:
        mmc = "E:\\folder\\28aug\\salar.mkv"
        os.startfile(mmc)
    elif "ip address" in query:
        ip = get('http://api.ipify.org').text
        speak(f"Your IP address is {ip}")
    elif "open youtube" in query:
        webbrowser.open("www.youtube.com")
    elif "open instagram" in query:
        webbrowser.open("www.instagram.com")
    elif "send message" in query:
        kit.sendwhatmsg("+919535349517", "hi", 1, 1)
    elif "wikipedia" in query:
        speak("Searching Wikipedia")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        speak(results)
    elif "open google" in query:
        speak("Sir, what should I search?")
        cm = takecommand().lower()
        webbrowser.open(f"{cm}")
    elif "play song on youtube" in query:
        kit.playonyt("Kurchi Madathapetti")
    elif "tell a joke" in query:
        joke = pyjokes.get_joke()
        speak(joke)
    elif "email to varun" in query:
        try:
            speak("What should I say?")
            content = takecommand().lower()
            to = "vam22ainds@cmrit.ac.in"
            sendEmail(to, content)
            speak("Email sent successfully")
        except Exception as e:
            speak("Sorry, I could not send the email")
    elif "no thanks" in query:
        speak("Goodbye sir")
        sys.exit()
    elif "none" in query:
        speak("Hasta la vista, bye!")
        sys.exit()
    else:
        speak("I can't do that")
