### .\cargar_clientes.py

```py
from app import db, Cliente, app
import json

with app.app_context():
    with open('clientes.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for item in data:
        cliente = Cliente(nombre=item['nombre'], info_contexto=item['info_contexto'])
        db.session.add(cliente)

    db.session.commit()
    print("Clientes cargados correctamente.")


```