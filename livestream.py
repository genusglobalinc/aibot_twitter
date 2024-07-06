from flask import Flask, render_template, request, jsonify
import asyncio
import websockets
import json

app = Flask(__name__)

# OBS WebSocket URL - localhost port 4444 TODO:CHANGE TO EC2 INSTANCE OR VERIFY
OBS_WEBSOCKET_URL = "ws://localhost:4444"

# OBS Livestream Functions
async def obs_request(data):
    async with websockets.connect(OBS_WEBSOCKET_URL) as websocket:
        await websocket.send(json.dumps(data))
        response = await websocket.recv()
        return json.loads(response)

async def get_stream_status():
    data = {"request-type": "GetStreamingStatus", "message-id": "1"}
    return await obs_request(data)

async def start_stream():
    data = {"request-type": "StartStreaming", "message-id": "1"}
    return await obs_request(data)

async def stop_stream():
    data = {"request-type": "StopStreaming", "message-id": "1"}
    return await obs_request(data)

async def set_scene(scene_name):
    data = {"request-type": "SetCurrentScene", "scene-name": scene_name, "message-id": "1"}
    return await obs_request(data)

async def mute_audio(source_name):
    data = {"request-type": "SetMute", "source": source_name, "mute": True, "message-id": "1"}
    return await obs_request(data)

async def unmute_audio(source_name):
    data = {"request-type": "SetMute", "source": source_name, "mute": False, "message-id": "1"}
    return await obs_request(data)

async def set_volume(source_name, volume):
    data = {"request-type": "SetVolume", "source": source_name, "volume": volume, "message-id": "1"}
    return await obs_request(data)

# Flask Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/status', methods=['GET'])
def status():
    result = asyncio.run(get_stream_status())
    return jsonify(result)

@app.route('/start', methods=['POST'])
def start():
    result = asyncio.run(start_stream())
    return jsonify(result)

@app.route('/stop', methods=['POST'])
def stop():
    result = asyncio.run(stop_stream())
    return jsonify(result)

@app.route('/scene', methods=['POST'])
def scene():
    scene_name = request.form['scene_name']
    result = asyncio.run(set_scene(scene_name))
    return jsonify(result)

@app.route('/mute', methods=['POST'])
def mute():
    source_name = request.form['source_name']
    result = asyncio.run(mute_audio(source_name))
    return jsonify(result)

@app.route('/unmute', methods=['POST'])
def unmute():
    source_name = request.form['source_name']
    result = asyncio.run(unmute_audio(source_name))
    return jsonify(result)

@app.route('/volume', methods=['POST'])
def volume():
    source_name = request.form['source_name']
    volume = float(request.form['volume'])
    result = asyncio.run(set_volume(source_name, volume))
    return jsonify(result)

# Main function/execution
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
