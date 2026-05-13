#!/bin/bash

# Script per sincronizzare la cartella degli esercizi con una repository esterna per gli studenti.
# Utilizza 'git subtree' per estrarre la cronologia di una sottocartella e inviarla a un altro remote.

# Configurazione
SUBFOLDER="courses/web-develpment-intro/src"
REMOTE_NAME="students-web-dev"
# CAMBIA QUESTO URL con quello della tua repository GitHub creata per i ragazzi
REMOTE_URL="git@github.com:alarmfox/web-development-exercises.git"

# Verifica se il remote esiste, altrimenti lo aggiunge
if ! git remote | grep -q "$REMOTE_NAME"; then
    echo "Configurazione remote '$REMOTE_NAME' con URL: $REMOTE_URL..."
    git remote add "$REMOTE_NAME" "$REMOTE_URL"
fi

# Assicurati che i cambiamenti locali siano committati
if ! git diff-index --quiet HEAD --; then
    echo "Errore: Hai dei cambiamenti non committati. Committa prima di sincronizzare."
    exit 1
fi

echo "Sincronizzazione della cartella '$SUBFOLDER' verso il branch main di $REMOTE_NAME..."

# Il comando 'git subtree push' estrae i commit che riguardano la cartella specificata
# e li pusha sul branch 'main' del remote indicato.
git subtree push --prefix "$SUBFOLDER" "$REMOTE_NAME" main

if [ $? -eq 0 ]; then
    echo "Sincronizzazione completata con successo!"
else
    echo "Errore durante la sincronizzazione."
    exit 1
fi
