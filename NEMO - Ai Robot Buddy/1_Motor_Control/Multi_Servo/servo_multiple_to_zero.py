"""
Description: Moves multiple servos to zero position
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Define GPIO pins connected to servos
servo_pins = [11, 12, 15, 16]

# Use Broadcom pin numbering
GPIO.setmode(GPIO.BOARD)  # Use BOARD if you refer to pin numbers like 11,12,15,16

# Initialize all pins
for pin in servo_pins:
    GPIO.setup(pin, GPIO.OUT)

# Create PWM objects at 50Hz
pwms = [GPIO.PWM(pin, 50) for pin in servo_pins]

# Start PWM and set to 0 degrees (usually ~5% duty cycle)
for pwm in pwms:
    pwm.start(0)
    pwm.ChangeDutyCycle(5)  # Adjust this value depending on your servo
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Stop sending signal to avoid buzzing

try:
    while True:
        time.sleep(1)  # Keep program running

except KeyboardInterrupt:
    pass

# Clean up
for pwm in pwms:
    pwm.stop()
GPIO.cleanup()
