"""
Description: Basic TCP socket server listening on port 5000
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import socket

HOST = '0.0.0.0'  # Listen on all interfaces
PORT = 5000       # Must match client port

def start_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((HOST, PORT))
        server_socket.listen()
        print(f"Server listening on {HOST}:{PORT}")

        while True:
            client_socket, addr = server_socket.accept()
            with client_socket:
                print(f"Connected by {addr}")
                data = client_socket.recv(1024)
                if data:
                    message = data.decode('utf-8')
                    print(f"Received message: {message}")
                    # Example response
                    client_socket.sendall(b"Message received by RPi")

if __name__ == '__main__':
    start_server()
