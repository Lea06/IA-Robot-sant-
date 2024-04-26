import RPi.GPIO as GPIO
import time
import socket

# GPIO pin definitions
ENA = 17  # PWM for motor A speed
IN1 = 27  # Direction control for motor A
IN2 = 22  # Direction control for motor A
ENB = 18  # PWM for motor B speed
IN3 = 23  # Direction control for motor B
IN4 = 24  # Direction control for motor B
ldr_pin = 5
trigger_pin = 6
echo_pin = 13
light_threshold = 700
sonar_threshold = 200

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup([ENA, IN1, IN2, ENB, IN3, IN4], GPIO.OUT)
GPIO.setup([ldr_pin, echo_pin], GPIO.IN)
GPIO.setup(trigger_pin, GPIO.OUT)

# PWM initialization for speed control
pwm_a = GPIO.PWM(ENA, 100)
pwm_b = GPIO.PWM(ENB, 100)
pwm_a.start(0)
pwm_b.start(0)

def drive_forward():
    GPIO.output([IN1, IN4], GPIO.HIGH)
    GPIO.output([IN2, IN3], GPIO.LOW)
    pwm_a.ChangeDutyCycle(100)
    pwm_b.ChangeDutyCycle(100)

def stop():
    GPIO.output([ENA, ENB], GPIO.LOW)
    pwm_a.stop()
    pwm_b.stop()

def sonar_ping():
    GPIO.output(trigger_pin, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(trigger_pin, GPIO.LOW)
    start_time = time.time()
    while GPIO.input(echo_pin) == 0:
        start_time = time.time()
    while GPIO.input(echo_pin) == 1:
        stop_time = time.time()
    elapsed_time = stop_time - start_time
    distance = (elapsed_time * 34300) / 2
    return distance

# Server setup for listening to commands
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.listen(5)

print("Waiting for connections...")
client, address = server.accept()
print(f"Connection established with {address}")

try:
    while True:
        command = client.recv(1024).decode()
        print("Command received:", command)
        
        if command == "forward":
            drive_forward()
        elif command == "stop":
            stop()
        else:
            print("Command not recognized")

        ldr_reading = GPIO.input(ldr_pin)
        sonar_distance = sonar_ping()
        print("LDR Reading:", ldr_reading)
        print("Distance Reading:", sonar_distance)

        if ldr_reading < light_threshold or sonar_distance < sonar_threshold:
            stop()
            print("Stopping due to low light or detected obstacle")
            break

        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()