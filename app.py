from flask import Flask
import os
import threading
import json
from Balethon import Client
from Balethon.objects import Message
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

# ====== بارگذاری اطلاعات پزشکی ======
try:
    with open('medical_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
except FileNotFoundError:
    print("❌ فایل medical_data.json پیدا نشد!")
    data = []
except json.JSONDecodeError:
    print("❌ فرمت JSON نامعتبر است!")
    data = []

if data:
    texts = [item["موضوع"] + " " + item["علائم"] for item in data]
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(texts)
else:
    vectorizer = None
    vectors = None

def find_best(query):
    if vectorizer is None or vectors is None:
        return "اطلاعات پزشکی بارگذاری نشده است."
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, vectors)
    best_idx = similarities.argmax()
    if similarities[0][best_idx] > 0.1:
        return data[best_idx]["توصیه"]
    else:
        return "متاسفم اطلاعاتی درباره این موضوع ندارم. لطفاً دقیق‌تر بپرس."

# ====== مسیرهای Flask ======
@app.route('/')
def home():
    return "✅ ربات پزشکی آنلاین است!"

@app.route('/health')
def health():
    return "OK", 200

# ====== تابع اجرای ربات ======
def run_bot():
    client = Client(token="458869954:jMNBFOv_vG1I_wXzUA_eHAsV5f8YIZBEhk")
    
    @client.on_message()
    async def handle_message(message: Message):
        if message.text == "/start":
            await message.reply(
                "سلام! 🩺 من دستیار پزشکی تو هستم.\n\n"
                "از علائم یا نام بیماری بگو تا راهنماییت کنم.\n"
                "مثال: 'سردرد شدید دارم' یا 'آنفولانزا'"
            )
        else:
            answer = find_best(message.text)
            await message.reply(answer)
    
    print("✅ ربات پزشکی روشن شد...")
    client.run()

# ====== اجرای همزمان ======
if __name__ == "__main__":
    # ربات رو در یک ترد جداگانه اجرا کن
    bot_thread = threading.Thread(target=run_bot)
    bot_thread.daemon = True
    bot_thread.start()
    
    # Flask رو اجرا کن (تا Render خوشحال بشه!)
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)