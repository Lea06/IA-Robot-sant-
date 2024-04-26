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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import STTTrobotapp
import SRrobotapp
from SRrobotapp import res1
from SRrobotapp import command_list

class CommandExecutor:
    def __init__(self):
        # Pin setup
        self.motorLeftA = 17
        self.motorLeftB = 18
        self.motorRightA = 22
        self.motorRightB = 23

        # Set up GPIO pins
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.motorLeftA, GPIO.OUT)
        GPIO.setup(self.motorLeftB, GPIO.OUT)
        GPIO.setup(self.motorRightA, GPIO.OUT)
        GPIO.setup(self.motorRightB, GPIO.OUT)

    # Function to control motors
    def control_motors(self, leftA, leftB, rightA, rightB, duration=None):
        GPIO.output(self.motorLeftA, leftA)
        GPIO.output(self.motorLeftB, leftB)
        GPIO.output(self.motorRightA, rightA)
        GPIO.output(self.motorRightB, rightB)
        if duration:
            time.sleep(duration)
            self.stop_motors()

    def stop_motors(self):
        GPIO.output(self.motorLeftA, False)
        GPIO.output(self.motorLeftB, False)
        GPIO.output(self.motorRightA, False)
        GPIO.output(self.motorRightB, False)

    # Command functions
    def go_left(self, duration=1):
        self.control_motors(True, False, False, True, duration)

    def go_right(self, duration=1):
        self.control_motors(False, True, True, False, duration)

    def go_forward(self, duration=1):
        self.control_motors(True, False, True, False, duration)

    def go_backward(self, duration=1):
        self.control_motors(False, True, False, True, duration)

    def make_u_turn(self, duration=2):
        self.go_right(duration)

    def return_to_base(self):
        # Example sequence to return to base
        print("Returning to base...")
        self.go_backward(2)
        self.go_left(1)
        self.go_forward(3)
        self.stop()
        print("Arrived at base")

    def stop(self):
        self.stop_motors()

    def execute_command(self, command):
        # Dictionary mapping commands to functions
        commands = {
            "left": self.go_left,
            "right": self.go_right,
            "forward": self.go_forward,
            "ahead": self.go_forward,
            "backward": self.go_backward,
            "back": self.go_backward,
            "u-turn": self.make_u_turn,
            "stop": self.stop,
            "return to base": self.return_to_base
        }

        if command in commands:
            commands[command]()
        else:
            print("Unknown command:", command)


class SpeechProcessor:
    def process_speech(self):
        with open("transcript.txt", "r") as file:
            context_variable = file.read()

            template = """Synthetise the following conversation:

            {context}
            You must capable of:
            - Understand the context of the conversation. 
                Example 1: A patient requires medical attention.
                Example 2: A doctor is talking to a patient.
                Example 3: A doctor is giving you information.
            - Differenciate the different persons in the conversation.
            """

            prompt = PromptTemplate(
             input_variables=["context"],
             template=template
            )

            llm = ChatOpenAI(model="gpt-4-1106-preview",temperature=0)
                # The prompt here should take as an input variable the
                # `document_variable_name`

            llm_chain = LLMChain(llm=llm, prompt=prompt)
            
            res_speech = llm_chain.run(context=context_variable)
            # Save the synthesized speech to a file
            with open("synthesized_speech.txt", "w") as file:
                file.write(res_speech)


command_executor = CommandExecutor()
speech_processor = SpeechProcessor()

if res1 == "command":
        for command in command_list:
            command_executor.execute_command(command)
elif res1 == "speech":
        speech_processor.process_speech()
        def send_email():
            # Email configuration
            sender_email = "arthur.perrot@epitech.digital"
            receiver_email = "arthur.perrot@epitech.digital"
            subject = "Synthesized Speech"
            message = "Please find the synthesized speech attached."

            # Create a multipart message
            email_message = MIMEMultipart()
            email_message["From"] = sender_email
            email_message["To"] = receiver_email
            email_message["Subject"] = subject

            # Attach the synthesized speech file
            with open("synthesized_speech.txt", "r") as file:
                attachment = MIMEText(file.read())
                attachment.add_header("Content-Disposition", "attachment", filename="synthesized_speech.txt")
                email_message.attach(attachment)

            # Send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, "your_password")
                server.send_message(email_message)

        # Call the send_email function
        send_email()

