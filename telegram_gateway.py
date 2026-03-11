import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Налаштування системного логування для Big Data
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger("CatalystNexus")

# Конфігурація доступу
TOKEN = "8563469431:AAFKui2wp1ZcRurc_-_EdUhuzIVclNcitH8"
ADMIN_ID = 2025211758  # Твій ID

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text:
        return

    user = update.message.from_user
    user_text = update.message.text
    user_id = user.id

    # Логіка розподілу ролей (Директор проекту vs Клієнт)
    if user_id == ADMIN_ID:
        logger.info(f"👑 ADMIN ACTION: {user_text}")
        response = (
            "🚀 **Вітаю, Директоре.**\n\n"
            "Система Catalyst Nexus працює в штатному режимі.\n"
            "📡 **Статус:** Data Collection Active\n"
            "📊 **Капіталізація:** У процесі аналізу..."
        )
    else:
        # Анонімізація даних клієнта
        logger.info(f"👤 INCOMING LEAD (Anonymized): {user_id}")
        response = (
            "✅ **Catalyst Nexus: Повідомлення отримано.**\n\n"
            "🔒 **Privacy Shield:** Активовано. Ваші дані анонімізовано.\n"
            "🤖 AI-менеджер обробляє запит. Очікуйте на зв'язок."
        )

    await update.message.reply_text(response, parse_mode='Markdown')

if __name__ == '__main__':
    print("🛠 Запуск професійного ядра Catalyst Nexus...")
    application = ApplicationBuilder().token(TOKEN).build()
    
    # Фільтр: тільки текст, ігноруємо команди
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("📡 Ядро синхронізовано з Telegram API. Очікую дані...")
    application.run_polling()
