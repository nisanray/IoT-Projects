"""
Description: Complete dance routine - variant 1
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time
import random

# Define GPIO pins for the 4 servos
SERVO_PINS = [17, 18, 22, 23]

GPIO.setmode(GPIO.BCM)

# Initialize and start PWM for each pin
servos = []
for pin in SERVO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)  # 50Hz PWM for servos
    pwm.start(0)
    servos.append(pwm)

# Convert angle (0–180) to duty cycle (2.5–12.5)
def set_servo_angle(pwm, angle):
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.15)  # Fast response

# Move all servos to 0 degrees
def reset_all_servos():
    for pwm in servos:
        set_servo_angle(pwm, 0)
    time.sleep(0.2)

# Move servos to different angle ranges
def move_servos_random():
    for i, pwm in enumerate(servos):
        if i < 2:
            angle = random.uniform(15, 20)  # For pins 17, 18
        else:
            angle = random.uniform(10, 15)  # For pins 22, 23
        print(f"Servo on pin {SERVO_PINS[i]} → {angle:.1f}°")
        set_servo_angle(pwm, angle)
    time.sleep(0.2)

try:
    print("Setting all servos to 0°")
    reset_all_servos()
    time.sleep(0.5)

    for cycle in range(100):
        print(f"\n--- Cycle {cycle + 1} ---")
        move_servos_random()
        print("Returning to 0°")
        reset_all_servos()

    print("All done. Servos at 0°")

except KeyboardInterrupt:
    print("Program interrupted")

finally:
    for pwm in servos:
        pwm.stop()
    GPIO.cleanup()
