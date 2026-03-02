"""
Description: Monitors microphone levels with sounddevice
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import sounddevice as sd
import numpy as np
import time

def mic_monitor(sample_rate=44100, channels=1, device=None, monitor_time=30):
    """
    Continuously displays input audio level as dB and an animated bar.
    No audio is recorded or saved.
    """
    print(f"🔊 Mic Monitor Active (Device: {device if device else 'Default'})")
    print(f"Listening for {monitor_time} seconds...\n")

    try:
        stream = sd.InputStream(samplerate=sample_rate,
                                channels=channels,
                                dtype='float32',
                                device=device)
        stream.start()
        start_time = time.time()

        while time.time() - start_time < monitor_time:
            data, overflowed = stream.read(1024)
            if overflowed:
                print("\n[!] Audio input overflowed")

            # Calculate volume
            rms = np.sqrt(np.mean(data**2))
            db = 20 * np.log10(rms) if rms > 0 else -90.0

            # Animation bar
            bar_length = max(0, min(int((db + 90) / 5), 20))
            animation = "." * bar_length

            # Add context message
            if db < -70:
                status = "Silence"
            elif db < -40:
                status = "Listening..."
            elif db < -20:
                status = "Normal Speech"
            else:
                status = "Loud!"

            print(f"\r🎙️  Input Level: {db:6.2f} dB [{animation:<20}] {status:<15}", end='')

        stream.stop()
        stream.close()
        print("\n✅ Monitoring ended.")

    except sd.PortAudioError as e:
        print(f"\n[Error] PortAudioError: {e}")
        print("Make sure your microphone is working and selected correctly.")
        print(sd.query_devices())

if __name__ == "__main__":
    mic_monitor(monitor_time=500)  # Monitor for 30 seconds
