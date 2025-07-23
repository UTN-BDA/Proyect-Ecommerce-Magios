# 🛒 Proyecto Ecommerce - Magios

Aplicación web de comercio electrónico basada en microservicios. Actualmente permite operar con un único producto, pero está preparada para escalar su complejidad según los requerimientos del proyecto.

---

## 🚀 Tecnologías principales

- **Backend:** Python, Flask
- **Base de datos:** PostgreSQL
- **Cache / Cola de tareas:** Redis
- **Contenedores:** Docker + Docker Compose
- **Orquestación de servicios:** Scripts en PowerShell
- **Control de versiones:** Git + GitHub

---

## ⚠️ Requisitos previos

- [Docker](https://www.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- PowerShell 

---

## 📁 Estructura del repositorio

```
/docker-postgresql/    --> Configuración y datos persistentes de PostgreSQL
/docker-redis/         --> Configuración de Redis
/docker/               --> Archivos y configuración de los microservicios
setup_ecommerce_noemoji.ps1  --> Script automático para levantar todo
```

---

## 🛠️ Instalación y ejecución

### 🔹 Opción 1: Paso por paso (manual)

1. **Levantar PostgreSQL**

   ```powershell
   cd docker-postgresql
   docker-compose --env-file .env up --build -d
   ```

2. **Levantar Redis**

   ```powershell
   cd ../docker-redis
   docker compose up -d
   ```

3. **Levantar microservicios**

   ```powershell
   cd ../docker
   docker-compose --env-file .env up --build -d
   ```

4. **Verificar contenedores activos**

   ```bash
   docker ps
   ```

---

### 🔹 Opción 2: Automática (recomendada en Windows)

Ejecutar el siguiente script para que todo el entorno se levante automáticamente:

```powershell
.\setup_ecommerce_noemoji.ps1
```

Este script realiza los tres pasos anteriores sin intervención del usuario.

---

## 📌 Notas adicionales

- Asegurate de que el archivo `.env` esté bien configurado antes de ejecutar los servicios.
- Los servicios levantan en segundo plano (`-d`) y reconstruyen imágenes si es necesario (`--build`).
- Puede ser necesario para ejecutar "setup...ps1" en Windows habilitar la ejecucion de scrips para
  eso uar elsiguiente comando:
  Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
- Tener en ejecucion docker (docker desktop en windows)
- Controlar en el caso de tener instalado el motor de postgres en windows de detener el servicio
  en services Tecla_Windows + R y ejecutar services.msc. Detener servicio postgres.
---


---

## 🔹 Optimización con Índices (PostgreSQL + SQLAlchemy)

### 📌 Objetivo

Mejorar el rendimiento de las consultas sobre la tabla `inventarios` agregando **índices** en las columnas más utilizadas, y demostrar su impacto mediante análisis de tiempos de ejecución con `EXPLAIN ANALYZE`.

---

### 🛠️ Script: `crear_indices.py`

Este script crea **tres índices** en la tabla `inventarios`, utilizando SQL puro ejecutado mediante SQLAlchemy. No requiere modificar modelos ni migraciones. Es útil para pruebas de rendimiento sin alterar la lógica del microservicio.

#### Índices creados:

* `producto_id`
* `cantidad`
* `fecha_ingreso`

#### Código clave:

```python
indices = [
    ("idx_inventarios_producto_id", "producto_id"),
    ("idx_inventarios_cantidad", "cantidad"),
    ("idx_inventarios_fecha", "fecha_ingreso")
]

for nombre_indice, columna in indices:
    sql = f"CREATE INDEX IF NOT EXISTS {nombre_indice} ON inventarios ({columna});"
    conn.execute(text(sql))
```

#### Cómo ejecutar:

```bash
cd ms-inventario/Scripts-PruebasBD
python crear_indices.py
```

📎 Asegúrate de tener el entorno virtual activo y el archivo `.env` con la variable `DEV_DATABASE_URI`.

---

### 📊 Medición de rendimiento

Se utilizó el comando SQL:

```sql
EXPLAIN ANALYZE SELECT * FROM inventarios WHERE producto_id = 123;
```

Este comando fue ejecutado 11 veces **antes y después** de crear los índices.

---

### 🔬 Resultados (Resumen)

| N° de Prueba | Tiempo sin índice (ms) | Tiempo con índice (ms) |
| ------------ | ---------------------- | ---------------------- |
| 1            | 8.30                   | 3.56                   |
| 2            | 2.16                   | 1.61                   |
| 3            | 2.09                   | 1.77                   |
| 4            | 1.89                   | 1.24                   |
| 5            | 1.70                   | 1.13                   |
| 6            | 1.58                   | 0.84                   |
| 7            | 1.47                   | 0.59                   |
| 8            | 1.35                   | 0.91                   |
| 9            | 1.22                   | 0.95                   |
| 10           | 1.11                   | 1.56                   |
| 11           | 1.04                   | 1.00                   |
| **Promedio** | **2.17 ms**            | **1.42 ms**            |

📉 **Mejora de rendimiento promedio:** \~35% de reducción en el tiempo de ejecución

---

### ✅ Conclusión

* **Antes:** PostgreSQL utilizaba un *Sequential Scan* (`Seq Scan`), recorriendo toda la tabla.
* **Después:** Se logra optimizar parcialmente, aunque sigue usando `Seq Scan` debido a la baja selectividad o tamaño reducido de la tabla.

🔍 Aun así, con una base de datos más grande o `producto_id` con alta selectividad, el motor podría usar el índice activamente.

---

### 📌 ¿Los índices se guardan?

✅ **Sí. Los índices son persistentes en PostgreSQL.**  
Una vez creados, **se guardan dentro de la estructura de la base de datos** y **no es necesario volver a crearlos cada vez que se inicia el sistema**.

Solo deberías volver a ejecutar el script en los siguientes casos:

- Si eliminás manualmente los índices con `DROP INDEX`
- Si restaurás un backup que no los contiene
- Si trabajás en otra base (TEST/PROD) donde aún no existen
- Si eliminás o recreás la tabla `inventarios`

Gracias al uso de `CREATE INDEX IF NOT EXISTS`, el script es seguro de ejecutar múltiples veces sin generar errores.


## 👥 Miembros del equipo

- [Lucas Candia]
- [Fausto Basile]
- [Mauricio Valdés]
