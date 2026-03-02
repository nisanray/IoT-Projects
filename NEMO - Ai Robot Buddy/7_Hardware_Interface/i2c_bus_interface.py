"""
Description: I2C bus interface using smbus2
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

from smbus2 import SMBus

def scan_i2c():
    with SMBus(1) as bus:
        print("Scanning I2C bus...")
        for addr in range(0x03, 0x78):
            try:
                bus.read_byte(addr)
                print(f"Found device at 0x{addr:02X}")
            except: pass

scan_i2c()
