"""
Description: Continuous servo with direction control
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

SERVO_PIN = 17  # Use GPIO17 (Pin 11)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set PWM frequency to 50Hz
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def stop_servo():
    pwm.ChangeDutyCycle(7.5)  # Stop signal
    time.sleep(1)

def rotate_forward(speed=1):
    duty = 7.5 - speed  # Lower than 7.5 to rotate forward
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)

def rotate_backward(speed=1):
    duty = 7.5 + speed  # Higher than 7.5 to rotate backward
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)

try:
    while True:
        print("Rotating forward")
        rotate_forward(1.5)  # Adjust speed (0.5 to 2.5)
        time.sleep(2)

        print("Stopping")
        stop_servo()
        time.sleep(1)

        print("Rotating backward")
        rotate_backward(1.5)
        time.sleep(2)

        print("Stopping")
        stop_servo()
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    pwm.stop()
    GPIO.cleanup()
