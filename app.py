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
        "parse_mode": "Markdown" # Opzionale: rende il testo più bello
    }
    try:
        r = requests.post(url, json=payload, timeout=10)
        r.raise_for_status()
    except Exception as e:
        print(f"Errore invio Telegram: {e}")

@app.route("/", methods=["GET"])
def home():
    return "XAU TREND BOT is running"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return jsonify({"status": "no data"}), 400

    # Estrazione dati (Match perfetto con la tua V5 su TradingView)
    signal = data.get("signal", "N/A")
    symbol = data.get("symbol", "XAUUSD")
    entry = data.get("entry", "0.0")
    sl = data.get("sl", "0.0")
    tp = data.get("tp", "0.0")
    risk = data.get("risk", "1.5%")

    # Messaggio ottimizzato: 1 solo Target, layout pulito
    message = f"""📊 *XAU TREND BOT*

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
    # Render usa la porta 10000 di default o quella passata dall'ambiente
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
