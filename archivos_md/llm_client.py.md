### .\llm_client.py

```py
# llm_client.py

import requests

LLM_SERVICE_URL = "http://localhost:5001/analizar"  # Cambia esto si usas otro puerto o en producción

def analizar_mensaje_llm(mensaje):
    try:
        response = requests.post(LLM_SERVICE_URL, json={"mensaje": mensaje})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error al contactar el LLM: {response.status_code}")
            return {}
    except Exception as e:
        print(f"Error llamando al servicio LLM: {e}")
        return {}

```