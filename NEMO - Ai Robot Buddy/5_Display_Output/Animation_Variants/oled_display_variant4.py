"""
Description: OLED display - variant 4
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import time
import board
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306

# OLED display dimensions
WIDTH = 128
HEIGHT = 64

# Eye parameters
EYE_WIDTH = 28
EYE_Y = 20
LEFT_X = 20
RIGHT_X = 80

# Expressions
expressions = [
    {"name": "happy", "eye_height": 24, "corner_radius": 10, "left_offset": 0, "right_offset": 0, "slant": "none"},
    {"name": "angry-down", "eye_height": 14, "corner_radius": 2, "left_offset": 4, "right_offset": -4, "slant": "angry-down"},
    {"name": "angry-up", "eye_height": 14, "corner_radius": 2, "left_offset": 4, "right_offset": -4, "slant": "angry-up"},
    {"name": "surprised", "eye_height": 34, "corner_radius": 12, "left_offset": 0, "right_offset": 0, "slant": "none"},
    {"name": "blink", "eye_height": 6, "corner_radius": 2, "left_offset": 0, "right_offset": 0, "slant": "none"},
]

# Setup I2C and OLED
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c)
oled.fill(0)
oled.show()

def draw_eye(draw, x, y, height, radius, pupil_offset, slant):
    if slant == "left-down":  # right eye slanted downward toward center (⭷)
        points = [(x, y), (x + EYE_WIDTH, y + 6), (x + EYE_WIDTH, y + height), (x, y + height)]
        draw.polygon(points, outline=255, fill=255)
    elif slant == "right-down":  # left eye slanted downward toward center (⭶)
        points = [(x, y + 6), (x + EYE_WIDTH, y), (x + EYE_WIDTH, y + height), (x, y + height)]
        draw.polygon(points, outline=255, fill=255)
    elif slant == "left-up":  # right eye slanted upward toward center (⭹)
        points = [(x, y + 6), (x + EYE_WIDTH, y), (x + EYE_WIDTH, y + height), (x, y + height)]
        draw.polygon(points, outline=255, fill=255)
    elif slant == "right-up":  # left eye slanted upward toward center (⭸)
        points = [(x, y), (x + EYE_WIDTH, y + 6), (x + EYE_WIDTH, y + height), (x, y + height)]
        draw.polygon(points, outline=255, fill=255)
    else:
        draw.rounded_rectangle((x, y, x + EYE_WIDTH, y + height), radius=radius, outline=255, fill=255)

    # Draw pupil
    pupil_size = 6 if height > 10 else 3
    px = x + EYE_WIDTH // 2 - pupil_size // 2 + pupil_offset
    py = y + height // 2 - pupil_size // 2
    draw.ellipse((px, py, px + pupil_size, py + pupil_size), fill=0)

def get_slants(slant_type):
    if slant_type == "angry-down":
        return "right-down", "left-down"
    elif slant_type == "angry-up":
        return "right-up", "left-up"
    return "none", "none"

# Animation loop
while True:
    for expr in expressions:
        for step in range(10):
            factor = step / 9.0
            if step == 0:
                prev_expr = expr
            eye_h = int(expr["eye_height"] * factor + prev_expr["eye_height"] * (1 - factor))
            radius = int(expr["corner_radius"] * factor + prev_expr["corner_radius"] * (1 - factor))
            l_offset = int(expr["left_offset"] * factor + prev_expr["left_offset"] * (1 - factor))
            r_offset = int(expr["right_offset"] * factor + prev_expr["right_offset"] * (1 - factor))

            image = Image.new("1", (WIDTH, HEIGHT))
            draw = ImageDraw.Draw(image)

            slant_left, slant_right = get_slants(expr["slant"])

            draw_eye(draw, LEFT_X, EYE_Y, eye_h, radius, l_offset, slant_left)
            draw_eye(draw, RIGHT_X, EYE_Y, eye_h, radius, r_offset, slant_right)

            oled.image(image)
            oled.show()
            time.sleep(0.05)
        prev_expr = expr
        time.sleep(1.5)
