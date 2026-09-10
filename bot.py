import os
import requests
import telebot
from flask import Flask
from threading import Thread

# =========================================================
# الإعدادات
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN غير موجود في Environment Variables")

bot = telebot.TeleBot(BOT_TOKEN)

# =========================================================
# سيرفر صغير حتى يبقى Render يعتبر الخدمة تعمل
# =========================================================

app = Flask(__name__)

@app.route("/")
def home():
    return "Market Analyzer Bot is running!"

def run_server():
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 10000)))

# =========================================================
# /start
# =========================================================

@bot.message_handler(commands=["start"])
def start(message):

    text = """
🤖 مرحبًا بك في Market Analyzer

📊 بوت لتحليل الأسواق باستخدام مؤشرات فنية.

الأوامر:

/analyze BTCUSDT
/analyze EURUSD
/help

⚠️ التحليل احتمالي وليس ضمانًا للربح.
"""

    bot.reply_to(message, text)

# =========================================================
# /help
# =========================================================

@bot.message_handler(commands=["help"])
def help_command(message):

    text = """
📚 طريقة الاستخدام:

مثال:

/analyze BTCUSDT

أو:

/analyze EURUSD

سيقوم البوت لاحقًا بتحليل:
• الاتجاه
• RSI
• MACD
• EMA
• Bollinger Bands
• قوة الإشارة

⚠️ لا توجد إشارة مضمونة 100%.
"""

    bot.reply_to(message, text)

# =========================================================
# تحليل تجريبي مؤقت
# =========================================================

@bot.message_handler(commands=["analyze"])
def analyze(message):

    parts = message.text.split()

    if len(parts) < 2:
        bot.reply_to(
            message,
            "❌ اكتب الأصل بعد الأمر.\n\nمثال:\n/analyze BTCUSDT"
        )
        return

    symbol = parts[1].upper()

    message_text = f"""
📊 تحليل {symbol}

⏳ جاري تجهيز البيانات...

🔹 الاتجاه: سيتم حسابه
🔹 RSI: سيتم حسابه
🔹 MACD: سيتم حسابه
🔹 EMA: سيتم حسابه
🔹 Bollinger Bands: سيتم حسابها

🎯 درجة الثقة: سيتم حسابها

⚠️ هذه النسخة أولية، ولا تعتبر توصية مالية.
"""

    bot.reply_to(message, message_text)

# =========================================================
# تشغيل البوت
# =========================================================

if __name__ == "__main__":

    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()

    print("🤖 Bot is running...")

    bot.infinity_polling(
        timeout=60,
        long_polling_timeout=60
  )
