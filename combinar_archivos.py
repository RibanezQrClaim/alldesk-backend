import os

# Configuración
carpeta_base = '.'
extensiones = ['.py', '.html', '.js', '.css', '.txt']
carpeta_salida = 'archivos_md'
carpetas_excluidas = ['venv', '__pycache__', '.git', 'archivos_md']

# Crear carpeta de salida si no existe
os.makedirs(carpeta_salida, exist_ok=True)

for root, dirs, files in os.walk(carpeta_base):
    # Excluir carpetas no deseadas
    if any(excluida in root.split(os.sep) for excluida in carpetas_excluidas):
        continue

    for file in files:
        if any(file.endswith(ext) for ext in extensiones):
            ruta_original = os.path.join(root, file)
            nombre_relativo = os.path.relpath(ruta_original, carpeta_base).replace(os.sep, '_')
            nombre_md = f"{nombre_relativo}.md"
            ruta_salida = os.path.join(carpeta_salida, nombre_md)

            try:
                with open(ruta_original, 'r', encoding='utf-8', errors='ignore') as f:
                    contenido = f.read()

                with open(ruta_salida, 'w', encoding='utf-8') as f:
                    f.write(f"### {ruta_original}\n\n```{file.split('.')[-1]}\n{contenido}\n```")
            except Exception as e:
                print(f"⚠️ Error procesando {ruta_original}: {e}")

print(f"\n✅ Archivos .md generados en: {os.path.abspath(carpeta_salida)}")

