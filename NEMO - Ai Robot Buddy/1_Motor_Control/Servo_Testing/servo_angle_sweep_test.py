"""
Description: Tests servo angle sweep (0°-180°)
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Pin configuration
SERVO_PIN = 17  # Use GPIO 17 (Physical pin 11)

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set PWM to 50Hz (standard for servos)
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def set_angle(angle):
    """Set servo angle (0 to 180 degrees)"""
    duty = 2 + (angle / 18)
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

try:
    while True:
        print("Moving to 0°")
        set_angle(0)
        time.sleep(1)
        
        print("Moving to 90°")
        set_angle(90)
        time.sleep(1)
        
        print("Moving to 180°")
        set_angle(180)
        time.sleep(1)

except KeyboardInterrupt:
    print("Stopped by User")

finally:
    pwm.stop()
    GPIO.cleanup()
