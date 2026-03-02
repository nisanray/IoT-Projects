"""
Description: Basic GPIO servo control test
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
    time.sleep(0.1)  # faster movement
    pwm.ChangeDutyCycle(0)  # prevent buzzing

# Move all servos to 0 degrees
def reset_all_servos():
    for pwm in servos:
        set_servo_angle(pwm, 0)

# Move servos to random angles with randomness in delay and order
def move_servos_random():
    indices = list(range(len(servos)))
    random.shuffle(indices)  # randomize order
    for i in indices:
        angle = random.uniform(-10, 30)  # expanded range
        print(f"Servo {i+1} → {angle:.1f}°")
        set_servo_angle(servos[i], angle)
        time.sleep(random.uniform(0.05, 0.15))  # random delay

try:
    print("Moving all servos to 0 degrees (initial position)")
    reset_all_servos()
    time.sleep(0.5)

    for cycle in range(100):  # more cycles
        print(f"\n--- Cycle {cycle+1} ---")
        move_servos_random()
        print("Returning all servos to 0 degrees")
        reset_all_servos()
        time.sleep(0.2)

    print("Done. Returning all servos to 0 degrees.")
    reset_all_servos()

except KeyboardInterrupt:
    print("Interrupted by user.")

finally:
    for pwm in servos:
        pwm.stop()
    GPIO.cleanup()
