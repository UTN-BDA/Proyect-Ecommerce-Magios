from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Cargar las variables del archivo .env
load_dotenv(".env")  # Asegurate que .env está en la misma carpeta que este script

# Obtener la URI de conexión a la base de datos
DATABASE_URI = os.getenv("DEV_DATABASE_URI")

if not DATABASE_URI:
    raise ValueError("❌ No se encontró la variable DEV_DATABASE_URI en el archivo .env")

# Crear motor SQLAlchemy
engine = create_engine(DATABASE_URI)

# Ejecutar creación de índices
with engine.connect() as conn:
    print("🔧 Creando índices en la tabla 'inventarios'...")

    indices = [
        ("idx_inventarios_producto_id", "producto_id"),
        ("idx_inventarios_cantidad", "cantidad"),
        ("idx_inventarios_fecha", "fecha_transaccion")  # corregido
    ]

    for nombre_indice, columna in indices:
        sql = f"CREATE INDEX IF NOT EXISTS {nombre_indice} ON inventarios ({columna});"
        conn.execute(text(sql))
        print(f"✅ Índice '{nombre_indice}' creado sobre la columna '{columna}'")

    print("🎉 Todos los índices fueron creados correctamente.")
