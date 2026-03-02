"""
Description: Records audio to WAV file using sounddevice
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import sounddevice as sd
import numpy as np
import wave
import time

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

def calculate_decibel(data, sample_rate):
    """Calculates the Root Mean Square (RMS) and converts it to decibels."""
    if data.size == 0:
        return -float('inf')  # Return negative infinity for silence
    rms = np.sqrt(np.mean(data**2))
    # Avoid log of zero
    if rms == 0:
        return -float('inf')
    return 20 * np.log10(rms)

def record_audio_with_decibel_check(filename="output.wav", duration=5, sample_rate=44100, channels=1, device=None, decibel_threshold=-30):
    """Records audio only if the decibel level exceeds the threshold.

    Args:
        filename (str): The name of the WAV file to save.
        duration (int): The recording duration in seconds.
        sample_rate (int): The sampling rate in Hz.
        channels (int): The number of audio channels (1 for mono, 2 for stereo).
        device (str or int, optional): The name or index of the audio device to use.
                                         If None, the user will be prompted to choose.
        decibel_threshold (float): The decibel level (dBFS) above which recording starts.
                                   Defaults to -30 dBFS.
    """
    if device is None:
        device = get_input_device_with_decibel()
        if device is None:
            return

    print(f"Monitoring audio levels (threshold: {decibel_threshold} dBFS)...")

    try:
        with sd.InputStream(samplerate=sample_rate, channels=channels, dtype='int16', device=device) as stream:
            audio_data = []
            start_time = None
            recording = False

            while True:
                data, overflowed = stream.read(1024)  # Read data in chunks
                if overflowed:
                    print("Audio input overflowed!")
                decibel_level = calculate_decibel(data, sample_rate)
                print(f"Current level: {decibel_level:.2f} dBFS", end='\r')

                if not recording and decibel_level > decibel_threshold:
                    print("\nThreshold exceeded! Starting recording...")
                    recording = True
                    start_time = time.time()
                    audio_data.append(data)
                elif recording:
                    audio_data.append(data)
                    if time.time() - start_time >= duration:
                        print("\nRecording finished (duration reached).")
                        break
                elif recording is False and start_time is not None and time.time() - start_time >= 1:
                    # Reset start_time if no audio for 1 second after initial trigger
                    start_time = None

            if recording and audio_data:
                print("Saving recorded audio...")
                recording_array = np.concatenate(audio_data, axis=0)
                with wave.open(filename, 'w') as wf:
                    wf.setnchannels(channels)
                    wf.setsampwidth(2)  # 2 bytes for int16
                    wf.setframerate(sample_rate)
                    wf.writeframes(recording_array.tobytes())
                print(f"Audio saved to {filename}")
            else:
                print("No audio recorded above the threshold.")

    except sd.PortAudioError as e:
        print(f"\nError recording audio: {e}")
        print("Please ensure your audio input device is correctly configured.")
        print("List available devices using: python3 -m sounddevice")
        if device:
            print(f"You specified device: {device}. Double-check if this is correct.")

if __name__ == "__main__":
    recording_duration = 5  # Maximum recording duration in seconds after trigger
    output_filename = "triggered_audio.wav"
    sample_rate = 44100
    channels = 1  # Mono recording
    decibel_threshold = -30  # Adjust this value as needed

    record_audio_with_decibel_check(
        filename=output_filename,
        duration=recording_duration,
        sample_rate=sample_rate,
        channels=channels,
        decibel_threshold=decibel_threshold
    )
