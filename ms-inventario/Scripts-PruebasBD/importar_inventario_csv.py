import sys
import os
import csv
from datetime import datetime
from dotenv import load_dotenv

# ✅ Cargar .env desde el mismo directorio del script
dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path)

# ✅ Agregar ms-inventario al path para importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.stock import Stock

# ✅ Ruta al archivo CSV
CSV_PATH = os.path.join(os.path.dirname(__file__), "datos_inventario_falsos.csv")

def importar_csv():
    app = create_app()
    with app.app_context():
        try:
            print("🧹 Eliminando datos existentes de inventarios...")
            db.session.query(Stock).delete()
            db.session.commit()

            registros = []
            with open(CSV_PATH, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for fila in reader:
                    registro = Stock(
                        producto=int(fila["producto_id"]),
                        fecha_transaccion=datetime.strptime(fila["fecha_transaccion"], "%Y-%m-%d %H:%M:%S"),
                        cantidad=float(fila["cantidad"]),
                        entrada_salida=int(fila["entrada_salida"])
                    )
                    registros.append(registro)

            print(f"📦 Insertando {len(registros)} registros en lotes...")
            BATCH_SIZE = 1000
            total = len(registros)
            for i in range(0, total, BATCH_SIZE):
                batch = registros[i:i+BATCH_SIZE]
                db.session.bulk_save_objects(batch)
                db.session.commit()
                print(f"✅ Insertados {i + len(batch)} de {total} registros...")

            print("🎉 Todos los registros fueron insertados correctamente.")

        except Exception as e:
            print("❌ Error al importar CSV:", str(e))

if __name__ == "__main__":
    importar_csv()
