const WebSocket = require('ws');
const http = require('http');

const server = http.createServer();
const wss = new WebSocket.Server({ server });

// Mappa per tracciare i client connessi: id -> { socket, ip }
const clients = new Map();

wss.on('connection', (ws, req) => {
    // Otteniamo l'IP (gestendo eventuali proxy)
    const ip = req.socket.remoteAddress.replace('::ffff:', '');
    const id = Math.random().toString(36).substring(2, 9);
    
    clients.set(id, { ws, ip });
    console.log(`[+] Nuovo peer connesso: ${ip} (ID: ${id})`);

    // Invia l'ID assegnato al client
    ws.send(JSON.stringify({ type: 'welcome', id, ip }));

    // Notifica a tutti la lista aggiornata dei peer
    broadcastPeerList();

    ws.on('message', (message) => {
        try {
            const data = JSON.parse(message);
            
            // Se il messaggio ha un destinatario specifico, inoltralo
            if (data.to && clients.has(data.to)) {
                console.log(`Forwarding ${Object.keys(data).find(k => ['offer','answer','candidate', 'decline'].includes(k))} from ${id} to ${data.to}`);
                clients.get(data.to).ws.send(JSON.stringify({ 
                    ...data, 
                    from: id,
                    fromIP: clients.get(id).ip // Aggiungiamo l'IP del mittente per la UI
                }));
            }
        } catch (err) {
            console.error("Errore nel processare il messaggio:", err);
        }
    });

    ws.on('close', () => {
        console.log(`[-] Peer disconnesso: ${ip} (ID: ${id})`);
        clients.delete(id);
        broadcastPeerList();
    });
});

function broadcastPeerList() {
    const list = Array.from(clients.entries()).map(([id, info]) => ({
        id,
        ip: info.ip
    }));
    
    const message = JSON.stringify({ type: 'peer-list', peers: list });
    clients.forEach(client => {
        if (client.ws.readyState === WebSocket.OPEN) {
            client.ws.send(message);
        }
    });
}

const PORT = 3000;
server.listen(PORT, '0.0.0.0', () => {
    console.log(`
==================================================
  WebRTC SIGNALING SERVER attivo sulla porta ${PORT}
  In ascolto su tutti gli indirizzi (0.0.0.0)
==================================================
    `);
});
