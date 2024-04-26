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
import SRrobotapp


def STTrobotapp():
    with sr.Microphone() as source:
        print("Listening...")

        # Adjust for ambient noise levels
        r.adjust_for_ambient_noise(source)

        # Capture the audio input from the user
        audio = r.listen(source)
    # Create a recognizer object
    try:
        # Use the recognizer to convert speech to text
        text = r.recognize_google(audio)
        print("You said:", text)

        # Save the transcribed text to a file
        with open("transcript.txt", "w") as file:
            file.write(text + "\n")

    except sr.UnknownValueError as e:
        print("Sorry, I could not understand your speech.")

    except sr.RequestError as e:
        print("Sorry, an error occurred. Please check your internet connection.")

def execute_script2():
        print("Executing script...")
execute_script2(SRrobotapp)