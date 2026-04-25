Dispensa Tecnica: Amministrazione Remota,
Sicurezza e Systemd
Modulo: Linux System Administration - Lezione 5
Obiettivo: Imparare a gestire un server Linux "Headless" (senza interfaccia grafica) dal proprio PC
fisico, configurare servizi in background e proteggere il sistema con un firewall.

1. L'Ambiente Server e il "Port Forwarding"
I veri server non hanno un monitor attaccato. Sono macchine inserite in armadi (rack) all'interno di
datacenter lontani chilometri. Per simularlo, useremo Ubuntu Server su VirtualBox e lo gestiremo dal
terminale del nostro PC fisico (Host).
Poiché la nostra Macchina Virtuale (VM) è configurata in modalità NAT, si trova dietro un "router
virtuale" che la isola dal nostro PC. Per poterci entrare, dobbiamo creare un "tunnel" chiamato Port
Forwarding (Inoltro delle porte).

1.1 Come configurare il Port Forwarding su VirtualBox
Obiettivo: Dire a VirtualBox che tutto il traffico in arrivo sulla porta 2222 di Windows deve essere
spedito alla porta 22 (SSH) di Linux.
1. Apri VirtualBox, seleziona la tua VM (anche se è accesa) e clicca su Impostazioni.
2. Vai nella sezione Rete e assicurati che sia impostato su NAT.
3. Clicca su Avanzate e poi sul pulsante Inoltro delle porte.
4. Clicca sull'icona + verde a destra per aggiungere una regola:
• Nome: SSH_Access
• Protocollo: TCP
• IP Host: 127.0.0.1 (Indica il tuo computer locale)
• Porta Host: 2222
• IP Guest: (Lascia vuoto)
• Porta Guest: 22 (La porta standard del servizio SSH in Linux)
5. Clicca OK e applica le modifiche.

2. Secure Shell (SSH): Il controllo remoto
SSH è il protocollo standard per amministrare sistemi operativi remoti in modo sicuro. Crea una
connessione crittografata impenetrabile.

2.1 Il Primo Accesso
Ora che il Port Forwarding è attivo, riduci a icona VirtualBox. Apri PowerShell (o il Terminale) su
Windows e digita:
PowerShell
ssh -p 2222 studente@127.0.0.1

Se ti chiede di accettare un "fingerprint", scrivi yes. Poi inserisci la tua password di Linux.

2.2 Autenticazione a Chiavi (Key-Based Auth)
Usare le password è scomodo e insicuro (soggetto ad attacchi brute-force). I professionisti usano la
Crittografia Asimmetrica.
1. Genera le chiavi sul tuo PC Windows: (Apri una nuova scheda di PowerShell, non farlo
dentro Linux!)
PowerShell
ssh-keygen -t ed25519

(Premi sempre Invio per accettare i valori predefiniti).
2. Copia la chiave pubblica sul Server Linux: Esegui questo comando da PowerShell per
"spingere" la tua chiave pubblica dentro la VM:
PowerShell
cat $env:USERPROFILE\.ssh\id_ed25519.pub | ssh -p 2222 studente@127.0.0.1
"mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"

3. Il Test: Chiudi la connessione SSH digitando exit. Ricollegati con ssh -p 2222
studente@127.0.0.1. Se non ti chiede la password, hai configurato correttamente le
chiavi!

2.3 Blindare il Server (Disattivare le Password)
Dato che ora entriamo con la nostra chiave univoca, possiamo dire al server di rifiutare qualsiasi
tentativo di accesso tramite password.
Sul terminale Linux (tramite SSH), edita il file di configurazione:
Bash
sudo nano /etc/ssh/sshd_config

Cerca la riga #PasswordAuthentication yes, togli il commento (#) e modificala in:
Plaintext
PasswordAuthentication no

Attenzione: questa modifica avrà effetto solo dopo aver riavviato il servizio SSH (vedi capitolo 4).

3. Sicurezza di Base: Il Firewall (UFW)
Un server esposto in rete subisce continui tentativi di accesso. Dobbiamo usare un Firewall per
bloccare il traffico non desiderato. Su Ubuntu usiamo UFW (Uncomplicated Firewall).
REGOLA D'ORO: UFW lavora sulle porte interne di Linux. Quindi dovremo aprire la
porta 22 (SSH), a prescindere dal fatto che su VirtualBox abbiamo usato la 2222.

3.1 La sequenza di attivazione corretta
Se attivi il firewall prima di autorizzare la porta SSH, verrai "buttato fuori" dalla tua stessa connessione
remota! Segui questo ordine:
1. Imposta il blocco totale in entrata ("Default Deny"):
Bash
sudo ufw default deny incoming
sudo ufw default allow outgoing

2. Autorizza i servizi necessari (Whitelist):
Bash
sudo ufw allow ssh

# Oppure: sudo ufw allow 22/tcp

3. Attiva il Firewall:
Bash
sudo ufw enable

4. Controlla che tutto sia corretto:
Bash
sudo ufw status verbose

4. Systemd: Il "Manager" dei Servizi
I programmi che devono rimanere sempre accesi in background (come il server web o lo stesso SSH)
sono chiamati Demoni o Servizi. In Linux, questi servizi sono gestiti da un sistema centrale chiamato
Systemd.
Il comando per parlare con Systemd è systemctl.

4.1 Comandi Essenziali
Da imparare a memoria per la gestione quotidiana:
• sudo systemctl status [servizio] ➔ Verifica se il servizio sta funzionando (cerca
la scritta active (running)).
• sudo systemctl start [servizio] ➔ Accende il servizio.
• sudo systemctl stop [servizio] ➔ Spegne il servizio.
• sudo systemctl restart [servizio] ➔ Lo riavvia (necessario dopo aver
modificato i file in /etc/, come abbiamo fatto prima con SSH!).
• sudo systemctl enable [servizio] ➔ Dice a Linux di accendere questo servizio
automaticamente ogni volta che il server si avvia.
Prova subito ad applicare la modifica fatta nel capitolo 2.3 digitando: sudo systemctl
restart ssh

4.2 Creare un servizio personale da zero
Creiamo un piccolo server web Python e trasformiamolo in un servizio Systemd immortale.
1. Prepara i file:
Bash
sudo mkdir /opt/mioservizio
echo "<h1>Sito Web servito da Systemd!</h1>" | sudo tee
/opt/mioservizio/index.html

2. Crea la "Unit File" (Il manuale di istruzioni per Systemd):
Bash
sudo nano /etc/systemd/system/miniweb.service

3. Scrivi questa configurazione e salva (CTRL+O, CTRL+X):
Ini, TOML
[Unit]

Description=Il mio mini server web Python
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/mioservizio
# Esegue il modulo web di Python sulla porta 8000
ExecStart=/usr/bin/python3 -m http.server 8000
Restart=on-failure

[Install]
WantedBy=multi-user.target

4. Fai partire il tuo nuovo Demone:
Bash
sudo systemctl daemon-reload

# Fai leggere a Systemd i nuovi file

sudo systemctl start miniweb

# Accendilo

sudo systemctl enable miniweb

# Rendilo automatico al riavvio

sudo systemctl status miniweb

# Verifica che sia acceso

Vuoi vederlo funzionare? Ritorna su VirtualBox (Port Forwarding) e aggiungi una regola:
• Nome: Web_Access, Porta Host: 8080, Porta Guest: 8000. Poi vai sul terminale Linux e
apri la porta nel firewall: sudo ufw allow 8000. Infine, apri il browser su Windows e vai
all'indirizzo http://127.0.0.1:8080. Se vedi la scritta, sei ufficialmente un SysAdmin!

