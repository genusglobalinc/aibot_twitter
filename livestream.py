import os
import time
from datetime import datetime, timedelta
from flask import Flask, request, render_template, jsonify
import threading
import subprocess

# Configuration
VIDEO_FOLDER = "/path/to/lofi/background/videos"
SPOTIFY_CLIENT_ID = 'your_spotify_client_id'
SPOTIFY_CLIENT_SECRET = 'your_spotify_client_secret'
SPOTIFY_REDIRECT_URI = 'your_spotify_redirect_uri'
SPOTIFY_PLAYLIST_URI = 'spotify:playlist:your_playlist_uri'
OBS_LUA_SCRIPTS_PATH = '/path/to/obs/scripts'
RESTREAM_API_KEY = 'your_restream_api_key'

# Flask setup
app = Flask(__name__)

# Load videos from folder
def load_videos():
    return [os.path.join(VIDEO_FOLDER, video) for video in os.listdir(VIDEO_FOLDER) if video.endswith(".mp4")]

# Function to execute Lua script
def execute_lua_script(script_name):
    script_path = os.path.join(OBS_LUA_SCRIPTS_PATH, script_name)
    subprocess.run(['obs-cli', '--run-script', script_path])

# Flask routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/commands')
def commands():
    return render_template('commands.html', commands=[
        "start_stream", "stop_stream", "start_recording", "stop_recording",
        "center_scene_element", "move_scene_element_top_right", "add_text", "edit_text"
    ])

@app.route('/start_stream', methods=['POST'])
def start_stream():
    execute_lua_script('start_stream.lua')
    return jsonify({"status": "Stream started"})

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    execute_lua_script('stop_stream.lua')
    return jsonify({"status": "Stream stopped"})

@app.route('/start_recording', methods=['POST'])
def start_recording():
    execute_lua_script('start_recording.lua')
    return jsonify({"status": "Recording started"})

@app.route('/stop_recording', methods=['POST'])
def stop_recording():
    execute_lua_script('stop_recording.lua')
    return jsonify({"status": "Recording stopped"})

@app.route('/preview_stream', methods=['POST'])
def preview_stream():
    # Add your preview stream logic here
    return jsonify({"status": "Preview started"})

@app.route('/center_scene_element', methods=['POST'])
def center_scene_element():
    execute_lua_script('center_scene_element.lua')
    return jsonify({"status": "Element centered"})

@app.route('/move_scene_element_top_right', methods=['POST'])
def move_scene_element_top_right():
    execute_lua_script('move_scene_element_top_right.lua')
    return jsonify({"status": "Element moved to top right"})

@app.route('/add_text', methods=['POST'])
def add_text():
    text = request.form.get('text')
    # You may need to modify the Lua script to take the text as an argument
    execute_lua_script('add_text.lua')
    return jsonify({"status": f"Text '{text}' added"})

@app.route('/edit_text', methods=['POST'])
def edit_text():
    text = request.form.get('text')
    # You may need to modify the Lua script to take the text as an argument
    execute_lua_script('edit_text.lua')
    return jsonify({"status": f"Text changed to '{text}'"})

@app.route('/restream_status', methods=['GET'])
def restream_status():
    # Add your restream status check logic here
    return jsonify({"status": "Restream status"})

# Scheduler
def scheduler():
    while True:
        now = datetime.now()
        next_start = (now + timedelta(days=1)).replace(hour=6, minute=0, second=0, microsecond=0)
        time_to_sleep = (next_start - now).total_seconds()
        time.sleep(time_to_sleep)
        execute_lua_script('start_stream.lua')
        time.sleep(12 * 3600)  # Run for 12 hours
        execute_lua_script('stop_stream.lua')

if __name__ == '__main__':
    threading.Thread(target=scheduler).start()
    app.run(host='0.0.0.0', port=5000)
