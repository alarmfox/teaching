const WebSocket = require('ws');
const http = require('http');
const fs = require('fs');
const path = require('path');

// Server HTTP per servire il file statico
const server = http.createServer((req, res) => {
    const filePath = path.join(__dirname, '../public', 'index.html');
    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(500);
            return res.end('Errore caricamento index.html');
        }
        res.writeHead(200, { 'Content-Type': 'text/html' });
        res.end(data);
    });
});

// Server WebSocket
const wss = new WebSocket.Server({ server });

wss.on('connection', (ws) => {
    console.log('Nuovo client connesso');

    ws.on('message', (data) => {
        const message = data.toString();
        console.log(`Messaggio ricevuto: ${message}`);
        
        // Broadcast a tutti i client connessi
        wss.clients.forEach((client) => {
            if (client.readyState === WebSocket.OPEN) {
                client.send(message);
            }
        });
    });

    ws.on('close', () => console.log('Client disconnesso'));
});

server.listen(3000, () => {
    console.log('Server in ascolto su http://localhost:3000');
});
