"""
Description: Tests servo angle control functionality
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import RPi.GPIO as GPIO
import time

# Configurations
SERVO_PIN = 18
PWM_FREQ = 50  # 50 Hz
MOVE_DELAY = 0.03  # Smooth sweep step delay
HOLD_DELAY = 0.5   # Delay to hold at position

# Setup GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)
pwm.start(0)

def set_angle(angle):
    """Move servo to the specified angle with logging."""
    angle = max(0, min(180, angle))
    duty = angle / 18 + 2
    print(f"[INFO] Moving to {angle:>3}°  -> Duty Cycle: {duty:.2f}%")
    pwm.ChangeDutyCycle(duty)
    time.sleep(HOLD_DELAY)
    pwm.ChangeDutyCycle(0)

def smooth_sweep(start=0, end=180, step=1):
    """Smooth sweep from start to end angle."""
    print(f"[SWEEP] Sweeping from {start}° to {end}°...")
    for angle in range(start, end + 1, step):
        duty = angle / 18 + 2
        pwm.ChangeDutyCycle(duty)
        print(f" - Angle: {angle:>3}°  | Duty: {duty:.2f}%")
        time.sleep(MOVE_DELAY)
    pwm.ChangeDutyCycle(0)
    print(f"[SWEEP] Reached {end}°.\n")

try:
    print("[START] Starting servo movement sequence.\n")

    # Basic test
    for angle in [0, 45, 90, 135, 180, 90, 0]:
        set_angle(angle)
        time.sleep(0.5)

    # Smooth sweep forward
    smooth_sweep(0, 180, 2)

    # Smooth sweep backward
    smooth_sweep(180, 0, -2)

    # Fast jumps (simulate tapping action)
    print("[ACTION] Fast movement test...")
    for i in range(3):
        set_angle(60)
        time.sleep(0.3)
        set_angle(120)
        time.sleep(0.3)
    set_angle(90)

except KeyboardInterrupt:
    print("\n[INTERRUPT] Program interrupted by user.")

finally:
    print("\n[CLEANUP] Stopping PWM and cleaning up GPIO...")
    pwm.stop()
    GPIO.cleanup()
    print("[DONE] Servo control ended.")
