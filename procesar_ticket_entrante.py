from app import db
from models import Ticket, Mensaje, Cliente
from llm_client import analizar_mensaje_llm
import datetime

def procesar_ticket_entrante(remitente, asunto, cuerpo, canal):
    cliente = Cliente.query.filter_by(nombre=remitente).first()
    contexto = cliente.info_contexto if cliente else None

    mensaje_completo = f"Asunto: {asunto}\n\nMensaje:\n{cuerpo}"
    analisis = analizar_mensaje_llm(mensaje_completo, contexto_cliente=contexto)

    tipo = analisis.get("tipo", "Consulta")
    prioridad = analisis.get("prioridad", "Normal")
    clasificacion = analisis.get("clasificacion", "Otro")
    sentimiento = analisis.get("sentimiento", "Neutro")
    urgencia = analisis.get("urgencia", 3)
    resumen = analisis.get("resumen", "")
    tags = ", ".join(analisis.get("tags", [])) if analisis.get("tags") else ""

    ultimo_ticket = Ticket.query.order_by(Ticket.id.desc()).first()
    next_id = (ultimo_ticket.id + 1) if ultimo_ticket else 1
    nuevo_id_publico = f"T-00{next_id}"

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

    primer_mensaje = Mensaje(contenido=cuerpo, ticket_asociado=nuevo_ticket)

    db.session.add(nuevo_ticket)
    db.session.add(primer_mensaje)
    db.session.commit()

    return nuevo_ticket
