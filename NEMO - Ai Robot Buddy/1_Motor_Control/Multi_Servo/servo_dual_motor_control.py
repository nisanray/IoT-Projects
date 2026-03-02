"""
Description: Controls two continuous rotation servos
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Define pins for each servo
SERVO1_PIN = 17  # Left motor
SERVO2_PIN = 18  # Right motor

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

# Set PWM frequency to 50Hz
pwm1 = GPIO.PWM(SERVO1_PIN, 50)
pwm2 = GPIO.PWM(SERVO2_PIN, 50)
pwm1.start(0)
pwm2.start(0)

def stop_servo(pwm):
    pwm.ChangeDutyCycle(7.5)  # Stop signal
    time.sleep(1)

def rotate_forward(pwm, speed=1):
    duty = 7.5 - speed  # <7.5 for forward
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)

def rotate_backward(pwm, speed=1):
    duty = 7.5 + speed  # >7.5 for backward
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)

try:
    while True:
        print("Servo 1 Forward")
        rotate_forward(pwm1, 1.5)
        time.sleep(2)
        print("Servo 1 Stop")
        stop_servo(pwm1)
        time.sleep(1)

        print("Servo 2 Backward")
        rotate_backward(pwm2, 1.5)
        time.sleep(2)
        print("Servo 2 Stop")
        stop_servo(pwm2)
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by user")

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
