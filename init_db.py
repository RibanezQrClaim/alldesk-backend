import sqlite3

conn = sqlite3.connect('instance/alldesk.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        remitente TEXT,
        asunto TEXT,
        cuerpo TEXT,
        fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()
print("Tabla 'tickets' creada o verificada con éxito.")
