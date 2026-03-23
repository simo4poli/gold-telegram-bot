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
    timeframe_raw = data.get("timeframe", "")

    try:
        entry = round(float(data.get("entry", 0)), 2)
        sl = round(float(data.get("sl", 0)), 2)
        tp1 = round(float(data.get("tp1", 0)), 2)
        tp2 = round(float(data.get("tp2", 0)), 2)
    except (TypeError, ValueError):
        return jsonify({"status": "error", "message": "Prezzi non validi"}), 400

    timeframe = f"M{timeframe_raw}"

    message = f"""📊 XAU TREND BOT

📌 Simbolo: {symbol}
📈 Direzione: {signal}
⏱ Timeframe: {timeframe}

💰 Entry: {entry}
🛑 Stop Loss: {sl}

🎯 TP1: {tp1}
🎯 TP2: {tp2}
"""

    send_telegram_message(message)

    return jsonify({"status": "ok"})


# Per Render / produzione
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
