"""
Description: Continuous rotation variant 2
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# GPIO Pins
SERVO1_PIN = 17
SERVO2_PIN = 18

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

# Initialize PWM
pwm1 = GPIO.PWM(SERVO1_PIN, 50)
pwm2 = GPIO.PWM(SERVO2_PIN, 50)
pwm1.start(0)
pwm2.start(0)

# Helper: Stop motors safely
def stop_both():
    pwm1.ChangeDutyCycle(7.5)
    pwm2.ChangeDutyCycle(7.5)
    time.sleep(0.5)
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

# Rotate both forward
def rotate_both_forward(speed=1.5, duration=0.6):
    print("→ Rotating forward")
    pwm1.ChangeDutyCycle(7.5 - speed)
    pwm2.ChangeDutyCycle(7.5 - speed)
    time.sleep(duration)
    stop_both()

# Rotate both backward
def rotate_both_backward(speed=1.5, duration=0.6):
    print("← Rotating backward")
    pwm1.ChangeDutyCycle(7.5 + speed)
    pwm2.ChangeDutyCycle(7.5 + speed)
    time.sleep(duration)
    stop_both()

# Main loop
try:
    while True:
        rotate_both_forward()
        time.sleep(1)
        rotate_both_backward()
        
        print("⏳ Waiting 5 seconds...")
        stop_both()
        time.sleep(5)

except KeyboardInterrupt:
    print("🔌 Stopped by user")

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
