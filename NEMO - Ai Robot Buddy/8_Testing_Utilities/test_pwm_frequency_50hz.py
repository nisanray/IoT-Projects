"""
Description: PWM frequency test at 50Hz
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

SERVO_PIN = 18

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)  # 50 Hz
pwm.start(0)

# Converts angle (0 to 270) to duty cycle (approx)
def set_angle(angle):
    duty = 2.5 + (angle / 270.0) * 10  # Adjust if needed
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.5)
    pwm.ChangeDutyCycle(0)  # Optional: let it hold or relax

try:
    while True:
        print("Go to 0°")
        set_angle(0)
        time.sleep(1)

        print("Go to 135°")
        set_angle(135)
        time.sleep(1)

        print("Go to 270°")
        set_angle(270)
        time.sleep(1)

except KeyboardInterrupt:
    print("Exiting...")

finally:
    pwm.stop()  # Let servo go limp
    GPIO.cleanup()
