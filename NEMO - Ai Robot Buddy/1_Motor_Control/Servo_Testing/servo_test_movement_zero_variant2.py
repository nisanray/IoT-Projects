"""
Description: Servo movement test - variant 2
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

# The MG996R typically expects PWM values between 2.2ms and 12.8ms
# which corresponds to duty cycles of approximately 2.2% to 12.8%
MIN_DUTY = 2.2
MAX_DUTY = 12.8

# Start PWM at 0 degrees position
pwm.start(MIN_DUTY)
time.sleep(1)  # Give time for servo to initialize

def set_angle(angle):
    # Convert angle to duty cycle for MG996R
    # Map angle 0-180 to duty cycle MIN_DUTY-MAX_DUTY
    duty_cycle = MIN_DUTY + (angle / 180 * (MAX_DUTY - MIN_DUTY))
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.15)  # MG996R is a heavier servo, give it time to reach position

try:
    print("Starting continuous 0-100 degree rotation...")
    
    # Continuous loop
    while True:
        # Rotate from 0 to 100 degrees
        print("Rotating 0 → 100 degrees")
        for angle in range(0, 101, 5):  # 5-degree steps for smoother motion
            print(f"  Angle: {angle}°")
            set_angle(angle)
            
        time.sleep(0.5)  # Short pause at 100 degrees
        
        # Rotate from 100 back to 0 degrees
        print("Rotating 100 → 0 degrees")
        for angle in range(100, -1, -5):  # 5-degree steps
            print(f"  Angle: {angle}°")
            set_angle(angle)
            
        time.sleep(0.5)  # Short pause at 0 degrees
    
except KeyboardInterrupt:
    print("Program stopped by user")
    
finally:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
