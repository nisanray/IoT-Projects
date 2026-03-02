"""
Description: Robot eye simulation - variant 2
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

# 1. Imports
import cv2
import time
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import threading

# Attempt to import Raspberry Pi specific modules, provide dummies if not available
try:
    import board
    import busio
    from PIL import Image, ImageDraw
    import adafruit_ssd1306
    RASPBERRY_PI_MODULES_AVAILABLE = True
except ImportError:
    RASPBERRY_PI_MODULES_AVAILABLE = False
    print("Warning: Raspberry Pi specific modules (board, busio, PIL, adafruit_ssd1306) not found. Eye animation will be skipped.")
    # Dummy classes/functions if modules are missing, so the script can run without error (eye part will be disabled)
    class Image:
        @staticmethod
        def new(mode, size): return None
    class ImageDraw:
        @staticmethod
        def Draw(img): return None
    class adafruit_ssd1306:
        class SSD1306_I2C:
            def __init__(self, w, h, i2c_bus, addr=0x3C, reset=None): pass
            def fill(self, val): pass
            def image(self, img): pass
            def show(self): pass
    class busio:
        class I2C:
            def __init__(self, scl, sda): pass
    class board:
        SCL = None
        SDA = None


# 2. Global Variables & Constants

# From cc.py
HOST = '0.0.0.0'
PORT = 8080
RESOLUTION = (640, 480)
FRAMERATE = 15
camera = None # Will be initialized in main

# From eye.py (or defaults if modules missing)
OLED_WIDTH = 128
OLED_HEIGHT = 64
EYE_WIDTH_PARAM = 28
EYE_Y_PARAM = 20
LEFT_X_PARAM = 20
RIGHT_X_PARAM = 80
expressions = [
    {"name": "happy", "eye_height": 24, "corner_radius": 10, "left_offset": 0, "right_offset": 0, "slant": "none"},
    {"name": "angry-down", "eye_height": 14, "corner_radius": 2, "left_offset": 4, "right_offset": -4, "slant": "angry-down"},
    {"name": "angry-up", "eye_height": 14, "corner_radius": 2, "left_offset": 4, "right_offset": -4, "slant": "angry-up"},
    {"name": "surprised", "eye_height": 34, "corner_radius": 12, "left_offset": 0, "right_offset": 0, "slant": "none"},
    {"name": "blink", "eye_height": 6, "corner_radius": 2, "left_offset": 0, "right_offset": 0, "slant": "none"},
]

# For graceful shutdown
stop_event = threading.Event()

# 3. CCTV Functionality (adapted from cc.py)

def capture_frame():
    global camera
    if camera is None or not camera.isOpened():
        return None
    try:
        ret, frame = camera.read()
        if not ret:
            return None
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    except Exception as e:
        print(f"Camera error during capture: {e}")
        return None

class StreamingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html; charset=utf-8')
            self.end_headers()
            html_content = """<!DOCTYPE html>
<html>
<head>
    <title>CCTV Stream</title>
</head>
<body>
<center>
    <img src="stream.mjpg" alt="Live Stream" />
</center>
</body>
</html>"""
            self.wfile.write(html_content.encode('utf-8'))

        elif self.path == '/stream.mjpg':
            self.send_response(200)
            self.send_header('Content-type', 'multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            try:
                while not stop_event.is_set():
                    frame = capture_frame()
                    if frame is None:
                        if not camera or not camera.isOpened() or stop_event.is_set():
                            break
                        time.sleep(0.1) # Wait if frame capture failed but camera should be there
                        continue

                    self.wfile.write(b'--jpgboundary\r\n')
                    self.send_header('Content-type', 'image/jpeg')
                    self.send_header('Content-length', str(len(frame)))
                    self.end_headers()
                    self.wfile.write(frame)
                    self.wfile.write(b'\r\n')

                    sleep_duration = 1.0 / FRAMERATE
                    check_interval = 0.05 # Check stop_event every 50ms
                    num_checks = int(sleep_duration / check_interval)
                    for _ in range(num_checks):
                        if stop_event.is_set(): break
                        time.sleep(check_interval)
                    if stop_event.is_set(): break
                    remaining_sleep = sleep_duration - (num_checks * check_interval)
                    if remaining_sleep > 0: time.sleep(remaining_sleep)

            except (BrokenPipeError, ConnectionResetError):
                pass
            except Exception as e:
                if not stop_event.is_set():
                    print(f"MJPEG Stream error: {e}")
        else:
            self.send_error(404)
            self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True

def run_cctv_server():
    try:
        server = ThreadedHTTPServer((HOST, PORT), StreamingHandler)
        print(f"🌐 CCTV Server starting at: http://{HOST}:{PORT}/")
        server.timeout = 1 # Timeout for server.handle_request()
        while not stop_event.is_set():
            server.handle_request()
        print("CCTV server shutting down...")
        server.server_close()
    except Exception as e:
        if not stop_event.is_set():
            print(f"CCTV Server error: {e}")
    finally:
        print("CCTV server thread finished.")

# 4. Eye Animation Functionality (adapted from eye.py)

def draw_eye_on_image(draw_context, x, y, eye_height, corner_radius, pupil_offset, slant_direction):
    if not RASPBERRY_PI_MODULES_AVAILABLE or draw_context is None: return

    eye_actual_width = EYE_WIDTH_PARAM

    if slant_direction == "right-down":
        points = [(x, y + 6), (x + eye_actual_width, y), (x + eye_actual_width, y + eye_height), (x, y + eye_height)]
        draw_context.polygon(points, outline=255, fill=255)
    elif slant_direction == "left-down":
        points = [(x, y), (x + eye_actual_width, y + 6), (x + eye_actual_width, y + eye_height), (x, y + eye_height)]
        draw_context.polygon(points, outline=255, fill=255)
    elif slant_direction == "right-up":
        points = [(x, y + eye_height -6), (x + eye_actual_width, y + eye_height), (x + eye_actual_width, y), (x,y)]
        draw_context.polygon(points, outline=255, fill=255)
    elif slant_direction == "left-up":
        points = [(x, y + eye_height), (x + eye_actual_width, y + eye_height -6), (x + eye_actual_width, y), (x,y)]
        draw_context.polygon(points, outline=255, fill=255)
    else: # "none" or default
        draw_context.rounded_rectangle((x, y, x + eye_actual_width, y + eye_height), radius=corner_radius, outline=255, fill=255)

    pupil_size = 6 if eye_height > 10 else 3
    px = x + eye_actual_width // 2 - pupil_size // 2 + pupil_offset
    py = y + eye_height // 2 - pupil_size // 2
    draw_context.ellipse((px, py, px + pupil_size, py + pupil_size), fill=0)


def get_eye_slants(slant_type_name):
    if slant_type_name == "angry-down":
        return "right-down", "left-down"
    elif slant_type_name == "angry-up":
        return "right-up", "left-up"
    return "none", "none"


def run_eye_animation():
    if not RASPBERRY_PI_MODULES_AVAILABLE:
        print("Eye animation skipped as required modules are not available.")
        return

    oled = None
    try:
        i2c = busio.I2C(board.SCL, board.SDA)
        oled = adafruit_ssd1306.SSD1306_I2C(OLED_WIDTH, OLED_HEIGHT, i2c)
        oled.fill(0)
        oled.show()
        print("OLED display initialized for eye animation.")

        current_expr_index = 0
        prev_expr_params = expressions[-1]

        while not stop_event.is_set():
            target_expr_params = expressions[current_expr_index]

            for step in range(10):
                if stop_event.is_set(): break
                factor = step / 9.0

                current_eye_h = int(target_expr_params["eye_height"] * factor + prev_expr_params["eye_height"] * (1 - factor))
                current_radius = int(target_expr_params["corner_radius"] * factor + prev_expr_params["corner_radius"] * (1 - factor))
                current_l_offset = int(target_expr_params["left_offset"] * factor + prev_expr_params["left_offset"] * (1 - factor))
                current_r_offset = int(target_expr_params["right_offset"] * factor + prev_expr_params["right_offset"] * (1 - factor))
                slant_left, slant_right = get_eye_slants(target_expr_params["slant"])

                image = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
                draw_context = ImageDraw.Draw(image)

                draw_eye_on_image(draw_context, LEFT_X_PARAM, EYE_Y_PARAM, current_eye_h, current_radius, current_l_offset, slant_left)
                draw_eye_on_image(draw_context, RIGHT_X_PARAM, EYE_Y_PARAM, current_eye_h, current_radius, current_r_offset, slant_right)

                if oled and image:
                    oled.image(image)
                    oled.show()
                time.sleep(0.05)

            if stop_event.is_set(): break
            prev_expr_params = target_expr_params

            hold_duration = 1.5
            check_interval = 0.1
            num_hold_checks = int(hold_duration / check_interval)
            for _ in range(num_hold_checks):
                if stop_event.is_set(): break
                time.sleep(check_interval)
            if stop_event.is_set(): break

            current_expr_index = (current_expr_index + 1) % len(expressions)

    except Exception as e:
        if not stop_event.is_set():
            print(f"Eye animation error: {e}")
    finally:
        if RASPBERRY_PI_MODULES_AVAILABLE and oled:
            try:
                oled.fill(0)
                oled.show()
            except Exception as e_clear:
                print(f"Error clearing OLED: {e_clear}")
        print("Eye animation thread finished.")


# 5. Main Execution
if __name__ == '__main__':
    print("Starting combined CCTV and Eye Animation application...")

    try:
        camera = cv2.VideoCapture(0)
        if not camera.isOpened():
            raise IOError("Cannot open camera")
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])
        print("Camera initialized successfully.")
    except Exception as e:
        print(f"🚨 FATAL: Failed to initialize camera: {e}. CCTV stream will not work.")
        camera = None

    cctv_thread = None
    if camera:
        cctv_thread = threading.Thread(target=run_cctv_server, daemon=True)

    eye_thread = None
    if RASPBERRY_PI_MODULES_AVAILABLE:
        eye_thread = threading.Thread(target=run_eye_animation, daemon=True)

    if cctv_thread:
        cctv_thread.start()
    if eye_thread:
        eye_thread.start()

    if not cctv_thread and not eye_thread:
        print("Neither CCTV nor Eye Animation could be started. Exiting.")
        if camera and camera.isOpened(): camera.release()
        exit()

    print("Threads started. Press Ctrl+C to stop.")

    try:
        while True:
            all_threads_done = True
            if cctv_thread and cctv_thread.is_alive():
                all_threads_done = False
            if eye_thread and eye_thread.is_alive():
                all_threads_done = False
            
            if cctv_thread and not cctv_thread.is_alive() and eye_thread and not eye_thread.is_alive():
                 print("Both worker threads have stopped. Exiting main.")
                 break
            if cctv_thread and not cctv_thread.is_alive() and not eye_thread:
                  print("CCTV thread has stopped. Exiting main.")
                  break
            if eye_thread and not eye_thread.is_alive() and not cctv_thread:
                  print("Eye animation thread has stopped. Exiting main.")
                  break
            if all_threads_done and (cctv_thread or eye_thread): # If at least one thread was supposed to run
                print("All worker threads have unexpectedly stopped. Exiting main.")
                break

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n🛑 KeyboardInterrupt received. Signaling threads to stop...")
    except Exception as e_main:
        print(f"An unexpected error occurred in the main thread: {e_main}")
    finally:
        stop_event.set()
        print("Main thread: Waiting for worker threads to complete...")

        if cctv_thread and cctv_thread.is_alive():
            cctv_thread.join(timeout=5.0)
            if cctv_thread.is_alive(): print("CCTV thread did not stop in time.")

        if eye_thread and eye_thread.is_alive():
            eye_thread.join(timeout=5.0)
            if eye_thread.is_alive(): print("Eye animation thread did not stop in time.")

        if camera and camera.isOpened():
            camera.release()
            print("Camera released.")

        print("Application finished.")
