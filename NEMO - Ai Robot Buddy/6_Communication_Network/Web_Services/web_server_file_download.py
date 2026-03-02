"""
Description: Flask web server for file download/sharing
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

from flask import Flask, render_template_string, request, send_file
import os
import zipfile
import io
import socket
import qrcode
import base64
from PIL import Image

app = Flask(__name__)

# Get the local IP address to generate access URL
def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip

# Generate base64-encoded QR code from URL
def generate_qr(url):
    img = qrcode.make(url)
    buffered = io.BytesIO()
    img.save(buffered, format="PNG")
    img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_b64

@app.route('/')
def index():
    files = [f for f in os.listdir('.') if os.path.isfile(f)]
    url = f"http://{get_local_ip()}:8000"
    qr = generate_qr(url)
    return render_template_string(PAGE_HTML, files=files, ip=url, qr=qr)

@app.route('/download_selected', methods=['POST'])
def download_selected():
    selected_files = request.form.getlist('files')
    if not selected_files:
        return "No files selected", 400

    zip_stream = io.BytesIO()
    with zipfile.ZipFile(zip_stream, 'w') as zf:
        for filename in selected_files:
            if os.path.isfile(filename):
                zf.write(filename)
    zip_stream.seek(0)

    return send_file(zip_stream,
                     mimetype='application/zip',
                     as_attachment=True,
                     attachment_filename='selected_files.zip')  # For older Flask versions

# HTML template included as a string
PAGE_HTML = '''
<!DOCTYPE html>
<html>
<head>
    <title>Local File Share</title>
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: #f7f7f7;
            color: #333;
            padding: 40px;
            max-width: 800px;
            margin: auto;
        }
        h1 {
            text-align: center;
            color: #222;
        }
        .qr {
            text-align: center;
            margin-bottom: 30px;
        }
        .file-list {
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .file-item {
            margin-bottom: 10px;
        }
        .actions {
            text-align: center;
            margin-top: 20px;
        }
        button {
            background: #007BFF;
            color: white;
            padding: 10px 18px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
        }
        button:hover {
            background: #0056b3;
        }
        label {
            margin-left: 8px;
        }
    </style>
</head>
<body>
    <h1>📂 File Share via WiFi</h1>
    <div class="qr">
        <img src="data:image/png;base64,{{ qr }}" width="160"><br>
        <small>Scan to open: <b>{{ ip }}</b></small>
    </div>

    <form method="POST" action="/download_selected">
        <div class="file-list">
            <div><input type="checkbox" id="selectAll" onclick="toggleAll(this)"> <label for="selectAll"><strong>Select All</strong></label></div><hr>
            {% for file in files %}
                <div class="file-item">
                    <input type="checkbox" name="files" value="{{ file }}" id="{{ file }}">
                    <label for="{{ file }}">{{ file }}</label>
                </div>
            {% endfor %}
        </div>
        <div class="actions">
            <button type="submit">⬇ Download Selected</button>
        </div>
    </form>

    <script>
        function toggleAll(source) {
            checkboxes = document.getElementsByName('files');
            for(let i = 0; i < checkboxes.length; i++) {
                checkboxes[i].checked = source.checked;
            }
        }
    </script>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
