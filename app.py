from flask import Flask, render_template, request, send_from_directory
import os
import subprocess
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Folder to save downloaded music
DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

# Function to download music using SpotDL
def download_spotify_playlist(playlist_url):
    command = f"spotdl {playlist_url} --output {DOWNLOAD_FOLDER}"
    subprocess.run(command, shell=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    playlist_url = request.form['playlist_url']
    if playlist_url:
        download_spotify_playlist(playlist_url)
        return render_template('index.html', success=True)
    return render_template('index.html', error="Please enter a valid Spotify playlist URL.")

@app.route('/downloads/<filename>')
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename)

if __name__ == '__main__':
    app.run(debug=True)
