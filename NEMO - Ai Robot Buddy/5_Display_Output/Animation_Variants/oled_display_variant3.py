"""
Description: OLED display - variant 3
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import time
import board
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306

# === OLED Setup ===
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()

# === Constants ===
WIDTH, HEIGHT = 128, 64
EYE_WIDTH = 28
EYE_SPACING = 16
EYE_Y = 20
LEFT_X = 20
RIGHT_X = LEFT_X + EYE_WIDTH + EYE_SPACING

# === Expression Sequence ===
expressions = [
    {
        "name": "happy",
        "eye_height": 20,
        "corner_radius": 6,
        "left_offset": 0,
        "right_offset": 0,
        "slant": "none"
    },
    {
        "name": "angry",
        "eye_height": 14,
        "corner_radius": 2,
        "left_offset": 4,
        "right_offset": -4,
        "slant": "angry"
    },
    {
        "name": "surprised",
        "eye_height": 30,
        "corner_radius": 10,
        "left_offset": 0,
        "right_offset": 0,
        "slant": "none"
    },
    {
        "name": "blink",
        "eye_height": 4,
        "corner_radius": 2,
        "left_offset": 0,
        "right_offset": 0,
        "slant": "none"
    },
]

# === Helper: Draw Eye ===
def draw_eye(draw, x, y, height, radius, pupil_offset, slant):
    if slant == "left":  # right eye slanted
        points = [
            (x, y + 0),
            (x + EYE_WIDTH, y + 6),
            (x + EYE_WIDTH, y + height),
            (x, y + height)
        ]
        draw.polygon(points, outline=255, fill=255)
    elif slant == "right":  # left eye slanted
        points = [
            (x, y + 6),
            (x + EYE_WIDTH, y + 0),
            (x + EYE_WIDTH, y + height),
            (x, y + height)
        ]
        draw.polygon(points, outline=255, fill=255)
    else:
        draw.rounded_rectangle(
            (x, y, x + EYE_WIDTH, y + height),
            radius=radius, outline=255, fill=255
        )

    # Draw pupil
    pupil_size = 6 if height > 10 else 3
    px = x + EYE_WIDTH // 2 - pupil_size // 2 + pupil_offset
    py = y + height // 2 - pupil_size // 2
    draw.ellipse((px, py, px + pupil_size, py + pupil_size), fill=0)

# === Main Loop ===
try:
    while True:
        for expr in expressions:
            steps = 10

            # Get current and target values
            eye_height = expr["eye_height"]
            radius = expr["corner_radius"]
            left_offset = expr["left_offset"]
            right_offset = expr["right_offset"]
            slant = expr["slant"]

            for step in range(steps):
                progress = step / steps
                interp = lambda s, e: int(s + (e - s) * progress)

                # Linear interpolation from "happy" to target
                curr_height = interp(20, eye_height)
                curr_radius = interp(6, radius)
                l_offset = interp(0, left_offset)
                r_offset = interp(0, right_offset)

                image = Image.new("1", (WIDTH, HEIGHT))
                draw = ImageDraw.Draw(image)

                # Left and right eye drawing
                if slant == "angry":
                    draw_eye(draw, LEFT_X, EYE_Y, curr_height, curr_radius, l_offset, slant="right")
                    draw_eye(draw, RIGHT_X, EYE_Y, curr_height, curr_radius, r_offset, slant="left")
                else:
                    draw_eye(draw, LEFT_X, EYE_Y, curr_height, curr_radius, l_offset, slant="none")
                    draw_eye(draw, RIGHT_X, EYE_Y, curr_height, curr_radius, r_offset, slant="none")

                oled.image(image)
                oled.show()
                time.sleep(0.05)

            # Hold expression briefly
            time.sleep(1.5)

except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    print("Stopped.")
