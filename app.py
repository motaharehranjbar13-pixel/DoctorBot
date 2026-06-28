from balethon import Client
from balethon.objects import Message
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
# ====== بارگذاری اطلاعات پزشکی ======
try:
    with open('medical_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)  # ✅ این خط ۴ فاصله جلوتر رفت
except FileNotFoundError:
    print("❌ فایل medical_data.json پیدا نشد!")
    exit()
except json.JSONDecodeError:
    print("❌ فرمت JSON نامعتبر است!")
    exit()

# ترکیب موضوع + علائم برای جستجو
texts = [item["موضوع"] + " " + item["علائم"] for item in data]  # ✅ کلیدها اصلاح شدن
vectorizer = TfidfVectorizer()
vectors = vectorizer.fit_transform(texts)

def find_best(query):
    query_vec = vectorizer.transform([query])
    similarities = cosine_similarity(query_vec, vectors)
    best_idx = similarities.argmax()
    if similarities[0][best_idx] > 0.1:
        return data[best_idx]["توصیه"]
    else:
        return "متاسفم اطلاعاتی درباره این موضوع ندارم. لطفاً دقیق‌تر بپرس."

# ====== راه‌اندازی ربات ======
client = Client(token="458860954:jMNBFBo_vVG1I_wXzUA-eHAsV5f8YIZBEhk")

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

# ====== اجرای ربات ======
if __name__ == "__main__":
    print("✅ ربات پزشکی روشن شد...")
    print("📱 برو تو پیام‌رسان بله و رباتت رو تست کن!")
    client.run()