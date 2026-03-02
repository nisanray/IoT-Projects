"""
Description: Servo movement test with zero position
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

# Start PWM at 0 degrees position
pwm.start(2.5)
time.sleep(1)

def set_angle(angle):
    # Convert angle to duty cycle (0 degrees = 2.5, 180 degrees = 12.5)
    duty_cycle = 2.5 + (angle / 180 * 10)
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)  # Give the servo time to reach position

try:
    print("Starting 3 rotation cycles...")
    
    # Perform 3 complete rotation cycles
    for cycle in range(1, 4):
        print(f"Cycle {cycle} of 3")
        
        # Rotate from 0 to 180 degrees
        print("  Rotating 0 → 180 degrees")
        for angle in range(0, 181, 5):
            set_angle(angle)
            
        time.sleep(0.5)  # Short pause at 180 degrees
        
        # Rotate from 180 back to 0 degrees
        print("  Rotating 180 → 0 degrees")
        for angle in range(180, -1, -5):
            set_angle(angle)
            
        time.sleep(0.5)  # Short pause at 0 degrees
    
    # Ensure final position is 0 degrees
    print("Completed 3 cycles. Resetting to 0 degrees position.")
    set_angle(0)
    time.sleep(1)  # Hold at 0 degrees
    
    print("Test complete!")
    
except KeyboardInterrupt:
    print("Program stopped by user")
    
finally:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
