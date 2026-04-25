Dispensa Tecnica: Servizi, SSH e Sicurezza di
Base
Modulo: Linux System Administration - Lezione 5
Obiettivo: Gestire un server "Headless" (senza monitor), configurare l'accesso remoto sicuro, gestire i
servizi di sistema (Demoni) e configurare il Firewall.

1. Benvenuti nel "Vero" Linux (Ubuntu Server)
Fino ad ora abbiamo usato una versione Desktop con interfaccia grafica. Tuttavia, nel mondo reale, i
server Linux (Cloud, Datacenter) sono Headless: non hanno monitor, mouse o finestre. Tutto si
gestisce tramite riga di comando da remoto.
Perché?
• Risorse: L'interfaccia grafica consuma RAM e CPU inutilmente.
• Sicurezza: Meno software installato significa meno bug potenziali.
• Automazione: La CLI è facile da scriptare, la GUI no.

2. Secure Shell (SSH)
Poiché non possiamo sederci fisicamente davanti al server, usiamo SSH. È un protocollo che crea un
"tunnel" crittografato tra il tuo computer (Client) e il server.

2.1 Autenticazione: Password vs Chiavi
SSH supporta due metodi principali di accesso:
1. Password: Semplice, ma vulnerabile agli attacchi "Brute Force" (hacker che provano milioni di
password al secondo).
2. Chiavi Asimmetriche (Key-Based): Metodo standard professionale. Si basa su una coppia di
file crittografici.
• Chiave Privata (Private Key): Risiede sul tuo PC (Client). È la tua "chiave di casa". Non va
mai condivisa.
• Chiave Pubblica (Public Key): Risiede sul Server. È come la "serratura". Puoi darla a
chiunque. Il server ti fa entrare solo se la tua chiave privata "apre" la chiave pubblica che hai
installato lì.

2.2 Comandi SSH Fondamentali
Comando (sul tuo PC)
Descrizione
ssh user@192.168.1.50 Si collega al server specificato.
ssh-keygen -t ed25519 Genera una nuova coppia di chiavi sul tuo PC.
ssh-copy-id user@IP
Copia la tua chiave pubblica sul server remoto.
Esporta in Fogli

3. Gestione dei Servizi (Systemd)
Un Servizio (o Demone) è un programma che gira in background, senza interfaccia utente, in attesa di
richieste (es. Web Server, Database, SSH). In Linux moderni, il "capo" che gestisce questi servizi si
chiama Systemd. Il comando per controllarlo è systemctl.

3.1 Ciclo di vita di un servizio
Azione

Comando
Significato
sudo systemctl start
Avviare apache2
Accende il servizio ora (fino al prossimo riavvio).
sudo systemctl stop
Fermare apache2
Spegne il servizio immediatamente.
sudo systemctl restart
Riavviare apache2
Stop + Start (utile quando cambi le configurazioni).
sudo systemctl status
Stato
Ti dice se è "Active (running)" o "Failed".
apache2
sudo systemctl enable Fondamentale: Dice al servizio di partire
Abilitare apache2
automaticamente all'avvio del server.
Esporta in Fogli

4. Sicurezza di Rete: Firewall (UFW)
Linux ha un firewall integrato potentissimo (Netfilter/Iptables), ma difficile da configurare. Noi
useremo UFW (Uncomplicated Firewall), un'interfaccia semplificata.

4.1 Principio del "Default Deny"
La regola d'oro della sicurezza è: Blocca tutto ciò che entra, tranne quello che serve esplicitamente.

4.2 Configurazione UFW
1. Imposta le policy di base:
Bash
sudo ufw default deny incoming

# Blocca tutto in entrata

sudo ufw default allow outgoing

# Permetti tutto in uscita

2. Apri le porte necessarie (Whitelist):
Bash
sudo ufw allow ssh

# (Porta 22) - FONDAMENTALE FARLO PRIMA DI ATTIVARE!

sudo ufw allow http

# (Porta 80)

3. Attiva il firewall:
Bash
sudo ufw enable

ATTENZIONE: Se attivi UFW senza aver prima dato allow ssh, verrai buttato fuori
dal server e non potrai più rientrare da remoto!

5. Gestione dei Log (Troubleshooting)
Quando qualcosa non funziona, Linux scrive il motivo in un file di testo. I log si trovano quasi sempre
in /var/log.

5.1 File di Log Critici
• /var/log/syslog (o messages): Il diario generale del sistema.
• /var/log/auth.log: Log di Sicurezza. Registra chi entra, chi esce e chi sbaglia la
password (SSH, sudo).
• /var/log/apache2/access.log: Chi sta visitando il tuo sito web.
• /var/log/apache2/error.log: Perché il tuo sito web non funziona.

5.2 Analisi in Tempo Reale
Non aprire i log con un editor di testo! Sono enormi. Usa tail.
Bash
# Segue il file in diretta mentre vengono scritte nuove righe
tail -f /var/log/auth.log

(Premi CTRL+C per uscire)

Laboratorio Pratico: Server Hardening
Scenario: Hai appena installato una nuova macchina Ubuntu Server. Devi metterla in sicurezza,
configurare un web server e disabilitare l'accesso via password.

Parte 1: Setup e Accesso SSH
1. Avvia la VM Ubuntu Server e fai login.
2. Trova il tuo IP: ip addr show.
3. DA ORA IN POI, lavora dal terminale del tuo PC reale (Host):
• Collegati: ssh studente@Tuo_IP.
• Accetta il fingerprint (scrivi yes).
• Inserisci la password.

Parte 2: Configurazione Chiavi (Key-Based Auth)
1. Sul tuo PC Host (apri un altro terminale):
• Genera le chiavi: ssh-keygen -t ed25519 (Premi Invio a tutte le domande).
• Copia la chiave sulla VM: ssh-copy-id studente@Tuo_IP.
2. Prova: Prova a collegarti di nuovo via SSH. Se non ti chiede la password, hai fatto tutto
correttamente.

Parte 3: Blindare SSH
Ora che le chiavi funzionano, disabilitiamo le password per evitare attacchi hacker.
1. Sulla VM, edita la configurazione SSH:
Bash
sudo nano /etc/ssh/sshd_config

2. Trova la riga #PasswordAuthentication yes, togli il commento (#) e cambiala in:
PasswordAuthentication no
3. Salva ed esci (CTRL+O, CTRL+X).
4. Riavvia il servizio per applicare le modifiche:
Bash
sudo systemctl restart ssh

Parte 4: Web Server e Servizi
1. Installa Nginx: sudo apt update && sudo apt install nginx.
2. Verifica che sia attivo: systemctl status nginx.
3. Controlla se è abilitato al boot: systemctl is-enabled nginx.

Parte 5: Configurazione Firewall
1. Imposta le regole:
Bash
sudo ufw default deny incoming
sudo ufw allow ssh
sudo ufw allow http

2. Attivalo: sudo ufw enable.
3. Verifica lo stato: sudo ufw status.

Parte 6: Analisi Intrusioni (Log)
1. Tieni aperto il collegamento SSH.
2. Prova ad aprire un nuovo terminale dal tuo PC e prova a collegarti come un utente inesistente:
ssh hacker@Tuo_IP (Fallirà).
3. Torna al terminale SSH connesso e cerca la traccia del tentativo nel log:
Bash
sudo grep "Invalid user" /var/log/auth.log

Dovresti vedere il tentativo fallito dell'utente "hacker".

