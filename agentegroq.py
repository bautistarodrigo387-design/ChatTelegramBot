import os
import traceback
import telebot

from dotenv import load_dotenv
from groq import Groq

# =====================================================
# Cargar variables de entorno
# =====================================================
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not TOKEN:
    raise ValueError("No se encontró TELEGRAM_TOKEN en el archivo .env")

if not GROQ_API_KEY:
    raise ValueError("No se encontró GROQ_API_KEY en el archivo .env")

# =====================================================
# Inicializar Telegram
# =====================================================
bot = telebot.TeleBot(TOKEN)

# =====================================================
# Inicializar Groq
# =====================================================
client = Groq(
    api_key=GROQ_API_KEY
)

MODEL_ID = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
Eres LeonBot.

Eres un asistente virtual inteligente, amable y profesional.

Siempre responde en español, excepto cuando el usuario solicite otro idioma.

Responde de forma clara y detallada.
"""

print("🦁 LeonBot iniciado correctamente.")
print("Esperando mensajes...")

# =====================================================
# Comando /start
# =====================================================
@bot.message_handler(commands=["start"])
def start(message):

    bot.reply_to(
        message,
        "👋 ¡Hola!\n\nSoy LeonBot 🤖\n\nEstoy conectado a Groq.\n\n¿En qué puedo ayudarte?"
    )

# =====================================================
# Responder mensajes
# =====================================================
@bot.message_handler(func=lambda message: True)
def responder(message):

    bot.send_chat_action(message.chat.id, "typing")

    user_text = message.text.strip()

    try:

        respuesta = client.chat.completions.create(

            model=MODEL_ID,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_text
                }
            ],

            temperature=0.7,
            max_tokens=1024,
        )

        texto = respuesta.choices[0].message.content.strip()

        if len(texto) > 4000:

            for i in range(0, len(texto), 4000):
                bot.reply_to(message, texto[i:i+4000])

        else:

            bot.reply_to(message, texto)

        print("----------------------------------------")
        print("Pregunta :", user_text)
        print("Respuesta enviada correctamente.")
        print("----------------------------------------")

    except Exception as e:

        print("\n================ ERROR ==================")
        traceback.print_exc()
        print("=========================================\n")

        bot.reply_to(
            message,
            f"❌ Ocurrió un error.\n\n{e}"
        )

# =====================================================
# Ejecutar Bot
# =====================================================
if __name__ == "__main__":

    bot.infinity_polling(skip_pending=True)