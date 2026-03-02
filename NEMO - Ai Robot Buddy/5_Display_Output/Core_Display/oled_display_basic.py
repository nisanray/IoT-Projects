"""
Description: Basic OLED display functionality
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import time
import board
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306

# Initialize I2C interface and OLED display
i2c = busio.I2C(board.SCL, board.SDA)
oled = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
oled.fill(0)
oled.show()

# Define eye positions and dimensions
left_eye_x = 20
right_eye_x = 80
eye_y = 20
eye_width = 28
eye_height = 20

def draw_expression(expression):
    image = Image.new("1", (oled.width, oled.height))
    draw = ImageDraw.Draw(image)

    def draw_eye(x, pupil_offset=0, height=eye_height, slant=None):
        # Draw eye outline
        if slant == "left":
            # Slanted top-left corner
            draw.polygon([
                (x, eye_y + 5),
                (x + eye_width, eye_y),
                (x + eye_width, eye_y + height),
                (x, eye_y + height)
            ], outline=255, fill=0)
        elif slant == "right":
            # Slanted top-right corner
            draw.polygon([
                (x, eye_y),
                (x + eye_width, eye_y + 5),
                (x + eye_width, eye_y + height),
                (x, eye_y + height)
            ], outline=255, fill=0)
        else:
            # Regular eye
            draw.rectangle((x, eye_y, x + eye_width, eye_y + height), outline=255, fill=0)

        # Draw pupil
        pupil_size = 6 if height > 10 else 3
        px = x + eye_width // 2 - pupil_size // 2 + pupil_offset
        py = eye_y + height // 2 - pupil_size // 2
        draw.ellipse((px, py, px + pupil_size, py + pupil_size), outline=255, fill=255)

    if expression == 'happy':
        draw_eye(left_eye_x)
        draw_eye(right_eye_x)
    elif expression == 'angry':
        draw_eye(left_eye_x, pupil_offset=2, height=14, slant="left")
        draw_eye(right_eye_x, pupil_offset=-2, height=14, slant="right")
    elif expression == 'surprised':
        draw_eye(left_eye_x, height=24)
        draw_eye(right_eye_x, height=24)
    elif expression == 'blink':
        # Draw closed eyes as horizontal lines
        draw.line((left_eye_x, eye_y + eye_height // 2, left_eye_x + eye_width, eye_y + eye_height // 2), fill=255)
        draw.line((right_eye_x, eye_y + eye_height // 2, right_eye_x + eye_width, eye_y + eye_height // 2), fill=255)

    # Display expression label
    draw.text((32, 56), expression.upper(), fill=255)

    # Update OLED display
    oled.image(image)
    oled.show()

# Cycle through expressions
expressions = ['happy', 'angry', 'surprised', 'blink']
while True:
    for expr in expressions:
        draw_expression(expr)
        time.sleep(2)
