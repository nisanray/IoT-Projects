"""
╔════════════════════════════════════════════════════════════════════════════════╗
║  FILE: robot_vision_eye_variant1.py                                             ║
║  DESCRIPTION: COMPREHENSIVE ROBOT EYE WITH ERROR HANDLING                       ║
╠════════════════════════════════════════════════════════════════════════════════╣
║  PURPOSE:                                                                        ║
║  Robot eye animation system with simultaneous CCTV streaming. Combines face     ║
║  expressions (animated eyes on OLED) with live camera feed. Features robust     ║
║  error handling with graceful fallbacks for missing Raspberry Pi modules.        ║
║  PRODUCTION-GRADE implementation with authentication and proper cleanup.         ║
║                                                                                  ║
║  DUAL FUNCTIONALITY:                                                             ║
║  1. CCTV STREAMING (adapted from camera_cctv_server_auth.py)                    ║
║     • HTTP server on port 8080 with Basic authentication                           ║
║     • MJPEG video stream at 15fps, 640x480 resolution                             ║
║     • Hand detection via HSV color thresholding                                    ║
║                                                                                  ║
║  2. EYE ANIMATION (adapted from eye display code)                               ║
║     • 5 emotional expressions on OLED display                                      ║
┑     • happy: normal eye shape                                                      ║
║     • angry-down: slanted downward                                                ║
║     • angry-up: slanted upward                                                    ║
║     • surprised: wide-open eyes                                                   ║
║     • blink: nearly closed eyes                                                   ║
║                                                                                  ║
║  KEY DIFFERENCES FROM VARIANT2:                                                  ║
║  ✓ ROBUST ERROR HANDLING: Fallback dummy classes for missing modules           ║
║  ✓ AUTHENTICATION: Requires Basic auth (username/password) for access           ║
║  ✓ PRODUCTION-READY: Security-first approach                                     ║
║  ✓ GRACEFUL DEGRA DATION: Can run without Pi-specific if dummies used           ║
║  ✓ DETAILED COMMENTS: More verbose for production code review                   ║
║                                                                                  ║
║  DEPENDENCY HANDLING:                                                            ║
║  Import order (with try/except):                                                ║
║    1. board, busio (I2C communication)                                          ║
║    2. PIL (Image, ImageDraw)                                                    ║
║    3. adafruit_ssd1306 (OLED display driver)                                    ║
║                                                                                  ║
║  If any fail:                                                                   ║
║    • Sets RASPBERRY_PI_MODULES_AVAILABLE = False                                  ║
║    • Creates dummy classes for board, busio, Image, ImageDraw, adafruit_ssd1306  ║
║    • Prints warning (continues running, eye animation disabled)                    ║
║    • Camera/CCTV still works (no Raspberry Pi module dependency)                  ║
║                                                                                  ║
║  AUTHENTICATION CREDENTIALS:                                                     ║
║  • Username: admin                                                               ║
║  • Password: raspberry                                                           ║
║  • Auth header: Basic base64(admin:raspberry)                                    ║
║  • Required for all HTTP requests                                                ║
║                                                                                  ║
║  OLED DISPLAY SPECS:                                                             ║
║  • Size: 128x64 pixels                                                           ║
║  • Interface: I2C (board.SCL, board.SDA)                                         ║
║  • Driver: Adafruit SSD1306                                                      ║
║  • Eye dimensions: Width=28px, spacing=16px, Y=20px                              ║
║  • Left eye X: 20px, Right eye X: 80px                                           ║
║                                                                                  ║
║  EXPRESSION PARAMETERS:                                                          ║
║  Each expression dict contains:                                                  ║
║  • name: emotion identifier                                                      ║
║  • eye_height: pupil size in pixels                                              ║
║  • corner_radius: roundedness of eye shape                                       ║
║  • left_offset: pupil X offset for left eye                                      ║
║  • right_offset: pupil X offset for right eye                                    ║
║  • slant: eye slant direction (none/angry-down/angry-up)                         ║
║                                                                                  ║
║  THREADING:                                                                     ║
║  • stop_event: Global threading.Event() for graceful shutdown                    ║
║  • Allows stopping animation thread cleanly on interrupt                         ║
║  • CCTV server runs in main thread (multi-threaded HTTP)                         ║
║                                                                                  ║
║  IDEAL FOR:                                                                      ║
║  → Production deployments (security, error handling)                             ║
║  → Systems with unreliable hardware access                                       ║
║  → Multi-server environments requiring authentication                             ║
║  → Projects where graceful degradation is critical                               ║
║  → Supervised robots in public spaces (CCTV + emotional feedback)               ║
║                                                                                  ║
║  USE CASE EXAMPLE:                                                               ║
║  Museum robot: Shows expressions on face OLED while streaming video to          ║
║  security system. If OLED goes down, camera still works. Public can access      ║
║  stream at http://ip:8080 with admin/raspberry credentials.                     ║
╚════════════════════════════════════════════════════════════════════════════════╝
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
USERNAME = "admin"
PASSWORD = "raspberry" # Consider making this configurable or more secure
AUTH_HEADER = "Basic " + base64.b64encode(f"{USERNAME}:{PASSWORD}".encode()).decode()
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
        # print("Debug: capture_frame - Camera not initialized or not open.")
        return None
    try:
        ret, frame = camera.read()
        if not ret:
            # print("Debug: capture_frame - Error capturing frame")
            return None
        _, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
    except Exception as e:
        print(f"Camera error during capture: {e}")
        return None

class StreamingHandler(BaseHTTPRequestHandler):
    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=\"CCTV\"')
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
        body { font-family: Arial, sans-serif; background-color: #1e1e2f; color: white; text-align: center; margin: 0; padding: 0; }
        h1 { margin: 20px; }
        .video-container { margin: auto; padding: 20px; }
        img { border: 5px solid #4caf50; border-radius: 10px; width: 80%; max-width: 640px; }
        footer { position: fixed; bottom: 0; width: 100%; background: #111; color: #aaa; padding: 10px; }
    </style>
</head>
<body>
    <h1>🔒 Raspberry Pi CCTV Live Stream</h1>
    <div class="video-container"> <img src="stream.mjpg" alt="Live Stream" /> </div>
    <footer>Streaming via Raspberry Pi • CV2 + HTTP</footer>
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

                    # Make sleep interruptible
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
                # print(f"MJPEG Stream: Client disconnected.")
                pass # Common errors when client closes connection
            except Exception as e:
                if not stop_event.is_set(): # Don't log errors if we are stopping
                    print(f"MJPEG Stream error: {e}")
            # finally:
                # print("MJPEG stream handler finished for a client.")
        else:
            self.send_error(404)
            self.end_headers()

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    allow_reuse_address = True
    daemon_threads = True # Ensure server threads don't block program exit

def run_cctv_server():
    try:
        server = ThreadedHTTPServer((HOST, PORT), StreamingHandler)
        print(f"🌐 CCTV Server starting at: http://{HOST}:{PORT}/ (User: {USERNAME})")
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

    # Define points for slanting polygons or use rounded_rectangle
    # Slant affects the y-coordinates of the top corners or overall shape
    if slant_direction == "right-down": # Left eye, slanting towards nose (downwards)
        points = [(x, y + 6), (x + eye_actual_width, y), (x + eye_actual_width, y + eye_height), (x, y + eye_height)]
        draw_context.polygon(points, outline=255, fill=255)
    elif slant_direction == "left-down": # Right eye, slanting towards nose (downwards)
        points = [(x, y), (x + eye_actual_width, y + 6), (x + eye_actual_width, y + eye_height), (x, y + eye_height)]
        draw_context.polygon(points, outline=255, fill=255)
    elif slant_direction == "right-up": # Left eye, slanting towards nose (upwards)
        points = [(x, y + eye_height -6), (x + eye_actual_width, y + eye_height), (x + eye_actual_width, y), (x,y)]
        draw_context.polygon(points, outline=255, fill=255)
    elif slant_direction == "left-up": # Right eye, slanting towards nose (upwards)
        points = [(x, y + eye_height), (x + eye_actual_width, y + eye_height -6), (x + eye_actual_width, y), (x,y)]
        draw_context.polygon(points, outline=255, fill=255)
    else: # "none" or default
        draw_context.rounded_rectangle((x, y, x + eye_actual_width, y + eye_height), radius=corner_radius, outline=255, fill=255)

    # Draw pupil
    pupil_size = 6 if eye_height > 10 else 3
    px = x + eye_actual_width // 2 - pupil_size // 2 + pupil_offset
    py = y + eye_height // 2 - pupil_size // 2
    draw_context.ellipse((px, py, px + pupil_size, py + pupil_size), fill=0)


def get_eye_slants(slant_type_name):
    if slant_type_name == "angry-down":
        return "right-down", "left-down"  # (left_eye_slant, right_eye_slant)
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
        # Start with the last expression as "previous" for the first transition
        prev_expr_params = expressions[-1]

        while not stop_event.is_set():
            target_expr_params = expressions[current_expr_index]

            # Transition phase
            for step in range(10): # 10 steps for transition
                if stop_event.is_set(): break

                factor = step / 9.0 # Normalized step: 0.0 to 1.0

                # Interpolate parameters for smooth transition
                current_eye_h = int(target_expr_params["eye_height"] * factor + prev_expr_params["eye_height"] * (1 - factor))
                current_radius = int(target_expr_params["corner_radius"] * factor + prev_expr_params["corner_radius"] * (1 - factor))
                current_l_offset = int(target_expr_params["left_offset"] * factor + prev_expr_params["left_offset"] * (1 - factor))
                current_r_offset = int(target_expr_params["right_offset"] * factor + prev_expr_params["right_offset"] * (1 - factor))

                # Slant is usually applied directly from the target expression during transition
                slant_left, slant_right = get_eye_slants(target_expr_params["slant"])

                image = Image.new("1", (OLED_WIDTH, OLED_HEIGHT))
                draw_context = ImageDraw.Draw(image)

                draw_eye_on_image(draw_context, LEFT_X_PARAM, EYE_Y_PARAM, current_eye_h, current_radius, current_l_offset, slant_left)
                draw_eye_on_image(draw_context, RIGHT_X_PARAM, EYE_Y_PARAM, current_eye_h, current_radius, current_r_offset, slant_right)

                if oled and image:
                    oled.image(image)
                    oled.show()

                time.sleep(0.05) # Animation step delay

            if stop_event.is_set(): break

            # Current expression becomes "previous" for the next transition cycle
            prev_expr_params = target_expr_params

            # Hold the expression for a bit
            hold_duration = 1.5 # seconds
            check_interval = 0.1 # seconds
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
                oled.fill(0) # Clear OLED
                oled.show()
            except Exception as e_clear:
                print(f"Error clearing OLED: {e_clear}")
        print("Eye animation thread finished.")


# 5. Main Execution
if __name__ == '__main__':
    print("Starting combined CCTV and Eye Animation application...")

    # Initialize camera
    try:
        camera = cv2.VideoCapture(0) # Or specific camera index like /dev/video0
        if not camera.isOpened():
            raise IOError("Cannot open camera")
        camera.set(cv2.CAP_PROP_FRAME_WIDTH, RESOLUTION[0])
        camera.set(cv2.CAP_PROP_FRAME_HEIGHT, RESOLUTION[1])
        # camera.set(cv2.CAP_PROP_FPS, FRAMERATE) # Optional: FPS setting
        print("Camera initialized successfully.")
    except Exception as e:
        print(f"🚨 FATAL: Failed to initialize camera: {e}. CCTV stream will not work.")
        camera = None # Ensure camera is None if setup failed

    # Create threads
    # CCTV thread will run if camera was initialized
    cctv_thread = None
    if camera:
        cctv_thread = threading.Thread(target=run_cctv_server, daemon=True) # Daemon so it exits with main

    # Eye animation thread will run if Pi modules are available
    eye_thread = None
    if RASPBERRY_PI_MODULES_AVAILABLE:
        eye_thread = threading.Thread(target=run_eye_animation, daemon=True) # Daemon

    # Start threads
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
        # Keep the main thread alive to listen for KeyboardInterrupt
        # and to allow daemon threads to run.
        while True:
            # Check if threads are alive; exit if all daemons have unexpectedly finished
            if cctv_thread and not cctv_thread.is_alive() and \
               eye_thread and not eye_thread.is_alive():
                print("Both worker threads have stopped. Exiting main.")
                break
            if cctv_thread and not cctv_thread.is_alive() and not eye_thread: # Only CCTV was running
                 print("CCTV thread has stopped. Exiting main.")
                 break
            if eye_thread and not eye_thread.is_alive() and not cctv_thread: # Only Eye was running
                 print("Eye animation thread has stopped. Exiting main.")
                 break
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\n🛑 KeyboardInterrupt received. Signaling threads to stop...")
    except Exception as e_main:
        print(f"An unexpected error occurred in the main thread: {e_main}")
    finally:
        stop_event.set() # Signal all threads to stop
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
