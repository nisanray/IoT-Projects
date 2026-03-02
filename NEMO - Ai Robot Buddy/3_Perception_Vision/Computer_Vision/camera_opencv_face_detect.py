"""
Description: OpenCV camera with face detection
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import cv2
import numpy as np
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn

HOST = '0.0.0.0'
PORT = 8080
RESOLUTION = (640, 480)
FRAMERATE = 15

class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html = """
                <html>
                <head><title>Hand Gesture Stream</title></head>
                <body style="background:#222;color:white;text-align:center;">
                    <h1>🖐️ Hand Gesture Recognition</h1>
                    <img src="/stream.mjpg" width="80%" style="border:5px solid green;border-radius:10px;" />
                </body>
                </html>
            """
            self.wfile.write(html.encode('utf-8'))
        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
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
        else:
            self.send_error(404)
            self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

def detect_gesture(contour, defects, frame):
    if defects is None or contour is None:
        return "No Hand Detected"

    count_defects = 0
    for i in range(defects.shape[0]):
        s, e, f, _ = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        far = tuple(contour[f][0])

        a = np.linalg.norm(np.array(end) - np.array(start))
        b = np.linalg.norm(np.array(far) - np.array(start))
        c = np.linalg.norm(np.array(end) - np.array(far))
        angle = np.arccos((b**2 + c**2 - a**2) / (2 * b * c + 1e-5)) * 57

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
    ret, frame = camera.read()
    if not ret:
        return None

    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_skin = np.array([0, 20, 70], dtype=np.uint8)
    upper_skin = np.array([20, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(hsv, lower_skin, upper_skin)
    mask = cv2.GaussianBlur(mask, (5, 5), 100)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    gesture = "No Hand Detected"

    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        if cv2.contourArea(max_contour) > 2000:
            hull = cv2.convexHull(max_contour)
            cv2.drawContours(frame, [max_contour], -1, (0, 255, 0), 2)
            cv2.drawContours(frame, [hull], -1, (0, 0, 255), 2)
            hull_indices = cv2.convexHull(max_contour, returnPoints=False)
            if len(hull_indices) > 3:
                defects = cv2.convexityDefects(max_contour, hull_indices)
                gesture = detect_gesture(max_contour, defects, frame)

    cv2.putText(frame, gesture, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3)

    _, jpeg = cv2.imencode('.jpg', frame)
    return jpeg.tobytes()

def main():
    global camera
    camera = cv2.VideoCapture(0)
    camera.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
    camera.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])

    try:
        server = ThreadedHTTPServer((HOST, PORT), StreamingHandler)
        print(f"🌐 Open in browser: http://localhost:{PORT}/")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")
        camera.release()

if __name__ == '__main__':
    main()
