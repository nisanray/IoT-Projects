"""
Description: MG996R servo angle positioning test
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

# Start PWM at 40 degrees position
min_angle = 40
max_angle = 80

# Calculate duty cycle for 40 degrees
initial_duty = MIN_DUTY + (min_angle / 180 * (MAX_DUTY - MIN_DUTY))
pwm.start(initial_duty)
time.sleep(1)  # Give time for servo to initialize

def set_angle(angle):
    # Convert angle to duty cycle for MG996R
    # Map angle 0-180 to duty cycle MIN_DUTY-MAX_DUTY
    duty_cycle = MIN_DUTY + (angle / 180 * (MAX_DUTY - MIN_DUTY))
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.1)  # Adjusted for smaller movement range

try:
    print(f"Starting continuous {min_angle}-{max_angle} degree rotation...")
    
    # Continuous loop
    while True:
        # Rotate from 40 to 80 degrees
        print(f"Rotating {min_angle} → {max_angle} degrees")
        for angle in range(min_angle, max_angle + 1, 2):  # 2-degree steps for smoother motion
            print(f"  Angle: {angle}°")
            set_angle(angle)
            
        time.sleep(0.3)  # Short pause at 80 degrees
        
        # Rotate from 80 back to 40 degrees
        print(f"Rotating {max_angle} → {min_angle} degrees")
        for angle in range(max_angle, min_angle - 1, -2):  # 2-degree steps
            print(f"  Angle: {angle}°")
            set_angle(angle)
            
        time.sleep(0.3)  # Short pause at 40 degrees
    
except KeyboardInterrupt:
    print("Program stopped by user")
    
finally:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
