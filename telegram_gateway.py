import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from openai import OpenAI

# --- СТАБІЛЬНІСТЬ RENDER (HEALTH CHECK) ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"AI_ASSISTANT_ONLINE")

def run_health_check():
    port = int(os.environ.get('PORT', 10000))
    httpd = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    httpd.serve_forever()

# --- КОНФІГУРАЦІЯ ---
TOKEN = "8563469431:AAFKui2wp1ZcRurc_-_EdUhuzIVclNcitH8"
ADMIN_ID = 2025211758 # Твій ID
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

# --- ІНТЕЛЕКТУАЛЬНИЙ МОДУЛЬ (GPT-4o) ---
def get_ai_response(user_text, user_name):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": f"""
                Jesteś profesjonalnym asystentem biznesowym o nazwie Catalyst AI. 
                Twoim zadaniem jest obsługa klientów w języku polskim. 
                Klient ma na imię {user_name}. 
                Zasady:
                1. Używaj formy Pan/Pani. Bądź niezwykle uprzejmy i profesjonalny.
                2. Jeśli klient chce zmienić termin wizyty, powiedz, że sprawdzasz grafik i zaproponuj rozwiązanie.
                3. Jeśli klient prosi o rabat, zaproponuj 5-10% zniżki jako gest dobrej woli, ale zaznacz, że musisz to potwierdzić z właścicielem.
                4. Jeśli klient chce pilnego kontaktu z właścicielem, poinformuj, że wiadomość została wysłana priorytetowo.
                5. Twoim celem jest, aby właściciel (Dyrektor) nie musiał zajmować się rutyną.
                """},
                {"role": "user", "content": user_text}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        logging.error(f"OpenAI Error: {e}")
        return "Przepraszam, mam chwilowe trudności techniczne. Zaraz wrócę do Pana/Pani z informacją."

# --- ОБРОБКА ПОВІДОМЛЕНЬ ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message or not update.message.text: return
    u = update.message.from_user
    text = update.message.text

    # Якщо пишеш ти (Адмін)
    if u.id == ADMIN_ID:
        await update.message.reply_text("🚀 Catalyst AI: Dyrektorze, system działa w trybie inteligentnym. Wszystkie zapytania są analizowane.")
    
    # Якщо пише клієнт
    else:
        # 1. AI готує професійну відповідь
        ai_reply = get_ai_response(text, u.first_name)
        await update.message.reply_text(ai_reply)

        # 2. Тобі приходить повний звіт про переговори
        alert = (f"🔔 **INTELIGENTNY ALERT (PL)**\n"
                 f"👤 Klient: {u.first_name} (@{u.username if u.username else 'brak'})\n"
                 f"📝 Napisał: {text}\n"
                 f"🤖 AI Odpowiedziało: {ai_reply}")
        await context.bot.send_message(chat_id=ADMIN_ID, text=alert)

if __name__ == '__main__':
    Thread(target=run_health_check, daemon=True).start()
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("📡 PREMIUM POLISH AI ASSISTANT STARTING...")
    app.run_polling()
