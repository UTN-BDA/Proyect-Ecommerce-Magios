#!/bin/bash

# === Ruta al archivo .env (dentro de la misma carpeta) ===
ENV_FILE=".env"

# === Cargar variables del .env ===
if [ -f "$ENV_FILE" ]; then
  export $(grep -v '^#' "$ENV_FILE" | xargs)
else
  echo "❌ No se encontró el archivo .env en $ENV_FILE"
  exit 1
fi

# === Configuración ===
DATE=$(date +%F_%H-%M-%S)
BACKUP_DIR="../backups"
FILENAME="commerce_backup_$DATE.sql"

# === Crear carpeta si no existe ===
mkdir -p "$BACKUP_DIR"

# === Ejecutar pg_dump desde contenedor temporal ===
docker run --rm \
  --network=mired \
  -e PGPASSWORD="$POSTGRES_PASSWORD" \
  postgres:16.4 \
  pg_dump -h postgresql-servidor \
          -U "$POSTGRES_USER" \
          -d "$POSTGRES_DB" \
          -F p \
          --no-owner \
          --no-privileges \
          -v \
          > "$BACKUP_DIR/$FILENAME"

# === Verificar resultado ===
if [ $? -eq 0 ]; then
  echo "✅ Backup completo guardado en $BACKUP_DIR/$FILENAME"
else
  echo "❌ Error durante el backup"
fi
