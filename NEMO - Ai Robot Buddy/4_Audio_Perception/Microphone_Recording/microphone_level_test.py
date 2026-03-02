"""
Description: Tests microphone input and decibel levels
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import sounddevice as sd
import numpy as np
import time

def calculate_decibel(data, sample_rate):
    """Calculates the Root Mean Square (RMS) and converts it to decibels."""
    if data.size == 0:
        return -float('inf')
    rms = np.sqrt(np.mean(data**2))
    if rms == 0:
        return -float('inf')
    return 20 * np.log10(rms)

def get_loudness_representation(decibel_level, threshold=-60):
    """Generates a visual representation of loudness using dots."""
    if decibel_level <= -float('inf'):
        return ""
    normalized_level = max(0, decibel_level - threshold)
    num_dots = int(normalized_level * 0.5)  # Adjust multiplier for sensitivity
    return "." * num_dots

def monitor_audio_level(sample_rate=44100, channels=1, device=None, interval=0.1):
    """Monitors the audio input level and displays it in the terminal."""
    if device is None:
        print("Available audio input devices:")
        devices = sd.query_devices()
        input_devices = [dev for dev in devices if dev['max_input_channels'] > 0]
        if not input_devices:
            print("No input devices found.")
            return
        for i, dev in enumerate(input_devices):
            print(f"[{i}] {dev['name']}")
        while True:
            try:
                choice = int(input("Enter the number of the input device to monitor: "))
                if 0 <= choice < len(input_devices):
                    device = input_devices[choice]['name']
                    break
                else:
                    print("Invalid choice.")
            except ValueError:
                print("Invalid input.")
        if device is None:
            return

    print(f"Monitoring audio level from device: {device}")
    print("Press Ctrl+C to stop.")

    try:
        with sd.InputStream(samplerate=sample_rate, channels=channels, dtype='int16', device=device) as stream:
            while True:
                data, overflowed = stream.read(int(sample_rate * interval))
                if overflowed:
                    print("Audio input overflowed!")
                if data.size > 0:
                    decibel_level = calculate_decibel(data, sample_rate)
                    loudness_representation = get_loudness_representation(decibel_level)
                    print(f"Audio Level: {decibel_level:.2f} dBFS  [{loudness_representation}]", end='\r')
                time.sleep(interval)
    except sd.PortAudioError as e:
        print(f"\nError monitoring audio: {e}")
        print("Please ensure your audio input device is correctly configured.")
        print("List available devices using: python3 -m sounddevice")
        if device:
            print(f"You specified device: {device}. Double-check if this is correct.")
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    sample_rate = 44100
    channels = 1
    monitor_audio_level(sample_rate=sample_rate, channels=channels)
