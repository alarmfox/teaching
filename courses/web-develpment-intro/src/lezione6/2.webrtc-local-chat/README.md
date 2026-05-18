# WebRTC Local Chat

Simulazione di una connessione Peer-to-Peer (P2P) sulla stessa pagina.

## Descrizione
Questo esempio dimostra il funzionamento di WebRTC utilizzando i `RTCDataChannel`. Per semplicità didattica, i due peer (A e B) risiedono nella stessa finestra del browser. Lo scambio di segnali (Signaling) necessario per stabilire la connessione avviene localmente in memoria invece di passare attraverso un server esterno.

## Concetti Chiave
- **RTCPeerConnection**: L'oggetto principale che gestisce la connessione P2P.
- **RTCDataChannel**: API per lo scambio di dati arbitrari (testo, file) con bassa latenza.
- **Signaling**: Il processo di scambio di `Offer`, `Answer` e `ICE Candidates`.
- **ICE (Interactive Connectivity Establishment)**: Protocollo per trovare il percorso migliore per connettere due peer (attraverso NAT e Firewall).

## Come eseguire
Basta aprire il file `public/index.html` in un browser moderno.
Cliccare su **"Avvia Handshake P2P"** per simulare la negoziazione della connessione.
Una volta stabilita la connessione, è possibile inviare messaggi tra i due "Peer".
