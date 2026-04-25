Obiettivo: Mettere in pratica tutte le competenze acquisite nel corso (CLI, Storage, Permessi, Rete,
Servizi, Sicurezza) configurando un server di produzione da zero.
Durata stimata: 2 Ore Scenario: Sei stato assunto come Junior System Administrator presso la startup
"TechNova". Ti è stata consegnata una macchina virtuale nuda (Ubuntu Server) e un secondo disco
vuoto. Devi preparare l'infrastruttura per ospitare il nuovo sito aziendale in modo sicuro e resiliente.

Fase 1: Accesso e Sicurezza Iniziale (Lezione 2 & 5)
Il server non deve mai essere gestito direttamente dalla console di VirtualBox, e l'accesso deve essere
blindato.
1. Configura il Port Forwarding su VirtualBox per la porta SSH (es. 2222 -> 22) e per il traffico
Web (es. 8080 -> 80).
2. Collegati via SSH dal tuo terminale Windows/Mac locale.
3. Genera e copia le tue chiavi SSH sul server.
4. Modifica /etc/ssh/sshd_config per disabilitare l'accesso con password
(PasswordAuthentication no). Riavvia il servizio SSH.
5. Configura il Firewall (UFW):
• Blocca tutto in ingresso.
• Consenti SSH e HTTP.
• Attiva UFW e verifica lo stato.

Fase 2: Provisioning dello Storage (Lezione 3)
Il sito aziendale produrrà molti dati. Non possiamo salvarli sul disco di sistema, ci serve il disco
secondario.
1. Aggiungi un disco da 5GB alla VM su VirtualBox (se non lo hai già fatto).
2. Trova il nuovo disco usando lsblk.
3. Usa cfdisk per creare un'unica partizione primaria che occupi tutto lo spazio.
4. Formatta la partizione in ext4.
5. Crea la cartella /var/www/technova.
6. Ottieni l'UUID del nuovo disco e configura /etc/fstab affinché la nuova partizione venga
montata in automatico su /var/www/technova.
7. Testa il mount con sudo mount -a e verifica con df -h.

Fase 3: Deploy dell'Applicazione (Lezione 2 & 4)
Installiamo il server web e prepariamo i permessi.
1. Installa il server web Nginx: sudo apt update && sudo apt install nginx.
2. Cambia il proprietario della cartella /var/www/technova: assegnala all'utente www-data
e al gruppo www-data.
3. Imposta i permessi della cartella a 755.
4. Crea un file index.html all'interno di /var/www/technova contenente il messaggio:
<h1>Benvenuti in TechNova - Server Sicuro</h1>.
5. Trick avanzato: Di default, Nginx legge da /var/www/html. Rinomina la cartella di default e
crea un link simbolico, oppure semplicemente modifica la configurazione di default di Nginx
(/etc/nginx/sites-available/default) cambiando root /var/www/html; in
root /var/www/technova;.
6. Riavvia Nginx con Systemd.

Fase 4: Servizio di Sicurezza Personalizzato (Lezione 5)
L'azienda vuole un sistema che registri l'orario di accensione del server su un file di testo ogni volta che
la macchina fa il boot.
1. Crea uno script semplicissimo in /usr/local/bin/boot_logger.sh:
Bash
#!/bin/bash
echo "Server TechNova avviato alle: $(date)" >> /var/log/technova_boot.log

2. Rendi lo script eseguibile (chmod +x).
3. Crea una Unit Systemd chiamata bootlogger.service che esegua questo script al boot
(usa Type=oneshot).
4. Abilita il servizio.

Fase 5: Strategia di Backup (Lezione 3)
Il sito deve essere salvato periodicamente.
1. Crea la cartella /backup.
2. Usa tar per creare un archivio compresso (.tar.gz) dell'intera cartella
/var/www/technova e salvalo dentro /backup.

3. Bonus: Inserisci il comando tar in crontab -e (cerca su internet come si fa!) per farlo
eseguire automaticamente ogni notte a mezzanotte (0 0 * * *).
IL TEST FINALE: Apri il browser sul tuo PC fisico e vai su http://127.0.0.1:8080. Se vedi
la pagina di TechNova, hai completato con successo l'infrastruttura!

