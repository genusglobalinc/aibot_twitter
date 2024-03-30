from flask import Flask, send_file, render_template
import random
import os
import time
from flask_socketio import SocketIO, emit

#start 24/7 server (supposed to be anyway.. the goal is to not turn this off on the AWS instance)
app = Flask(__name__)
socketio = SocketIO(app)

# Path to the folder containing MP3 files
music_folder = "/home/ubuntu/Desktop/LiveStream Music"
print(f"Music from: {music_folder}")

# Path to the background video file
video_file = "/home/ubuntu/Videos/202402164830_48333566.mp4"
print(f"Animation from: {video_file}")

# Variables for controlling the music playback
music_paused = False
start_time = time.time()

# Variable for indicating preview mode
preview_mode = False

##-----------------------------------------------------------------------------------------------------------------------------
# Flask Routes
##-----------------------------------------------------------------------------------------------------------------------------

#this is the homepage for "genusstudios.info"
@app.route('/')
def index():
    # Return HTML template with video background and control buttons
    return render_template('livestream.html')

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
    print("Music has been paused.")
    print()

@app.route('/resume_music', methods=['GET'])
def resume_music():
    global music_paused
    music_paused = False
    return "Music resumed"
    print("Music has been resumed.")
    print()

@app.route('/get_timer', methods=['GET'])
def get_timer():
    global start_time
    elapsed_time = int(time.time() - start_time)
    minutes = elapsed_time // 60
    seconds = elapsed_time % 60
    return '{:02d}:{:02d}'.format(minutes, seconds)

#CURRENTLY NEEDS THE MOST WORK TO DISPLAY SCENE PREVIEW IN HTML PAGE
@app.route('/capture_scene')
def capture_scene():
    # Dummy implementation to serve a placeholder image
    # Replace this with actual implementation to capture scene image from OBS
    return send_file('placeholder.png', mimetype='image/png')

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
    # Run Flask-SocketIO server with host='0.0.0.0' to listen on all available network interfaces
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
