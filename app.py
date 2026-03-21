from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Variabili ambiente (Render)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(text: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text
    }
    r = requests.post(url, json=payload, timeout=10)
    r.raise_for_status()


@app.route("/", methods=["GET"])
def home():
    return "XAU TREND BOT is running"


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"status": "no data"}), 400

    signal = data.get("signal", "")
    symbol = data.get("symbol", "")
    timeframe = data.get("timeframe", "")
    entry = data.get("entry", "")
    sl = data.get("sl", "")
    tp1 = data.get("tp1", "")
    tp2 = data.get("tp2", "")

    message = f"""📊 XAU TREND BOT

📈 Direzione: {signal}
⏱ Timeframe: {timeframe}

💰 Entry: {entry}
🛑 Stop Loss: {sl}

🎯 Take Profit 1: {tp1}
🎯 Take Profit 2: {tp2}
"""

    send_telegram_message(message)

    return jsonify({"status": "ok"})


# Per Render / produzione
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
