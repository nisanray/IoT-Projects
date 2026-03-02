"""
Description: SSD1306 OLED display with hello text
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import time
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

# Create I2C interface
i2c = busio.I2C(board.SCL, board.SDA)

# Create display object (change height if using 32px screen)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)

# Clear display.
display.fill(0)
display.show()

# Create blank image for drawing.
image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)

# Load default font.
font = ImageFont.load_default()

# Draw some text
draw.text((0, 0), "Hello from Pi!", font=font, fill=255)

# Display image
display.image(image)
display.show()
