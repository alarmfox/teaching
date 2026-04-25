Laboratorio Pratico: Da Zero a SysAdmin
(Ubuntu Server)
Obiettivo: Installare un server Linux "nudo", prenderne il controllo da remoto tramite Windows,
metterlo in sicurezza con un firewall e creare un servizio di sistema immortale. Strumenti: VirtualBox,
Ubuntu Server (ISO), Windows Terminal / PowerShell.

FASE 1: Creazione VM e "Port Forwarding"
I veri server sono chiusi nei datacenter. Per simulare questa condizione, la nostra VM sarà isolata in
modalità NAT, e creeremo dei "tunnel" per potervi accedere dal nostro PC Windows fisico.
1. Crea la Macchina Virtuale in VirtualBox:
• OS: Ubuntu Server (64-bit).
• RAM: 2048 MB (2 GB).
• Disco: 15 GB.
• Attenzione durante l'installazione: Quando l'installer te lo chiede, spunta la casella
"Install OpenSSH server". Crea un utente chiamato studente con password
studente.
2. Configura il Port Forwarding (A VM spenta o accesa):
• Vai su Impostazioni della VM -> Rete -> Avanzate -> Inoltro delle porte.
• Crea due regole cliccando sull'icona [+]:
• Regola 1 (SSH): Nome SSH, Protocollo TCP, IP Host 127.0.0.1, Porta Host
2222, Porta Guest 22.
• Regola 2 (Web): Nome Web, Protocollo TCP, IP Host 127.0.0.1, Porta Host
8080, Porta Guest 8000.
• Clicca OK e avvia la VM. Fai il login una volta sola dalla finestra nera di VirtualBox per
assicurarti che sia viva, poi riducila a icona. Non la useremo più.

FASE 2: Presa di controllo remota (Windows Terminal)
Ora lavoreremo come veri amministratori di sistema, dal terminale del nostro PC fisico.
1. Apri PowerShell (o Windows Terminal) sul tuo PC.

2. Collegati al server usando il tunnel che abbiamo creato sulla porta 2222:
PowerShell
ssh -p 2222 studente@127.0.0.1

(Scrivi yes per accettare il fingerprint e inserisci la password studente).

2.1 Configurazione Autenticazione a Chiavi (SSH Keys)
Basta password. Usiamo la crittografia.
1. Apri una SECONDA scheda di PowerShell (non dentro Linux, ma sul tuo Windows locale).
2. Genera le chiavi (premi sempre Invio per lasciare i valori di default):
PowerShell
ssh-keygen -t ed25519

3. Copia la chiave pubblica sul server Linux usando questo comando magico da PowerShell:
PowerShell
cat $env:USERPROFILE\.ssh\id_ed25519.pub | ssh -p 2222 studente@127.0.0.1
"mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

4. Test: Torna alla prima scheda (quella collegata a Linux), scrivi exit per uscire, e poi
ricollegati con ssh -p 2222 studente@127.0.0.1. Se entri istantaneamente senza che
ti venga chiesta la password, ha funzionato!

2.2 Blindare SSH
Ora che hai la chiave, chiudi la porta a chi tenta di usare le password.
1. Nel terminale Linux, modifica il file di configurazione SSH:
Bash
sudo nano /etc/ssh/sshd_config

2. Trova la riga #PasswordAuthentication yes, togli il commento (#) e cambiala in:
Plaintext
PasswordAuthentication no

3. Salva (CTRL+O, CTRL+X) e riavvia il servizio:
Bash
sudo systemctl restart ssh

FASE 3: Sicurezza (UFW Firewall)
Il server è raggiungibile, ora dobbiamo difenderlo. Attenzione all'ordine dei comandi o ti chiuderai
fuori!
1. Blocca tutto il traffico in entrata di default:
Bash
sudo ufw default deny incoming

2. Consenti il traffico in uscita:
Bash
sudo ufw default allow outgoing

3. VITALIZIO: Apri la porta SSH prima di attivare il firewall!
Bash
sudo ufw allow 22/tcp

4. Apri la porta per il nostro futuro server web Python (porta 8000):
Bash
sudo ufw allow 8000/tcp

5. Attiva il firewall:
Bash
sudo ufw enable

(Rispondi y alla domanda se vuoi procedere).
6. Verifica che le regole siano corrette:
Bash
sudo ufw status

FASE 4: Systemd - Il Servizio Immortale
Costruiamo un piccolo server web e diciamo a Linux di tenerlo sempre acceso in background.
1. Prepara i file del sito: Crea una directory e un file HTML di base.
Bash
sudo mkdir -p /var/www/pythonweb
echo "<h1>Vittoria! Il servizio Systemd funziona!</h1>" | sudo tee
/var/www/pythonweb/index.html

2. Crea il file del Servizio (Unit File): Questo file spiega a Systemd come far partire la nostra
applicazione.
Bash
sudo nano /etc/systemd/system/pythonweb.service

3. Incolla questa configurazione esatta:
Ini, TOML
[Unit]
Description=Web Server Python di Test
After=network.target

[Service]
Type=simple
User=studente
WorkingDirectory=/var/www/pythonweb
ExecStart=/usr/bin/python3 -m http.server 8000
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target

(Salva con CTRL+O ed esci con CTRL+X).
4. Inizializza e Avvia il Servizio: Invia i comandi a Systemd per caricare il file, avviare il server e
abilitarlo al boot automatico:
Bash
sudo systemctl daemon-reload
sudo systemctl start pythonweb
sudo systemctl enable pythonweb
sudo systemctl status pythonweb

(Dovresti vedere un pallino verde e la scritta active (running). Premi q per uscire dalla
schermata di status).

FASE 5: Il Test Finale (Prova del Nove)
È il momento di raccogliere i frutti del lavoro.
1. Test del Web Server: Apri Google Chrome o Edge sul tuo PC Windows. Nella barra degli
indirizzi, digita: http://127.0.0.1:8080 (Se vedi la scritta "Vittoria!", il port
forwarding e il servizio Systemd stanno dialogando perfettamente).
2. Test di Resilienza (Chaos Monkey): Torna nel terminale Linux. Uccidiamo brutalmente il
processo Python per simulare un crash del server:
Bash
sudo killall python3

Ora ricarica velocemente la pagina web su Windows. Funziona ancora? Controlla lo stato del
servizio:
Bash
sudo systemctl status pythonweb

Noterai che Systemd, obbedendo alla direttiva Restart=always, ha rianimato il processo in
meno di 3 secondi!

