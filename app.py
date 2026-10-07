from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)
TRADES = []

@app.route('/')
def home():
    return "✅ Gold Bot Server FREE FOREVER - Ready! Time: " + str(datetime.now())

@app.route('/trade', methods=['POST'])
def trade():
    data = request.get_json()
    data['server_time'] = str(datetime.now())
    TRADES.append(data)
    print("Trade:", data)
    return jsonify({"status": "success", "received": data, "mt5_linked": True})

@app.route('/trades')
def list_trades():
    return jsonify(TRADES)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
