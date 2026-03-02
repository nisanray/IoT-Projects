"""
Description: Advanced servo movement test
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Clean up any previous GPIO setup
GPIO.cleanup()

# Set up GPIO
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM instance with 50Hz frequency
pwm = GPIO.PWM(servo_pin, 50)

# Start PWM
pwm.start(7.5)  # Start at middle position (90 degrees)
time.sleep(1)

try:
    while True:
        # Move to 0 degrees (minimum position)
        print("Moving to 0 degrees")
        pwm.ChangeDutyCycle(2.5)
        time.sleep(1)
        
        # Move to 90 degrees (middle position)
        print("Moving to 90 degrees")
        pwm.ChangeDutyCycle(7.5)
        time.sleep(1)
        
        # Move to 180 degrees (maximum position)
        print("Moving to 180 degrees")
        pwm.ChangeDutyCycle(12.5)
        time.sleep(1)
        
        # Return to 90 degrees (middle position)
        print("Returning to 90 degrees")
        pwm.ChangeDutyCycle(7.5)
        time.sleep(1)

except KeyboardInterrupt:
    print("Program stopped by user")
    
finally:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
