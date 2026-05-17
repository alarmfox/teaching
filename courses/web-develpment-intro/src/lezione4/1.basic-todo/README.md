# Esercitazione: Basic Todo (Client-Server)

Questo progetto è il punto di partenza per trasformare la Todo App della Lezione 2 in un'applicazione Client-Server completa.

## Obiettivo
Spostare la logica di gestione dei task dal `localStorage` del browser a un server centralizzato, gestendo l'autenticazione e il formato JSON.

## Struttura
- `index.html`: Il frontend che comunica con le API tramite `fetch()`.
- `server/`: La logica backend.

## Come avviare il Server

### Opzione A: Node.js (Express)
1. Entra nella cartella server: `cd server`
2. Installa le dipendenze: `npm install`
3. Avvia il server: `node app.js`
4. Il server sarà attivo su `http://localhost:3000`.

### Opzione B: Python (Flask)
1. Entra nella cartella server: `cd server`
2. Installa Flask: `pip install flask`
3. Avvia il server: `python app.py`
4. Il server sarà attivo su `http://localhost:5000`.

## Nota sulla Persistenza
In questa versione "Basic", i dati vengono caricati dal file `tasks.json` all'avvio, ma le modifiche (aggiunta/eliminazione) rimangono solo nella RAM del server. **Se riavvii il server, le modifiche andranno perse.** Questo serve a dimostrare la differenza tra stato in memoria e persistenza su disco.
