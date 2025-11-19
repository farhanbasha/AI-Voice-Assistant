import speech_recognition as sr
import webbrowser
import pyttsx3
from youtube_search import YoutubeSearch
import pyjokes
import edge_tts
import asyncio
import threading
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1" #to hide pygame startup banner
import pygame
import wikipedia
import requests
import time
import google.generativeai as genai
import re
from pathlib import Path

recognizer = sr.Recognizer()
engine = pyttsx3.init()
newsapi = "News_API_Here"
GEMINI_API_KEY = "Gemini_API_Key_Here"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.5-flash')

def speak(text):
    engine.say(text)
    engine.runAndWait()
    return

def speakNatural(text, voice="en-US-AndrewNeural"):
    def tts_thread(text):
        async def _speak_async():
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save("voice.mp3")
        asyncio.run(_speak_async())
        play_audio("voice.mp3")
        os.remove("voice.mp3")
    
    threading.Thread(target=tts_thread, args=(text,)).start()

def play_audio(file_path): 
    try:
        pygame.mixer.init()
        pygame.mixer.music.load(file_path)
        pygame.mixer.music.play()
        
        # Wait while the audio is playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)
        
        pygame.mixer.quit()
    except Exception as e:
        print(f"Audio playback error: {e}")
def process_gemini(comm):
    prompt = f"Reply in short, consise sentences. {comm}"
    response = model.generate_content(prompt)
    reply = response.text
    if "code" or "program" not in comm:
        speakNatural(reply)
    print(reply)
    return
def processCommand(c):
    if "play" in c.lower():
        song_name = c.replace("play ","")
        results = YoutubeSearch(song_name, max_results=1).to_dict()
        if results:
            url = "https://www.youtube.com" + results[0]['url_suffix']
        
        if url:
            speak(f"Playing {song_name}")
            webbrowser.open(f"{url}")
            return "exit"
        else:
            speak("Song Not Found")
            print("Song Not Found!")
    elif "search" in c.lower() and "about" not in c.lower():
        webbrowser.open(f"https://www.google.com/search?q={c.replace("search","")}")
    elif "open" in c.lower():
        temp = c.replace("open","").replace(" ","")
        webbrowser.open(f"https://{temp.lower()}.com")
    elif "joke" in c.lower():
        jokes = pyjokes.get_joke()
        speakNatural(jokes)
        print(jokes)

    elif "news" in c.lower():
        newspage = ""
        url = "https://newsapi.org/v2/top-headlines"
        params = {
        "country": "us",       
        "pageSize": 5,         #number of headlines
        "apiKey": newsapi
        }
        response = requests.get(url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data["status"] == "ok":
                speak(" Top Headlines:")
                for i, article in enumerate(data["articles"], start=1):
                    title = article["title"]
                    source = article["source"]["name"]
                    newspage += f"{i}. {title} \n"
                speakNatural(newspage)
            else:
                print("Error:", data)
        else:
            print("HTTP Error:", response.status_code, response.text)
    elif "wikipedia" in c.lower():
        query = c.replace("wikipedia", "")
        result = wikipedia.summary(query, sentences=1)
        speakNatural(f"According to wikipedia:{result}")
    else:
        process_gemini(c.lower())
def commandListener():
    #speak("Initializing...")
    play_audio("Initializing.mp3")
    while True:
        r = sr.Recognizer()
        
        # recognize speech using Google
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source)
            word = r.recognize_google(audio)
            
            if "hello" in word.lower():
                #speak("Yes sir")
                play_audio("yesSir.mp3")
                with sr.Microphone() as source:
                    print("Assistant Activated...")
                    r.pause_threshold = 1.5  # wait longer (default is 0.8)
                    r.energy_threshold = 300
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)
            if word.lower() == "exit":
                #speak("Goodbye Sir")
                play_audio("GoodByeSir.mp3")
                return
            print(r.recognize_google(audio))
        except Exception as e:
            print("Audio Error!; {0}".format(e))
            #speak("Pardon me sir, please repeat")
#main program
if __name__ == "__main__":
    commandListener()
