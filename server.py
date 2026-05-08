from flask import Flask, request, jsonify
import time

app = Flask(__name__)

state = {
    "emotion": "CHILL",
    "remaining": 0,
    "playing": 0,
    "beat": 0,
    "song": "",
    "artist": "",
    "mode": "neutral",
    "updated": 0,
    "control": "",
    "control_time": 0
}

API_KEY = "ybeebot2024secret"

@app.route('/push', methods=['POST'])
def push():
    if request.headers.get('X-API-Key') != API_KEY:
        return jsonify({"error": "unauthorized"}), 401
    data = request.json
    state.update(data)
    state["updated"] = time.time()
    return jsonify({"ok": True})

@app.route('/poll', methods=['GET'])
def poll():
    return jsonify(state)

@app.route('/control', methods=['POST'])
def control():
    if request.headers.get('X-API-Key') != API_KEY:
        return jsonify({"error": "unauthorized"}), 401
    cmd = request.json.get("cmd", "")
    state["control"] = cmd
    state["control_time"] = time.time()
    return jsonify({"ok": True})

@app.route('/getcontrol', methods=['GET'])
def getcontrol():
    cmd = state.get("control", "")
    t = state.get("control_time", 0)
    state["control"] = ""
    return jsonify({"cmd": cmd, "time": t})

@app.route('/')
def index():
    return "YBee Bot server running!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
