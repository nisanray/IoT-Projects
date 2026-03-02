"""
Description: Synchronizes movement of two servos
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Define GPIO pins
SERVO1_PIN = 17  # Left motor
SERVO2_PIN = 18  # Right motor

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

# Initialize PWM with 50Hz frequency
pwm1 = GPIO.PWM(SERVO1_PIN, 50)
pwm2 = GPIO.PWM(SERVO2_PIN, 50)
pwm1.start(0)
pwm2.start(0)

def stop_both():
    pwm1.ChangeDutyCycle(7.5)  # Stop
    pwm2.ChangeDutyCycle(7.5)
    time.sleep(1)

def forward_both(speed=1.5):
    duty = 7.5 - speed  # Forward direction
    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    time.sleep(1)

def backward_both(speed=1.5):
    duty = 7.5 + speed  # Backward direction
    pwm1.ChangeDutyCycle(duty)
    pwm2.ChangeDutyCycle(duty)
    time.sleep(1)

try:
    while True:
        print("Rotating BOTH forward")
        forward_both()
        time.sleep(2)

        print("Stopping BOTH")
        stop_both()
        time.sleep(1)

        print("Rotating BOTH backward")
        backward_both()
        time.sleep(2)

        print("Stopping BOTH")
        stop_both()
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
