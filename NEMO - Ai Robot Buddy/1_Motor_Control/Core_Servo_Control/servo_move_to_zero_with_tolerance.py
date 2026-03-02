"""
Description: Moves servo to zero with angle tolerance
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Use BCM GPIO numbering
GPIO.setmode(GPIO.BCM)

# Define servo control pin
servo_pin = 15
GPIO.setup(servo_pin, GPIO.OUT)

# Set PWM frequency to 50Hz (standard for servos)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def move_servo_to_left():
    duty = 2.5  # Duty cycle for 0 degrees (full left for most servos)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Stop signal to prevent jitter

try:
    print("Moving servo to full left (0°)...")
    move_servo_to_left()

finally:
    pwm.stop()
    GPIO.cleanup()
