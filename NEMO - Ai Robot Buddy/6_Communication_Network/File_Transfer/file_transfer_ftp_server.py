"""
Description: File transfer/FTP functionality
Project: Raspberry Pi Robotics Control System
Author: Generated automatically
Purpose: Controls and coordinates robot functionality
"""

import os
import io
import zipfile
import datetime
from flask import Flask, send_file, send_from_directory, render_template_string, request
import socket
import qrcode
import base64

app = Flask(__name__)
SHARED_FOLDER = os.getcwd()

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # Get local IP
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def generate_qr(url):
    qr = qrcode.make(url)
    buf = io.BytesIO()
    qr.save(buf, format='PNG')
    return base64.b64encode(buf.getvalue()).decode('utf-8')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en" class="dark">
<head>
  <meta charset="UTF-8">
  <title>Advanced Pi File Server</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      darkMode: 'class',
    }
  </script>
</head>
<body class="bg-gray-100 dark:bg-gray-900 text-gray-900 dark:text-gray-100 min-h-screen">
  <div class="max-w-5xl mx-auto p-6">
    <div class="flex items-center justify-between mb-6">
      <h1 class="text-3xl font-bold">Raspberry Pi File Server</h1>
      <button onclick="toggleTheme()" class="px-3 py-1 text-sm rounded bg-gray-800 text-white dark:bg-gray-200 dark:text-black">Toggle Theme</button>
    </div>

    <div class="flex items-center justify-between mb-4">
      <div class="text-sm text-gray-500 dark:text-gray-400">Serving from: <code>{{ folder }}</code></div>
      <img src="data:image/png;base64,{{ qr }}" alt="QR Code" class="h-16">
    </div>

    <form method="POST" action="/download_selected">
      <div class="bg-white dark:bg-gray-800 rounded-lg shadow p-4">
        {% if files %}
        <div class="flex items-center mb-4 space-x-4">
          <button type="button" onclick="selectAll(true)" class="px-3 py-1 rounded bg-blue-600 text-white">Select All</button>
          <button type="button" onclick="selectAll(false)" class="px-3 py-1 rounded bg-gray-600 text-white">Clear All</button>
          <button type="submit" class="ml-auto px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded">Download Selected</button>
        </div>
        <div class="overflow-x-auto">
          <table class="w-full text-sm">
            <thead class="border-b border-gray-300 dark:border-gray-600">
              <tr>
                <th class="text-left p-2">Select</th>
                <th class="text-left p-2">File</th>
                <th class="text-left p-2">Size</th>
                <th class="text-left p-2">Modified</th>
                <th class="text-left p-2">Action</th>
              </tr>
            </thead>
            <tbody>
              {% for f in files %}
              <tr class="border-b border-gray-200 dark:border-gray-700">
                <td class="p-2">
                  <input type="checkbox" name="files" value="{{ f.name }}" class="file-checkbox">
                </td>
                <td class="p-2 font-medium">{{ f.name }}</td>
                <td class="p-2 text-gray-600 dark:text-gray-400">{{ f.size }}</td>
                <td class="p-2 text-gray-600 dark:text-gray-400">{{ f.modified }}</td>
                <td class="p-2">
                  <a href="/download/{{ f.name }}" class="text-blue-600 dark:text-blue-400 hover:underline">Download</a>
                </td>
              </tr>
              {% endfor %}
            </tbody>
          </table>
        </div>
        {% else %}
        <p class="text-gray-500 dark:text-gray-400">No files found.</p>
        {% endif %}
      </div>
    </form>
  </div>

  <script>
    function toggleTheme() {
      document.documentElement.classList.toggle('dark');
    }
    function selectAll(state) {
      document.querySelectorAll('.file-checkbox').forEach(cb => cb.checked = state);
    }
  </script>
</body>
</html>
'''

@app.route('/')
def index():
    files = []
    for fname in os.listdir(SHARED_FOLDER):
        path = os.path.join(SHARED_FOLDER, fname)
        if os.path.isfile(path):
            files.append({
                'name': fname,
                'size': f"{os.path.getsize(path) / 1024:.1f} KB",
                'modified': datetime.datetime.fromtimestamp(os.path.getmtime(path)).strftime('%Y-%m-%d %H:%M')
            })
    url = f"http://{get_ip()}:8000"
    qr = generate_qr(url)
    return render_template_string(HTML_TEMPLATE, files=files, folder=SHARED_FOLDER, qr=qr)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory(SHARED_FOLDER, filename, as_attachment=True)

@app.route('/download_selected', methods=['POST'])
def download_selected():
    selected_files = request.form.getlist('files')
    if not selected_files:
        return "No files selected", 400

    zip_stream = io.BytesIO()
    with zipfile.ZipFile(zip_stream, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for fname in selected_files:
            fpath = os.path.join(SHARED_FOLDER, fname)
            if os.path.isfile(fpath):
                zipf.write(fpath, arcname=fname)
    zip_stream.seek(0)
    return send_file(zip_stream, mimetype='application/zip',
                     as_attachment=True, download_name='selected_files.zip')

if __name__ == '__main__':
    ip = get_ip()
    print(f"Serving on http://{ip}:8000")
    app.run(host='0.0.0.0', port=8000)
