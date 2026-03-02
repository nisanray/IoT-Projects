"""
Description: Tests servo speed control with percentage values
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Configuration
SERVO_PIN = 17  # GPIO pin connected to the servo signal wire (adjust as needed)
FREQUENCY = 50  # Standard servo PWM frequency is 50Hz

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create PWM instance
pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
pwm.start(0)  # Start with 0% duty cycle

def set_servo_speed(speed):
    """
    Controls the speed and direction of a continuous rotation servo
    
    Args:
        speed: Value between -100 and 100 representing speed percentage
               0 = stop, 100 = full forward, -100 = full reverse
    """
    # Convert speed (-100 to 100) to duty cycle (typically 5-10 for servos)
    # 7.5 is typically the center/stop position
    if speed > 100:
        speed = 100
    if speed < -100:
        speed = -100
        
    # Map the speed to a duty cycle (adjust these values for your specific servo)
    # For continuous rotation servos, values slightly above/below the neutral point
    # will cause the servo to rotate in different directions
    if speed == 0:
        duty_cycle = 7.5  # Neutral/stop position (adjust as needed)
    elif speed > 0:
        # Forward rotation (adjust range as needed)
        duty_cycle = 7.5 + (speed / 100.0) * 2.5
    else:
        # Reverse rotation (adjust range as needed)
        duty_cycle = 7.5 - (abs(speed) / 100.0) * 2.5
    
    pwm.ChangeDutyCycle(duty_cycle)

try:
    print("Servo control started. Press Ctrl+C to exit.")
    
    # Example movement sequence
    print("Rotating clockwise at 50% speed")
    set_servo_speed(50)
    time.sleep(3)
    
    print("Stopping")
    set_servo_speed(0)
    time.sleep(1)
    
    print("Rotating counter-clockwise at 70% speed")
    set_servo_speed(-70)
    time.sleep(3)
    
    print("Stopping")
    set_servo_speed(0)
    
    # Continuous rotation demo
    print("\nStarting continuous rotation demo:")
    print("Use Ctrl+C to exit")
    
    while True:
        # Ask for speed
        try:
            speed = float(input("Enter speed (-100 to 100, 0 to stop): "))
            set_servo_speed(speed)
        except ValueError:
            print("Please enter a number between -100 and 100")

except KeyboardInterrupt:
    print("\nExiting program")
    
finally:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
