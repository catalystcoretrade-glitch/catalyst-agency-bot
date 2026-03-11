import logging
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Налаштування логування для аудиту
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("CatalystNexus")

# Конфігурація активів
TOKEN = "8563469431:AAFKui2wp1ZcRurc_-_EdUhuzIVclNcitH8"
ADMIN_ID = 2025211758

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user = update.message.from_user
    user_text = update.message.text
    user_id = user.id
    username = f"@{user.username}" if user.username else "No Username"

    # Сценарій 1: Ти пишеш боту (Управління)
    if user_id == ADMIN_ID:
        logger.info(f"👑 ADMIN COMMAND: {user_text}")
        await update.message.reply_text(
            "🚀 **Система Catalyst Nexus активна.**\nПотік даних стабільний. Всі запити пересилаються вам.",
            parse_mode='Markdown'
        )
    
    # Сценарій 2: Клієнт пише боту (Збір активів)
    else:
        # 1. Відповідь клієнту (Privacy Protocol)
        await update.message.reply_text(
            "✅ **Повідомлення отримано.**\nВаші дані захищено протоколом Catalyst.",
            parse_mode='Markdown'
        )

        # 2. Пересилка даних тобі (Lead Generation)
        alert_text = (
            f"⚡️ **INCOMING DATA ALERT**\n\n"
            f"👤 **User:** {user.first_name} ({username})\n"
            f"🆔 **ID:** `{user_id}`\n"
            f"📝 **Message:** {user_text}"
        )
        
        try:
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=alert_text,
                parse_mode='Markdown'
            )
            logger.info(f"📲 Повідомлення від {user_id} переслано адміну.")
        except Exception as e:
            logger.error(f"❌ Помилка пересилки: {e}")

if __name__ == '__main__':
    print("🛠 Оновлення ядра: Модуль сповіщень активовано.")
    application = ApplicationBuilder().token(TOKEN).build()
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("📡 Моніторинг ринку запущено 24/7...")
    application.run_polling()
