# Lezione 6: Real-Time Communication

Questa lezione esplora le tecnologie per la comunicazione in tempo reale sul web, focalizzandosi su WebSocket e WebRTC.

## Contenuti

1.  **WebSocket Chat** (`1.websocket-chat/`): Una semplice applicazione di chat bi-direzionale che utilizza il protocollo WebSocket per la comunicazione client-server in tempo reale.
2.  **WebRTC Local Chat** (`2.webrtc-local-chat/`): Una simulazione di connessione Peer-to-Peer (P2P) per lo scambio di messaggi di testo utilizzando i Data Channel di WebRTC.
3.  **WebRTC Video Streaming** (`3.video-streaming/`): Un esempio di acquisizione multimediale (camera e microfono) e trasmissione video P2P locale.

## Obiettivi Didattici

- Comprendere la differenza tra il modello Request/Response (HTTP) e la comunicazione Full-Duplex (WebSocket).
- Apprendere i concetti base di WebRTC: Peer Connection, Media Streams e Data Channels.
- Sperimentare il processo di "handshake" (Offer/Answer) e lo scambio di candidati ICE per stabilire connessioni P2P.
- Analizzare i vantaggi e le sfide della comunicazione real-time (latenza, NAT traversal, segnalazione).

## Requisiti

- Node.js installato per eseguire il server WebSocket.
- Un browser moderno con supporto WebRTC (Chrome, Firefox, Edge, Safari).
