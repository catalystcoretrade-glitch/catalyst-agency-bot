import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# --- RENDER STABILITY ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"PREMIUM_AI_ASSISTANT_ONLINE")

def run_health_check():
    httpd = HTTPServer(('0.0.0.0', int(os.environ.get('PORT', 10000))), HealthCheckHandler)
    httpd.serve_forever()

# --- CONFIGURATION ---
TOKEN = "8563469431:AAFKui2wp1ZcRurc_-_EdUhuzIVclNcitH8"
ADMIN_ID = 2025211758 # Власник (Ти)

# --- POLISH LOCALIZATION (High Quality) ---
MESSAGES = {
    "pl": {
        "welcome": "Dzień dobry! Jestem AI-asystentem wspierającym Twój biznes. Jak mogę Panu/Pani pomóc?",
        "options": "🗓 Zmiana terminu wizyty\n💰 Zapytanie o rabat\n👤 Kontakt z właścicielem",
        "confirm": "Dziękuję. Twoja wiadomość została przekazana. Sprawdzam harmonogram i wrócę z odpowiedzią wkrótce.",
        "admin_alert": "🔔 **NOWY KLIENT (POLSKA)**\n👤 {name} (@{username})\n📝 Wiadomość: {text}"
    }
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    u = update.message.from_user
    if u.id == ADMIN_ID:
        await update.message.reply_text("🚀 System operacyjny Catalyst Nexus aktywnй. Język ustawiony: Polski (PL).")
    else:
        lang = "pl" # За замовчуванням для польського ринку
        await update.message.reply_text(f"{MESSAGES[lang]['welcome']}\n\n{MESSAGES[lang]['options']}")

async def handle_communication(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    lang = "pl"

    if user.id == ADMIN_ID:
        # Логіка управління (інструкції для бота)
        print(f"⚙️ INSTRUKCJA ADMINA: {text}")
        await update.message.reply_text("✅ Instrukcja przyjęta. Realizuję zmiany w harmonogramie.")
    else:
        # Сповіщення тебе
        alert = MESSAGES[lang]['admin_alert'].format(name=user.first_name, username=user.username, text=text)
        await context.bot.send_message(chat_id=ADMIN_ID, text=alert, parse_mode='Markdown')
        
        # Відповідь клієнту
        await update.message.reply_text(MESSAGES[lang]['confirm'])

if __name__ == '__main__':
    Thread(target=run_health_check, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_communication))
    
    print("📡 HIGH-QUALITY POLISH MVP LAUNCHED.")
    app.run_polling()
