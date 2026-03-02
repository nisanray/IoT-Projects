"""
Description: Camera with audio integration
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import cv2
import time
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import sounddevice as sd
import numpy as np
import threading
import queue
import wave

# Configuration
HOST = '0.0.0.0'
PORT = 8080
RESOLUTION = (640, 480)
FRAMERATE = 15
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHANNELS = 1
AUDIO_CHUNK_SIZE = 1024  # Adjust as needed
AUDIO_DEVICE = None  # Set your audio input device if needed

# Authentication Credentials
USERNAME = "admin"
PASSWORD = "raspberry"
AUTH_HEADER = "Basic " + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

# Global variables
camera = None
audio_queue = queue.Queue(maxsize=10)  # Queue to hold audio chunks

def capture_frame():
    global camera
    try:
        ret, frame = camera.read()
        if not ret:
            print("Error capturing frame")
            return None
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    except Exception as e:
        print(f"Camera error: {e}")
        return None

def audio_stream_generator():
    try:
        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            audio_queue.put(indata.tobytes())

        with sd.InputStream(samplerate=AUDIO_SAMPLE_RATE,
                            channels=AUDIO_CHANNELS,
                            dtype='int16',
                            blocksize=AUDIO_CHUNK_SIZE,
                            callback=callback,
                            device=AUDIO_DEVICE):
            while True:
                audio_data = audio_queue.get()
                yield (b'--audioboundary\r\n'
                       b'Content-Type: audio/wav\r\n'
                       b'Content-Length: ' + str(len(audio_data)).encode() + b'\r\n'
                       b'\r\n' + audio_data + b'\r\n')
    except sd.PortAudioError as e:
        print(f"Audio stream error: {e}")
    except Exception as e:
        print(f"Audio generator error: {e}")

class StreamingHandler(BaseHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm="CCTV"')
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def is_authenticated(self):
        auth_header = self.headers.get('Authorization')
        return auth_header == AUTH_HEADER

    def do_GET(self):
        if not self.is_authenticated():
            self.do_AUTHHEAD()
            self.wfile.write(b"<html><body><h1>Authentication Required</h1></body></html>")
            return

        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()

            html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Raspberry Pi CCTV Live Stream with Audio</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #1e1e2f;
            color: white;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        h1 {
            margin: 20px;
        }
        .container {
            display: flex;
            flex-direction: column;
            align-items: center;
            padding: 20px;
        }
        .video-container {
            margin-bottom: 20px;
        }
        img {
            border: 5px solid #4caf50;
            border-radius: 10px;
            width: 80%;
            max-width: 640px;
        }
        audio {
            width: 80%;
            max-width: 640px;
        }
        footer {
            position: fixed;
            bottom: 0;
            width: 100%;
            background: #111;
            color: #aaa;
            padding: 10px;
        }
    </style>
</head>
<body>
    <h1>🔒 Raspberry Pi CCTV Live Stream with Audio</h1>
    <div class="container">
        <div class="video-container">
            <img src="stream.mjpg" alt="Live Video Stream" />
        </div>
        <audio controls autoplay src="audio_stream.wav"></audio>
    </div>
    <footer>Streaming via Raspberry Pi • CV2 + HTTP + SoundDevice</footer>
</body>
</html>"""

            self.wfile.write(html_content.encode('utf-8'))

        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            try:
                while True:
                    frame = capture_frame()
                    if frame is None:
                        break
                    self.wfile.write(b'--jpgboundary\r\n')
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(len(frame)))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
                    time.sleep(1 / FRAMERATE)
            except Exception as e:
                print(f"Video stream error: {e}")

        elif self.path == '/audio_stream.wav':
            self.send_response(200)
            self.send_header('Content-type', 'audio/x-wav') # Or 'audio/mpeg' if you encode differently
            self.end_headers()
            try:
                for chunk in audio_stream_generator():
                    self.wfile.write(chunk)
            except Exception as e:
                print(f"Audio sending error: {e}")

        else:
            self.send_error(404)
            self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def main():
    global camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])

    try:
        server = ThreadedHTTPServer((HOST, PORT), StreamingHandler)
        print(f"🌐 Server started at: http://{HOST}:{PORT}/")
        print(f"🔐 Username: {USERNAME}, Password: {PASSWORD}")
        print("🎧 Streaming audio...")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server and releasing camera.")
        if camera and camera.isOpened():
            camera.release()
    except Exception as e:
        print(f"Server error: {e}")
        if camera and camera.isOpened():
            camera.release()

if __name__ == '__main__':
    import sys
    print("Listing available audio devices:")
    print(sd.query_devices())
    print("\nTrying to stream audio from the default input device. If you encounter issues,")
    print("check the device list above and set the 'AUDIO_DEVICE' variable in the script.")
    main()

