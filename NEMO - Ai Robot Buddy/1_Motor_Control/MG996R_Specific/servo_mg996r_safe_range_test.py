"""
Description: MG996R servo with safe PWM range
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

# Adjusted PWM values for MG996R (these may need fine-tuning for your specific servo)
MIN_DUTY = 3.0  # Increased from 2.2 to avoid stalling at lower bound
MAX_DUTY = 12.0  # Decreased from 12.8 to avoid stalling at upper bound

# Movement range
min_angle = 40
max_angle = 80

# Start PWM with no signal
pwm.start(0)
time.sleep(0.5)  # Brief pause

def set_angle(angle):
    # Convert angle to duty cycle with safety margins
    duty_cycle = MIN_DUTY + (angle / 180 * (MAX_DUTY - MIN_DUTY))
    
    # Apply PWM
    pwm.ChangeDutyCycle(duty_cycle)
    time.sleep(0.15)  # Give servo time to reach position
    
    # Turn off PWM after positioning to reduce jitter and prevent locking
    pwm.ChangeDutyCycle(0)
    time.sleep(0.05)  # Brief pause

try:
    print(f"Starting {min_angle}-{max_angle} degree rotation with anti-locking measures...")
    
    counter = 0
    
    # Continuous loop
    while True:
        # Rotate from min_angle to max_angle
        print(f"Rotating {min_angle} → {max_angle} degrees")
        for angle in range(min_angle, max_angle + 1, 5):  # Increased step size to reduce stress
            print(f"  Angle: {angle}°")
            set_angle(angle)
            
        time.sleep(0.2)  # Reduce pause time
        
        # Rotate from max_angle back to min_angle
        print(f"Rotating {max_angle} → {min_angle} degrees")
        for angle in range(max_angle, min_angle - 1, -5):  # Increased step size
            print(f"  Angle: {angle}°")
            set_angle(angle)
            
        time.sleep(0.2)  # Reduce pause time
        
        # Every 5 cycles, give servo a rest to prevent overheating
        counter += 1
        if counter % 5 == 0:
            print("Giving servo a brief rest to prevent overheating...")
            pwm.ChangeDutyCycle(0)  # Stop sending PWM signal
            time.sleep(1)  # Rest for 1 second
    
except KeyboardInterrupt:
    print("Program stopped by user")
    
finally:
    # Clean up
    pwm.ChangeDutyCycle(0)
    time.sleep(0.5)
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
