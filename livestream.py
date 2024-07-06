# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import requests

# Initialize Flask app
app = Flask(__name__)

# OBS WebSockets and Lua Script endpoints
OBS_WEBSOCKET_URL = "ws://localhost:4444"
OBS_LUA_SCRIPT_URL = "http://localhost:4444/lua"

# Placeholder for user credentials (replace with actual credentials)
OBS_USERNAME = "username"
OBS_PASSWORD = "password"

# Necessary functions
def obs_request(data):
    """Send a request to the OBS WebSocket server."""
    response = requests.post(OBS_LUA_SCRIPT_URL, json=data, auth=(OBS_USERNAME, OBS_PASSWORD))
    return response.json()

def get_stream_status():
    """Get the current stream status."""
    data = {"request-type": "GetStreamingStatus"}
    return obs_request(data)

def start_stream():
    """Start the livestream."""
    data = {"request-type": "StartStreaming"}
    return obs_request(data)

def stop_stream():
    """Stop the livestream."""
    data = {"request-type": "StopStreaming"}
    return obs_request(data)

def set_scene(scene_name):
    """Set the current scene."""
    data = {"request-type": "SetCurrentScene", "scene-name": scene_name}
    return obs_request(data)

def mute_audio(source_name):
    """Mute the specified audio source."""
    data = {"request-type": "SetMute", "source": source_name, "mute": True}
    return obs_request(data)

def unmute_audio(source_name):
    """Unmute the specified audio source."""
    data = {"request-type": "SetMute", "source": source_name, "mute": False}
    return obs_request(data)

def set_volume(source_name, volume):
    """Set the volume level of the specified audio source."""
    data = {"request-type": "SetVolume", "source": source_name, "volume": volume}
    return obs_request(data)

# Necessary routes for Flask server
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
    return jsonify(get_stream_status())

@app.route('/start', methods=['POST'])
def start():
    return jsonify(start_stream())

@app.route('/stop', methods=['POST'])
def stop():
    return jsonify(stop_stream())

@app.route('/scene', methods=['POST'])
def scene():
    scene_name = request.form['scene_name']
    return jsonify(set_scene(scene_name))

@app.route('/mute', methods=['POST'])
def mute():
    source_name = request.form['source_name']
    return jsonify(mute_audio(source_name))

@app.route('/unmute', methods=['POST'])
def unmute():
    source_name = request.form['source_name']
    return jsonify(unmute_audio(source_name))

@app.route('/volume', methods=['POST'])
def volume():
    source_name = request.form['source_name']
    volume = float(request.form['volume'])
    return jsonify(set_volume(source_name, volume))

# Main function/execution
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
