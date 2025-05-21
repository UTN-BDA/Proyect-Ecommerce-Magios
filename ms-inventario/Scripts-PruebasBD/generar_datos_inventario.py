from faker import Faker
import random
import csv
import os

# Configuración
faker = Faker()
cantidad_registros = 10000
cantidad_productos = 100  # producto_id entre 1 y 100

# Ruta actual del script
ruta_actual = os.path.dirname(os.path.abspath(__file__))
output_file = os.path.join(ruta_actual, "datos_inventario_falsos.csv")

# Crear y escribir el CSV
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["producto_id", "fecha_transaccion", "cantidad", "entrada_salida"])

    for _ in range(cantidad_registros):
        producto_id = random.randint(1, cantidad_productos)
        fecha = faker.date_time_between(start_date='-3y', end_date='now').strftime('%Y-%m-%d %H:%M:%S')
        cantidad = round(random.uniform(1, 50), 2)
        entrada_salida = random.choice([0, 1])  # 1 = entrada, 0 = salida
        writer.writerow([producto_id, fecha, cantidad, entrada_salida])

print(f"✅ Se generaron {cantidad_registros} registros en:\n{output_file}")
