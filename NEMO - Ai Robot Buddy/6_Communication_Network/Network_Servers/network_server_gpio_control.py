"""
Description: Network server with GPIO control functionality
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import socket
import RPi.GPIO as GPIO
import time
import random
import threading

# --- Server Configuration ---
HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000       # Must match client port

# --- Servo Configuration ---
SERVO_PINS = [17, 18, 22, 23]
GPIO.setmode(GPIO.BCM)

# Setup pins and create PWM objects
servos = []
for pin in SERVO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)  # 50Hz for standard servo
    pwm.start(0)
    servos.append(pwm)

# --- Dance Functions ---
def set_servo_angle(pwm, angle):
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.1)  # faster movement
    pwm.ChangeDutyCycle(0)  # prevent buzzing

def reset_all_servos():
    print("Resetting all servos to 0 degrees")
    for pwm in servos:
        set_servo_angle(pwm, 0)

def move_servos_random():
    indices = list(range(len(servos)))
    random.shuffle(indices)  # randomize order
    for i in indices:
        angle = random.uniform(-10, 30)  # expanded range
        print(f"Servo {i+1} → {angle:.1f}°")
        set_servo_angle(servos[i], angle)
        time.sleep(random.uniform(0.05, 0.15))  # random delay

def dance_routine():
    """Performs the dance routine for a specified duration."""
    print("Starting dance routine...")
    start_time = time.time()
    try:
        while time.time() - start_time < 30: # Dance for 30 seconds
            print(f"--- Dancing (Time left: {30 - (time.time() - start_time):.1f}s) ---")
            move_servos_random()
            reset_all_servos() # Reset between random moves for more varied dance
            time.sleep(0.2) # Short pause
        print("Dance routine finished.")
    except Exception as e:
        print(f"Error during dance routine: {e}")
    finally:
        reset_all_servos()
        print("Servos reset after dance routine.")

# --- Server Function ---
def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Allow address reuse
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening continuously on {HOST}:{PORT}")
        print("Waiting for 'dance' command...")

        # This loop runs forever, allowing the server to accept multiple client connections
        while True:
            try:
                client_socket, addr = server_socket.accept() # Waits for a new connection
                with client_socket:
                    print(f"Connected by {addr}")
                    data = client_socket.recv(1024)
                    if data:
                        message = data.decode('utf-8').strip().lower()
                        print(f"Received message: {message}")
                        if message == "dance":
                            print("'dance' command received. Starting dance routine in a background thread.")
                            # Run dance routine in a new thread to avoid blocking the server
                            dance_thread = threading.Thread(target=dance_routine)
                            dance_thread.start()
                            client_socket.sendall(b"Dance routine started!")
                        else:
                            client_socket.sendall(b"Message received. Send 'dance' to start the routine.")
                    else:
                        print(f"No data received from {addr}. Client might have disconnected.")
            except ConnectionResetError:
                print(f"Connection reset by {addr}. Client likely disconnected abruptly.")
            except Exception as e:
                print(f"Error in server loop: {e}")
                # Depending on the error, you might want to break or continue
                # For now, we'll continue to try and keep the server alive

if __name__ == '__main__':
    try:
        print("Initializing servos...")
        reset_all_servos() # Initial reset
        time.sleep(0.5)
        start_server() # This function contains the infinite loop for listening
    except KeyboardInterrupt:
        print("\nInterrupted by user (Ctrl+C). Cleaning up...")
    except Exception as e:
        print(f"A critical error occurred: {e}")
    finally:
        print("Cleaning up GPIO...")
        for pwm in servos:
            pwm.stop()
        GPIO.cleanup()
        print("Cleanup complete. Exiting.")
