import speech_recognition as sr 
import pyttsx3
import datetime
import subprocess
import wikipedia
import webbrowser
import requests
import geocoder
import math
from geopy.geocoders import Nominatim

chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"

def speak(text):
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	engine.setProperty('voice', voices[1].id)
	engine.setProperty('rate', 180) 
	engine.say(text)
	engine.runAndWait()

def wish_me():
	hour = int(datetime.datetime.now().hour)
	if hour>=0 and hour<12:
		speak("Good Morning!")
	elif hour>=12 and hour<18:
		speak("Good Afternoon!")
	else:
		speak("Good Evening!")
        
def introduction():
	speak("Hello!")
	speak("I'm Friday. An under development fully functional Virtual Assistant, I can take a note of something for you, I can get you the latest headlines, I can get the weather report of your location, can perform various map operations, show you navigations, open google, youtube and search for something you like, tell you current time, fetch some info from the wikipedia.")

def get_audio():
	r = sr.Recognizer() 		#using the speech_recognizer inported as sr
	with sr.Microphone() as source:
		print ("Listening . . .")
		r.pause_threshold = 0.5
		r.adjust_for_ambient_noise(source) 
		audio = r.listen(source) 		#listening to the user through microphone of your laptop/pc
		said=""

		try:
			print("Recognising . . .")
			said = r.recognize_google(audio) 	#storing the said string in said and using the Google API to try and recognize it
			print(f"You just said {(said)} \n")
		
		except Exception as e:
			speak("Sorry! I couldn't get you.")		#printing exceptions if "said" is not recognized

		return said.lower()

def note(text):
	date = datetime.datetime.now()
	file_name = str(date).replace(":", "-") + "-note.txt"
	with open(file_name, "w") as f:
		f.write(text)

	#opening the file and naming it as "file_name" in notepad.exe
	subprocess.Popen(["notepad.exe", file_name])
    
def newstoday():
    news_api_key="2ee76ac0998e4a1c939d4bcc6c6f6b0c"
    main_url="https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey="+news_api_key
    news=requests.get(main_url).json()
    article=news["articles"]
    news_article=[]
    for a in article:
        news_article.append(a['title'])
    for i in range(3):
        print(news_article[i])
        speak(news_article[i])

def weathertoday():
    weather_api="ffd681dd4aa28773eb7c5c85f6b86014"
    g = geocoder.ip('me')
    coordinates=g.latlng
    lat=str(coordinates[0])
    lon=str(coordinates[1])
    main_url="https://api.openweathermap.org/data/2.5/weather?lat="+lat+"&lon="+lon+"&appid="+weather_api
    weather=requests.get(main_url).json()
    temp_city=round((weather['main']['temp'])-273.15)
    description=weather['weather'][0]['description']
    high=math.ceil((weather['main']['temp_max'])-273.15)
    low=math.floor((weather['main']['temp_min'])-273.15)
    speak(f"Its {(temp_city)} with {(description)}, the forcast is with a high of {(high)} and a low of {(low)}")
    
def mapfeatures(text):
    g = geocoder.ip('me')
    coordinates=g.latlng
    lat=str(coordinates[0])
    lon=str(coordinates[1])
    if 'restaurants' or 'restaurant' in text:
        url='https://www.google.co.in/maps/search/Restaurants/@'+lat+','+lon
        speak("I found a few restaurants near you.")
        webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open_new_tab(url)
    elif 'hotel' or 'hotels' in text:
        url='https://www.google.co.in/maps/search/Hotels/@'+lat+','+lon
        speak("I found a few hotels near you.")
        webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open_new_tab(url)
    elif 'grocery' or 'groceries' in text:
        url='https://www.google.co.in/maps/search/Groceries/@'+lat+','+lon
        speak("I found a few groceries near you.")
        webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open_new_tab(url)
    elif 'takeouts' or 'takeout' in text:
        url='https://www.google.co.in/maps/search/Takeout/@'+lat+','+lon
        speak("I found a few take outs near you.")
        webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open_new_tab(url)
        
def navigations(destination):
    g = geocoder.ip('me')
    coordinates=g.latlng
    lat=str(coordinates[0])
    lon=str(coordinates[1])
    geolocator = Nominatim(user_agent="Your_Name")
    location = geolocator.geocode(destination)
    d_lat=str(location.latitude)
    d_lon=str(location.longitude)
    url='https://www.google.co.in/maps/dir/'+lat+','+lon+'/'+destination+'/@'+d_lat+','+d_lon
    speak(f"The best way to get to {(destination)} is:")
    webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open_new_tab(url)
    
def basic_operations(text):
    
    NOTE_STRS = ["make a note", "write down", "remember this"]
    for phrase in NOTE_STRS:
        if phrase in text:
            speak("Sure! What would you like me to note down?")
            note_text = get_audio()
            note(note_text)
            speak("I've made a note of that.")
    
    WEB_INFO = ["information", "wikipedia", "knowledge", "know something"]
    for phrase in WEB_INFO:
        if phrase in text:
            string2 = str(phrase)
            speak("Just a second,")
            text = text.replace(string2, "")
            results = wikipedia.summary(text, sentences=2)
            print("According to Wikipedia " + results)
            speak(results)
            
    if 'time' in text:
        str_time = datetime.datetime.now().strftime("%H:%M %p")
        print(str_time)
        speak(f"Its {(str_time)}")
        
    elif 'open youtube' in text:
        url1 = 'https://www.youtube.com/'
        webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
        print("Opening Youtube . . .")
        webbrowser.get('chrome').open_new_tab(url1)
        
    elif 'open google' in text:
        url2 = 'https://www.google.co.in/'
        webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
        print("Opening Google...")
        webbrowser.get('chrome').open_new_tab(url2)
        
    elif 'search' in text:
        speak("What should I search for?")
        search_keyword = get_audio()
        search_address = 'https://www.google.co.in/search?q='
        new_word = search_address + search_keyword
        print("Searching . . .")
        speak(f"Searching for {(search_keyword)} in Google.")
        webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
        webbrowser.get('chrome').open_new_tab(new_word)
        
    elif 'news' in text:
        print("Getting todays news . . .")
        newstoday()
        
    elif 'weather' in text:
        print("Currently: ")
        weathertoday()
        
    elif 'nearby' in text:
        mapfeatures(text)
        
    elif 'route' in text:
        destination=text.split("to ",1)[1]
        navigations(destination)
        
    elif 'introduce' or 'introduction' in text:
        introduction()
        
def shutting_down(text):
	if 'yeah' or 'yes' or 'quit' or 'quit for now' or 'abort' or 'bye' in text:
		speak("Okey!")

WAKE = "friday"
c=0
flag = 0
print("I'm Online!")

while True:
	text = get_audio()

	if c == 0:

		if text.count(WAKE) > 0 and text.count(WAKE) <= 1:

			wish_me()
			speak("How may I help you?")
			text = get_audio()

			basic_operations(text)
			c+=1

		break

