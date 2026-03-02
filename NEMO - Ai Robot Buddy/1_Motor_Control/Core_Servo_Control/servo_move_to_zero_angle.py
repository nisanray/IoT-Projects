"""
Description: Moves single servo to zero angle position
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO 18 as output
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)

# Set PWM frequency to 50Hz
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def set_angle(angle):
    # Convert angle to duty cycle (for typical servos)
    duty = 2.5 + (angle / 18)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # stop sending signal after move to prevent jitter

try:
    print("Setting servo to 0 degrees")
    set_angle(0)

finally:
    pwm.stop()
    GPIO.cleanup()
