"""
Description: Continuous servo requiring signal loop
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Configuration
SERVO_PIN = 17  # GPIO pin connected to the servo
FREQUENCY = 50  # PWM frequency (Hz)

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Create PWM instance
pwm = GPIO.PWM(SERVO_PIN, FREQUENCY)
pwm.start(0)

try:
    print("Servo continuous rotation test")
    
    # For MG995 modified for continuous rotation:
    # Try different values between 2-12% duty cycle
    # 7.5% is typically neutral (stop)
    # Values above 7.5% rotate one direction
    # Values below 7.5% rotate the other direction
    
    # Rotate continuously clockwise
    print("Rotating clockwise continuously...")
    
    # Important: Use a loop to continuously send the signal
    # This is crucial - a single command won't maintain rotation!
    for _ in range(200):  # Send signal for ~10 seconds
        pwm.ChangeDutyCycle(9.5)  # Try 8.5-10.5 if this doesn't work
        time.sleep(0.05)  # Small delay between updates
    
    # Stop
    print("Stopping...")
    for _ in range(20):  # Send stop signal for ~1 second
        pwm.ChangeDutyCycle(7.5)  # Neutral position
        time.sleep(0.05)
    
    # Rotate continuously counter-clockwise
    print("Rotating counter-clockwise continuously...")
    for _ in range(200):  # Send signal for ~10 seconds
        pwm.ChangeDutyCycle(5.5)  # Try 4.5-6.5 if this doesn't work
        time.sleep(0.05)
    
    # Stop
    print("Stopping...")
    for _ in range(20):
        pwm.ChangeDutyCycle(7.5)
        time.sleep(0.05)
    
    print("Test complete")

except KeyboardInterrupt:
    print("\nProgram stopped by user")
    
finally:
    # Clean up
    pwm.stop()
    GPIO.cleanup()
    print("GPIO cleaned up")
