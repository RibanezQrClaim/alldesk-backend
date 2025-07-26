from flask import Flask, request, jsonify
import os
import requests

app = Flask(__name__)

# Configuración desde entorno
LLM_API_URL = os.getenv("LLM_API_URL", "https://openrouter.ai/api/v1/chat/completions")
LLM_API_KEY = os.getenv("LLM_API_KEY")
LLM_MODEL = os.getenv("LLM_MODEL", "mistralai/mistral-7b-instruct")
LLM_PROVIDER = os.getenv("LLM_API_PROVIDER", "openrouter")

def construir_prompt(mensaje):
    return f"""
Eres un asistente que clasifica mensajes de clientes.

Devuelve en JSON los siguientes campos:
- tipo: Consulta, Reclamo, Sugerencia, Felicitación, etc.
- prioridad: Alta, Normal, Baja
- clasificacion: categoría del mensaje (producto, entrega, soporte, etc.)
- sentimiento: Positivo, Neutro o Negativo
- urgencia: número entre 1 (baja) y 5 (crítica)
- resumen: una frase corta con la idea principal del mensaje
- tags: lista de palabras clave

Mensaje:
{mensaje}
"""

def llamar_llm_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://tu-app.com",  # opcional pero recomendado
        "X-Title": "AllDesk-MVP"
    }

    body = {
        "model": LLM_MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(LLM_API_URL, headers=headers, json=body)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]

    try:
        return eval(content)  # asume respuesta en JSON válido como string
    except:
        return {"error": "Respuesta LLM inválida", "raw": content}

@app.route("/analizar", methods=["POST"])
def analizar_ticket():
    data = request.json
    mensaje = data.get("mensaje", "")

    prompt = construir_prompt(mensaje)
    resultado = llamar_llm_openrouter(prompt)
    return jsonify(resultado)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(debug=True, port=port)

