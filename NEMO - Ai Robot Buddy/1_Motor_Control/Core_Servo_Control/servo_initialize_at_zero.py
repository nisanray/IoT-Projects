"""
Description: Initializes and positions servo at zero degrees
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for the servo
servo_pin = 18

# Set up the GPIO pin as output
GPIO.setup(servo_pin, GPIO.OUT)

# Create a PWM instance
pwm = GPIO.PWM(servo_pin, 50)  # 50Hz frequency

# Start PWM with 0% duty cycle
pwm.start(0)

def set_angle(angle):
    """Sets the servo to the specified angle."""
    duty = angle / 18 + 2  # Calculate duty cycle (empirically derived)
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1) #allow time for servo to move
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0) #stop sending signal, to prevent servo jitter
    time.sleep(0.02) #short delay

try:
    # Set servo to 0 degrees
    print("Setting servo to 0 degrees...")
    set_angle(0)
    time.sleep(2) #hold the position for 2 seconds

    # Optional: other angles, for testing.
    #print("Setting servo to 90 degrees...")
    #set_angle(90)
    #time.sleep(2)

    #print("Setting servo to 180 degrees...")
    #set_angle(180)
    #time.sleep(2)

except KeyboardInterrupt:
    # Clean up GPIO on Ctrl+C exit
    print("\nCleaning up GPIO...")
    pwm.stop()
    GPIO.cleanup()

finally:
    pwm.stop()
    GPIO.cleanup()
