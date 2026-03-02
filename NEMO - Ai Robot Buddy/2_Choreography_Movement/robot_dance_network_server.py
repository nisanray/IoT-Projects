"""
Description: Dance control via network server
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
HOST = '0.0.0.0'  # Listen on all interfaces (e.g., Wi-Fi, Ethernet)
PORT = 5000       # Port for clients to connect to

# --- Servo Configuration ---
SERVO_PINS = [17, 18, 22, 23] # GPIO pins connected to your servos
# Using BCM pin numbering
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False) # Optional: to disable warnings if pins are already in use

# Setup pins and create PWM objects for each servo
servos = []
for pin in SERVO_PINS:
    GPIO.setup(pin, GPIO.OUT)
    pwm = GPIO.PWM(pin, 50)  # 50Hz is standard for most servos
    pwm.start(0) # Start PWM with 0% duty cycle (servo at neutral position)
    servos.append(pwm)

# --- Dance Functions ---
def set_servo_angle(pwm, angle):
    """Converts an angle to a PWM duty cycle and moves the servo."""
    # Duty cycle calculation: 2.5 is 0 degrees, 12.5 is 180 degrees for typical servos
    # (angle / 18) + 2.5 is a common formula, or (angle / 180.0) * 10 + 2.5
    duty = 2.5 + (angle / 180.0) * 10
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.1)  # Allow time for the servo to move
    pwm.ChangeDutyCycle(0)  # Stop sending signal to prevent jitter/buzzing

def reset_all_servos():
    """Moves all servos to their initial (0 degrees) position."""
    print("Resetting all servos to 0 degrees...")
    for pwm in servos:
        set_servo_angle(pwm, 0)
    print("Servos reset.")

def move_servos_random():
    """Moves servos to random angles in a random order."""
    indices = list(range(len(servos)))
    random.shuffle(indices)  # Randomize the order of servo movement
    for i in indices:
        angle = random.uniform(-10, 30)  # Define the random angle range
        print(f"Moving Servo {SERVO_PINS[i]} (index {i}) to {angle:.1f}°")
        set_servo_angle(servos[i], angle)
        time.sleep(random.uniform(0.05, 0.15))  # Random delay between servo movements

def dance_routine():
    """Performs the dance sequence for 30 seconds."""
    print("Dance routine initiated...")
    start_time = time.time()
    try:
        # Initial reset before starting the dance sequence
        reset_all_servos()
        time.sleep(0.5)

        while time.time() - start_time < 10: # Loop for 10 seconds
            elapsed_time = time.time() - start_time
            print(f"--- Dancing... (Time remaining: {10 - elapsed_time:.1f}s) ---")
            move_servos_random()
            # Optional: reset servos between random moves for a different dance style
            # reset_all_servos()
            # time.sleep(0.2)
        print("10-second dance routine finished.")
    except Exception as e:
        print(f"Error during dance routine: {e}")
    finally:
        # Ensure servos are reset after the dance, regardless of errors
        reset_all_servos()
        print("Servos reset after dance routine completion.")

# --- Server Function ---
def start_server():
    """Initializes and starts the TCP/IP server."""
    # Create a socket object
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Allow the socket to be reused immediately after closing
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        # Bind the socket to the host and port
        server_socket.bind((HOST, PORT))
        
        # Enable the server to accept connections (1 is the backlog size)
        server_socket.listen(1)
        
        print(f"Server successfully started. Listening continuously on {HOST}:{PORT}")
        print("Waiting for a 'dance' command from a client...")

        # This is the main server loop that listens for connections indefinitely
        while True: # <--- THIS LOOP ENSURES CONTINUOUS LISTENING
            try:
                # Wait for a client to connect (blocking call)
                client_socket, addr = server_socket.accept()
                with client_socket:
                    print(f"Connection established with {addr}")
                    
                    # Receive data from the client (up to 1024 bytes)
                    data = client_socket.recv(1024)
                    if data:
                        message = data.decode('utf-8').strip().lower()
                        print(f"Received message from {addr}: '{message}'")
                        
                        if message == "dance":
                            print(f"'dance' command received from {addr}. Initiating dance routine in a background thread.")
                            # Start the dance routine in a new thread
                            # This allows the server to remain responsive and listen for other commands/connections
                            dance_thread = threading.Thread(target=dance_routine)
                            dance_thread.start()
                            client_socket.sendall(b"Dance routine initiated!")
                        else:
                            response = f"Message '{message}' received. Send 'dance' to start the robot."
                            client_socket.sendall(response.encode('utf-8'))
                    else:
                        # No data received, client might have just connected and disconnected
                        print(f"No data received from {addr}. Client may have disconnected.")
            
            except ConnectionResetError:
                print(f"Connection with {addr} was reset by the client.")
            except socket.timeout:
                print("Socket timed out. (This shouldn't happen with accept() unless a timeout is set)")
            except Exception as e:
                # Catch other potential errors in the server loop
                print(f"An error occurred in the server loop: {e}")
            
            # The loop continues, and server_socket.accept() is called again,
            # ensuring the server is always listening for the next connection.
            print(f"Returning to listen for new connections on {HOST}:{PORT}...")


if __name__ == '__main__':
    try:
        print("Initializing system...")
        reset_all_servos() # Ensure servos are in a known state at startup
        time.sleep(0.5) # Brief pause after initial reset
        
        # Start the server (this function contains the infinite listening loop)
        start_server()
        
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        print("\nShutdown signal received (KeyboardInterrupt). Cleaning up and exiting...")
    except Exception as e:
        # Catch any other unexpected errors during startup or shutdown
        print(f"A critical error occurred: {e}")
    finally:
        # This block executes regardless of how the try block exits
        print("Performing final GPIO cleanup...")
        for pwm in servos:
            pwm.stop() # Stop PWM signals
        GPIO.cleanup() # Reset GPIO pin configurations
        print("GPIO cleanup complete. Program terminated.")
