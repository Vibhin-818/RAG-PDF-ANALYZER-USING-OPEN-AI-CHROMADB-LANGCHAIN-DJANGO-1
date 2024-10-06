import pyttsx3
import speech_recognition as sr
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

# Initialize TTS engine
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to recognize speech
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            speak("Sorry, the speech service is not available.")
            return ""

# Function to find the search bar with the given attributes
def find_search_bar(driver):
    try:
        # Try finding the search bar by 'id' (specific to the input you shared)
        search_box = driver.find_element(By.ID, "searchInput")
        return search_box
    except:
        pass
    try:
        # If 'id' fails, try finding by 'name' as a fallback
        search_box = driver.find_element(By.NAME, "search")
        return search_box
    except:
        pass
    
    # If no search bar is found, return None
    return None

# Function to open the browser and perform actions based on voice commands
def voice_control_browser():
    # Manually set the website URL
    site = "https://www.wikipedia.org"  # You can change this to any website URL
    driver = webdriver.Chrome()  # or webdriver.Firefox()
    driver.maximize_window()

    speak(f"Opening {site}")
    driver.get(site)

    while True:
        speak("What would you like to do next?")
        command = recognize_speech()

        if 'scroll down' in command:
            driver.execute_script("window.scrollBy(0, 500);")
            speak("Scrolling down")
        elif 'scroll up' in command:
            driver.execute_script("window.scrollBy(0, -500);")
            speak("Scrolling up")
        elif 'go back' in command:
            driver.back()
            speak("Going back")
        elif 'go forward' in command:
            driver.forward()
            speak("Going forward")
        elif 'search for' in command:
            speak("What do you want to search for?")
            search_query = recognize_speech()
            if search_query:
                search_box = find_search_bar(driver)
                if search_box:
                    try:
                        search_box.clear()
                        search_box.send_keys(search_query)
                        search_box.send_keys(Keys.RETURN)
                        speak(f"Searching for {search_query}")
                    except Exception as e:
                        speak(f"Could not perform the search. Error: {str(e)}")
                else:
                    speak("Sorry, I could not find the search box on this page.")
        elif 'type in' in command:
            input_text(driver)  # Call the function to handle typing in text fields
        elif 'exit' in command or 'close browser' in command:
            speak("Closing the browser")
            driver.quit()
            break
        else:
            speak("Sorry, I did not understand the command.")

# Function to type text into a field
def input_text(driver):
    speak("Which field would you like to type in? Say something like 'search bar' or 'form'.")
    field_type = recognize_speech()
    
    if 'search' in field_type:
        search_box = find_search_bar(driver)
        if search_box:
            try:
                speak("What would you like to type?")
                text_to_type = recognize_speech()
                if text_to_type:
                    search_box.clear()
                    search_box.send_keys(text_to_type)
                    search_box.send_keys(Keys.RETURN)
                    speak(f"Typed {text_to_type} into the search bar")
            except Exception as e:
                speak(f"Sorry, I could not interact with the search bar. Error: {str(e)}")
        else:
            speak("Sorry, I could not find the search bar.")
    else:
        speak("Currently, I can only handle the search bar. More input fields will be supported later.")

if __name__ == "__main__":
    voice_control_browser()
