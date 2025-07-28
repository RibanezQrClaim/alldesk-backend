from app import db
from models import Ticket, Mensaje, Cliente
from llm_client import analizar_mensaje_llm
import datetime

# Cargar contexto general si no existe contexto del cliente
with open("contexto_empresa.txt", "r", encoding="utf-8") as f:
    CONTEXTO_EMPRESA = f.read()

def procesar_ticket_entrante(remitente, asunto, cuerpo, canal):
    cliente = Cliente.query.filter_by(nombre=remitente).first()
    contexto = cliente.info_contexto if cliente and cliente.info_contexto else CONTEXTO_EMPRESA

    mensaje_completo = f"Asunto: {asunto}\n\nMensaje:\n{cuerpo}"
    analisis = analizar_mensaje_llm(mensaje_completo, contexto_cliente=contexto)

    tipo = analisis.get("tipo", "Consulta")
    prioridad = analisis.get("prioridad", "Normal")
    clasificacion = analisis.get("clasificacion", "Otro")
    sentimiento = analisis.get("sentimiento", "Neutro")
    urgencia = analisis.get("urgencia", "Media")
    resumen = analisis.get("resumen", "")
    tags = ", ".join(analisis.get("tags", [])) if analisis.get("tags") else ""

    ultimo_ticket = Ticket.query.order_by(Ticket.id.desc()).first()
    next_id = (ultimo_ticket.id + 1) if ultimo_ticket else 1
    nuevo_id_publico = f"T-{next_id:03d}"

    nuevo_ticket = Ticket(
        id_publico=nuevo_id_publico,
        cliente_nombre=remitente,
        asunto=asunto,
        tipo=tipo,
        prioridad=prioridad,
        clasificacion=clasificacion,
        sentimiento=sentimiento,
        urgencia=urgencia,
        resumen=resumen,
        tags=tags,
        canal_nombre=canal,
        cliente_id=cliente.id_cliente if cliente else None,
        id_sac_asignado=None
    )

    db.session.add(nuevo_ticket)
    db.session.flush()  # Para obtener nuevo_ticket.id antes del commit

    primer_mensaje = Mensaje(contenido=cuerpo, id_ticket=nuevo_ticket.id)
    db.session.add(primer_mensaje)
    db.session.commit()

    return nuevo_ticket
