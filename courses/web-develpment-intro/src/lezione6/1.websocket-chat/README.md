# WebSocket Chat

Semplice applicazione di chat bi-direzionale basata su WebSocket.

## Struttura
- `public/`: Contiene il frontend (HTML/JS).
- `server/`: Contiene il server Node.js.

## Come eseguire
1. Entra nella cartella del server:
   ```bash
   cd server
   ```
2. Installa le dipendenze:
   ```bash
   npm install
   ```
3. Avvia il server:
   ```bash
   node server.js
   ```
4. Apri il browser su `http://localhost:3000`.
5. Apri una seconda scheda o un secondo browser per testare la chat tra più client.

## Concetti Chiave
- **Full-Duplex**: Il server può inviare dati al client senza una richiesta esplicita.
- **Event-Driven**: La comunicazione è gestita tramite eventi (`connection`, `message`, `close`).
- **Broadcast**: Il server inoltra ogni messaggio ricevuto a tutti gli altri client connessi.
