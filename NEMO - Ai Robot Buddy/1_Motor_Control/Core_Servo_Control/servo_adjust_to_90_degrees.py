"""
Description: Adjusts servo angle to 90 degrees
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

# Fixed angle position
fixed_angle = 90

# Calculate duty cycle for 90 degrees
# For most servos, 90 degrees corresponds to approximately 7.5% duty cycle
# But we'll calculate it precisely based on our min/max values
duty_cycle = MIN_DUTY + (fixed_angle / 180 * (MAX_DUTY - MIN_DUTY))

try:
    print("Positioning servo at 90 degrees...")
    
    # Start PWM with the 90-degree duty cycle
    pwm.start(duty_cycle)
    time.sleep(1)  # Give servo time to reach position
    
    print(f"Servo is now fixed at {fixed_angle} degrees (duty cycle: {duty_cycle:.2f}%)")
    print("Press Ctrl+C to exit")
    
    # Keep the servo at this position
    while True:
        # Periodically refresh the position to ensure it stays in place
        # But use a low refresh rate to prevent jitter
        time.sleep(5)
        pwm.ChangeDutyCycle(duty_cycle)
        time.sleep(0.2)
        pwm.ChangeDutyCycle(0)  # Stop signal to reduce jitter
    
except KeyboardInterrupt:
    print("Program stopped by user")
    
finally:
    # Clean up
    pwm.ChangeDutyCycle(0)
    time.sleep(0.5)
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
