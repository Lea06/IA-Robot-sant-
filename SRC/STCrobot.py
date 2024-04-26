import RPi.GPIO as GPIO
import time

class CommandExecutor:
    def __init__(self):
        # Setup GPIO pins for motor control
        self.setup_pins()

    def setup_pins(self):
        self.motorLeftA = 17
        self.motorLeftB = 18
        self.motorRightA = 22
        self.motorRightB = 23
        GPIO.setmode(GPIO.BCM)
        GPIO.setup([self.motorLeftA, self.motorLeftB, self.motorRightA, self.motorRightB], GPIO.OUT)

    def control_motors(self, leftA, leftB, rightA, rightB, duration=None):
        GPIO.output(self.motorLeftA, leftA)
        GPIO.output(self.motorLeftB, leftB)
        GPIO.output(self.motorRightA, rightA)
        GPIO.output(self.motorRightB, rightB)
        if duration:
            time.sleep(duration)
            self.stop_motors()

    def stop_motors(self):
        GPIO.output([self.motorLeftA, self.motorLeftB, self.motorRightA, self.motorRightB], False)

    def execute_command(self, command):
        # Map commands to motor actions
        command_actions = {
            "left": lambda: self.control_motors(True, False, False, True, 1),
            "right": lambda: self.control_motors(False, True, True, False, 1),
            "forward": lambda: self.control_motors(True, False, True, False, 1),
            "backward": lambda: self.control_motors(False, True, False, True, 1),
            "stop": self.stop_motors
        }
        
        action = command_actions.get(command)
        if action:
            action()
        else:
            print("Unknown command:", command)

class SpeechProcessor:
    # Process speech from text file
    def process_speech(self):
        with open("transcript.txt", "r") as file:
            text = file.read()
            # Processing logic here
            print("Processed speech:", text)

# Example usage
command_executor = CommandExecutor()
speech_processor = SpeechProcessor()

# Example command execution
command_executor.execute_command("forward")
speech_processor.process_speech()