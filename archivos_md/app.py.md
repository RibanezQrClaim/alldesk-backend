### .\app.py

```py
from flask import Flask, render_template, request, redirect, url_for
from llm_client import analizar_mensaje_llm
from models import db, Usuario, Ticket, Cliente, Mensaje
from procesar_ticket_entrante import procesar_ticket_entrante
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS ---
database_uri = os.environ.get('DATABASE_URL')
if database_uri and database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)
else:
    database_uri = 'sqlite:///' + os.path.join(basedir, 'instance', 'alldesk.db')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# --- RUTAS DE LA APLICACIÓN ---

@app.route('/')
def pagina_principal():
    tickets = Ticket.query.order_by(Ticket.fecha_creacion.desc()).all()
    return render_template('inbox.html', tickets=tickets)

@app.route('/ticket/<ticket_id_publico>', methods=['GET', 'POST'])
def ver_ticket(ticket_id_publico):
    ticket = Ticket.query.filter_by(id_publico=ticket_id_publico).first_or_404()
    
    if request.method == 'POST':
        contenido_respuesta = request.form.get('respuesta')
        es_privado = 'es_privado' in request.form

        if contenido_respuesta:
            autor_actual = ticket.agente_asignado
            if autor_actual:
                nuevo_mensaje = Mensaje(
                    contenido=contenido_respuesta,
                    es_privado=es_privado,
                    ticket_asociado=ticket,
                    autor=autor_actual
                )
                db.session.add(nuevo_mensaje)
                db.session.commit()
            return redirect(url_for('ver_ticket', ticket_id_publico=ticket.id_publico))

    return render_template('ticket_detalle.html', ticket=ticket)

@app.route('/ticket/nuevo', methods=['GET', 'POST'])
def crear_ticket():
    if request.method == 'POST':
        cliente = request.form.get('cliente_nombre')
        asunto = request.form.get('asunto')
        tipo = request.form.get('tipo')
        canal = request.form.get('canal_nombre')
        id_agente = request.form.get('id_sac_asignado')

        ultimo_ticket = Ticket.query.order_by(Ticket.id.desc()).first()
        next_id = (ultimo_ticket.id + 1) if ultimo_ticket else 1
        nuevo_id_publico = f"T-00{next_id}"

        nuevo_ticket = Ticket(
            id_publico=nuevo_id_publico,
            cliente_nombre=cliente,
            asunto=asunto,
            tipo=tipo,
            canal_nombre=canal,
            id_sac_asignado=id_agente if id_agente else None
        )

        db.session.add(nuevo_ticket)
        db.session.commit()

        return redirect(url_for('pagina_principal'))

    agentes = Usuario.query.filter_by(rol='Agente SAC').all()
    return render_template('nuevo_ticket.html', agentes=agentes)

@app.route('/contacto', methods=['GET', 'POST'])
def pagina_contacto():
    if request.method == 'POST':
        cliente = request.form.get('cliente_nombre')
        asunto = request.form.get('asunto')
        contenido_mensaje = request.form.get('mensaje')

        procesar_ticket_entrante(
            remitente=cliente,
            asunto=asunto,
            cuerpo=contenido_mensaje,
            canal="Formulario Web"
        )

        return redirect(url_for('pagina_gracias'))

    return render_template('contacto.html')

@app.route('/gracias')
def pagina_gracias():
    return render_template('gracias.html')

@app.route('/webhooks/email', methods=['POST'])
def recibir_email_webhook():
    sender = request.form.get('sender')
    subject = request.form.get('subject')
    body = request.form.get('body-plain')

    if not sender or not subject or not body:
        return "Faltan datos (remitente, asunto o cuerpo)", 406

    nuevo = procesar_ticket_entrante(
        remitente=sender,
        asunto=subject,
        cuerpo=body,
        canal="Email"
    )

    return f"Ticket {nuevo.id_publico} creado", 200

# --- COMANDO PARA RESETEAR LA BASE DE DATOS ---
@app.cli.command("seed-db")
def seed_db_command():
    db.drop_all()
    db.create_all()

    user1 = Usuario(nombre="Juan Pérez", rol="Agente SAC")
    user2 = Usuario(nombre="Maria Gonzalez", rol="Agente SAC")
    
    ticket1 = Ticket(
        id_publico="T-001",
        tipo="Reclamo",
        cliente_nombre="Constructora XYZ",
        asunto="Falla en sistema de riego",
        agente_asignado=user1,
        canal_nombre="Email"
    )

    ticket2 = Ticket(
        id_publico="T-002",
        tipo="Consulta",
        cliente_nombre="Clínica Sonrisa",
        asunto="Info sobre plan de mantención",
        agente_asignado=user2,
        canal_nombre="Formulario Web"
    )

    msg1_t1 = Mensaje(contenido="Mi pedido no ha llegado a tiempo.", es_privado=False, ticket_asociado=ticket1)
    msg2_t1 = Mensaje(contenido="Revisando estado del despacho con courier.", es_privado=True, ticket_asociado=ticket1, autor=user1)
    msg1_t2 = Mensaje(contenido="Quisiera saber el precio del servicio Plus.", es_privado=False, ticket_asociado=ticket2)
    msg2_t2 = Mensaje(contenido="Hola, el plan Plus cuesta $79 USD/mes.", es_privado=False, ticket_asociado=ticket2, autor=user2)
    
    db.session.add_all([user1, user2, ticket1, ticket2, msg1_t1, msg2_t1, msg1_t2, msg2_t2])
    db.session.commit()
    print("Base de datos reiniciada y poblada con datos de ejemplo.")

if __name__ == '__main__':
    app.run(debug=True)

```