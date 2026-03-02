"""
Description: Continuous servo control using gpiozero library
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

from gpiozero import Servo
from gpiozero.pins.pigpio import PiGPIOFactory
from time import sleep

# pigpio ব্যবহার করে PWM আরো স্ট্যাবল হয়
factory = PiGPIOFactory()
servo = Servo(18, pin_factory=factory, min_pulse_width=0.5/1000, max_pulse_width=2.5/1000)

def angle_to_value(angle):
    # 0° to 180° → -1 to 1 mapping
    return (angle - 90) / 90

try:
    while True:
        # 60° থেকে 120° ঘোরাও
        for angle in range(60, 121):
            servo.value = angle_to_value(angle)
            sleep(0.02)

        for angle in range(120, 59, -1):
            servo.value = angle_to_value(angle)
            sleep(0.02)

except KeyboardInterrupt:
    print("Stopped")
    servo.detach()  # PWM বন্ধ
