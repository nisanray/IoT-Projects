"""
Description: Records audio from INMP441 I2S microphone
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import sounddevice as sd
import numpy as np
import wave

def record_audio(filename="output.wav", duration=5, sample_rate=44100, channels=1, device=None):
    """Records audio from the specified input device and saves it to a WAV file.

    Args:
        filename (str): The name of the WAV file to save.
        duration (int): The recording duration in seconds.
        sample_rate (int): The sampling rate in Hz.
        channels (int): The number of audio channels (1 for mono, 2 for stereo).
        device (str or int, optional): The name or index of the audio device to use.
                                        If None, the default input device is used.
    """
    print(f"Recording for {duration} seconds...")
    try:
        recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16', device=device)
        sd.wait()  # Wait until recording is finished
        print("Recording finished.")

        # Save the recording to a WAV file
        with wave.open(filename, 'w') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 2 bytes for int16
            wf.setframerate(sample_rate)
            wf.writeframes(recording.tobytes())
        print(f"Audio saved to {filename}")

    except sd.PortAudioError as e:
        print(f"Error recording audio: {e}")
        print("Please ensure your INMP441 is correctly configured as an input device.")
        print("List available devices using: python3 -m sounddevice")
        if device:
            print(f"You specified device: {device}. Double-check if this is correct.")

if __name__ == "__main__":
    recording_duration = 10  # Set the recording duration in seconds
    output_filename = "recorded_audio.wav"
    sample_rate = 44100
    channels = 1  # Mono recording

    # You can try recording with the default device first:
    # record_audio(filename=output_filename, duration=recording_duration, sample_rate=sample_rate, channels=channels)

    # If the default device doesn't work, specify the device name or index
    # you found using 'python3 -m sounddevice' or 'arecord -l'.
    # Example (replace 'hw:1,0' with your actual device information):
    # record_audio(filename=output_filename, duration=recording_duration, sample_rate=sample_rate, channels=channels, device='hw:1,0')

    # To list available devices, run this in your terminal:
    # python3 -m sounddevice
    print("Listing available audio devices:")
    print(sd.query_devices())
    print("\nTrying to record from the default input device. If it fails, check the device list above and try specifying the 'device' parameter in the script.")
    record_audio(filename=output_filename, duration=recording_duration, sample_rate=sample_rate, channels=channels)
