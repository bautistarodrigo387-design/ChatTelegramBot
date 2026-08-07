const chatToggle = document.getElementById("chat-toggle");
const chatWindow = document.getElementById("chat-window");
const chatClose = document.getElementById("chat-close");
const chatInput = document.getElementById("chat-input");
const chatSend = document.getElementById("chat-send");
const chatMessages = document.getElementById("chat-messages");

// Abrir / cerrar el widget de chat
chatToggle.addEventListener("click", () => {
    chatWindow.classList.toggle("hidden");
});

chatClose.addEventListener("click", () => {
    chatWindow.classList.add("hidden");
});

// Función para agregar un mensaje a la ventana de chat
function addMessage(text, sender) {
    const msg = document.createElement("div");
    msg.classList.add("msg", sender);
    msg.textContent = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Función para enviar el mensaje al servidor (app.py)
async function sendMessage() {
    const text = chatInput.value.trim();

    if (!text) return;

    addMessage(text, "user");
    chatInput.value = "";

    addMessage("Escribiendo...", "bot");

    try {
        const response = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();

        // Quitar el mensaje de "Escribiendo..."
        chatMessages.removeChild(chatMessages.lastChild);

        addMessage(data.response, "bot");

    } catch (error) {
        chatMessages.removeChild(chatMessages.lastChild);
        addMessage("❌ Ocurrió un error al conectar con el servidor.", "bot");
    }
}

chatSend.addEventListener("click", sendMessage);

chatInput.addEventListener("keypress", (e) => {
    if (e.key === "Enter") {
        sendMessage();
    }
});