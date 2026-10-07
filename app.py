from flask import Flask, request, jsonify, render_template_string
from datetime import datetime

app = Flask(__name__)

# Last signal for MT5 Exness EA
last_signal = {
    "action": "HOLD",
    "symbol": "XAUUSD",
    "time": str(datetime.now()),
    "lot": 0.01
}

HTML = """
<html>
<head>
<title>GOLD BOT MT5 EXNESS</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body{background:#111;color:gold;text-align:center;font-family:Arial;padding:20px}
button{width:95%;padding:22px;margin:12px;font-size:22px;font-weight:bold;border:none;border-radius:16px}
.buy{background:#00ff88} .sell{background:#ff3b3b;color:white}
.box{background:#222;padding:15px;border-radius:12px;margin:15px}
</style>
</head>
<body>
<h2>🦁 GOLD BOT<br>MT5 EXNESS</h2>
<div class="box">
<b>{{s['action']}}</b><br>
{{s['symbol']}} | Lot: {{s['lot']}}<br>
{{s['time']}}
</div>
<button class="buy" onclick="trade('BUY')">BUY GOLD</button>
<button class="sell" onclick="trade('SELL')">SELL GOLD</button>
<button style="background:gold" onclick="trade('CLOSE')">CLOSE ALL</button>
<button style="background:#555;color:white" onclick="trade('HOLD')">STOP</button>
<h3 id="msg"></h3>
<script>
function trade(act){
 fetch('/api/trade',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({action:act,symbol:'XAUUSD'})})
 .then(r=>r.json()).then(d=>{document.getElementById('msg').innerText='✅ SIGNAL SENT: '+d.action})
}
setInterval(()=>{fetch('/api/get_signal').then(r=>r.json()).then(d=>{document.title=d.action})},3000)
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML, s=last_signal)

@app.route('/api/trade', methods=['POST'])
def api_trade():
    global last_signal
    j = request.get_json()
    last_signal = {
        "action": j.get('action','HOLD'),
        "symbol": "XAUUSD",
        "time": str(datetime.now()),
        "lot": 0.01
    }
    print(f"MT5 EXNESS SIGNAL: {last_signal}")
    return jsonify(last_signal)

@app.route('/api/get_signal')
def get_signal():
    # MT5 EA reads this
    return jsonify(last_signal)

@app.route('/webhook', methods=['POST'])
def webhook():
    global last_signal
    j = request.get_json()
    last_signal = {
        "action": j.get('action','HOLD'),
        "symbol": "XAUUSD",
        "time": str(datetime.now()),
        "lot": j.get('lot',0.01)
    }
    return jsonify(last_signal)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
