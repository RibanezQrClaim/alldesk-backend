from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import datetime
import os

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)

# --- CONFIGURACIÓN DE BASE DE DATOS INTELIGENTE (LA ÚNICA Y CORRECTA) ---
database_uri = os.environ.get('DATABASE_URL')
if database_uri and database_uri.startswith("postgres://"):
    # Usa la base de datos de Heroku (PostgreSQL)
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)
else:
    # Usa la base de datos local (SQLite)
    database_uri = 'sqlite:///' + os.path.join(basedir, 'instance', 'alldesk.db')

app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# --- MODELOS DE LA BASE DE DATOS ---
class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    tickets_asignados = db.relationship('Ticket', backref='agente_asignado', lazy=True)
    mensajes_enviados = db.relationship('Mensaje', backref='autor', lazy=True)

class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = db.Column(db.Integer, primary_key=True)
    id_publico = db.Column(db.String(20), unique=True, nullable=False)
    tipo = db.Column(db.String(50), nullable=False)
    cliente_nombre = db.Column(db.String(150), nullable=False)
    asunto = db.Column(db.String(250), nullable=False)
    estado = db.Column(db.String(50), default='Abierto')
    canal_nombre = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime, nullable=True)
    id_sac_asignado = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=True)
    historial = db.relationship('Mensaje', backref='ticket_asociado', lazy=True, cascade="all, delete-orphan")

class Mensaje(db.Model):
    __tablename__ = 'mensaje'
    id_mensaje = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    es_privado = db.Column(db.Boolean, default=False)
    id_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    id_usuario_autor = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=True)

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
                nuevo_mensaje = Mensaje(contenido=contenido_respuesta, es_privado=es_privado, ticket_asociado=ticket, autor=autor_actual)
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
        if ultimo_ticket:
            next_id = ultimo_ticket.id + 1
        else:
            next_id = 1
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

        ultimo_ticket = Ticket.query.order_by(Ticket.id.desc()).first()
        if ultimo_ticket:
            next_id = ultimo_ticket.id + 1
        else:
            next_id = 1
        nuevo_id_publico = f"T-00{next_id}"
        
        nuevo_ticket = Ticket(id_publico=nuevo_id_publico, cliente_nombre=cliente, asunto=asunto, tipo='Consulta', canal_nombre='Formulario Web', id_sac_asignado=None)
        primer_mensaje = Mensaje(contenido=contenido_mensaje, ticket_asociado=nuevo_ticket)

        db.session.add(nuevo_ticket)
        db.session.add(primer_mensaje)
        db.session.commit()

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

    ultimo_ticket = Ticket.query.order_by(Ticket.id.desc()).first()
    if ultimo_ticket:
        next_id = ultimo_ticket.id + 1
    else:
        next_id = 1
    nuevo_id_publico = f"T-00{next_id}"
    
    nuevo_ticket = Ticket(id_publico=nuevo_id_publico, cliente_nombre=sender, asunto=subject, tipo='Consulta', canal_nombre='Email', id_sac_asignado=None)
    primer_mensaje = Mensaje(contenido=body, ticket_asociado=nuevo_ticket)

    db.session.add(nuevo_ticket)
    db.session.add(primer_mensaje)
    db.session.commit()

    return "OK", 200

# --- COMANDO PARA INICIALIZAR LA BASE DE DATOS ---
@app.cli.command("seed-db")
def seed_db_command():
    """Borra y recrea la BD con datos de ejemplo."""
    db.drop_all()
    db.create_all()

    user1 = Usuario(nombre="Juan Pérez", rol="Agente SAC")
    user2 = Usuario(nombre="Maria Gonzalez", rol="Agente SAC")
    
    ticket1 = Ticket(id_publico="T-001", tipo="Reclamo", cliente_nombre="Constructora XYZ", asunto="Falla en sistema de riego", agente_asignado=user1, canal_nombre="Email")
    ticket2 = Ticket(id_publico="T-002", tipo="Consulta", cliente_nombre="Clínica Sonrisa", asunto="Info sobre plan de mantención", agente_asignado=user2, canal_nombre="Formulario Web")

    msg1_t1 = Mensaje(contenido="Mi pedido no ha llegado a tiempo.", es_privado=False, ticket_asociado=ticket1)
    msg2_t1 = Mensaje(contenido="Revisando estado del despacho con courier.", es_privado=True, ticket_asociado=ticket1, autor=user1)
    msg1_t2 = Mensaje(contenido="Quisiera saber el precio del servicio Plus.", es_privado=False, ticket_asociado=ticket2)
    msg2_t2 = Mensaje(contenido="Hola, el plan Plus cuesta $79 USD/mes.", es_privado=False, ticket_asociado=ticket2, autor=user2)
    
    db.session.add_all([user1, user2, ticket1, ticket2, msg1_t1, msg2_t1, msg1_t2, msg2_t2])
    db.session.commit()
    print("Base de datos reiniciada y poblada con datos de ejemplo.")

if __name__ == '__main__':
    app.run(debug=True)