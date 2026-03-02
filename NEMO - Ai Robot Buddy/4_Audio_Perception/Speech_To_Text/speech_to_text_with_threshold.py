"""
Description: Speech recognition with decibel threshold detection
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import sounddevice as sd
import numpy as np
import speech_recognition as sr
import time
import queue

def get_input_device_with_decibel():
    """Lists audio input devices and prompts the user to choose one."""
    print("Available audio input devices:")
    devices = sd.query_devices()
    input_devices = [dev for dev in devices if dev['max_input_channels'] > 0]
    if not input_devices:
        print("No input devices found.")
        return None

    for i, device in enumerate(input_devices):
        print(f"[{i}] {device['name']}")

    while True:
        try:
            choice = int(input("Enter the number of the input device to use: "))
            if 0 <= choice < len(input_devices):
                return input_devices[choice]['name']
            else:
                print("Invalid choice. Please enter a number from the list.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def calculate_decibel(data):
    """Calculates RMS and converts to decibel level safely."""
    data = np.array(data, dtype=np.float32)
    if data.size == 0:
        return -float('inf')

    mean_square = np.mean(data**2)
    if mean_square <= 0:
        return -float('inf')

    rms = np.sqrt(mean_square)
    # Normalize by max int16 value for dBFS
    return 20 * np.log10(rms / 32768.0)

def stream_to_text(duration=5, sample_rate=16000, channels=1, decibel_threshold=-35):
    print(f"Monitoring mic (threshold: {decibel_threshold} dBFS)...")

    device = get_input_device_with_decibel()
    if device is None:
        return

    recognizer = sr.Recognizer()
    q_audio = queue.Queue()

    def callback(indata, frames, time_info, status):
        if status:
            print("InputStream status:", status)
        q_audio.put(indata.copy())

    try:
        with sd.InputStream(callback=callback,
                            samplerate=sample_rate,
                            channels=channels,
                            dtype='int16',
                            blocksize=1024,
                            device=device):
            while True:
                audio_chunk = q_audio.get()
                decibel = calculate_decibel(audio_chunk)
                print(f"Current Level: {decibel:.2f} dBFS", end='\r')

                if decibel > decibel_threshold:
                    print("\nDecibel threshold exceeded. Listening...")

                    # Collect frames for the specified duration
                    frames = [audio_chunk]
                    start_time = time.time()
                    while time.time() - start_time < duration:
                        frames.append(q_audio.get())

                    # Concatenate and flatten frames to 1D int16 array
                    audio_data = np.concatenate(frames, axis=0).flatten()

                    # Convert to bytes for recognizer
                    audio_bytes = audio_data.tobytes()

                    try:
                        audio = sr.AudioData(audio_bytes, sample_rate, 2)  # 2 bytes per sample (int16)
                        text = recognizer.recognize_sphinx(audio)
                        print("You said:", text)
                    except sr.UnknownValueError:
                        print("Could not understand audio (Sphinx)")
                    except sr.RequestError as e:
                        print(f"Sphinx error: {e}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    stream_to_text(duration=5, sample_rate=16000, channels=1, decibel_threshold=-35)
