/**
 * WebRTC Video Loopback Example
 * 
 * Questo script dimostra come catturare uno stream multimediale locale
 * e trasmetterlo a un Peer remoto (simulato nella stessa pagina) 
 * utilizzando le API RTCPeerConnection.
 */

const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');
const cameraBtn = document.getElementById('cameraBtn');
const callBtn = document.getElementById('callBtn');
const hangupBtn = document.getElementById('hangupBtn');
const logArea = document.getElementById('logArea');

let localStream;
let pc1; // Peer Chiamante
let pc2; // Peer Ricevente

function log(msg) {
    const time = new Date().toLocaleTimeString();
    logArea.innerHTML += `<div>> [${time}] ${msg}</div>`;
    logArea.scrollTop = logArea.scrollHeight;
}

// 1. Acquisizione Media
cameraBtn.onclick = async () => {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ 
            video: true, 
            audio: true 
        });
        localVideo.srcObject = localStream;
        document.getElementById('localPlaceholder').classList.add('hidden');
        document.getElementById('statusLocal').innerText = "Camera ON";
        document.getElementById('statusLocal').classList.replace('bg-gray-200', 'bg-green-100');
        
        cameraBtn.disabled = true;
        callBtn.disabled = false;
        log("Media locale acquisito con successo.");
    } catch (err) {
        log(`Errore acquisizione: ${err.message}`);
    }
};

// 2. Avvio Video Chiamata (Handshake)
callBtn.onclick = async () => {
    callBtn.disabled = true;
    hangupBtn.disabled = false;
    log("Inizio negoziazione P2P...");

    // Creazione dei Peer
    pc1 = new RTCPeerConnection();
    pc2 = new RTCPeerConnection();

    // Gestione dei candidati ICE
    pc1.onicecandidate = e => e.candidate && pc2.addIceCandidate(e.candidate);
    pc2.onicecandidate = e => e.candidate && pc1.addIceCandidate(e.candidate);

    // Gestione dell'arrivo dello stream remoto su Peer 2
    pc2.ontrack = e => {
        log("Stream remoto ricevuto!");
        remoteVideo.srcObject = e.streams[0];
        document.getElementById('remotePlaceholder').classList.add('hidden');
        document.getElementById('statusRemote').innerText = "Streaming P2P";
        document.getElementById('statusRemote').classList.replace('bg-gray-200', 'bg-blue-100');
    };

    // Aggiunta dei track locali a Peer 1
    localStream.getTracks().forEach(track => {
        pc1.addTrack(track, localStream);
    });
    log("Track multimediali aggiunti a Peer 1.");

    // Handshake: Offer/Answer
    try {
        const offer = await pc1.createOffer();
        await pc1.setLocalDescription(offer);
        log("Peer 1: Offer inviata.");

        await pc2.setRemoteDescription(offer);
        const answer = await pc2.createAnswer();
        await pc2.setLocalDescription(answer);
        log("Peer 2: Answer inviata.");

        await pc1.setRemoteDescription(answer);
        log("Connessione P2P stabilita.");
    } catch (err) {
        log(`Errore handshake: ${err.message}`);
    }
};

// 3. Chiusura
hangupBtn.onclick = () => {
    pc1.close();
    pc2.close();
    pc1 = null;
    pc2 = null;
    
    remoteVideo.srcObject = null;
    document.getElementById('remotePlaceholder').classList.remove('hidden');
    document.getElementById('statusRemote').innerText = "No Stream";
    
    hangupBtn.disabled = true;
    callBtn.disabled = false;
    log("Chiamata terminata.");
};
