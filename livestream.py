from flask import Flask, send_file, request
import random
import os
import time
from flask_socketio import SocketIO, emit

app = Flask(__name__)
socketio = SocketIO(app)

# Path to the folder containing MP3 files
music_folder = "path/to/music/folder"

# Path to the background video file
video_file = "path/to/background/video.mp4"

# Variables for controlling the music playback
music_paused = False
start_time = time.time()

# Variable for indicating preview mode
preview_mode = False

# Flask route to capture and serve scene image
@app.route('/capture_scene')
def capture_scene():
    # Dummy implementation to serve a placeholder image
    # Replace this with actual implementation to capture scene image from OBS
    return send_file('placeholder.png', mimetype='image/png')

@app.route('/')
def index():
    # Return HTML page with video background and control buttons
    return send_file('index.html')

@app.route('/video')
def get_video():
    # Serve the background video file
    return send_file(video_file, mimetype='video/mp4')

@app.route('/music')
def stream_music():
    global music_paused
    if not music_paused:
        # Randomly select an MP3 file from the music folder
        mp3_files = [f for f in os.listdir(music_folder) if f.endswith('.mp3')]
        random_mp3 = random.choice(mp3_files)
        return send_file(os.path.join(music_folder, random_mp3), mimetype='audio/mpeg')
    else:
        return '', 204  # No content if music is paused

@app.route('/pause_music', methods=['GET'])
def pause_music():
    global music_paused
    music_paused = True
    return "Music paused"

@app.route('/resume_music', methods=['GET'])
def resume_music():
    global music_paused
    music_paused = False
    return "Music resumed"

@app.route('/get_timer', methods=['GET'])
def get_timer():
    global start_time
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    return '{:02d}:{:02d}'.format(minutes, seconds)

@app.route('/toggle_preview', methods=['GET'])
def toggle_preview():
    global preview_mode
    preview_mode = not preview_mode
    return str(preview_mode)

@socketio.on('pause_music')
def handle_pause_music():
    global music_paused
    music_paused = True
    emit('music_paused', 'Music paused')

@socketio.on('resume_music')
def handle_resume_music():
    global music_paused
    music_paused = False
    emit('music_resumed', 'Music resumed')

if __name__ == '__main__':
    socketio.run(app, debug=True)
