"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  FILE: camera_audio_servo_fixed_movement.py                                     ║
║  DESCRIPTION: PATTERN-BASED CHOREOGRAPHED MOVEMENT                              ║
╠════════════════════════════════════════════════════════════════════════════════╣
║  PURPOSE:                                                                        ║
║  Move away from pure randomness to CHOREOGRAPHED PATTERNS. Instead of           ║
║  generating random movement, this selects from 3 predefined movement            ║
║  patterns, making movements more organized and repeatable.                       ║
║                                                                                  ║
║  KEY DIFFERENCES FROM OTHER VARIANTS:                                            ║
║  ✓ PATTERN-BASED: Selects from 3 predefined movement strategies                 ║
║  ✓ CHOREOGRAPHED: Movements feel organized, not chaotic                          ║
║  ✓ SMOOTH TRANSITIONS: Still uses 5-step interpolation like V1/V2               ║
║  ✓ LESS RANDOM: More controlled than pure random variants                       ║
║  ✓ THREE STYLES: Pattern 1 (±10-30°), Pattern 2 (±5-15°), Pattern 3 (±20-40°)  ║
║                                                                                  ║
║  COMPARISON:                                                                     ║
║  vs. VARIANT1: V1 = any target angle; This = constrained patterns               ║
║  vs. VARIANT2: V2 = directional increments; This = predefined pattern strategies ║
║  vs. FIXED_VARIANT1: This = 3 patterns; Extended = 8 patterns                   ║
║  vs. FIXED_FINAL: This = patterns; Final = hardcoded angle sequences            ║
║                                                                                  ║
║  THE 3 MOVEMENT PATTERNS:                                                        ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 1: LARGE MOVEMENTS (±10-30°)                               │       ║
║  │ • Movement range: 20° total range (10-30°)                          │       ║
║  │ • Use case: Dramatic, visible servo motion                          │       ║
║  │ • Visual effect: Big head turns                                     │       ║
║  │ • Selected probability: 1/3 (33%)                                   │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 2: MEDIUM MOVEMENTS (±5-15°)                               │       ║
║  │ • Movement range: 10° total range (5-15°)                           │       ║
║  │ • Use case: Moderate head adjustments                               │       ║
║  │ • Visual effect: Normal head movements                              │       ║
║  │ • Selected probability: 1/3 (33%)                                   │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 3: EXTRA LARGE (±20-40°)                                   │       ║
║  │ • Movement range: 20° total range (20-40°)                          │       ║
║  │ • Use case: Exaggerated gestures                                    │       ║
║  │ • Visual effect: Extended head movements                            │       ║
║  │ • Selected probability: 1/3 (33%)                                   │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║                                                                                  ║
║  EXECUTION FLOW:                                                                 ║
║  1. Pick pattern: pattern = rand(1-3)                                            ║
║  2. Based on pattern, determine movement range                                   ║
║  3. Calculate target angle within that range + bounds                            ║
║  4. Smooth interpolate to target (5 steps × 50ms = 250ms)                       ║
║  5. Repeat for each audio playback cycle                                         ║
║                                                                                  ║
║  IDEAL FOR:                                                                      ║
║  → Choreographed performances (predictable but varied)                           ║
║  → Demonstrations where consistency matters                                      ║
║  → Training data collection (known patterns)                                     ║
║  → Systems where randomness should be controlled/limited                         ║
║  → Balancing between variety and predictability                                  ║
║                                                                                  ║
║  TECHNICAL SPECS:                                                                ║
║  • Total patterns: 3 distinct movement styles                                    ║
║  • Smoothing: 5-step interpolation (same as V1/V2)                               ║
║  • Timing: ~250ms per movement + ~100ms audio play margin                        ║
║  • Bounds: Always constrained to 60-120° (safe servo range)                      ║
║  • Randomness level: MEDIUM (patterns are random, movement is constrained)       ║
╚════════════════════════════════════════════════════════════════════════════════╝
"""

import cv2
import time
import base64
import subprocess
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import RPi.GPIO as GPIO

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
    #"/home/nisan/Desktop/output_speech.mp3",
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
SERVO_PIN = 18
GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)
pwm = GPIO.PWM(SERVO_PIN, 50)

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
    def __init__(self, *args, **kwargs):
        HTTPServer.__init__(self, *args, **kwargs)

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
            play_audio_and_move_servo()

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    except Exception as e:
        print(f"Camera error: {e}")
        return None

def play_audio_and_move_servo():
    try:
        audio_file = random.choice(audio_files)
        process = subprocess.Popen(["cvlc", "--play-and-exit", audio_file])
        time.sleep(0.1)

        current_angle = 90
        while process.poll() is None:
            pattern = random.randint(1, 3)
            if pattern == 1:
                direction = random.choice([-1, 1])
                target_angle = current_angle + direction * random.randint(10, 30)
                target_angle = max(60, min(120, target_angle))
            elif pattern == 2:
                target_angle = current_angle + random.choice([-1, 1]) * random.randint(5, 15)
                target_angle = max(60, min(120, target_angle))
            elif pattern == 3:
                target_angle = current_angle + random.choice([-1, 1]) * random.randint(20, 40)
                target_angle = max(60, min(120, target_angle))

            steps = 5
            for i in range(steps):
                intermediate_angle = current_angle + (target_angle - current_angle) * (i / steps)
                set_servo_angle(intermediate_angle)
                time.sleep(0.05)
            current_angle = target_angle
        set_servo_angle(90)
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
