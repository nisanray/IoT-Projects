"""
Description: Servo movement test - variant 1
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
# MG996R operates at standard 50Hz frequency
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
    print("Starting 3 rotation cycles with MG996R servo...")
    
    # Perform 3 complete rotation cycles
    for cycle in range(1, 4):
        print(f"Cycle {cycle} of 3")
        
        # Rotate from 0 to 180 degrees
        print("  Rotating 0 → 180 degrees")
        for angle in range(0, 181, 10):  # 10-degree steps for MG996R (it's a stronger servo)
            print(f"    Angle: {angle}°")
            set_angle(angle)
            
        time.sleep(0.5)  # Short pause at 180 degrees
        
        # Rotate from 180 back to 0 degrees
        print("  Rotating 180 → 0 degrees")
        for angle in range(180, -1, -10):  # 10-degree steps
            print(f"    Angle: {angle}°")
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
