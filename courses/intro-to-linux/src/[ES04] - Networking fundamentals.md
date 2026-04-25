Esercitazione Networking: "The Double
Identity"
Obiettivo: Configurare indirizzi IP multipli, manipolare la risoluzione dei nomi (DNS locale) e testare
la connettività specifica.
Scenario: Sei l'amministratore di un server che deve offrire due servizi diversi:
1. Un servizio pubblico (accesso Internet).
2. Un servizio "Intranet Segreta" accessibile solo su una rete privata specifica. Non hai budget per
una seconda scheda di rete. Devi configurare la tua unica interfaccia per gestire una "doppia
identità".

Parte 1: Ricognizione (Discovery)
Prima di toccare qualsiasi cosa, devi capire la situazione attuale.
1. Trova il nome della tua interfaccia: Usa il comando moderno (non ifconfig!) per elencare
le interfacce.
• Comando: ip addr show (o ip a).
• Nota: Cerca l'interfaccia che ha un IP (solitamente enp0s3, eth0 o ens33). Ignora
lo (loopback).
2. Identifica il tuo IP attuale: Segnati l'indirizzo IP dinamico che VirtualBox ti ha assegnato
(probabilmente simile a 10.0.2.15).
3. Identifica il Gateway: Scopri chi ti dà accesso a Internet.
• Comando: ip route
• Cerca la riga che inizia con default via ....

Parte 2: IP Aliasing (L'Identità Segreta)
Ora aggiungeremo manualmente un secondo indirizzo IP statico alla stessa scheda di rete. Questo IP
apparterrà a una rete completamente inventata (192.168.99.x).
1. Aggiungi l'IP secondario: Sostituisci [NOME_INTERFACCIA] con il nome trovato nella
Parte 1 (es. enp0s3).
Bash
sudo ip addr add 192.168.99.10/24 dev [NOME_INTERFACCIA]

2. Verifica: Lancia di nuovo ip a.
• Dovresti vedere due righe "inet" sotto la stessa interfaccia.
• Una è quella vecchia (DHCP), l'altra è la tua nuova 192.168.99.10.
3. Ping Test (Loopback): Prova a pingare te stesso sul nuovo IP.
Bash
ping 192.168.99.10

(Funziona? Bene, il kernel ha accettato l'indirizzo).

Parte 3: DNS Spoofing Locale (/etc/hosts)
I server non si chiamano per numero, ma per nome. Faremo finta che questo nuovo IP corrisponda al
dominio segreto dell'azienda.
1. Apri il file hosts:
Bash
sudo nano /etc/hosts

2. Aggiungi in fondo al file questa riga:
Plaintext
192.168.99.10

portale-segreto.corp

3. Salva (CTRL+O) ed esci (CTRL+X).
4. Test di risoluzione: Prova a pingare il nome invece del numero:
Bash
ping portale-segreto.corp

(Se risponde l'IP 192.168.99.10, hai configurato correttamente il DNS locale).

Parte 4: Simulazione Servizio Dedicato
Ora avviamo un Web Server Python che risponde SOLO sulla rete segreta, ignorando quella pubblica.
1. Crea una cartella per il sito segreto:
Bash
mkdir /tmp/top_secret
echo "<h1>ACCESSO AUTORIZZATO AL PORTALE SEGRETO</h1>" >
/tmp/top_secret/index.html

2. Binding specifico: Avvia il server Python dicendogli di ascoltare (bind) solo sull'IP
192.168.99.10 e non sull'IP pubblico.
Bash
cd /tmp/top_secret
python3 -m http.server 8080 --bind 192.168.99.10

(Nota: Non chiudere questo terminale).
3. Il Test Finale: Apri un secondo terminale (o usa un'altra tab).
• Prova a scaricare la pagina usando il nome DNS creato prima:
Bash
curl http://portale-segreto.corp:8080

• Risultato atteso: Vedi il codice HTML "ACCESSO AUTORIZZATO...".
• Prova ora a collegarti usando l'IP "normale" della VM (es. 10.0.2.15) sulla porta 8080:
Bash
curl http://10.0.2.15:8080

• Risultato atteso: Connection Refused o timeout.
Perché? Perché abbiamo configurato il servizio per ascoltare solo sull'identità segreta!

Parte 5: Pulizia (Reset)
Poiché abbiamo usato il comando ip addr add (che è volatile), per pulire tutto basta un comando o
un riavvio. Ma facciamolo da veri SysAdmin, manualmente.
1. Rimuovi l'IP secondario:
Bash
sudo ip addr del 192.168.99.10/24 dev [NOME_INTERFACCIA]

2. Rimuovi la riga da /etc/hosts (con nano).
3. Verifica con ip a che tutto sia tornato come prima.

Mini-Progetto: Deploy di un Forum Aziendale
(phpBB)
Scenario: Il team di supporto tecnico ha bisogno di una piattaforma interna per discutere dei ticket e
condividere soluzioni (Knowledge Base). Ti è stato chiesto di installare un forum phpBB sul server di
test. Devi configurare il server LAMP, il database e i permessi del filesystem affinché l'applicazione
funzioni correttamente.
Obiettivo: Avere un forum funzionante accessibile via browser all'indirizzo
http://[IP_VM]/forum. Tempo stimato: 60-70 Minuti

Fase 1: Preparazione dello Stack (Dipendenze)
phpBB è un software robusto che richiede moduli PHP specifici per gestire immagini (avatar) e file
XML.
1. Aggiorna e installa LAMP di base:
Bash
sudo apt update
sudo apt install apache2 mariadb-server php libapache2-mod-php php-mysql
unzip wget -y

2. Installa i moduli PHP specifici per phpBB: Senza questi, l'installazione si bloccherà.
Bash
sudo apt install php-xml php-mbstring php-gd php-intl php-curl php-zip -y

3. Riavvia Apache per caricare i nuovi moduli:
Bash
sudo systemctl restart apache2

Fase 2: Configurazione del Database
1. Accedi a MariaDB:
Bash
sudo mysql

2. Crea il database e l'utente dedicato (Esegui una riga alla volta):
SQL

CREATE DATABASE forum_db;
CREATE USER 'forum_admin'@'localhost' IDENTIFIED BY 'password_sicura';
GRANT ALL PRIVILEGES ON forum_db.* TO 'forum_admin'@'localhost';
FLUSH PRIVILEGES;
EXIT;

Fase 3: Download e Setup Filesystem
A differenza dell'esercizio precedente, qui non metteremo il sito nella root (/), ma in una sottocartella
/forum.
1. Vai in /tmp e scarica l'ultima versione di phpBB (in italiano):
Bash
cd /tmp
# Scarichiamo la versione 3.3.11 (o latest stabile)
wget https://download.phpbb.com/pub/release/3.3/3.3.11/phpBB-3.3.11.zip

2. Scompatta:
Bash
unzip phpBB-3.3.11.zip

(Questo creerà una cartella chiamata phpBB3).
3. Deploy: Sposta la cartella nella directory web e rinominala in "forum":
Bash
sudo mv phpBB3 /var/www/html/forum

Fase 4: Gestione Avanzata dei Permessi
phpBB è molto severo sulla sicurezza. Alcune cartelle devono essere scrivibili dal server web (wwwdata), altre no.
1. Assegna la proprietà: Tutto appartiene a www-data (l'utente di Apache).
Bash
sudo chown -R www-data:www-data /var/www/html/forum

2. Permessi specifici (Security Hardening): Di base, i file devono essere leggibili ma non
modificabili. Le cartelle di cache e upload devono essere scrivibili.
Imposta permessi standard (755 per cartelle, 644 per file):

Bash
sudo find /var/www/html/forum -type d -exec chmod 755 {} \;
sudo find /var/www/html/forum -type f -exec chmod 644 {} \;

Apri i permessi solo dove serve (Cache, Store, Files, Images):
Bash
sudo chmod 777 /var/www/html/forum/cache
sudo chmod 777 /var/www/html/forum/store
sudo chmod 777 /var/www/html/forum/files
sudo chmod 777 /var/www/html/forum/images/avatars/upload

(Nota: In produzione useremmo permessi più stretti tipo 775 con il gruppo corretto, ma per
questo lab 777 su queste specifiche cartelle interne va bene per capire il concetto di
"writable").

Fase 5: Installazione via Browser
1. Apri il browser sul tuo PC Host.
2. Digita: http://[IP_DELLA_TUA_VM]/forum
3. Dovresti vedere la pagina di installazione di phpBB. Clicca sulla scheda Installazione (Install).
4. Segui il wizard:
• Dati Amministratore: Crea il tuo utente (es. admin, pass: admin123).
• Database:
• Tipo: MySQL with MySQLi Extension
• Host: localhost
• Nome DB: forum_db
• Utente: forum_admin
• Password: password_sicura
• Configurazione Server: Lascia i default.
5. Prosegui fino alla fine dell'installazione.

Fase 6: Pulizia Obbligatoria (Security)
Alla fine dell'installazione, phpBB ti mostrerà un avviso rosso gigante: "Rimuovere, spostare o
rinominare la cartella install". Finché non lo fai, il forum sarà bloccato per sicurezza.
1. Torna sul terminale della VM.
2. Elimina la cartella di installazione:
Bash
sudo rm -rf /var/www/html/forum/install

3. Torna sul browser e ricarica la pagina. Il tuo forum è online!

🔎 Troubleshooting
• Errore 500 o pagina bianca: Controlla se hai installato php-xml e riavviato Apache. È
l'errore più comune con phpBB.
• "Directory is not writable": Hai sbagliato la Fase 4. Ricontrolla i comandi chmod.
• Impossibile connettersi al DB: Hai usato root invece dell'utente forum_admin? In alcune
installazioni di MariaDB, root non può accedere via password esterna per sicurezza. Usa sempre
l'utente dedicato.

★ Challenge Extra (Per i più veloci)
Customizzazione del messaggio di benvenuto (HTML/CSS Base) Il forum funziona, ma è brutto.
1. Entra nel Pannello di Controllo Amministrazione (Link in fondo alla pagina del forum ->
"ACP").
2. Vai su "Generale" -> "Configurazione Board".
3. Cambia il nome del sito e la descrizione.
4. Livello Pro: Prova a sostituire il logo di phpBB via terminale.
• Trova un'immagine .png su internet.
• Scaricala con wget dentro
/var/www/html/forum/styles/prosilver/theme/images/.
• Rinominala per sovrascrivere site_logo.svg (o modifica il CSS se sei capace).

