from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(50), nullable=False)
    tickets_asignados = db.relationship('Ticket', backref='agente_asignado', lazy=True)
    mensajes_enviados = db.relationship('Mensaje', backref='autor', lazy=True)

class Cliente(db.Model):
    __tablename__ = 'cliente'
    id_cliente = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(150), nullable=False)
    info_contexto = db.Column(db.Text)

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
    prioridad = db.Column(db.String(20), default='Normal')
    clasificacion = db.Column(db.String(100), default='Otro')
    sentimiento = db.Column(db.String(20), default='Neutro')
    urgencia = db.Column(db.Integer, default=3)
    resumen = db.Column(db.Text)
    tags = db.Column(db.String(255))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'), nullable=True)
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
