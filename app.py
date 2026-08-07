import os
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from groq import Groq

# ============================================
# Cargar variables de entorno
# ============================================
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("No se encontró GROQ_API_KEY en el archivo .env")

# ============================================
# Inicializar Flask
# ============================================
app = Flask(__name__)

# ============================================
# Inicializar Groq
# ============================================
client = Groq(api_key=GROQ_API_KEY)

MODEL_ID = "llama-3.3-70b-versatile"

SYSTEM_PROMPT = """
Eres LeonBot, el asistente virtual del proyecto de Rodrigo Rafael Bautista Navarrete.
Eres amable, profesional y respondes siempre en español.
"""

# ============================================
# Ruta principal: muestra la página web
# ============================================
@app.route("/")
def home():
    return render_template("index.html")

# ============================================
# Ruta del chat: recibe un mensaje y responde
# ============================================
@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({"response": "No recibí ningún mensaje."})

    try:
        respuesta = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=1024,
        )

        texto = respuesta.choices[0].message.content.strip()
        return jsonify({"response": texto})

    except Exception as e:
        return jsonify({"response": f"Ocurrió un error: {e}"})

# ============================================
# Ejecutar la aplicación
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port)