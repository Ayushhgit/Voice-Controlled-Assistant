import pyttsx3
import speech_recognition as sr
import wikipedia as wp
import webbrowser as wb
import datetime
from googleapiclient.discovery import build
import pyjokes
import os
import random as rd

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

api_key = "API-KEY"
youtube = build("youtube", "v3", developerKey=api_key)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def intro():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good Morning")
        print("Good Morning")
    elif 12 <= hour < 16:
        speak("Good Afternoon")
        print("Good Afternoon")
    else:
        print("Good Evening")
        speak("Good Evening")
    print("How may is help you?")
    speak("How may I help you?")

def command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
    try:
        print("Processing...")
        speak("I'm trying to understand what you said. Please wait a moment.")
        query = recognizer.recognize_google(audio, language="en-in")
        print(f"User said: {query}")
        speak(query)
        return query
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand what you said.")
        return None
    except sr.RequestError as e:
        print(f"Could not request results; {e}")
        return None
    
def perform_calc(operation, num1, num2):
    result = None
    if operation == 'addition':
        result = num1 + num2
    elif operation == 'subtraction':
        result = num1 - num2
    elif operation == 'multiplication':
        result = num1 * num2
    elif operation == 'division':
        if num2 != 0:
            result = num1 / num2
        else:
            return "Error: Division by zero"
    return result

def create_file(file_name, file_content):
    try:
        with open(file_name, 'w') as file:
            file.write(file_content)
        print(f"File '{file_name}' created successfully!")
        speak(f"File '{file_name}' created successfully!")
    except Exception as e:
        print(f"Error: {e}")
        speak("An error occurred while creating the file.")


def rules(cc, user_choice):
  uc = user_choice.lower()
  if(cc == uc):
    print("its a draw")
    speak("its a draw")
  elif 'rock' in uc and cc == "paper":
    print("you loose")
    speak("you loose")
  elif 'rock' in uc and cc == "scissors":
    print("you Win")
    speak("you win") 
  elif 'paper' in uc and cc == "rock":
    print("you win")
    speak("you win") 
  elif 'paper' in uc and cc == "scissors":
    print("you loose")
    speak("you loose")
  elif 'scissor' in uc and cc == "paper":
    print("you win") 
    speak("you win") 
  elif 'scissors' in uc and cc == "rock":
    print("you loose")
    speak("you loose")
    


if __name__ == "__main__":
    intro()
    while True:
        query = command().lower()
        if query:
            if 'calculate' in query:
                print("Sure, what would you like to calculate?")
                speak("Sure, what would you like to calculate?")
                squery = command().lower()
                operations = {
                    'addition': '+',
                    'subtraction': '-',
                    'multiplication': '*',
                    'division': '/'
                }
                for operation, symbol in operations.items():
                    if operation in squery:
                        print(f"Please provide the first number for {operation}")
                        speak(f"Please provide the first number for {operation}")
                        tquery = command().lower()
                        num1 = float(tquery)
                        print(f"Please provide the second number for {operation}")
                        speak(f"Please provide the second number for {operation}")
                        fquery = command().lower()
                        num2 = float(fquery)
                        result = perform_calc(operation, num1, num2)
                        if result is not None:
                            print(f"The result of {num1} {symbol} {num2} is {result}")
                            speak(f"The result of {num1} {symbol} {num2} is {result}")
                        else:
                            print("Invalid operation")
                            speak("Invalid operation")
                        break
            

            elif 'play a game' in query:
                print("sure, but i only know Rock paper and scissors. Do you want to play?")
                print("Yes or no?")
                speak("sure,but i only know Rock paper and scissors. Do you want to play?")
                speak("Yes or no?")
                us_res = command().lower()
                if 'yes' in us_res:
                    speak("what do you pick?")
                    print("what do you pick?")
                    user_choice  = command().lower()
                    cc = rd.choice(["rock","paper","scissors","rock","paper"])
                    rules(cc,user_choice)
                    



            elif 'create a file' in query:
                print("Tell me the name of the file you want to create:")
                speak("Tell me the name of the file you want to create:")
                file_name = command().lower()
                print("What should be the content of the file?")
                speak("What should be the content of the file?")
                file_content = command().lower()  
                directory = "files"
                if not os.path.exists(directory):
                  os.makedirs(directory)
                  file_path = os.path.join(directory, file_name)
                  create_file(file_path, file_content)  


            elif 'wikipedia' in query:
                speak("Searching...")
                query = query.replace("wikipedia", "")
                result = wp.summary(query, sentences=3)
                speak("According to Wikipedia")
                print(result)
                speak(result)


            elif 'open instagram' in query:
                wb.open("https://www.instagram.com")


            elif 'open google' in query:
                wb.open("https://www.google.com")


            elif 'open twitter' in query:
                wb.open("https://www.twitter.com")


            elif 'open chatgpt' in query:
                wb.open("https://chat.openai.com")


            elif 'open youtube' in query:
                wb.open("https://www.youtube.com")


            elif 'what is your name' in query:
                speak("I do not have one, im simply a prototype")


            elif 'tell me a joke' in query:
                my_joke = pyjokes.get_joke(language = 'en', category= 'all')   
                print(my_joke)
                speak(my_joke) 
                speak("ha ha ha ha ha")


            elif 'in youtube' in query:
                search_query = query.replace("in youtube", "")
                search_response = youtube.search().list(q=search_query, part="id,snippet", maxResults=10).execute()

                for search_result in search_response.get("items", []):
                    if search_result["id"]["kind"] == "youtube#video":
                        video_title = search_result["snippet"]["title"]
                        video_description = search_result["snippet"]["description"]
                        video_id = search_result["id"]["videoId"]
                        video_url = f"https://www.youtube.com/watch?v={video_id}"

                        print(f"Title: {video_title}")
                        print(f"Description: {video_description}")
                        print(f"URL: {video_url}")
                        print()


            elif 'the time' in query:
                current_time = datetime.datetime.now().strftime("%H:%M:%S")
                print(f"The current time is {current_time}")
                speak(f"The current time is {current_time}")


            elif 'exit' in query:
                print("Goodbye!")
                speak("Goodbye!")
                break


            else:
                print("I'm sorry, I do not have enough information to provide you with that.")
                speak("I'm sorry, I do not have enough information to provide you with that.")