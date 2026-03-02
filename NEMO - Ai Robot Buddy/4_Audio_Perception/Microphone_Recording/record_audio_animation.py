"""
Description: Records audio for animation synchronization
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import sounddevice as sd
import numpy as np
import wave
import time
import os

def record_audio(filename="output.wav", duration=5, sample_rate=44100, channels=1, device=None):
    """Records audio from the specified input device and saves it to a WAV file,
    while also displaying the input level in dB and an animation in the SSH.

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
        stream = sd.InputStream(samplerate=sample_rate, channels=channels, dtype='int16', device=device)
        stream.start()
        start_time = time.time()
        recording = []

        while time.time() - start_time < duration:
            data, overflowed = stream.read(1024)  # Read data in chunks
            if overflowed:
                print('Audio input overflowed')
            recording.append(data)

            # Calculate RMS (Root Mean Square) for a rough estimate of volume
            rms = np.sqrt(np.mean(data**2))
            # Convert RMS to dB (a common way to represent audio level)
            if rms > 0:
                db = 20 * np.log10(rms / 32768.0)  # Normalize by the maximum value of int16
            else:
                db = -90.0  # Set a very low dB value for silence

            # Create a simple animation based on the dB level
            bar_length = max(0, min(int((db + 90) / 5), 20)) # Scale dB to a reasonable bar length (adjust -90 if needed)
            animation = "." * bar_length

            # Clear the previous line in the terminal and print the current status
            print(f"\rInput Level: {db:.2f} dB [{animation:<20}]", end='')

        stream.stop()
        stream.close()
        print("\nRecording finished.")

        recording_array = np.concatenate(recording, axis=0)

        # Save the recording to a WAV file
        with wave.open(filename, 'w') as wf:
            wf.setnchannels(channels)
            wf.setsampwidth(2)  # 2 bytes for int16
            wf.setframerate(sample_rate)
            wf.writeframes(recording_array.tobytes())
        print(f"Audio saved to {filename}")

    except sd.PortAudioError as e:
        print(f"\nError recording audio: {e}")
        print("Please ensure your INMP441 is correctly configured as an input device.")
        print("List available devices using: python3 -m sounddevice")
        if device:
            print(f"You specified device: {device}. Double-check if this is correct.")

if __name__ == "__main__":
    recording_duration = 30  # Set the recording duration in seconds
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
