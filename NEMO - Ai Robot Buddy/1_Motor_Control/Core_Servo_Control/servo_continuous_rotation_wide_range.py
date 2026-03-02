"""
Description: Continuous rotation with wider angle range
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# GPIO Pins
SERVO1_PIN = 17
SERVO2_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

# Set PWM frequency
pwm1 = GPIO.PWM(SERVO1_PIN, 50)
pwm2 = GPIO.PWM(SERVO2_PIN, 50)
pwm1.start(0)
pwm2.start(0)

def stop_both():
    pwm1.ChangeDutyCycle(7.5)
    pwm2.ChangeDutyCycle(7.5)
    time.sleep(1)

def rotate_both_forward(speed=1.5, duration=0.6):  # wider turn
    duty = 7.5 - speed
    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    time.sleep(duration)
    stop_both()

def rotate_both_backward(speed=1.5, duration=0.6):  # wider turn
    duty = 7.5 + speed
    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    time.sleep(duration)
    stop_both()

try:
    while True:
        print("WIDE FORWARD")
        rotate_both_forward(speed=1.5, duration=0.6)

        time.sleep(1)

        print("WIDE BACKWARD")
        rotate_both_backward(speed=1.5, duration=0.6)

        time.sleep(1)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
