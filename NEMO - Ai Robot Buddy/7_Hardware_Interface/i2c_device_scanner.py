"""
Description: Scans and lists I2C devices on the bus
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import smbus

def scan_i2c_bus():
    bus = smbus.SMBus(1)  # Use I2C bus 1
    devices = []
    for address in range(0x03, 0x78):
        try:
            bus.write_byte(address, 0)
            devices.append(hex(address))
        except:
            pass
    return devices

print("Scanning I2C bus...")
found = scan_i2c_bus()
if found:
    print("I2C devices found at:", found)
else:
    print("No I2C devices found.")
