import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os
import smtplib
from PyDictionary import PyDictionary
import random
import plyer as pl
from youtubesearchpython import VideosSearch


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()


def wishMe(start):
    hour = int(datetime.datetime.now().hour)
    if start == True:
        if hour>=0 and hour<12:
            speak("Good Morning!")

        elif hour>=12 and hour<18:
            speak("Good Afternoon!")   

        else:
            speak("Good Evening!")  

        speak("I am David Sir. Good to see you again.")
    else:
        speak('Goodbye sir')
        if hour>=0 and hour<12:
            speak("Have a good day!")

        elif hour>=18 and hour<24:
            speak("Have a good night!")   
            
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}\n")

    except Exception as e:  
        print("Say that again please...")  
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('omkar.kulkarni20@vit.edu', '12010457@ok')
    server.sendmail('omkar.kulkarni20@vit.edu', to, content)
    server.close()
    
def waterReminder():
    M = int(datetime.datetime.now().minute)    
    if M == 0 or M == 30:
        pl.notification.notify(
            title= 'Break Reminder.',
            message= 'Hey, take a break and drink some water.',
            timeout=60
        )
        speak("Hello sir, time to take a short break")
    
def setReminder(reminders):
    speak("At what time do you want me to remind you?")
    reminder_time = takeCommand().lower()
    speak('What do you want me to remind you of?')
    content = takeCommand()
    
    try:
        reminder_time = reminder_time.replace(':', ' ').split()
        reminder_time[0], reminder_time[1] = int(reminder_time[0]), int(reminder_time[1])
        if ('p.m.' in reminder_time) and reminder_time[0]<12:
            reminder_time[0] += 12
        elif 'a.m.' in reminder_time and reminder_time[0]==12:
            reminder_time[0] = 0
        reminder_time[2] = content
        reminders.append(reminder_time)
        speak('Reminder was successfully set')
    except:
        speak('Could not set the reminder')

def checkReminder(reminders):
    H = int(datetime.datetime.now().hour)
    M = int(datetime.datetime.now().minute)
    for timestamp in reminders:
        if H == timestamp[0] and M == timestamp[1]:
            pl.notification.notify(
                title= 'Reminder from David',
                message= timestamp[2],
                timeout= 60,
                app_icon = 'david.ico'
            )
            speak(f'Sir, here  is a reminder to {timestamp[2]}')
            reminders.remove(timestamp)
            
def wordForTheDay():
    while True:
        f = open('words.txt', 'r')
        wordlist = f.readlines()
        f.close()
        word = wordlist[random.randint(0, 10000)]
        meanings = PyDictionary.meaning(word)
        try:
            means = '\n'.join(value[0] for value in meanings.values())
            break
        except:
            pass
    pl.notification.notify(
        title = 'Word for the Day',
        message = f'{word.capitalize()} {means}',
        timeout = 60,
        app_icon = 'david.ico'
    )
    

            
def Tasks(query):
    if 'search in browser' in query:
        query = query.replace('search in browser', '')
        webbrowser.open(f'https://www.google.com/search?q={query}')
                
    elif 'search in youtube' in query:
        query = query.replace('search in youtube', '')
        webbrowser.open(f'https://www.youtube.com/results?search_query={query}')
        
                
                
    if 'search in wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)

    elif 'open youtube' in query:
        webbrowser.open("youtube.com")

    elif 'open google' in query:
        webbrowser.open("google.com")

    elif 'open stackoverflow' in query:
        webbrowser.open("stackoverflow.com")   
                    
    elif 'open v i e r p' in query:
        webbrowser.open("learner.vierp.in/home")


    elif 'play music' in query:
        music_dir = 'D:\\Music\\timepass'
        songs = os.listdir(music_dir)
        print(songs)    
        os.startfile(os.path.join(music_dir, songs[0]))

    elif 'what is the time' in query:
        strTime = datetime.datetime.now().strftime("%H:%M:%S")    
        speak(f"Sir, the time is {strTime}")

    elif 'open vs' in query:
        codePath = "C:\\Users\\omkar\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"
        os.startfile(codePath)
                
    elif 'open whatsapp' in query:
        codePath = "C:\\Users\\omkar\\AppData\\Local\\WhatsApp\\WhatsApp.exe"
        os.startfile(codePath)

    elif 'email to myself' in query:
        try:
            speak("What should I say?")
            content = takeCommand()
            to = "jay.kumbharkar20@vit.edu"    
            sendEmail(to, content)
            speak("Email has been sent!")
        except Exception as e:
            print(e)
            speak("Sorry, could not send the email.")
        
        

if __name__ == "__main__":
    wishMe(True)
    wordForTheDay()
    reminders = []
    while True:
    # if 1:
        query = takeCommand().lower()

        # Logic for executing tasks based on query
        if query == 'hey david':
            speak('hello sir! How can I help you?')
            
            
            while True:
                query = takeCommand().lower()
                
                if 'set reminder' in query or 'set a reminder' in query:
                    setReminder(reminders)
                
                Tasks(query)
                
                if 'play in youtube' in query:
                    query = query.replace('play in youtube', '')
                    videosSearch = VideosSearch(query, limit = 1)
                    url = videosSearch.result()['result'][0]['link']
                    webbrowser.open(url)
                    break
                
                if 'introduce yourself' in query:
                    speak('''Hello! I am DAVID. I am a desktop assistance created by K1 group from VIT DESH 2021 for code with python course project. I can perform various taks like opening an app, setting reminder, open websites in browser, search in wikipedia, search a video in youtube, search a query in google and so on. Before telling me task you have to say, 'hey david' to enter task-mode, and after completion you have to say, 'thank you david', to exit task mode. In the same task mode you can ask me to play music or even to play a video on youtube and I will do it immediately. I can even send emails to specified clients. I can tell you the current time whenever you ask me in task-mode. I have some in built features like water reminder that will remind you to take a short break every 30 mins and word for the day feature that will show you a random english word with its meaning. To exit from the program say "goodbye david". Thank you! Special thanks to the developers of the modules and packages that were used in my creation.''')
                        
                if 'thank you david' in query:
                    speak('You are welcome sir!')
                    break
                
                waterReminder()
                checkReminder(reminders)
                
                
        waterReminder()
        checkReminder(reminders)
                
                    
        if 'goodbye david' in query:
            wishMe(False)
            exit(0)