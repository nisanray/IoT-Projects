"""
Description: OLED display test/initialization
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import time
import board
import busio
from PIL import Image, ImageDraw
import adafruit_ssd1306

# Create I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create the display
WIDTH = 128
HEIGHT = 64
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear the display
oled.fill(0)
oled.show()

# Create a blank image for drawing
image = Image.new("1", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

# Animation variables
x, y = 0, 0
dx, dy = 2, 2
radius = 5

try:
    while True:
        draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)  # Clear screen

        draw.ellipse((x, y, x + radius, y + radius), outline=255, fill=255)  # Draw ball

        oled.image(image)
        oled.show()

        x += dx
        y += dy

        if x + radius >= WIDTH or x <= 0:
            dx *= -1
        if y + radius >= HEIGHT or y <= 0:
            dy *= -1

        time.sleep(0.02)

except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    print("Animation stopped.")
