# WebRTC Video Streaming

Esempio di acquisizione multimediale e trasmissione video P2P locale.

## Descrizione
Questo progetto mostra come utilizzare WebRTC per trasmettere flussi audio/video in tempo reale. Viene simulata una videochiamata P2P all'interno della stessa pagina per illustrare la logica di gestione dei track multimediali.

## Concetti Chiave
- **getUserMedia**: API per accedere all'hardware locale (camera e microfono).
- **MediaStream & MediaStreamTrack**: Rappresentazione dei flussi multimediali.
- **addTrack**: Metodo per aggiungere un flusso alla connessione P2P.
- **ontrack**: Evento che scatta quando il peer remoto riceve un nuovo flusso multimediale.

## Come eseguire
1. Apri `public/index.html` nel browser.
2. Clicca su **"Attiva Camera"** per concedere i permessi e vedere il video locale.
3. Clicca su **"Avvia Video Chiamata"** per stabilire la connessione P2P e trasmettere il video al "Peer Remoto".
4. Usa il pulsante **"Termina"** per chiudere la connessione.

## Note Tecniche
In un'applicazione reale, il video locale viene mostrato immediatamente (Loopback), mentre il video remoto viene ricevuto solo dopo che la negoziazione P2P è andata a buon fine.
