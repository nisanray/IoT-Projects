"""
Description: Speech-to-text recognition using Whisper model
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import sounddevice as sd
import numpy as np
import whisper
import threading
import queue
import time

def list_devices():
    """Lists available audio input and output devices."""
    print("Available audio devices:")
    print(sd.query_devices())

class LiveTranscription:
    def __init__(self, sample_rate=16000, device=None, model_name="base"):
        self.sample_rate = sample_rate
        self.device = device
        self.model = whisper.load_model(model_name)
        self.audio_queue = queue.Queue()
        self.is_running = False
        self.recording_thread = None
        self.transcription_thread = None

    def start(self):
        """Starts live audio recording and transcription."""
        if self.is_running:
            print("Live transcription is already running.")
            return

        self.is_running = True
        self.recording_thread = threading.Thread(target=self._record_audio)
        self.transcription_thread = threading.Thread(target=self._transcribe_audio)
        self.recording_thread.start()
        self.transcription_thread.start()
        print("Live transcription started. Press Ctrl+C to stop.")

    def stop(self):
        """Stops live audio recording and transcription."""
        if not self.is_running:
            print("Live transcription is not running.")
            return

        self.is_running = False
        if self.recording_thread and self.recording_thread.is_alive():
            self.recording_thread.join()
        if self.transcription_thread and self.transcription_thread.is_alive():
            self.transcription_thread.join()
        print("Live transcription stopped.")

    def _record_audio(self):
        """Records audio chunks and puts them in the audio queue."""
        try:
            with sd.InputStream(samplerate=self.sample_rate, channels=1, dtype='int16', blocksize=int(self.sample_rate * 0.5), device=self.device) as stream:
                while self.is_running:
                    audio_chunk, overflowed = stream.read(int(self.sample_rate * 0.5)) # Read in 0.5 second chunks
                    if overflowed:
                        print("Audio input overflowed.")
                    self.audio_queue.put(audio_chunk.flatten().astype(np.float32) / 32768.0) # Normalize to [-1, 1]
        except sd.PortAudioError as e:
            print(f"Error recording audio: {e}")
            print("Please ensure your microphone is correctly configured.")
            self.is_running = False

    def _transcribe_audio(self):
        """Continuously processes audio chunks from the queue and prints the transcribed text."""
        while self.is_running:
            try:
                audio_data = self.audio_queue.get(timeout=1) # Wait for audio with a timeout
                result = self.model.transcribe(audio_data)
                if result["text"].strip():
                    print("Live:", result["text"].strip())
            except queue.Empty:
                pass # No audio to process yet
            except Exception as e:
                print(f"Error during transcription: {e}")
                self.is_running = False

if __name__ == "__main__":
    list_devices() # Show available devices for the user

    try:
        transcriber = LiveTranscription(device=None) # Use default input device, or specify device index/name
        transcriber.start()

        # Keep the main thread alive to allow background threads to continue
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nStopping live transcription...")
        if 'transcriber' in locals() and transcriber.is_running:
            transcriber.stop()
    except Exception as e:
        print(f"An error occurred: {e}")
