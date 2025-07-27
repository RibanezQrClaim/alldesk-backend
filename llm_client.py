import os
import requests

OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"
LLM_API_KEY = os.getenv("LLM_API_KEY")

def analizar_mensaje_llm(mensaje, contexto_cliente=None):
    if not LLM_API_KEY:
        raise Exception("LLM_API_KEY no configurada")

    mensaje_completo = f"Contexto del cliente:\n{contexto_cliente or 'N/A'}\n\nMensaje:\n{mensaje}"

    prompt = f"""Analiza el siguiente mensaje y responde en JSON con los campos: tipo, prioridad, clasificacion, sentimiento, urgencia, resumen, tags.

Mensaje:
{mensaje_completo}
"""

    headers = {
        "Authorization": f"Bearer {LLM_API_KEY}",
        "Content-Type": "application/json"
    }

    body = {
        "model": "mistralai/mistral-7b-instruct",
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(OPENROUTER_API_URL, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["choices"][0]["message"]["content"]

