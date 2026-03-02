"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  FILE: camera_audio_servo_control.py                                            ║
║  DESCRIPTION: BASE VERSION - SYNCHRONIZED CAMERA/AUDIO/SERVO                    ║
╠════════════════════════════════════════════════════════════════════════════════╣
║  PURPOSE:                                                                        ║
║  Foundation variant that combines camera capture, hand detection, audio          ║
║  playback, and servo control all in one system. Detects hands via HSV color      ║
║  thresholding, triggers random audio when hand appears, and moves servo          ║
║  randomly during audio playback. This is the BASE for all other variants.        ║
║                                                                                  ║
║  KEY FEATURES:                                                                   ║
║  ✓ HAND DETECTION: HSV-based skin detection with contour analysis              ║
║  ✓ AUDIO INTEGRATION: Random MP3 from 11 available files                        ║
║  ✓ SERVO SYNC: Moves servo while audio plays (until audio ends)                ║
║  ✓ HTTP STREAMING: MJPEG video stream with Basic auth on port 8080             ║
║  ✓ RANDOM MOTION: Abrupt random angles 60-120°                                ║
║  ✓ FAST RESPONSE: Direct angle changes, no interpolation (instant)             ║
║                                                                                  ║
║  MOVEMENT STRATEGY:                                                              ║
║  While audio is playing:                                                         ║
║    While process.poll() is None:  # Audio still playing                          ║
║      angle = random.randint(60, 120)  # Pick random angle within bounds         ║
║      set_servo_angle(angle)                                                     ║
║      time.sleep(0.1)  # 100ms between angle changes (10 changes/sec)            ║
║                                                                                  ║
║  COMPARISON WITH VARIANTS:                                                       ║
║  Variant1: Base + smooth interpolation (5 steps)                                 ║
║  Variant2: Variant1 + directional intelligence                                   ║
║  FixedMov: Base + predefined patterns (3 patterns)                               ║
║  FixedV1: FixedMov + extended patterns (8 algorithms)                            ║
║  FixedFinal: Hardcoded sequences (zero algorithms)                               ║
║                                                                                  ║
║  HAND DETECTION ALGORITHM:                                                       ║
║  1. Capture frame from USB camera                                                ║
║  2. Flip horizontally for mirror effect                                          ║
║  3. Convert BGR → HSV color space                                               ║
║  4. Threshold by skin color range: H[0-20], S[20-255], V[70-255]                ║
║  5. Apply Gaussian blur (5x5) to smooth                                          ║
║  6. Erode (2 iterations) to remove noise                                         ║
║  7. Dilate (2 iterations) to restore size                                        ║
║  8. Find contours and check area > 5000 pixels                                   ║
║  9. Draw bounding box + text label on frame                                      ║
║                                                                                  ║
║  NETWORK SPECIFICATIONS:                                                         ║
║  • Server: HTTP on 0.0.0.0:8080                                                 ║
║  • Auth: Basic HTTP (admin/raspberry)                                            ║
║  • Routes:                                                                      ║
║  •   /           → HTML page with embedded MJPEG stream                           ║
║  •   /stream.mjpg → Actual video stream (multipart JPEG)                          ║
║  • Framerate: 15fps (60ms per frame)                                             ║
║  • Resolution: 640x480 pixels                                                    ║
║  • Threading: Multi-threaded (handles multiple clients)                           ║
║                                                                                  ║
║  AUDIO FILES AVAILABLE:                                                          ║
║  1. /home/nisan/Desktop/output_speech.mp3                                        ║
║  2. /home/nisan/Downloads/1_1.mp3 through 1_9.mp3 (9 files)                     ║
║  3. /home/nisan/Downloads/nemo.mp3                                               ║
║  Total: 11 audio files available for random selection                            ║
║                                                                                  ║
║  SERVO SPECIFICATIONS:                                                           ║
║  • GPIO PIN: 18 (BCM numbering)                                                  ║
║  • PWM FREQUENCY: 50Hz (standard servo frequency)                                ║
║  • Angle range: 60-120° (safe limits)                                           ║
║  • Duty cycle: angle/18 + 2 (empirical formula)                                  ║
║  • Timing: Direct angle jumps (~20ms response)                                   ║
║                                                                                  ║
║  IDEAL USE CASE:                                                                 ║
║  → Quick prototype/proof-of-concept                                              ║
║  → Testing hand detection accuracy                                               ║
║  → Learning camera-servo integration                                             ║
║  → Interactive displays/robot demonstrations                                     ║
║  → Quick response systems (no smoothing overhead)                                ║
║                                                                                  ║
║  PERFORMANCE CHARACTERISTICS:                                                    ║
║  • Hand detection: Real-time (15fps pipeline)                                    ║
║  • Servo response: Instant (no interpolation)                                    ║
║  • Audio sync: Triggered on detection, runs to completion                        ║
║  • Visual quality: Herky-jerky (abrupt movements)                                ║
║  • Responsiveness: FAST (immediate angle changes)                                ║
║                                                                                  ║
║  START HERE IF:                                                                  ║
║  You want to understand the core system before exploring variant improvements    ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import cv2
import time
import base64
import subprocess
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import RPi.GPIO as GPIO  # Import GPIO library

# Configuration
HOST = '0.0.0.0'
PORT = 8080
RESOLUTION = (640, 480)
FRAMERATE = 15

# Authentication Credentials
USERNAME = "admin"
PASSWORD = "raspberry"
AUTH_HEADER = "Basic " + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()

# List of audio file locations
audio_files = [
    "/home/nisan/Desktop/output_speech.mp3",
    "/home/nisan/Downloads/1_1.mp3",
    "/home/nisan/Downloads/1_2.mp3",
    "/home/nisan/Downloads/1_3.mp3",
    "/home/nisan/Downloads/1_4.mp3",
    "/home/nisan/Downloads/1_5.mp3",
    "/home/nisan/Downloads/1_6.mp3",
    "/home/nisan/Downloads/1_7.mp3",
    "/home/nisan/Downloads/1_8.mp3",
    "/home/nisan/Downloads/1_9.mp3",
    "/home/nisan/Downloads/nemo.mp3"
]

# Servo motor setup
SERVO_PIN = 18  # GPIO pin for servo
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)  # 50Hz frequency

def set_servo_angle(angle):
    duty = angle / 18 + 2
    GPIO.output(SERVO_PIN, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(0.02)
    GPIO.output(SERVO_PIN, False)
    pwm.ChangeDutyCycle(0)

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
    <title>Raspberry Pi CCTV</title>
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
        .video-container {
            margin: auto;
            padding: 20px;
        }
        img {
            border: 5px solid #4caf50;
            border-radius: 10px;
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
    <h1>🔒 Raspberry Pi CCTV Live Stream</h1>
    <div class="video-container">
        <img src="stream.mjpg" alt="Live Stream" />
    </div>
    <footer>Streaming via Raspberry Pi • CV2 + HTTP</footer>
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
                print(f"Stream error: {e}")
        else:
            self.send_error(404)
            self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def capture_frame():
    global camera
    try:
        ret, frame = camera.read()
        if not ret:
            print("Error capturing frame")
            return None

        frame = cv2.flip(frame, 1)
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_skin = (0, 20, 70)
        upper_skin = (20, 255, 255)
        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        mask = cv2.GaussianBlur(mask, (5, 5), 0)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        hand_detected = False
        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > 5000:
                hand_detected = True
                x, y, w, h = cv2.boundingRect(cnt)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                break

        label = "Hand Detected" if hand_detected else "No Hand"
        color = (0, 255, 0) if hand_detected else (0, 0, 255)
        cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

        if hand_detected:
            play_audio_and_move_servo() #Play audio and move servo

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    except Exception as e:
        print(f"Camera error: {e}")
        return None

def play_audio_and_move_servo():
    try:
        audio_file = random.choice(audio_files)
        process = subprocess.Popen(["cvlc", "--play-and-exit", audio_file])
        time.sleep(0.1) # small delay to start audio
        while process.poll() is None: #while audio is playing
            angle = random.randint(60, 120)
            set_servo_angle(angle)
            time.sleep(0.1)
    except Exception as e:
        print(f"Error playing audio or moving servo: {e}")

def main():
    global camera, pwm
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])
    pwm.start(0)

    try:
        server = ThreadedHTTPServer((HOST, PORT), StreamingHandler)
        print(f"🌐 Server started at: http://{HOST}:{PORT}/")
        print(f"🔐 Username: {USERNAME}, Password: {PASSWORD}")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Stopping server and releasing camera.")
        camera.release()
        pwm.stop()
        GPIO.cleanup()
    except Exception as e:
        print(f"Server error: {e}")
        camera.release()
        pwm.stop()
        GPIO.cleanup()

if __name__ == '__main__':
    main()
