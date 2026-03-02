"""
Description: Basic robot dance with synchronized servo movement
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# GPIO Pins
SERVO1_PIN = 17
SERVO2_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO1_PIN, GPIO.OUT)
GPIO.setup(SERVO2_PIN, GPIO.OUT)

# Set PWM frequency
pwm1 = GPIO.PWM(SERVO1_PIN, 50)
pwm2 = GPIO.PWM(SERVO2_PIN, 50)
pwm1.start(0)
pwm2.start(0)

# Helper to move to angle
def set_servo_angle(pwm, angle):
    # Convert angle (0-180) to duty cycle (2.5-12.5)
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)

def move_servos(angle):
    set_servo_angle(pwm1, angle)
    set_servo_angle(pwm2, angle)

try:
    print("Moving both servos to 0 degrees")
    move_servos(0)
    time.sleep(1)

    for i in range(3):
        print(f"Cycle {i+1}: Moving to 10 degrees")
        move_servos(10)
        time.sleep(0.5)

        print(f"Cycle {i+1}: Returning to 0 degrees")
        move_servos(0)
        time.sleep(0.5)

    print("Returning to 0 degrees and stopping.")
    move_servos(0)
    time.sleep(1)

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    pwm1.stop()
    pwm2.stop()
    GPIO.cleanup()
