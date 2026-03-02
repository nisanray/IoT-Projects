"""
Description: OLED control using luma library
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import time
from luma.core.interface.serial import i2c
from luma.oled.device import ssd1306
from PIL import Image, ImageDraw, ImageFont

# Setup OLED
serial = i2c(port=1, address=0x3C)
device = ssd1306(serial, width=128, height=64)

# Expression settings
expressions = ['happy', 'angry', 'surprised', 'blink']
current_index = 0

def draw_eyes(draw, expression):
    draw.rectangle((0, 0, 128, 64), outline=0, fill=0)

    # Eye positions
    left_eye_x = 20
    right_eye_x = 80
    eye_y = 20
    eye_w = 28
    eye_h = 20

    # Draw eye shapes
    def draw_eye(x, pupil_offset=0, angry_slant=None):
        if expression == 'blink':
            draw.line((x, eye_y + eye_h//2, x + eye_w, eye_y + eye_h//2), fill=255, width=2)
        else:
            # For angry, draw slanted eyes
            if angry_slant == "left":
                draw.polygon([(x, eye_y), (x + eye_w, eye_y + 5),
                              (x + eye_w, eye_y + eye_h), (x, eye_y + eye_h)],
                             outline=255, fill=0)
            elif angry_slant == "right":
                draw.polygon([(x, eye_y + 5), (x + eye_w, eye_y),
                              (x + eye_w, eye_y + eye_h), (x, eye_y + eye_h)],
                             outline=255, fill=0)
            else:
                draw.rectangle((x, eye_y, x + eye_w, eye_y + eye_h), outline=255, fill=0)

            # Draw pupil
            px = x + eye_w//2 - 3 + pupil_offset
            py = eye_y + eye_h//2 - 3
            draw.ellipse((px, py, px+6, py+6), fill=255)

    if expression == 'happy':
        draw_eye(left_eye_x)
        draw_eye(right_eye_x)
    elif expression == 'angry':
        draw_eye(left_eye_x, pupil_offset=2, angry_slant="left")
        draw_eye(right_eye_x, pupil_offset=-2, angry_slant="right")
    elif expression == 'surprised':
        draw.ellipse((left_eye_x, eye_y, left_eye_x + eye_w, eye_y + eye_h + 10), outline=255)
        draw.ellipse((right_eye_x, eye_y, right_eye_x + eye_w, eye_y + eye_h + 10), outline=255)
        draw.ellipse((left_eye_x + 10, eye_y + 10, left_eye_x + 18, eye_y + 18), fill=255)
        draw.ellipse((right_eye_x + 10, eye_y + 10, right_eye_x + 18, eye_y + 18), fill=255)
    elif expression == 'blink':
        draw_eye(left_eye_x)
        draw_eye(right_eye_x)

    # Draw text label
    draw.text((20, 0), f"{expression.capitalize()}", fill=255)

# Main loop to animate
while True:
    image = Image.new("1", (device.width, device.height))
    draw = ImageDraw.Draw(image)

    expr = expressions[current_index]
    draw_eyes(draw, expr)

    device.display(image)
    time.sleep(2)

    current_index = (current_index + 1) % len(expressions)

