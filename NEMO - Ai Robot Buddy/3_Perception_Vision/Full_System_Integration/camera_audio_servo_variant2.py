"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  FILE: camera_audio_servo_variant2.py                                           ║
║  DESCRIPTION: DIRECTIONAL-AWARE SERVO MOVEMENT (MOST NATURAL)                   ║
╠════════════════════════════════════════════════════════════════════════════════╣
║  PURPOSE:                                                                        ║
║  Most natural-looking servo animation variant! Uses directional awareness to     ║
║  create intelligent, realistic movements. Instead of picking random angle,       ║
║  moves LEFT or RIGHT in incremental steps, creating smooth, predictable paths.   ║
║                                                                                  ║
║  KEY DIFFERENCES FROM OTHER VARIANTS:                                            ║
║  ✓ DIRECTIONAL INTELLIGENCE: Randomly chooses direction (-1 or +1)              ║
║  ✓ INCREMENTAL MOVEMENT: Moves in ±10 to ±30° steps from current position      ║
║  ✓ SMOOTH TRANSITIONS: Same 5-step interpolation as Variant1                     ║
║  ✓ BOUNDED ANGLES: Always respects 60-120° safety limits                        ║
║  ✓ NATURAL PATHS: Creates more realistic head/neck movement sequences           ║
║  ✓ MOST REALISTIC: Closest to how humans move (incremental, not random)         ║
║                                                                                  ║
║  COMPARISON:                                                                     ║
║  vs. BASE: Base = random angles; This = directional incremental angles           ║
║  vs. VARIANT1: V1 = any target angle; This = aware of direction/current angle   ║
║  vs. FIXED_MOVEMENT: Fixed = 3 patterns; This = intelligent directional moves   ║
║  vs. FIXED_FINAL: Final = hardcoded sequences; This = adaptive motion generation ║
║                                                                                  ║
║  MOVEMENT LOGIC:                                                                 ║
║  1. Pick random direction: direction = rand(-1, 1)  →  -1 (left) or 1 (right)   ║
║  2. Pick random offset: offset = rand(10, 30)  →  between 10-30 degrees         ║
║  3. Calculate target: target = current + (direction × offset)                    ║
║  4. Constrain: target = clamp(target, 60, 120)                                   ║
║  5. Smooth move: Use 5-step interpolation (same as Variant1)                     ║
║  6. Update current: current = target for next cycle                              ║
║                                                                                  ║
║  MOVEMENT EXAMPLES:                                                              ║
║  Current=90°, direction=-1, offset=20 → Target=70° (move LEFT)                  ║
║  Current=70°, direction=+1, offset=30 → Target=100° (move RIGHT)                ║
║  Current=110°, direction=+1, offset=25 → Target=120° (clamped to limit)         ║
║                                                                                  ║
║  IDEAL FOR:                                                                      ║
║  → Robot head/neck tracking systems (most natural-looking!)                      ║
║  → Expressive robot animations (looks deliberate, not random)                    ║
║  → Character interactions where movement pattern matters                         ║
║  → Projects emphasizing realistic motion over choreography                       ║
║  → Interactive robots that respond to stimuli naturally                          ║
║                                                                                  ║
║  TECHNICAL STATS:                                                                ║
║  • Movement speed: ~250ms per cycle (5 steps × 50ms)                             ║
║  • Direction randomness: 50% left, 50% right per cycle                           ║
║  • Typical angle change: 10-30° per movement (realistic increments)              ║
║  • Range constraint: Always within 60-120° (safe operating window)               ║
║  • Audio sync: Moves continuously while audio plays (realistic sync)             ║
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
            direction = random.choice([-1, 1])
            target_angle = current_angle + direction * random.randint(10, 30)
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
