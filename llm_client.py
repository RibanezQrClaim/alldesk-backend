# llm_client.py

import requests

LLM_SERVICE_URL = "http://localhost:5001/analizar"  # Cambia si mueves a producción

def analizar_mensaje_llm(mensaje, contexto_cliente=None):
    mensaje_completo = f"Contexto del cliente:\n{contexto_cliente or 'N/A'}\n\nMensaje:\n{mensaje}"
    
    try:
        response = requests.post(LLM_SERVICE_URL, json={"mensaje": mensaje_completo})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️ Error al contactar el LLM ({response.status_code}): {response.text}")
            return {}
    except Exception as e:
        print(f"❌ Error llamando al servicio LLM: {e}")
        return {}
