import pyaudio
import speech_recognition as sr
import os
from langchain.chains import StuffDocumentsChain, LLMChain
from langchain_core.prompts import PromptTemplate
from langchain_community.llms import OpenAI
from langchain.chat_models import ChatOpenAI
os.environ['OPEN_API_KEY']='sk-proj-MgwdEZ7nwXLtf5poVrUrT3BlbkFJo77w3iUBszaxUHlVio3n'
import RPi.GPIO as GPIO
import time
import STTTrobotapp

r = sr.Recognizer()

# Function to listen for the wake word
def listen_for_wake_word(wake_word="hey Carl"):
    with sr.Microphone() as source:
        print("Listening for wake word...")
        audio = r.listen(source)

    try:
        text = r.recognize_google(audio, language="en-US")
        if wake_word.lower() in text.lower():
            print("Wake word detected!")
            return True
        else:
            return False
    except sr.UnknownValueError:
        print("Could not understand audio")
    except sr.RequestError as e:
        print(f"Error; {e}")

    return False

# Function to execute after wake word is detected
def execute_script():
    print("Executing script...")
    # Add your script code here

# Main loop
while True:
    if listen_for_wake_word():
        execute_script(STTTrobotapp)