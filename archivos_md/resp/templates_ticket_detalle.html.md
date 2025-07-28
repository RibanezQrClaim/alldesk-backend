### .\templates\ticket_detalle.html

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Detalle del Ticket {{ ticket.id_publico }}</title>
    <style>
        body { font-family: sans-serif; display: flex; margin: 0; }
        .main-content { flex-grow: 1; padding: 2em; }
        .sidebar { width: 300px; background-color: #f2f2f2; padding: 1.5em; border-left: 1px solid #ccc; height: 100vh; }
        .chat-container { border: 1px solid #ccc; padding: 1em; margin-bottom: 20px; max-height: 500px; overflow-y: auto; }
        .mensaje { margin-bottom: 15px; padding: 10px; border-radius: 8px; max-width: 80%; }
        .mensaje p { margin: 0; }
        .mensaje .meta { font-size: 0.8em; color: #555; margin-top: 5px; }
        .mensaje-publico { background-color: #e1f5fe; }
        .mensaje-privado { background-color: #fff9c4; border: 1px dashed #fbc02d; } /* Nota interna amarilla */
        .mensaje-privado .meta::before { content: '🔒 '; font-family: sans-serif; } /* Ícono de candado */
        textarea { width: 100%; box-sizing: border-box; padding: 10px; border-radius: 5px; border: 1px solid #ccc; }
        .info-ticket p { margin: 8px 0; }
        a { color: #007bff; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>

    <div class="main-content">
        <a href="{{ url_for('pagina_principal') }}">&larr; Volver a la Bandeja de Entrada</a>
        <h1>Conversación del Ticket #{{ ticket.id_publico }}</h1>
        <h2>{{ ticket.asunto }}</h2>

        <div class="chat-container">
            {% for mensaje in ticket.historial %}
                <div class="mensaje {% if mensaje.es_privado %}mensaje-privado{% else %}mensaje-publico{% endif %}">
                    
                    <p><strong>{{ mensaje.autor.nombre if mensaje.autor else 'Cliente' }}:</strong></p>

                    <p>{{ mensaje.contenido }}</p>
                    <p class="meta">{{ mensaje.fecha_envio.strftime('%Y-%m-%d %H:%M') }}</p>
                </div>
            {% endfor %}
        </div>

        <h3>Responder</h3>
        <form action="{{ url_for('ver_ticket', ticket_id_publico=ticket.id_publico) }}" method="post">
            <textarea name="respuesta" rows="5" placeholder="Escribe tu respuesta aquí..."></textarea>
            <br><br>
            <input type="checkbox" name="es_privado" id="es_privado">
            <label for="es_privado">Marcar como nota interna</label>
            <br><br>
            <button type="submit">Enviar Respuesta</button>
        </form>
    </div>

    <div class="sidebar">
        <h3>Info del Ticket</h3>
        <div class="info-ticket">
            <p><strong>ID:</strong> {{ ticket.id_publico }}</p>
            <p><strong>Tipo:</strong> {{ ticket.tipo }}</p>
            <p><strong>Cliente:</strong> {{ ticket.cliente_nombre }}</p>
            <p><strong>Canal:</strong> {{ ticket.canal_nombre }}</p>
            <p><strong>Estado:</strong> {{ ticket.estado }}</p>
            <p><strong>Asignado a:</strong> {{ ticket.agente_asignado.nombre if ticket.agente_asignado else 'No asignado' }}</p>
        </div>
    </div>

</body>
</html>
```