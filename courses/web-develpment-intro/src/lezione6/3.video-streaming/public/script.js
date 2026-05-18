/**
 * WebRTC Video & Chat - Targeted Signaling Version
 */

// UI Elements
const modeSelect = document.getElementById('modeSelect');
const signalingConfig = document.getElementById('signalingConfig');
const signalingIp = document.getElementById('signalingIp');
const connectSignaling = document.getElementById('connectSignaling');
const signalingStatus = document.getElementById('signalingStatus');
const statusDot = document.getElementById('statusDot');
const peerDiscovery = document.getElementById('peerDiscovery');
const peerList = document.getElementById('peerList');

const localVideo = document.getElementById('localVideo');
const remoteVideo = document.getElementById('remoteVideo');
const cameraBtn = document.getElementById('cameraBtn');
const callBtn = document.getElementById('callBtn');
const hangupBtn = document.getElementById('hangupBtn');
const toggleMic = document.getElementById('toggleMic');
const toggleCam = document.getElementById('toggleCam');
const micIconContainer = document.getElementById('micIconContainer');
const camIconContainer = document.getElementById('camIconContainer');

const chatMessagesA = document.getElementById('chatMessagesA');
const chatInputA = document.getElementById('chatInputA');
const chatSendA = document.getElementById('chatSendA');
const chatMessagesB = document.getElementById('chatMessagesB');

const logArea = document.getElementById('logArea');

// State
let localStream;
let pc; // In Targeted Mode, we only have ONE pc locally
let dc;
let socket;
let isRemoteMode = false;
let myId = null;
let remotePeerId = null; // The ID of the targeted peer

const ICONS = {
    micOn: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>`,
    micOff: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5.586 15H4a1 1 0 01-1-1v-4a1 1 0 011-1h1.586l4.707-4.707C10.923 3.663 12 4.109 12 5v14c0 .891-1.077 1.337-1.707.707L5.586 15z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2"></path></svg>`,
    camOn: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>`,
    camOff: `<svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636"></path></svg>`
};

function log(msg) {
    const time = new Date().toLocaleTimeString();
    logArea.innerHTML += `<div>> [${time}] ${msg}</div>`;
    logArea.scrollTop = logArea.scrollHeight;
}

// Mode Selection
modeSelect.onchange = () => {
    isRemoteMode = modeSelect.value === 'remote';
    signalingConfig.classList.toggle('hidden', !isRemoteMode);
    peerDiscovery.classList.toggle('hidden', !isRemoteMode);
    if (!isRemoteMode) location.reload(); // Reset if switching back
};

// Signaling
connectSignaling.onclick = () => {
    const ip = signalingIp.value.trim() || 'localhost';
    const wsUrl = `ws://${ip}:3000`;
    
    log(`Connessione a ${wsUrl}...`);
    socket = new WebSocket(wsUrl);

    socket.onopen = () => {
        statusDot.classList.replace('bg-gray-300', 'bg-green-500');
        signalingStatus.innerHTML = `<span class="w-2 h-2 rounded-full bg-green-500"></span> Online`;
        signalingStatus.classList.replace('text-gray-400', 'text-green-600');
        connectSignaling.disabled = true;
    };

    socket.onmessage = async (e) => {
        const msg = JSON.parse(e.data);
        
        switch(msg.type) {
            case 'welcome':
                myId = msg.id;
                log(`Mio ID: ${myId} (IP: ${msg.ip})`);
                break;
            case 'peer-list':
                updatePeerList(msg.peers);
                break;
            default:
                handleSignalingData(msg);
        }
    };
};

function updatePeerList(peers) {
    peerList.innerHTML = '';
    peers.forEach(peer => {
        if (peer.id === myId) return;
        const btn = document.createElement('button');
        btn.className = "px-3 py-1 bg-blue-100 text-blue-900 rounded-full text-[10px] font-bold hover:bg-blue-200 border border-blue-200 transition flex items-center gap-1";
        btn.innerHTML = `<span class="w-1.5 h-1.5 rounded-full bg-blue-500"></span> Peer: ${peer.ip}`;
        btn.onclick = () => selectPeer(peer.id, peer.ip);
        peerList.appendChild(btn);
    });
}

function selectPeer(id, ip) {
    remotePeerId = id;
    log(`Selezionato Peer ${ip}. Clicca 'Avvia Handshake' per chiamare.`);
    callBtn.disabled = !localStream;
}

// Ringing UI Elements
const ringModal = document.getElementById('ringModal');
const callerIp = document.getElementById('callerIp');
const acceptBtn = document.getElementById('acceptBtn');
const declineBtn = document.getElementById('declineBtn');

let pendingOffer = null;

// ... (existing code remains same until handleSignalingData)

async function handleSignalingData(msg) {
    if (msg.offer) {
        remotePeerId = msg.from;
        pendingOffer = msg.offer;
        
        // Mostra il modal di chiamata (Ringing)
        callerIp.innerText = `da: ${msg.fromIP || 'Peer Remoto'}`;
        ringModal.classList.remove('hidden');
        log(`Chiamata in arrivo da ${remotePeerId}...`);
    } else if (msg.answer) {
        log("Risposta ricevuta.");
        await pc.setRemoteDescription(new RTCSessionDescription(msg.answer));
    } else if (msg.decline) {
        log("Il peer ha rifiutato la chiamata.");
        alert("Chiamata rifiutata dal destinatario.");
        callBtn.disabled = false;
        hangupBtn.disabled = true;
    } else if (msg.candidate) {
        if (pc) await pc.addIceCandidate(new RTCIceCandidate(msg.candidate));
    }
}

// Gestione Risposta (Accetta)
acceptBtn.onclick = async () => {
    ringModal.classList.add('hidden');
    if (!localStream) {
        log("Inizializzazione automatica hardware...");
        await cameraBtn.onclick();
    }
    
    log(`Accetto chiamata da ${remotePeerId}...`);
    await createPeerConnection();
    await pc.setRemoteDescription(new RTCSessionDescription(pendingOffer));
    const answer = await pc.createAnswer();
    await pc.setLocalDescription(answer);
    sendSignal({ answer, to: remotePeerId });
    pendingOffer = null;
    callBtn.disabled = true;
    hangupBtn.disabled = false;
};

// Gestione Rifiuto
declineBtn.onclick = () => {
    ringModal.classList.add('hidden');
    log("Chiamata rifiutata.");
    sendSignal({ decline: true, to: remotePeerId });
    pendingOffer = null;
};

// Modifica sendSignal per includere l'IP (opzionale, per UI)
function sendSignal(data) {
    if (socket && socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({ ...data, from: myId }));
    }
}

// Media
cameraBtn.onclick = async () => {
    try {
        localStream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true });
        localVideo.srcObject = localStream;
        document.getElementById('localPlaceholder').classList.add('hidden');
        document.getElementById('mediaControls').classList.remove('hidden');
        document.getElementById('statusLocal').innerText = "LIVE";
        document.getElementById('statusLocal').classList.replace('bg-gray-200', 'bg-green-100');
        cameraBtn.disabled = true;
        if (!isRemoteMode || remotePeerId) callBtn.disabled = false;
        log("Hardware pronto.");
    } catch (err) { log(`Errore: ${err.message}`); }
};

toggleMic.onclick = () => {
    const track = localStream.getAudioTracks()[0];
    if (track) {
        track.enabled = !track.enabled;
        micIconContainer.innerHTML = track.enabled ? ICONS.micOn : ICONS.micOff;
        toggleMic.classList.toggle('bg-red-500', !track.enabled);
    }
};

toggleCam.onclick = () => {
    const track = localStream.getVideoTracks()[0];
    if (track) {
        track.enabled = !track.enabled;
        camIconContainer.innerHTML = track.enabled ? ICONS.camOn : ICONS.camOff;
        toggleCam.classList.toggle('bg-red-500', !track.enabled);
        localVideo.classList.toggle('opacity-50', !track.enabled);
    }
};

// Call Handlers
callBtn.onclick = async () => {
    if (isRemoteMode) {
        await startRemoteCall();
    } else {
        await startLoopbackCall();
    }
};

async function createPeerConnection() {
    pc = new RTCPeerConnection({ iceServers: [{ urls: 'stun:stun.l.google.com:19302' }] });
    
    pc.onicecandidate = e => e.candidate && sendSignal({ candidate: e.candidate, to: remotePeerId });

    pc.ontrack = e => {
        remoteVideo.srcObject = e.streams[0];
        document.getElementById('remotePlaceholder').classList.add('hidden');
        document.getElementById('statusRemote').innerText = "CONNECTED";
        document.getElementById('statusRemote').classList.replace('bg-gray-200', 'bg-blue-100');
    };

    pc.ondatachannel = (e) => {
        dc = e.channel;
        setupChat(dc, "Peer Remoto", chatMessagesA, chatInputA, chatSendA);
    };

    localStream.getTracks().forEach(track => pc.addTrack(track, localStream));
}

async function startRemoteCall() {
    await createPeerConnection();
    dc = pc.createDataChannel("chat");
    setupChat(dc, "Tu", chatMessagesA, chatInputA, chatSendA);

    const offer = await pc.createOffer();
    await pc.setLocalDescription(offer);
    sendSignal({ offer, to: remotePeerId });
    log("Offerta inviata.");
    callBtn.disabled = true;
    hangupBtn.disabled = false;
}

// Loopback remains for demo (same logic as before but adapted for shared 'pc' variable)
async function startLoopbackCall() {
    log("Avvio Loopback...");
    // Special case for loopback: we keep two pc objects
    const pc1 = new RTCPeerConnection();
    const pc2 = new RTCPeerConnection();

    const dc1 = pc1.createDataChannel("chat");
    setupChat(dc1, "Tu (A)", chatMessagesA, chatInputA, chatSendA);

    pc2.ondatachannel = (e) => {
        const dc2 = e.channel;
        setupChat(dc2, "Tu (B)", chatMessagesB, document.getElementById('chatInputB'), document.getElementById('chatSendB'));
    };

    pc1.onicecandidate = e => e.candidate && pc2.addIceCandidate(e.candidate);
    pc2.onicecandidate = e => e.candidate && pc1.addIceCandidate(e.candidate);

    pc2.ontrack = e => {
        remoteVideo.srcObject = e.streams[0];
        document.getElementById('remotePlaceholder').classList.add('hidden');
        document.getElementById('statusRemote').innerText = "Loopback Stream";
    };

    localStream.getTracks().forEach(track => pc1.addTrack(track, localStream));

    const offer = await pc1.createOffer();
    await pc1.setLocalDescription(offer);
    await pc2.setRemoteDescription(offer);
    const answer = await pc2.createAnswer();
    await pc2.setLocalDescription(answer);
    await pc1.setRemoteDescription(answer);
    
    callBtn.disabled = true;
    hangupBtn.disabled = false;
}

// Chat
function setupChat(channel, label, myDisplay, myInput, myBtn) {
    const activate = () => {
        myInput.disabled = false;
        myBtn.disabled = false;
        myDisplay.innerHTML = `<p class="text-green-600 font-bold text-center">✓ P2P Chat Active</p>`;
    };
    if (channel.readyState === 'open') activate();
    channel.onopen = activate;

    channel.onmessage = (e) => {
        const msg = JSON.parse(e.data);
        appendBubble(myDisplay, msg.sender, msg.text, true);
    };

    const send = () => {
        const text = myInput.value.trim();
        if (text && channel.readyState === 'open') {
            channel.send(JSON.stringify({ sender: "Remote", text }));
            appendBubble(myDisplay, "Tu", text, false);
            myInput.value = "";
        }
    };
    myBtn.onclick = send;
    myInput.onkeypress = e => e.key === 'Enter' && send();
}

function appendBubble(display, sender, text, isReceived) {
    const wrapper = document.createElement('div');
    wrapper.className = `flex w-full ${isReceived ? 'justify-start' : 'justify-end'}`;
    const div = document.createElement('div');
    div.className = `p-2 rounded-lg shadow-sm max-w-[85%] ${isReceived ? 'bg-white border text-gray-800 rounded-tl-none' : 'bg-primary text-white rounded-tr-none'}`;
    div.innerHTML = `<div class="font-bold text-[8px] mb-0.5 opacity-70">${sender}</div><div class="text-[11px]">${text}</div>`;
    wrapper.appendChild(div);
    display.appendChild(wrapper);
    display.scrollTop = display.scrollHeight;
}

hangupBtn.onclick = () => location.reload();
