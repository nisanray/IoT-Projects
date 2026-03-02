"""
Description: MG996R servo setup and testing
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

# Adjusted PWM values for MG996R
MIN_DUTY = 3.0
MAX_DUTY = 12.0

# Movement range
center_angle = 90
min_angle = 60
max_angle = 120

def set_angle(angle):
    # Convert angle to duty cycle
    duty_cycle = MIN_DUTY + (angle / 180 * (MAX_DUTY - MIN_DUTY))
    
    # Apply PWM
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.05)  # Give servo time to reach position
    
    # Turn off PWM after positioning to reduce jitter
    pwm.ChangeDutyCycle(0)
    time.sleep(0.05)

try:
    # Start at center position (90 degrees)
    print(f"Setting initial position to {center_angle} degrees...")
    center_duty = MIN_DUTY + (center_angle / 180 * (MAX_DUTY - MIN_DUTY))
    pwm.start(center_duty)
    time.sleep(1)  # Give servo time to reach position
    pwm.ChangeDutyCycle(0)  # Stop signal to reduce jitter
    time.sleep(0.1)
    
    print(f"Starting continuous rotation between {min_angle} and {max_angle} degrees...")
    
    counter = 0
    
    # Continuous loop
    while True:
        # Rotate from center to max
        print(f"Rotating {center_angle} → {max_angle} degrees")
        for angle in range(center_angle, max_angle + 1, 5):
            print(f"  Angle: {angle}°")
            set_angle(angle)
            
        time.sleep(0.05)  # Pause at max angle
        
        # Rotate from max back to min
        print(f"Rotating {max_angle} → {min_angle} degrees")
        for angle in range(max_angle, min_angle - 1, -5):
            print(f"  Angle: {angle}°")
            set_angle(angle)
            
        time.sleep(0.05)  # Pause at min angle
        
        # Rotate from min back to center
        print(f"Rotating {min_angle} → {center_angle} degrees")
        for angle in range(min_angle, center_angle + 1, 5):
            print(f"  Angle: {angle}°")
            set_angle(angle)
            
        time.sleep(0.05)  # Pause at center
        
        # Every 5 cycles, give servo a brief rest
        counter += 1
        if counter % 5 == 0:
            print("Giving servo a brief rest...")
            time.sleep(1)
    
except KeyboardInterrupt:
    print("Program stopped by user")
    
finally:
    # Clean up
    pwm.ChangeDutyCycle(0)
    time.sleep(0.5)
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
