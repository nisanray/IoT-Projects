"""
Description: Sweeps servo between 75-105 degrees (PWM control)
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Use BCM numbering
GPIO.setmode(GPIO.BCM)

# Use GPIO 18 for PWM (supports hardware PWM)
SERVO_PIN = 18
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set PWM at 50Hz
pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

def angle_to_duty_cycle(angle):
    # Converts angle (0 to 180) to duty cycle
    return 2.5 + (angle / 180.0) * 10

try:
    while True:
        # Rotate to 75 degrees (center - 15°)
        pwm.ChangeDutyCycle(angle_to_duty_cycle(75))
        print("Moving to 75°")
        time.sleep(1)

        # Rotate to 105 degrees (center + 15°)
        pwm.ChangeDutyCycle(angle_to_duty_cycle(105))
        print("Moving to 105°")
        time.sleep(1)

except KeyboardInterrupt:
    pass

pwm.stop()
GPIO.cleanup()
