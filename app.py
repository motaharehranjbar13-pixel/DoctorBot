from flask import Flask, request
import requests
import os

app = Flask(__name__)
TOKEN = os.environ.get("TOKEN")
BASE_URL = f"https://bale.ai/{TOKEN}"

def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload)
    except:
        pass

@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "POST":
        data = request.get_json()
        if data and "message" in data:
            chat_id = data["message"]["chat"]["id"]
            text = data["message"].get("text", "")
            if text == "/start":
                send_message(chat_id, "سلام! من ربات پزشکی هستم.")
            else:
                send_message(chat_id, f"شما گفتید: {text}\n(اطلاعات پزشکی به زودی اضافه می‌شود)")
    return "OK", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)