from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

TOKEN = "458860954:nq14x2k1l94bMS4BCvR3rjZHWhXEvNV1T9I"
BASE_URL = f"https://tapi.bale.ai/bot{TOKEN}"
DATA_FILE = "medical_data.json"


def load_medical_data():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print("خطا در خواندن فایل پزشکی:", e)
        return []


medical_data = load_medical_data()


def send_message(chat_id, text):
    url = f"{BASE_URL}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print("خطا در ارسال پیام:", e)


def search_disease(user_text):
    user_text = user_text.strip()
    for disease in medical_data:
        if disease.get("موضوع", "").strip() == user_text:
            return disease
    return None


def calculate_similarity(user_text, symptoms):
    user_words = user_text.lower().split()
    symptom_words = symptoms.lower().split()
    if not symptom_words or not user_words:
        return 0
    score = sum(1 for word in user_words if word in symptom_words)
    percent = int((score / len(user_words)) * 100)
    return min(percent, 100)


def search_by_symptoms(user_text):
    results = []
    for disease in medical_data:
        similarity = calculate_similarity(user_text, disease.get("علائم", ""))
        if similarity > 0:
            results.append((similarity, disease))
    results.sort(reverse=True, key=lambda x: x[0])
    return results[:3]


def format_disease(disease):
    return f"""
━━━━━━━━━━━━━━━━━━━━━━
🩺 بیماری: {disease.get("موضوع", "")}

📖 تعریف
{disease.get("تعریف", "")}

━━━━━━━━━━━━━━━━━━━━━━
🤒 علائم
{disease.get("علائم", "")}

━━━━━━━━━━━━━━━━━━━━━━
🦠 علت
{disease.get("علت", "")}

━━━━━━━━━━━━━━━━━━━━━━
⚠️ عوامل خطر
{disease.get("عوامل خطر", "")}

━━━━━━━━━━━━━━━━━━━━━━
🔬 تشخیص
{disease.get("تشخیص", "")}

━━━━━━━━━━━━━━━━━━━━━━
💊 درمان
{disease.get("درمان", "")}

━━━━━━━━━━━━━━━━━━━━━━
💉 داروهای رایج
{disease.get("داروهای رایج", "")}

━━━━━━━━━━━━━━━━━━━━━━
🏠 مراقبت در منزل
{disease.get("مراقبت در منزل", "")}

━━━━━━━━━━━━━━━━━━━━━━
🥗 پیشگیری
{disease.get("پیشگیری", "")}

━━━━━━━━━━━━━━━━━━━━━━
⚠️ عوارض
{disease.get("عوارض", "")}

━━━━━━━━━━━━━━━━━━━━━━
🚨 هشدار
{disease.get("هشدار", "")}

━━━━━━━━━━━━━━━━━━━━━━
👨‍⚕️ زمان مراجعه به پزشک
{disease.get("زمان مراجعه به پزشک", "")}

━━━━━━━━━━━━━━━━━━━━━━
🏥 پزشک مرتبط
{disease.get("تخصص مرتبط", "")}

━━━━━━━━━━━━━━━━━━━━━━
⚠️ توجه

این اطلاعات فقط برای افزایش آگاهی عمومی است.
برای تشخیص و درمان حتماً به پزشک مراجعه کنید.

━━━━━━━━━━━━━━━━━━━━━━
🤖 DoctorBot
"""


def start_message():
    return """
🩺 سلام و خوش آمدید به DoctorBot

من دستیار هوشمند پزشکی شما هستم. 🤖💙

━━━━━━━━━━━━━━━━━━

می‌توانم درباره موارد زیر به شما کمک کنم:

🦠 بیماری‌ها
🤒 علائم بیماری‌ها
💊 داروهای رایج
🏥 درمان‌های اولیه
🧠 سلامت روان
👨‍⚕️ زمان مراجعه به پزشک

━━━━━━━━━━━━━━━━━━

⚠️ توجه

اطلاعات این ربات صرفاً جهت افزایش آگاهی عمومی است.
این ربات جایگزین پزشک نیست.

━━━━━━━━━━━━━━━━━━

لطفاً نام بیماری یا علائم خود را بنویسید.

مثال:
✅ میگرن
✅ دیابت
✅ کمردرد
✅ تب و سرفه

━━━━━━━━━━━━━━━━━━
🤖 DoctorBot
"""


def help_message():
    return """
🩺 راهنمای DoctorBot

من می‌توانم درباره موارد زیر به شما کمک کنم:

🦠 بیماری‌ها
🤒 علائم
💊 داروهای رایج
🏥 درمان اولیه
🧠 سلامت روان
⚠️ هشدارهای اورژانسی

━━━━━━━━━━━━━━━━━━

مثال‌ها:

میگرن
دیابت
تب و سرفه
کمردرد

━━━━━━━━━━━━━━━━━━
🤖 DoctorBot
"""


def emergency_message():
    return """
🚨 اگر یکی از موارد زیر را دارید:

• درد شدید قفسه سینه
• تنگی نفس شدید
• بیهوشی
• تشنج
• خونریزی شدید
• ضعف ناگهانی یک سمت بدن

لطفاً فوراً با اورژانس تماس بگیرید یا به نزدیک‌ترین مرکز درمانی مراجعه کنید.

⚠️ این ربات جایگزین پزشک نیست.
"""


def mental_health_message():
    return """
🧠 سلامت روان اهمیت زیادی دارد.

اگر این احساسات چند روز یا چند هفته ادامه پیدا کرده‌اند یا زندگی روزمره شما را مختل کرده‌اند، بهتر است با روانشناس یا روانپزشک مشورت کنید.

اگر احساس می‌کنید در خطر فوری هستید یا ممکن است به خود یا دیگران آسیب بزنید، فوراً از یک فرد مورد اعتماد یا خدمات اورژانس کمک بگیرید.
"""


def goodbye_message():
    return """
🌸 امیدوارم همیشه سالم باشید.

هر زمان سؤال پزشکی داشتید، من اینجا هستم.

خدانگهدار 💙
"""


@app.route("/", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return "DoctorBot Online", 200

    data = request.get_json()
    if not data or "message" not in data:
        return "OK", 200

    message = data["message"]
    chat_id = message["chat"]["id"]
    text = message.get("text", "").strip().lower()

    if not text:
        return "OK", 200

    # سلام
    greetings = ["سلام", "سلامم", "سلام خوبی", "سلام چطوری", "درود", "صبح بخیر", "ظهر بخیر", "عصر بخیر", "شب بخیر", "hi",
                 "hello"]
    if text in greetings:
        send_message(chat_id, start_message())
        return "OK", 200

    # تشکر
    thanks = ["مرسی", "ممنون", "تشکر", "دمت گرم", "سپاس"]
    if text in thanks:
        send_message(chat_id,
                     "🌸 خواهش می‌کنم.\n\nاگر سؤال پزشکی دیگری دارید خوشحال می‌شوم کمکتان کنم. 💙\n\n🩺 فقط نام بیماری یا علائم را ارسال کنید.")
        return "OK", 200

    # خداحافظ
    bye = ["خدافظ", "خدانگهدار", "بای", "فعلا"]
    if text in bye:
        send_message(chat_id, goodbye_message())
        return "OK", 200

    # سوالات عمومی
    general_questions = {
        "اسمت چیه": "🤖 من DoctorBot هستم؛ دستیار هوشمند پزشکی شما.",
        "کی هستی": "🤖 من DoctorBot هستم و برای پاسخ به سوالات عمومی پزشکی طراحی شده‌ام.",
        "چیکار میکنی": """🩺 من می‌توانم:\n\n• اطلاعات بیماری‌ها\n• علائم\n• درمان‌های اولیه\n• داروهای رایج\n• سلامت روان\n• زمان مراجعه به پزشک\n\nرا در اختیار شما قرار دهم.""",
        "چه کارهایی بلدی": """📋 قابلیت‌های من:\n\n✅ جستجوی بیماری\n✅ بررسی علائم\n✅ نمایش درمان\n✅ داروهای رایج\n✅ سلامت روان\n✅ هشدارهای اورژانسی""",
        "کمکم کن": "🌸 حتماً. لطفاً نام بیماری یا علائم خود را بنویسید."
    }
    if text in general_questions:
        send_message(chat_id, general_questions[text])
        return "OK", 200

    # راهنما
    if text in ["کمک", "راهنما", "help"]:
        send_message(chat_id, help_message())
        return "OK", 200

    # اورژانس
    if text in ["اورژانس", "فوری", "کمک فوری"]:
        send_message(chat_id, emergency_message())
        return "OK", 200

    # سلامت روان
    mental_words = ["افسردگی", "اضطراب", "استرس", "حمله پانیک", "غمگینم"]
    if any(word in text for word in mental_words):
        send_message(chat_id, mental_health_message())
        return "OK", 200

    # منو
    if text in ["منو", "قابلیت ها", "چه کارهایی بلدی"]:
        send_message(chat_id, help_message())
        return "OK", 200

    # دارو
    if text == "دارو":
        send_message(chat_id, "💊 لطفاً نام بیماری را ارسال کنید.\n\nمثال:\nمیگرن\nدیابت\nسرماخوردگی\n\nتا داروهای رایج آن را نمایش دهم.")
        return "OK", 200

    # علائم
    if text == "علائم":
        send_message(chat_id, "🤒 لطفاً نام بیماری را بنویسید.\n\nمثال:\nمیگرن\nآنفولانزا\nدیابت\n\nتا علائم آن را نمایش دهم.")
        return "OK", 200

    # درمان
    if text == "درمان":
        send_message(chat_id, "🏥 لطفاً نام بیماری را ارسال کنید تا روش‌های درمان اولیه نمایش داده شود.")
        return "OK", 200

    # جستجوی بیماری
    disease = search_disease(text)
    if disease:
        send_message(chat_id, format_disease(disease))
        return "OK", 200

    # جستجو بر اساس علائم (فقط اگر متن طولانی‌تر از 2 حرف باشد)
    if len(text) > 2:
        diseases = search_by_symptoms(text)
        if diseases:
            msg = "🔍 بیماری‌های احتمالی:\n\n"
            for i, (_, d) in enumerate(diseases, 1):
                msg += f"{i}. {d['موضوع']}\n"
            msg += "\nلطفاً نام یکی از بیماری‌های بالا را ارسال کنید تا اطلاعات کامل آن نمایش داده شود."
            send_message(chat_id, msg)
            return "OK", 200

    # اگر چیزی پیدا نشد
    send_message(chat_id, """
❌ متأسفانه بیماری موردنظر پیدا نشد.

🔍 لطفاً یکی از موارد زیر را انجام دهید:

✅ نام بیماری را بنویسید.
مثال:
میگرن
دیابت
کمردرد

یا

🤒 علائم خود را وارد کنید.

مثال:
تب
سرفه
گلودرد
تهوع

من نزدیک‌ترین بیماری را برای شما پیدا می‌کنم.

━━━━━━━━━━━━━━━━━━━━━━
🤖 DoctorBot
""")
    return "OK", 200


@app.route("/health")
def health():
    return "OK", 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
