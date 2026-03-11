import logging
import os
from threading import Thread
from flask import Flask
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# 1. Фіктивний сервер для Render (щоб не перезапускав бота)
app = Flask('')
@app.route('/')
def home(): return "Catalyst Nexus Core is Alive"

def run_web():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# 2. Налаштування логування
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger("CatalystNexus")

TOKEN = "8563469431:AAFKui2wp1ZcRurc_-_EdUhuzIVclNcitH8"
ADMIN_ID = 2025211758

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    user = update.message.from_user
    user_text = update.message.text
    
    if user.id == ADMIN_ID:
        await update.message.reply_text("🚀 Система активна. Потік даних стабільний.")
    else:
        await update.message.reply_text("✅ Повідомлення отримано. Дані захищено.")
        # Пересилка тобі
        await context.bot.send_message(
            chat_id=ADMIN_ID,
            text=f"⚡️ **DATA ALERT**\n👤 {user.first_name} (@{user.username})\n📝 {user_text}",
            parse_mode='Markdown'
        )

if __name__ == '__main__':
    # Запускаємо веб-сервер у фоновому потоці для Render Health Check
    Thread(target=run_web).start()
    
    print("🛠 Запуск ядра зі стабільним деплоєм...")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    application.run_polling()
