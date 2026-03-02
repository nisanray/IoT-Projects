"""
Description: OLED display - variant 2
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import time
import board
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306

# === Initialize I2C and OLED ===
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()

# === Constants ===
EYE_WIDTH = 28
EYE_SPACING = 16
EYE_Y = 20
LEFT_X = 20
RIGHT_X = LEFT_X + EYE_WIDTH + EYE_SPACING

# === Expression Parameters ===
expressions = [
    ("happy",    20,  6, 0,  0),    # normal eyes
    ("angry",    10,  2, 4, -4),    # slanted eyes with pupil offset
    ("surprised",30, 10, 0,  0),    # wide open
    ("blink",     5,  5, 0,  0)     # nearly closed
]

# === Helper: Draw Eye ===
def draw_eye(draw, x, y, height, radius, pupil_offset):
    # Draw white eye shape (rounded rectangle)
    draw.rounded_rectangle((x, y, x + EYE_WIDTH, y + height), radius=radius, outline=255, fill=255)

    # Draw black pupil
    pupil_size = 6 if height > 12 else 3
    px = x + EYE_WIDTH // 2 - pupil_size // 2 + pupil_offset
    py = y + height // 2 - pupil_size // 2
    draw.ellipse((px, py, px + pupil_size, py + pupil_size), fill=0)

# === Main Loop ===
try:
    while True:
        for expr_name, height, radius, left_offset, right_offset in expressions:
            steps = 10
            for step in range(steps):
                progress = step / steps
                # Linear interpolation between old and new values
                interp = lambda start, end: int(start + (end - start) * progress)

                # Create image buffer
                image = Image.new("1", (128, 64))
                draw = ImageDraw.Draw(image)

                # Animate eyes
                draw_eye(draw, LEFT_X, EYE_Y, interp(20, height), interp(6, radius), interp(0, left_offset))
                draw_eye(draw, RIGHT_X, EYE_Y, interp(20, height), interp(6, radius), interp(0, right_offset))

                # Push to OLED
                oled.image(image)
                oled.show()
                time.sleep(0.05)

            # Hold final expression briefly
            time.sleep(1.5)

except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    print("Animation stopped.")
