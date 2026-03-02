"""
Description: Offline speech-to-text using Vosk engine
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import sounddevice as sd
import numpy as np
import queue
import json
import time
from vosk import Model, KaldiRecognizer

def get_input_device_with_decibel():
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
                print("Invalid choice. Try again.")
        except ValueError:
            print("Invalid input. Enter a number.")

def calculate_decibel(data):
    if data.size == 0:
        return -float('inf')
    rms = np.sqrt(np.mean(data**2))
    if rms == 0:
        return -float('inf')
    return 20 * np.log10(rms / 32768.0)  # Normalize for int16

def stream_offline_speech_to_text(model_path, sample_rate=16000, channels=1, decibel_threshold=-35, max_phrase_duration=5):
    print(f"Loading Vosk model from: {model_path}")
    model = Model(model_path)
    recognizer = KaldiRecognizer(model, sample_rate)

    device = get_input_device_with_decibel()
    if device is None:
        return

    audio_queue = queue.Queue()

    def callback(indata, frames, time_info, status):
        if status:
            print(status)
        audio_queue.put(indata.copy())

    print("Starting audio stream...")
    try:
        with sd.InputStream(callback=callback,
                            samplerate=sample_rate,
                            channels=channels,
                            dtype='int16',
                            blocksize=1024,
                            device=device):
            print(f"Monitoring microphone... (Threshold: {decibel_threshold} dBFS)")
            while True:
                chunk = audio_queue.get()
                decibel = calculate_decibel(chunk)
                print(f"Current Level: {decibel:.2f} dBFS", end='\r')

                if decibel > decibel_threshold:
                    print("\nSpeech detected. Listening...")
                    start_time = time.time()
                    recognizer.Reset()
                    while time.time() - start_time < max_phrase_duration:
                        data = audio_queue.get()
                        if recognizer.AcceptWaveform(data.tobytes()):
                            result = json.loads(recognizer.Result())
                            if result.get("text"):
                                print("Recognized:", result["text"])
                    final_result = json.loads(recognizer.FinalResult())
                    if final_result.get("text"):
                        print("Final:", final_result["text"])
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    MODEL_PATH = "vosk-model-small-en-us-0.15"  # Update this if needed
    stream_offline_speech_to_text(model_path=MODEL_PATH)
