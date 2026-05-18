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

// Funzione per gestire i candidati ICE in modo sicuro
async function handleIceCandidate(peer, candidate) {
    try {
        if (candidate && peer.remoteDescription) {
            await peer.addIceCandidate(candidate);
        }
    } catch (err) {
        console.error("Errore nell'aggiunta del candidato ICE:", err);
    }
}

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
    // Usiamo un array per bufferizzare i candidati se arrivano prima della RemoteDescription
    const iceCandidatesA = [];
    const iceCandidatesB = [];

    peerA.onicecandidate = (e) => {
        if (!e.candidate) return;
        if (peerB.remoteDescription) {
            peerB.addIceCandidate(e.candidate).catch(console.error);
        } else {
            iceCandidatesA.push(e.candidate);
        }
    };

    peerB.onicecandidate = (e) => {
        if (!e.candidate) return;
        if (peerA.remoteDescription) {
            peerA.addIceCandidate(e.candidate).catch(console.error);
        } else {
            iceCandidatesB.push(e.candidate);
        }
    };

    // 5. Handshake: Offer & Answer
    try {
        const offer = await peerA.createOffer();
        await peerA.setLocalDescription(offer);
        console.log("Peer A: Offer creata e LocalDescription impostata");

        await peerB.setRemoteDescription(offer);
        // Ora che peerB ha la remote description, aggiungiamo i candidati bufferizzati di A
        while (iceCandidatesA.length > 0) {
            await peerB.addIceCandidate(iceCandidatesA.shift());
        }

        const answer = await peerB.createAnswer();
        await peerB.setLocalDescription(answer);
        console.log("Peer B: Answer creata e LocalDescription impostata");

        await peerA.setRemoteDescription(answer);
        // Ora che peerA ha la remote description, aggiungiamo i candidati bufferizzati di B
        while (iceCandidatesB.length > 0) {
            await peerA.addIceCandidate(iceCandidatesB.shift());
        }

        console.log("P2P Handshake Completato");
        startBtn.innerText = "P2P Connesso";
        startBtn.classList.replace('bg-green-600', 'bg-blue-800');
    } catch (err) {
        console.error("Errore durante l'handshake:", err);
        startBtn.innerText = "Errore Connessione";
        startBtn.classList.replace('bg-green-600', 'bg-red-600');
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
        
        // Visualizza messaggio ricevuto (Allineato a sinistra)
        const wrapper = document.createElement('div');
        wrapper.className = "flex w-full justify-start";
        
        const div = document.createElement('div');
        div.className = "bg-white border border-gray-200 text-gray-800 p-2 rounded-lg shadow-sm text-xs max-w-[80%] rounded-tl-none";
        div.innerHTML = `<span class="font-bold text-blue-800">${msg.sender}:</span><br>${msg.text}`;
        
        wrapper.appendChild(div);
        displayArea.appendChild(wrapper);
        displayArea.scrollTop = displayArea.scrollHeight;
    };

    const sendMessage = () => {
        const text = inputElement.value.trim();
        if (text) {
            const payload = { sender: peerName, text: text };
            channel.send(JSON.stringify(payload));
            
            // Visualizza localmente (Allineato a destra)
            const wrapper = document.createElement('div');
            wrapper.className = "flex w-full justify-end";
            
            const div = document.createElement('div');
            div.className = "bg-[rgb(38,66,139)] text-white p-2 rounded-lg shadow-sm text-xs max-w-[80%] rounded-tr-none";
            div.innerHTML = `<span class="font-bold opacity-75">Tu:</span><br>${text}`;
            
            wrapper.appendChild(div);
            displayArea.appendChild(wrapper);
            displayArea.scrollTop = displayArea.scrollHeight;
            
            inputElement.value = "";
        }
    };

    sendButton.onclick = sendMessage;
    inputElement.onkeypress = (e) => e.key === 'Enter' && sendMessage();
}

startBtn.onclick = startConnection;
document.getElementById('resetBtn').onclick = () => location.reload();
