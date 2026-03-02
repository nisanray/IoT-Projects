"""
Description: Complete dance routine with random patterns
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time
import random

# Define servo pins
SERVO_PINS = [17, 18, 22, 23]

GPIO.setmode(GPIO.BCM)

# Setup pins and create PWM objects
servos = []
for pin in SERVO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)  # 50Hz for standard servo
    pwm.start(0)
    servos.append(pwm)

# Convert angle to duty cycle
def set_servo_angle(pwm, angle):
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.3)

# Move all servos to 0 degrees
def reset_all_servos():
    for pwm in servos:
        set_servo_angle(pwm, 0)
    time.sleep(0.5)

# Move each servo to a random angle between 0 and 20 degrees
def move_servos_random():
    for index, pwm in enumerate(servos):
        angle = random.uniform(0, 20)  # Random angle in 0–20°
        print(f"Servo {index+1} moving to {angle:.2f} degrees")
        set_servo_angle(pwm, angle)
    time.sleep(0.5)

try:
    print("Moving all servos to 0 degrees (initial position)")
    reset_all_servos()
    time.sleep(1)

    for cycle in range(100):
        print(f"\n--- Cycle {cycle+1} ---")
        move_servos_random()
        print("Returning all servos to 0 degrees")
        reset_all_servos()

    print("Done. Returning all servos to 0 degrees.")
    reset_all_servos()

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    for pwm in servos:
        pwm.stop()
    GPIO.cleanup()
