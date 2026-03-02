"""
Description: Tests continuous servo rotation forward/backward
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

SERVO_PIN = 17  # Use GPIO17 (Pin 11)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set 50Hz PWM frequency
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def stop_servo():
    pwm.ChangeDutyCycle(7.5)  # Neutral position for stop
    time.sleep(1)

def rotate_forward(speed=1):
    duty = 7.5 - speed  # Decrease from 7.5 for forward
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)

def rotate_backward(speed=1):
    duty = 7.5 + speed  # Increase from 7.5 for backward
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)

try:
    print("Forward")
    rotate_forward(1.5)  # max ~2.5 for full speed
    time.sleep(2)

    print("Stop")
    stop_servo()
    time.sleep(1)

    print("Backward")
    rotate_backward(1.5)
    time.sleep(2)

    print("Stop")
    stop_servo()

except KeyboardInterrupt:
    print("Exiting...")

finally:
    pwm.stop()
    GPIO.cleanup()
