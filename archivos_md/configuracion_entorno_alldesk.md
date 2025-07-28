\# 🛠️ Configuración de entorno - AllDesk MVP



Este documento resume las variables, entornos y consideraciones importantes del backend de AllDesk.



---



\## ✅ Variables de entorno (Heroku)



| Variable       | Uso                                              |

|----------------|--------------------------------------------------|

| `DATABASE\_URL` | Conexión a base de datos PostgreSQL en Heroku    |

| `LLM\_API\_KEY`  | API Key para OpenRouter                          |



---



\## ⚙️ Variables importantes en código



| Variable              | Descripción                                           |

|------------------------|-------------------------------------------------------|

| `LLM\_API\_KEY`          | Se obtiene con `os.getenv()` en `llm\_client.py`       |

| `OPENROUTER\_API\_URL`   | URL del endpoint de OpenRouter                        |

| `LLM\_SERVICE\_URL`      | Solo en entorno local: se apunta a `localhost:5001`   |



---



\## 🧪 Entornos definidos



| Ambiente | Descripción                                   | Estado      |

|----------|-----------------------------------------------|-------------|

| Local    | Desarrollo en máquina personal (`localhost`) | ✅ operativo |

| Heroku   | Producción MVP (`alldesk-mvp-rodrigo`)        | ✅ operativo |



\### Detalles:



\- En \*\*entorno local\*\*, se ejecuta `llm\_service/main.py` y el backend se comunica con `http://localhost:5001/analizar`

\- En \*\*Heroku\*\*, `llm\_client.py` se comunica directamente con `https://openrouter.ai/api/v1/chat/completions` usando la variable `LLM\_API\_KEY`.



---



\## 📁 Consideraciones importantes para respaldar



\- \*\*Archivos .py\*\* clave como `app.py`, `models.py`, `procesar\_ticket\_entrante.py`, `llm\_client.py`, `llm\_service/main.py`

\- Templates HTML en `templates/`

\- Scripts de inicialización (`init\_db.py`, `cargar\_clientes.py`)

\- `requirements.txt`

\- Este documento y cualquier otro `.md` asociado a configuración o documentación



---



\## 🧠 Recordatorio



No subir el entorno virtual (`venv`) ni claves directamente al repositorio.



