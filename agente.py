import os
import traceback
import telebot

from dotenv import load_dotenv
from google import genai
from google.genai import types

# ==========================================
# Cargar variables de entorno
# ==========================================
load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not TOKEN:
    raise ValueError("No se encontró TELEGRAM_TOKEN en el archivo .env")

if not GEMINI_API_KEY:
    raise ValueError("No se encontró GEMINI_API_KEY en el archivo .env")

# ==========================================
# Inicializar Telegram
# ==========================================
bot = telebot.TeleBot(TOKEN)

# ==========================================
# Inicializar Gemini
# ==========================================
client = genai.Client(api_key=GEMINI_API_KEY)

# Puedes cambiar el modelo si tu cuenta usa otro
MODEL_ID = "gemini-flash-latest"

SYSTEM_PROMPT = """
Eres LeonBot, un asistente virtual útil, amable y creativo.
Responde siempre en español, salvo que el usuario solicite otro idioma.
"""

print("🦁 LeonBot recargado y listo...")
print("Esperando mensajes...")

# ==========================================
# Comando /start
# ==========================================
@bot.message_handler(commands=["start"])
def start(message):
    bot.reply_to(
        message,
        "👋 ¡Hola! Soy LeonBot.\n\nPregúntame lo que quieras."
    )

# ==========================================
# Responder cualquier mensaje
# ==========================================
@bot.message_handler(func=lambda message: True)
def handle_message(message):

    bot.send_chat_action(message.chat.id, "typing")

    user_text = message.text.strip()

    try:

        response = client.models.generate_content(
            model=MODEL_ID,
            contents=user_text,
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                temperature=0.7,
                max_output_tokens=1024,
                top_p=0.95,
            ),
        )

        if response and response.text:

            texto = response.text.strip()

            # Telegram permite aproximadamente 4096 caracteres por mensaje
            if len(texto) > 4000:
                for i in range(0, len(texto), 4000):
                    bot.reply_to(message, texto[i:i + 4000])
            else:
                bot.reply_to(message, texto)

            print(f"Pregunta: {user_text}")
            print("Respuesta enviada correctamente.\n")

        else:
            bot.reply_to(message, "No pude generar una respuesta.")

    except Exception as e:

        print("\n================ ERROR ================")
        traceback.print_exc()
        print("=======================================\n")

        bot.reply_to(
            message,
            f"❌ Ocurrió un error.\n\n{e}"
        )

# ==========================================
# Ejecutar el bot
# ==========================================
if __name__ == "__main__":
    bot.infinity_polling(skip_pending=True)