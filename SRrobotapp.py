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
import Commandrobotapp


def SrRobot():
    with open("transcript.txt", "r") as file:
        context_variable = file.read()

    template = """Answer the question based only on the following context:

    {context}

    Question: {question}

    You must only answer by "command" or "speech".

    For your knowledge, here are some possible commands:
    "left": "go to the left",
    "right": "go to the right",
    "forward": "go forward",
    "ahead": "go forward",
    "backward": "go backward",
    "back": "go backward",
    "u-turn": "make a U-turn",
    "stop": "stop"
    "return to your base": "return to base"
    """

    prompt = PromptTemplate(
        input_variables=["context","question"],
        template=template
    )



    llm = ChatOpenAI(model="gpt-4-1106-preview",temperature=0)
    # The prompt here should take as an input variable the
    # `document_variable_name`

    llm_chain = LLMChain(llm=llm, prompt=prompt)

    query = "Is this transcripted text about a movement command or a speech ?"
    res1 = llm_chain.run(context=context_variable, question=query)
    print(res1)

    if res1 == "command":
        # Define your commands
        commands = ["left", "right", "forward", "ahead", "backward", "back", "u-turn", "stop", "return to your base"]

        # Split the context into words
        words = context_variable.split()

        # Filter the words to get only the commands
        command_list = [word for word in words if word in commands]

        print(command_list)
    return res1

def execute_script3():
        print("Executing script...")
execute_script3(Commandrobotapp)