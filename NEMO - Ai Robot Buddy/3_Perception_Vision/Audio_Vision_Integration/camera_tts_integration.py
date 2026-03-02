"""
Description: Camera with Text-to-Speech output
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import cv2
import numpy as np
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import pyttsx3  # Import pyttsx3 for text-to-speech

# Configuration
HOST = '0.0.0.0'
PORT = 8080
RESOLUTION = (640, 480)
FRAMERATE = 15

# Initialize pyttsx3 engine
engine = pyttsx3.init()

class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Hand Gesture Recognition</title>
    <style>
        body { background-color: #1e1e2f; color: white; text-align: center; }
        h1 { margin: 20px; }
        img { border: 5px solid #4caf50; border-radius: 10px; width: 80%; max-width: 640px; }
        footer { position: fixed; bottom: 0; width: 100%; background: #111; color: #aaa; padding: 10px; }
    </style>
</head>
<body>
    <h1>🖐️ Hand Gesture Recognition</h1>
    <div><img src="stream.mjpg" alt="Live Stream" /></div>
    <footer>Streaming via OpenCV</footer>
</body>
</html>"""
            self.wfile.write(html_content.encode('utf-8'))
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            try:
                while True:
                    frame, gesture = capture_frame()
                    if frame is None:
                        break
                    self.wfile.write(b'--jpgboundary\r\n')
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(len(frame)))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')
                    time.sleep(1 / FRAMERATE)
                    # Speak the gesture
                    if gesture != "No Hand Detected": #only speak if a gesture is detected.
                      engine.say(gesture)
                      engine.runAndWait()

            except Exception as e:
                print(f"Stream error: {e}")
        else:
            self.send_error(404)
            self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

def detect_gesture(contour, defects, frame):
    if defects is None or contour is None:
        return "No Hand Detected"

    count_defects = 0
    for i in range(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])

        a = np.linalg.norm(np.array(end) - np.array(start))
        b = np.linalg.norm(np.array(far) - np.array(start))
        c = np.linalg.norm(np.array(end) - np.array(far))
        angle = np.arccos((b**2 + c**2 - a**2)/(2*b*c)) * 57

        if angle <= 90:
            count_defects += 1
            cv2.circle(frame, far, 8, [255, 0, 0], -1)

    if count_defects == 0:
        return "Fist ✊"
    elif count_defects == 1:
        return "Peace ✌️"
    elif count_defects == 4:
        return "Open Palm 🖐️"
    else:
        return "Unknown Gesture"

def capture_frame():
    global camera
    try:
        ret, frame = camera.read()
        if not ret:
            return None, None

        frame = cv2.flip(frame, 1)
        roi = frame[100:400, 100:400]
        hsv = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

        lower_skin = np.array([0, 20, 70], dtype=np.uint8)
        upper_skin = np.array([20, 255, 255], dtype=np.uint8)

        mask = cv2.inRange(hsv, lower_skin, upper_skin)
        mask = cv2.GaussianBlur(mask, (5, 5), 100)

        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        gesture = "No Hand Detected"

        if contours:
            max_contour = max(contours, key=cv2.contourArea)
            if cv2.contourArea(max_contour) > 1000:
                hull = cv2.convexHull(max_contour)
                cv2.drawContours(roi, [max_contour], -1, (0, 255, 0), 2)
                cv2.drawContours(roi, [hull], -1, (0, 0, 255), 2)
                hull_indices = cv2.convexHull(max_contour, returnPoints=False)
                if len(hull_indices) > 3:
                    defects = cv2.convexityDefects(max_contour, hull_indices)
                    gesture = detect_gesture(max_contour, defects, roi)

        cv2.rectangle(frame, (100, 100), (400, 400), (255, 0, 0), 2)
        cv2.putText(frame, gesture, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes(), gesture
    except Exception as e:
        print(f"Capture error: {e}")
        return None, None

def main():
    global camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])

    try:
        server = ThreadedHTTPServer((HOST, PORT), StreamingHandler)
        print(f"Server started at: http://{HOST}:{PORT}/")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nStopping server.")
        camera.release()
    except Exception as e:
        print(f"Server error: {e}")
        camera.release()

if __name__ == '__main__':
    main()
