"""
Description: Draws images on OLED display
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import time
from PIL import Image, ImageDraw
import board
import busio
import adafruit_ssd1306

# Create I2C interface.
i2c = busio.I2C(board.SCL, board.SDA)

# Create the SSD1306 OLED class.
# Change width and height if your OLED size is different.
WIDTH = 128
HEIGHT = 64
oled = adafruit_ssd1306.SSD1306_I2C(WIDTH, HEIGHT, i2c, addr=0x3C)

# Clear display.
oled.fill(0)
oled.show()

# Create blank image for drawing.
image = Image.new("1", (WIDTH, HEIGHT))

# Create drawing object.
draw = ImageDraw.Draw(image)

# Animation parameters
rect_width = 20
rect_height = 10
x_pos = 0
y_pos = (HEIGHT - rect_height) // 2
step = 2

try:
    while True:
        # Clear image
        draw.rectangle((0, 0, WIDTH, HEIGHT), outline=0, fill=0)
        
        # Draw moving rectangle
        draw.rectangle((x_pos, y_pos, x_pos + rect_width, y_pos + rect_height), outline=255, fill=255)
        
        # Display image
        oled.image(image)
        oled.show()
        
        # Update position
        x_pos += step
        if x_pos + rect_width > WIDTH or x_pos < 0:
            step = -step
        
        time.sleep(0.05)

except KeyboardInterrupt:
    oled.fill(0)
    oled.show()
    print("Animation stopped.")
