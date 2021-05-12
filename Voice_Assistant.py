import pyttsx3 
import speech_recognition as sr 
import datetime
import wikipedia 
import webbrowser
import os 
import googlemaps
import wolframalpha
import json
import requests
import smtplib
from instabot import Bot
import tweepy
from PIL import Image
from pytesseract import pytesseract
import PyPDF2
from config_secret import Config


engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')  #getting details of current voice
engine.setProperty('voice', voices[1].id)


def speak(audio):
    engine.say(audio)
    engine.runAndWait()  #Without this command, speech will not be audible to us.
    

def wishMe():
    hour = int(datetime.datetime.now().hour)  #takes time
    if hour>=0 and hour<12:
        speak("Good Morning!" )

    elif hour>=12 and hour<16:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!") 

    speak("I am your Desktop Assistant Buddy...How can I help you")
    print("I am your Desktop Assistant Buddy...How can I help you")
    
    

def takeCommand():
     #It takes microphone input from the user and returns string output
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        # r.energy_threshold = 100 
        audio = r.listen(source)

    try:
        print("Recognizing...") 
        #Using google for voice recognition.   
        query = r.recognize_google(audio, language='en-in')
        #User query will be printed.
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)    
        print("Say that again please...")  
        # return "none" string
        return "None"
    return query


def read_pdf(filename):
    # path of the PDF file
    path = open(filename, 'rb')
    # creating a PdfFileReader object
    pdfReader = PyPDF2.PdfFileReader(path)
    # return number of pages
    numpages = pdfReader.numPages
    # print number of pages
    print(numpages)
    speak(f"There are {numpages} pages in the pdf file. Which page should I read?")
    page_no = takeCommand()
    page_no = int(page_no)
    # the page with which you want to start
    page = pdfReader.getPage(page_no)
    # extracting the text from the PDF
    text = page.extractText()
    print(text)
    # reading the text
    speak(text)              


def post_a_tweet(tweet_content):
    # importing all keys from Config_secret
    consumer_key = Config.CONSUMER_KEY
    consumer_secret = Config.CONSUMER_SECRET
    access_token = Config.ACCESS_TOKEN
    access_token_secret = Config.ACCESS_TOKEN_SECRET

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    #updates tweeter
    api.update_status(status=tweet_content)


def upload_to_instagram(image_file_name):
    # creats image object
    image = Image.open(image_file_name)
    # resizeing the image
    new_image = image.resize((1080, 566))
    # new_image.show()
    resized_file_name = 'resized' + image_file_name
    # saving resized image
    new_image.save(resized_file_name)
    # initiating instabot
    bot = Bot()
    # logging in to instagram
    bot.login(username="iamratul986",  password=Config.INSTA_PASSWORD)
    # uploads photo and caption
    bot.upload_photo(resized_file_name, caption="Insta Bot testing")
    #after uploading the file name is changed into name+remove me
    resized_file_name = resized_file_name+'REMOVE_ME'
    try:
        os.remove(resized_file_name) # deletes the resized image 
    except:
        print("Error occured while deleting resized image file")


def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('biswaschandan0957@gmail.com', Config.EMAIL_PASSWORD)
    server.sendmail('biswaschandan0957@gmail.com', to, content)
    server.close()


def imagetovoice(image_file_name):
    image_path = image_file_name

    img = Image.open(image_path)
    pytesseract.tesseract_cmd = Config.PATH_TO_TESSERACT

    text = pytesseract.image_to_string(img)
    print(text)
    speak(text)


if __name__ == "__main__":
    wishMe()
    while True:
        query = takeCommand().lower() #Converting user query into lower case

        # Basic Conversation Logics

        if "how are you" in query:             
            speak("I am well")

        if "buddy" in query:
            speak("Yes friend I am here")

        if "who are you" in query:            
            speak("I am your Personal Desktop AI Assistant Buddy")

        if "what is your name" in query or "your name" in query:
            speak("My name is Buddy.")

        elif "what is" in query or "about" in query or "where" in query:
             
            # Use the same API key
            # that we have generated earlier
            client = wolframalpha.Client("KERTY8-RYKP7W52W9")
            res = client.query(query)
             
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                print("wait a minute")
                speak("let me think...")
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2) 
                speak("According to my information") 
                print(results)
                speak(results)

        elif 'search' in query :
            speak('Searching Sir...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to my information")
            print(results)
            speak(results)

        if "thank" in query:
            speak("you're welcome") 
        
        if "hello" in query:
            speak("Hello sir, I am Buddy")           

        if 'time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(f"Sir, the time is {strTime}")


        #WIKI logics :
            
        if 'wikipedia'in query:
            #if wikipedia found in the query then this block will be executed
            speak('Searching Wikipedia...')
            query = query.replace("wikipedia", "")
            results = wikipedia.summary(query, sentences=2)
            speak("According to Wikipedia")
            print(results)
            speak(results)

        

        if "who is" in query:
             
            # Use the same API key
            # that we have generated earlier
            client = wolframalpha.Client("KERTY8-RYKP7W52W9")
            res = client.query(query)
             
            try:
                print(next(res.results).text)
                speak(next(res.results).text)
            except StopIteration:
                query = query.replace("wikipedia", "")
                results = wikipedia.summary(query, sentences=2) 
                speak("According to my information") 
                print(results)
                speak(results)
                
        elif 'news' in query:
            news = webbrowser.open_new_tab('''https://timesofindia.indiatimes.com/home/headlines''')
            speak('Here are some headlines from the Times of India,Happy reading')
                   
        elif "weather" in query:
            api_key="3534682dfce338a5d50c15f8f4975af1"
            base_url="https://api.openweathermap.org/data/2.5/weather?"
            speak("what is the city name")
            print("what is the city name")
            city_name=takeCommand()
            print(city_name)
            complete_url=base_url+"appid="+api_key+"&q="+city_name
            response = requests.get(complete_url)
            x=response.json()
            if x["cod"]!="404":
                y=x["main"]
                current_temperature = y["temp"]
                current_humidiy = y["humidity"]
                z = x["weather"]
                weather_description = z[0]["description"]
                speak(" Temperature in kelvin unit is " +
                      str(current_temperature) +
                      "\n humidity in percentage is " +
                      str(current_humidiy) +
                      "\n description  " +
                      str(weather_description))
                print(" Temperature in kelvin unit = " +
                      str(current_temperature) +
                      "\n humidity (in percentage) = " +
                      str(current_humidiy) +
                      "\n description = " +
                      str(weather_description))
           
            

        #Youtube logics:

        elif 'open youtube' in query:
            webbrowser.open("youtube.com")

         
        elif 'open code' in query:
            codePath =r'C:\Users\User\AppData\Local\Programs\Microsoft VS Code\Code.exe'
            os.startfile(codePath)
        
        #GOOGLE logics:

        elif 'open google' in query:
            webbrowser.open("google.com")

        elif 'play music' in query:
            music_dir = 'F:\\song'
            songs = os.listdir(music_dir)
            # print(songs)
            os.startfile(os.path.join(music_dir, songs[0]))


        elif 'send a mail' in query:
            try:
                speak(" tell me the address")
                to = takeCommand()
                to = to.replace(" ","")
                to = to.lower()
                to = to+'@gmail.com'
                speak("What should I say")
                content = takeCommand()
                sendEmail(to, content)
                speak("Email has been sent!")
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to send this email")

        elif 'upload to instagram' in query:
            try:
                speak("Which image should I upload?")
                image_file_name = takeCommand()
                image_file_name = image_file_name+'.jpg'
                image_file_name = image_file_name.lower()
                # speak("what is the caption?")
                # print("what is the caption?")
                # caption = takeCommand()
                if (os.path.isfile(image_file_name)):
                    upload_to_instagram(image_file_name)
                    speak("Image uploaded to Instagram")
                else:
                    speak("The file you specified does not exist.")
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to upload this image")
        
        elif 'post a tweet' in query:
            try:
                speak("What message should I tweet?")
                content = takeCommand()
                post_a_tweet(content)
                print("tweet posted succesfully")
                speak("tweet posted succesfully")
            except Exception as e:
                print(e)
                speak("Sorry my friend. I am not able to tweet")

        elif 'read the picture' in query:
            try:
                speak("Which image should I read?")
                image_file_name = takeCommand()
                image_file_name = image_file_name+'.jpg'
                image_file_name = image_file_name.lower()
                if (os.path.isfile(image_file_name)):
                    imagetovoice(image_file_name)
                else:
                    speak("The file you specified does not exist.")
            except Exception as e:
                print(e)

        elif 'read the book' in query:
            try:
                speak("Which book should I read?")
                pdf_file_name = takeCommand()
                pdf_file_name = pdf_file_name+'.pdf'
                pdf_file_name = pdf_file_name.lower()
                if (os.path.isfile(pdf_file_name)):
                    read_pdf(pdf_file_name)
                else:
                    speak("The file you specified does not exist.")
            except Exception as e:
                print(e)
       
	
        #Exit Call
        if "exit" in query:
            speak("Exiting. Nice to talk to you. Bye")
            exit(0)
