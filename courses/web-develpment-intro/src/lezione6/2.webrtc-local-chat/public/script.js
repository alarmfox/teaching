/**
 * WebRTC Local P2P Chat
 * Questo script simula lo scambio di messaggi tra due Peer (A e B)
 * che risiedono nella stessa pagina. In un'applicazione reale,
 * lo scambio di Offer/Answer/ICE Candidates avverrebbe tramite un Signaling Server.
 */

let peerA, peerB;
let dataChannelA, dataChannelB;

const startBtn = document.getElementById('startBtn');
const chatA = document.getElementById('chatA');
const chatB = document.getElementById('chatB');
const inputA = document.getElementById('inputA');
const inputB = document.getElementById('inputB');
const sendA = document.getElementById('sendA');
const sendB = document.getElementById('sendB');

// Funzione per avviare la connessione P2P
async function startConnection() {
    startBtn.disabled = true;
    startBtn.innerText = "Connessione in corso...";

    // 1. Inizializzazione dei Peer
    peerA = new RTCPeerConnection();
    peerB = new RTCPeerConnection();

    // 2. Creazione del DataChannel su Peer A (il chiamante)
    dataChannelA = peerA.createDataChannel("chat");
    setupDataChannel(dataChannelA, "Peer A", chatA, inputA, sendA);

    // 3. Gestione del DataChannel su Peer B (il ricevente)
    peerB.ondatachannel = (event) => {
        dataChannelB = event.channel;
        setupDataChannel(dataChannelB, "Peer B", chatB, inputB, sendB);
    };

    // 4. Scambio ICE Candidates (Simulazione Signaling locale)
    peerA.onicecandidate = (e) => e.candidate && peerB.addIceCandidate(e.candidate);
    peerB.onicecandidate = (e) => e.candidate && peerA.addIceCandidate(e.candidate);

    // 5. Handshake: Offer & Answer
    try {
        const offer = await peerA.createOffer();
        await peerA.setLocalDescription(offer);
        console.log("Peer A: Offer creata");

        await peerB.setRemoteDescription(offer);
        const answer = await peerB.createAnswer();
        await peerB.setLocalDescription(answer);
        console.log("Peer B: Answer creata");

        await peerA.setRemoteDescription(answer);
        console.log("P2P Handshake Completato");
    } catch (err) {
        console.error("Errore durante l'handshake:", err);
    }
}

// Configurazione degli eventi del DataChannel
function setupDataChannel(channel, peerName, displayArea, inputElement, sendButton) {
    channel.onopen = () => {
        displayArea.innerHTML = `<p class="text-green-600 font-bold">✓ Connesso P2P con successo</p>`;
        inputElement.disabled = false;
        sendButton.disabled = false;
    };

    channel.onmessage = (e) => {
        const msg = JSON.parse(e.data);
        const p = document.createElement('p');
        p.innerHTML = `<span class="font-bold text-blue-800">${msg.sender}:</span> ${msg.text}`;
        displayArea.appendChild(p);
        displayArea.scrollTop = displayArea.scrollHeight;
    };

    const sendMessage = () => {
        const text = inputElement.value.trim();
        if (text) {
            const payload = { sender: peerName, text: text };
            channel.send(JSON.stringify(payload));
            
            // Visualizza localmente
            const p = document.createElement('p');
            p.innerHTML = `<span class="font-bold text-gray-600">Tu:</span> ${text}`;
            displayArea.appendChild(p);
            displayArea.scrollTop = displayArea.scrollHeight;
            
            inputElement.value = "";
        }
    };

    sendButton.onclick = sendMessage;
    inputElement.onkeypress = (e) => e.key === 'Enter' && sendMessage();
}

startBtn.onclick = startConnection;
document.getElementById('resetBtn').onclick = () => location.reload();
