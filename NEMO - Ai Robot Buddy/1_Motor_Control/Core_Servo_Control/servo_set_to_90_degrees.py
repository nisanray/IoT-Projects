"""
Description: Sets servo to 90 degrees (center position)
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Use BCM pin numbering
GPIO.setmode(GPIO.BCM)

# Set GPIO 17 as output
servo_pin = 18
GPIO.setup(servo_pin, GPIO.OUT)

# Set PWM frequency to 50Hz (standard for servos)
pwm = GPIO.PWM(servo_pin, 50)
pwm.start(0)

def set_angle(angle):
    duty = 2 + (angle / 18)  # Maps 0-180 to ~2-12% duty cycle
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)

try:
    # Set servo to 90 degrees
    set_angle(90)
    time.sleep(1)

finally:
    pwm.stop()
    GPIO.cleanup()
