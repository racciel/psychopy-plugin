from flask import Flask, request, jsonify
from flask_cors import CORS
from threading import Thread
import queue

app = Flask(__name__)
CORS(app)

gaze_data_queue = queue.Queue()
latest_gaze = {'x': None, 'y': None}

@app.route('/gaze', methods=['POST'])
def receive_gaze_data():
    data = request.json
    if data:
        gaze_data_queue.put(data)
        latest_gaze['x'] = data.get('x')
        latest_gaze['y'] = data.get('y')
    return jsonify(success=True)

@app.route('/gaze', methods=['GET'])
def send_gaze_data():
    return jsonify(latest_gaze)

def run_server():
    app.run(host='localhost', port=5000)

server_thread = Thread(target=run_server, daemon=True)
server_thread.start()

try:
    while True:
        pass
except KeyboardInterrupt:
    print("Server stopped.")