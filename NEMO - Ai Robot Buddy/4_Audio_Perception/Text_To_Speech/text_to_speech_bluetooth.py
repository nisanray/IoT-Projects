"""
Description: Text-to-speech output via Bluetooth
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import os
import subprocess
import time
import pyttsx3

def play_tts_bluetooth(text, bluetooth_name="BT SPEAKER"):
    """
    Plays text-to-speech audio on a previously connected Bluetooth speaker.

    Args:
        text (str): The text to synthesize and play.
        bluetooth_name (str): The name of the Bluetooth speaker.
    """

    try:
        # Initialize the TTS engine
        engine = pyttsx3.init()

        # Save the speech as an audio file
        temp_wav = "temp_tts.wav"
        engine.save_to_file(text, temp_wav)
        engine.runAndWait()

        # Find the Bluetooth device address from already paired devices
        try:
            result = subprocess.run(['bluetoothctl', 'devices'], capture_output=True, text=True, check=True)
            devices = result.stdout.split('\n')
            device_address = None
            for device in devices:
                if bluetooth_name in device:
                    device_address = device.split()[1]
                    break
            if device_address is None:
                print(f"Bluetooth device '{bluetooth_name}' not found in paired devices.")
                return

        except subprocess.CalledProcessError as e:
            print(f"Error finding Bluetooth device: {e}")
            return

        # Play the audio file on the Bluetooth speaker using aplay
        try:
            subprocess.run(['aplay', '-D', 'bluealsa:HCI=hci0,DEV=' + device_address + ',PROFILE=a2dp', temp_wav], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error playing audio: {e}")
            return

        # Clean up the temporary audio file
        os.remove(temp_wav)

        print("TTS audio played successfully on Bluetooth speaker.")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage:
if __name__ == "__main__":
    text_to_speak = "Hello, this is a test message played on your Bluetooth speaker."
    bluetooth_speaker_name = "BT SPEAKER"  # Replace with your speaker's name.
    play_tts_bluetooth(text_to_speak, bluetooth_speaker_name)
