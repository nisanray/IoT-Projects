"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  FILE: camera_audio_servo_fixed_variant1.py                                     ║
║  DESCRIPTION: EXTENDED PATTERN-BASED MOVEMENT (8 PATTERNS)                      ║
╠════════════════════════════════════════════════════════════════════════════════╣
║  PURPOSE:                                                                        ║
║  ADVANCED CHOREOGRAPHY with 8 distinct movement patterns. Expands on the         ║
║  3-pattern version to provide richer, more varied movement sequences with        ║
║  better performance quality. Includes extreme movements and varied intensities.  ║
║                                                                                  ║
║  KEY DIFFERENCES FROM OTHER VARIANTS:                                            ║
║  ✓ 8 PATTERNS: 2.6x more patterns than FIXED_MOVEMENT (3 vs 8)                 ║
║  ✓ EXTREME MOVEMENTS: Patterns 4-5 use full range extremes (60° or 120°)        ║
║  ✓ VARIED INTENSITIES: Patterns 1-3 range from 20-50° movement magnitudes       ║
║  ✓ BALANCED VARIATION: Includes moderate + extreme movements                    ║
║  ✓ CENTER-BASED: Patterns 6-8 based on ±offsets from center (90°)               ║
║  ✓ BETTER PERFORMANCES: More patterns = less repetitive, longer performances     ║
║                                                                                  ║
║  COMPARISON:                                                                     ║
║  vs. FIXED_MOVEMENT: 3 patterns vs 8 patterns (2.6x variety)                    ║
║  vs. VARIANT1/2: Variant uses random; this uses structured patterns             ║
║  vs. FIXED_FINAL: This = algorithmic patterns; Final = hardcoded sequences      ║
║                                                                                  ║
║  THE 8 MOVEMENT PATTERNS:                                                        ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 1: LARGE RANDOM (±20-40°)                                  │       ║
║  │ • Offset: Current ± random(20-40)°                                  │       ║
║  │ • Random direction: -1 or +1                                        │       ║
║  │ • Style: Large dramatic movements                                   │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 2: EXTRA LARGE (±25-45°)                                   │       ║
║  │ • Offset: Current ± random(25-45)°                                  │       ║
║  │ • Random direction: -1 or +1                                        │       ║
║  │ • Style: Very large movements, near extremes                        │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 3: MAXIMUM RANGE (±30-50°)                                 │       ║
║  │ • Offset: Current ± random(30-50)°                                  │       ║
║  │ • Random direction: -1 or +1                                        │       ║
║  │ • Style: LARGEST random movements allowed                           │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 4: LEFT EXTREME                                             │       ║
║  │ • Target: 60° (hard left bound)                                     │       ║
║  │ • Direction: LEFT                                                   │       ║
║  │ • Style: Move all the way to one side                               │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 5: RIGHT EXTREME (OPPOSITE OF 4)                             │       ║
║  │ • Target: 120° (hard right bound)                                   │       ║
║  │ • Direction: RIGHT                                                  │       ║
║  │ • Style: Move all the way to opposite side                          │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 6: CENTER-BASED LARGE (90° ± 40°)                          │       ║
║  │ • Target: 90 + random(-40, +40)  →  Range [50-130] clamped [60-120]│       ║
║  │ • Direction: Random choice of ±40 offsets                           │       ║
║  │ • Style: Jump around center point                                   │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 7: CENTER-BASED MEDIUM (90° ± 35°)                         │       ║
║  │ • Target: 90 + random(-35, +35)  →  Range [55-125] clamped [60-120]│       ║
║  │ • Direction: Random ±35 offsets                                     │       ║
║  │ • Style: Moderate swings around center                              │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║  ┌─────────────────────────────────────────────────────────────────────┐       ║
║  │ PATTERN 8: CENTER-BASED SMALL (90° ± 30°)                          │       ║
║  │ • Target: 90 + random(-30, +30)  →  Range [60-120]                 │       ║
║  │ • Direction: Random ±30 offsets                                     │       ║
║  │ • Style: Tight movements around center                              │       ║
║  └─────────────────────────────────────────────────────────────────────┘       ║
║                                                                                  ║
║  PATTERN COMPLEXITY SPECTRUM:                                                    ║
║  Patterns 1-3: LOW STRUCTURE (high randomness, large magnitudes)                ║
║  Patterns 4-5: EXTREMES (go to opposite corners)                                ║
║  Patterns 6-8: CENTER-BASED (orbiting around 90° with varying radii)           ║
║                                                                                  ║
║  IDEAL FOR:                                                                      ║
║  → Long-duration performances (8 patterns = less repetition)                     ║
║  → Complex choreography with varied movement styles                              ║
║  → Entertainment value (interesting movement patterns)                           ║
║  → Demonstrations showing movement capability/range                              ║
║  → Systems requiring more sophisticated movement generation                      ║
║                                                                                  ║
║  TECHNICAL SPECS:                                                                ║
║  • Total patterns: 8 distinct movement strategies                                ║
║  • Smoothing: 5-step interpolation (250ms per movement)                          ║
║  • Random patterns distribution: 1/8th chance (12.5%) each per cycle             ║
║  • Bounds enforcement: All patterns final-clamped to [60-120°]                   ║
║  • Randomness level: HIGH (8 different algorithms, plus internal randomness)     ║
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
            pattern = random.randint(1, 8)  # Increased pattern range
            if pattern == 1:
                direction = random.choice([-1, 1])
                target_angle = current_angle + direction * random.randint(20, 40)
            elif pattern == 2:
                target_angle = current_angle + random.choice([-1, 1]) * random.randint(25, 45)
            elif pattern == 3:
                target_angle = current_angle + random.choice([-1, 1]) * random.randint(30, 50)
            elif pattern == 4:
                target_angle = 60 if current_angle > 90 else 120
            elif pattern == 5:
                target_angle = 120 if current_angle < 90 else 60
            elif pattern == 6:
                target_angle = 90 + random.choice([-40,40])
            elif pattern == 7:
                target_angle = 90 + random.choice([-35,35])
            elif pattern == 8:
                target_angle = 90 + random.choice([-30,30])

            target_angle = max(60, min(120, target_angle)) # Ensure angle is within 60-120 range.
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
