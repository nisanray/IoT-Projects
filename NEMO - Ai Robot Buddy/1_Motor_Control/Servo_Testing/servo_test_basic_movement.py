"""
Description: Basic servo movement test
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Set up GPIO
servo_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(servo_pin, GPIO.OUT)

# Create PWM instance with 50Hz frequency
# 50Hz is standard for most servo motors
pwm = GPIO.PWM(servo_pin, 50)

# Start PWM with 0 duty cycle
pwm.start(0)

def set_angle(angle):
    # Convert angle to duty cycle
    # Typical servo expects duty cycle between 2.5% (0 degrees) and 12.5% (180 degrees)
    duty = angle / 18 + 2.5
    GPIO.output(servo_pin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)  # Give the servo time to reach the position
    GPIO.output(servo_pin, False)
    pwm.ChangeDutyCycle(0)  # Stop the PWM signal to prevent jitter

try:
    while True:
        # Rotate from 0 to 180 degrees
        print("Rotating from 0 to 180 degrees...")
        for angle in range(0, 181, 5):  # Increment by 5 degrees for smoother movement
            print(f"Angle: {angle}")
            set_angle(angle)
            time.sleep(0.1)  # Small delay between angle changes
        
        time.sleep(1)  # Pause at 180 degrees
        
        # Rotate from 180 to 0 degrees
        print("Rotating from 180 to 0 degrees...")
        for angle in range(180, -1, -5):  # Decrement by 5 degrees
            print(f"Angle: {angle}")
            set_angle(angle)
            time.sleep(0.1)  # Small delay between angle changes
            
        time.sleep(1)  # Pause at 0 degrees

except KeyboardInterrupt:
    # Clean up on Ctrl+C
    pwm.stop()
    GPIO.cleanup()
    print("Servo test stopped by user")

finally:
    # Clean up on normal exit
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
