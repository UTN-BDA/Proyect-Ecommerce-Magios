#!/bin/bash

ENV_FILE=".env"

if [ ! -f "$ENV_FILE" ]; then
  echo "❌ No se encontró el archivo .env"
  exit 1
fi

export $(grep -v '^#' "$ENV_FILE" | xargs)

BACKUP_SQL="$1"
if [ -z "$BACKUP_SQL" ]; then
  echo "❌ Debes indicar el archivo .sql como argumento."
  exit 1
fi

if [ ! -f "$BACKUP_SQL" ]; then
  echo "❌ El archivo '$BACKUP_SQL' no existe."
  exit 1
fi

# Ruta POSIX compatible para Bash y Docker
BACKUP_DIR=$(cd "$(dirname "$BACKUP_SQL")"; pwd)
FILENAME=$(basename "$BACKUP_SQL")
MERGED_FILE="restore_total.sql"
MERGED_PATH="$BACKUP_DIR/$MERGED_FILE"

echo "🧹 Generando archivo combinado con DROP SCHEMA + backup..."
echo "DROP SCHEMA public CASCADE; CREATE SCHEMA public;" > "$MERGED_PATH"
cat "$BACKUP_SQL" >> "$MERGED_PATH"

# ✅ Ejecutar directamente desde Bash, sin cmd.exe
echo "🚀 Restaurando desde: $MERGED_FILE"

docker run --rm \
  --network=mired \
  -v "$BACKUP_DIR:/restore" \
  -e PGPASSWORD="$POSTGRES_PASSWORD" \
  postgres:16.4 \
  psql -h postgresql-servidor \
       -U "$POSTGRES_USER" \
       -d "$POSTGRES_DB" \
       -f "/restore/$MERGED_FILE"

if [ $? -eq 0 ]; then
  echo "✅ Restauración completa realizada con éxito."
  rm "$MERGED_PATH"
else
  echo "❌ Error durante la restauración."
fi
