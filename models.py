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
    tipo = db.Column(db.String(50))
    cliente_nombre = db.Column(db.String(100))
    asunto = db.Column(db.String(255))
    estado = db.Column(db.String(50))
    canal_nombre = db.Column(db.String(50))
    fecha_creacion = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    fecha_cierre = db.Column(db.DateTime, nullable=True)
    prioridad = db.Column(db.String(50))
    clasificacion = db.Column(db.String(100))
    sentimiento = db.Column(db.String(50))
    urgencia = db.Column(db.String(50))
    resumen = db.Column(db.Text)
    tags = db.Column(db.String(255))
    cliente_id = db.Column(db.Integer, db.ForeignKey('cliente.id_cliente'))
    id_sac_asignado = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'))  ✅

    mensajes = db.relationship('Mensaje', backref='ticket', lazy=True)

class Mensaje(db.Model):
    __tablename__ = 'mensaje'
    id_mensaje = db.Column(db.Integer, primary_key=True)
    contenido = db.Column(db.Text, nullable=False)
    fecha_envio = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    es_privado = db.Column(db.Boolean, default=False)
    id_ticket = db.Column(db.Integer, db.ForeignKey('ticket.id'), nullable=False)
    id_usuario_autor = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=True)
