from flask import Flask, render_template
from flask_socketio import SocketIO
import random
import time

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

# Serve the web interface
@app.route('/')
def index():
    return render_template('index.html')

# Simulate EMG data from ESP32
def generate_emg_data():
    while True:
        emg_value = random.randint(0, 1023)  # Replace with real EMG data
        socketio.emit('emg_data', emg_value)  # Send data to frontend
        time.sleep(0.0005)  # 2000 samples per second

# Run background thread
@socketio.on('connect')
def handle_connect():
    print("Client connected")
    socketio.start_background_task(generate_emg_data)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
