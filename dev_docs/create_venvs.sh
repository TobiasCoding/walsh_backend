#!/bin/bash

set -e

echo "🧪 Inicializando entornos virtuales en subdirectorios de microservicios..."

BASE_DIR="$(pwd)"
SEARCH_PATHS=("services" "servers" "workers" "net")

for BASE in "${SEARCH_PATHS[@]}"; do
  if [ -d "$BASE" ]; then
    echo "🔍 Buscando en: $BASE/"
    for DIR in "$BASE"/*; do
      if [ -d "$DIR" ]; then
        REQ_FILE="$DIR/requirements.txt"
        VENV_DIR="$DIR/venv"

        # Crear requirements.txt si no existe
        if [ ! -f "$REQ_FILE" ]; then
          echo "📄 $DIR → no tiene requirements.txt, se crea vacío."
          touch "$REQ_FILE"
        fi

        # Crear entorno virtual si no existe
        if [ ! -d "$VENV_DIR" ]; then
          echo "⚙️  Creando entorno virtual en: $VENV_DIR"
          python3 -m venv "$VENV_DIR"
        else
          echo "♻️  Entorno virtual ya existe en: $VENV_DIR"
        fi

        echo "📥 Instalando dependencias desde $REQ_FILE..."
        source "$VENV_DIR/bin/activate"
        pip install --upgrade pip > /dev/null
        pip install -r "$REQ_FILE" || echo "⚠️  No se pudo instalar dependencias (puede estar vacío)"
        deactivate
      fi
    done
  fi
done

echo "✅ Todos los entornos virtuales fueron creados e inicializados correctamente."
