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
        "text": text,
        "parse_mode": "Markdown"
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Errore invio Telegram: {e}")

@app.route("/", methods=["GET"])
def home():
    return "BOT STRATEGY SERVER is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"status": "no data"}), 400

    # Estrazione dati dinamica
    # Prende il bot_name da TradingView, se non c'è mette "BOT"
    bot_name = data.get("bot_name", "🤖 BOT") 
    signal = data.get("signal", "N/A")
    symbol = data.get("symbol", "XAUUSD")
    entry = data.get("entry", "0.0")
    sl = data.get("sl", "0.0")
    tp = data.get("tp", "0.0")
    risk = data.get("risk", "1.5%")

    # Messaggio con Nome Bot dinamico
    message = f"""{bot_name}

📈 *Direzione:* {signal}
📌 *Simbolo:* {symbol}

💰 *Entry:* {entry}
🛑 *Stop Loss:* {sl}
🎯 *Target:* {tp}

⚠️ *Rischio:* {risk}
"""

    send_telegram_message(message)

    return jsonify({"status": "ok"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
