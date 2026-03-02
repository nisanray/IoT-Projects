"""
Description: Flask web server for playing WAV files
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import os
from flask import Flask, render_template, send_from_directory
from pydub import AudioSegment  # Import for getting audio info (optional)

app = Flask(__name__)
AUDIO_FOLDER = '.'  # Current directory

def get_audio_files():
    """Returns a list of WAV files in the AUDIO_FOLDER."""
    files = os.listdir(AUDIO_FOLDER)
    return [f for f in files if f.lower().endswith('.wav')]

def get_audio_info(filepath):
    """(Optional) Returns basic info about the audio file."""
    try:
        audio = AudioSegment.from_wav(filepath)
        duration_ms = len(audio)
        duration_sec = duration_ms / 1000
        return f"{duration_sec:.2f} seconds"
    except Exception as e:
        return "N/A"

@app.route('/')
def index():
    """Renders the main web page with the list of audio files."""
    audio_files = get_audio_files()
    audio_info = {f: get_audio_info(os.path.join(AUDIO_FOLDER, f)) for f in audio_files}
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>WAV Player</title>
        <style>
            body {{
                font-family: sans-serif;
                background-color: #f4f4f4;
                color: #333;
                margin: 20px;
            }}
            h1 {{
                color: #007bff;
                text-align: center;
                margin-bottom: 20px;
            }}
            .audio-list {{
                list-style: none;
                padding: 0;
            }}
            .audio-item {{
                background-color: #fff;
                border: 1px solid #ddd;
                padding: 15px;
                margin-bottom: 10px;
                border-radius: 5px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .audio-title {{
                flex-grow: 1;
            }}
            .play-button {{
                background-color: #28a745;
                color: white;
                border: none;
                padding: 8px 15px;
                border-radius: 5px;
                cursor: pointer;
                text-decoration: none;
            }}
            .play-button:hover {{
                background-color: #1e7e34;
            }}
            .audio-info {{
                color: #777;
                font-size: 0.9em;
                margin-left: 10px;
            }}
        </style>
    </head>
    <body>
        <h1>WAV File Player</h1>
        <ul class="audio-list">
            """
    for file in audio_files:
        info = audio_info.get(file, "N/A")
        html_content += f"""
            <li class="audio-item">
                <span class="audio-title">{file}</span>
                <span class="audio-info">({info})</span>
                <audio controls>
                    <source src="/play/{file}" type="audio/wav">
                    Your browser does not support the audio element.
                </audio>
            </li>
        """
    html_content += """
        </ul>
    </body>
    </html>
    """
    return html_content

@app.route('/play/<filename>')
def play_audio(filename):
    """Serves the requested audio file."""
    return send_from_directory(AUDIO_FOLDER, filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
