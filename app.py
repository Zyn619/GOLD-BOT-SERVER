from flask import Flask, request, jsonify, send_from_directory
import os
app = Flask(__name__)
current_signal = {"signal": "WAIT", "market": "GOLD", "price": "0", "lot": "0.05"}
@app.route("/")
def home():
    return send_from_directory(".", "index.html") if os.path.exists("index.html") else "V72 Live - Upload index.html!"
@app.route("/set_signal")
def set_signal():
    global current_signal
    current_signal = {"signal": request.args.get("signal","WAIT"), "market": "GOLD", "price": "0", "lot": "0.05"}
    return jsonify(current_signal)
@app.route("/signal_data")
def signal_data():
    return jsonify(current_signal)
@app.route("/signal")
def signal():
    return current_signal["signal"]
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
