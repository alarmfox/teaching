#!/bin/bash

# Script per sincronizzare gli esercizi copiandoli in una cartella separata.
# Hardened version: gestisce la mancanza della cartella .git e forza il ri-cloning se necessario.

# --- CONFIGURAZIONE ---
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SOURCE_DIR="$ROOT_DIR/courses/web-develpment-intro/src"
TARGET_DIR="/home/giuseppe/dev/work/teaching-students-exercises"
REMOTE_URL="git@github.com:alarmfox/students-webdev.git"

echo "=== Sincronizzazione Esercizi Studenti ==="

# 1. Verifica/Inizializzazione della cartella target
# Se la cartella non esiste o NON è un repo git valido (manca .git), la ricreiamo
if [ ! -d "$TARGET_DIR" ] || [ ! -d "$TARGET_DIR/.git" ]; then
    echo "Cartella target non valida o mancante. Preparazione clone in $TARGET_DIR..."
    rm -rf "$TARGET_DIR" # Pulizia totale per evitare conflitti
    mkdir -p "$(dirname "$TARGET_DIR")"
    git clone "$REMOTE_URL" "$TARGET_DIR"
    if [ $? -ne 0 ]; then
        echo "Errore fatale: Impossibile clonare la repository remota."
        exit 1
    fi
fi

# 2. Pulizia e Copia dei file
echo "Pulizia contenuti attuali (mantenendo .git)..."
# Rimuoviamo tutto ciò che non è .git
find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -not -name ".git" -exec rm -rf {} +

echo "Copia dei file da $SOURCE_DIR..."
if [ -d "$SOURCE_DIR" ]; then
    # Copiamo il contenuto della cartella src nella radice della repo target
    cp -r "$SOURCE_DIR"/* "$TARGET_DIR"/
else
    echo "Errore: Cartella sorgente $SOURCE_DIR non trovata!"
    exit 1
fi

# 3. Git Push
cd "$TARGET_DIR" || { echo "Errore: Impossibile entrare in $TARGET_DIR"; exit 1; }

echo "Verifica cambiamenti Git..."
git add .

# Committa solo se ci sono cambiamenti (rispetto all'ultimo commit del remote)
if ! git diff-index --quiet HEAD --; then
    COMMIT_MSG="Update esercizi: $(date +'%Y-%m-%d %H:%M')"
    git commit -m "$COMMIT_MSG"
    echo "Invio dei cambiamenti su GitHub..."
    # Prova a pushare su main, se fallisce prova master
    git push origin main || git push origin master
else
    echo "Nessun cambiamento rilevato rispetto all'ultima sincronizzazione."
fi

echo "=== Sincronizzazione completata! ==="
