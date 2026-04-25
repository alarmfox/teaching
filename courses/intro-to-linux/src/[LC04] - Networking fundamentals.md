Dispensa Tecnica: Fondamenti di Networking in
Linux
Modulo: Linux System Administration - Lezione 4
Obiettivo: Comprendere l'architettura di rete di base (Layer 2 e Layer 3) e gestire la configurazione di
rete di un host Linux tramite terminale.

1. Fondamenti di Networking: MAC vs IP
Per far comunicare due macchine, l'architettura di rete (modello OSI/TCP-IP) utilizza diversi livelli di
indirizzamento. I due più importanti per l'amministrazione di base sono il MAC Address e l'Indirizzo
IP.

1.1 MAC Address (Indirizzo Fisico)
Il Media Access Control (MAC) address è un identificatore univoco assegnato dal produttore alla
scheda di rete (NIC - Network Interface Card).
• Livello OSI: Lavora al Livello 2 (Data Link).
• Formato: 48 bit, espresso in 6 coppie di cifre esadecimali (es. 00:1A:2B:3C:4D:5E).
• Funzione: Viene utilizzato per la comunicazione all'interno della stessa rete locale (LAN).
Gli switch di rete usano i MAC address per consegnare i pacchetti fisici (Frame) alla porta
corretta.
• Analogia: È come il numero di telaio di un'automobile o il codice fiscale di una persona: non
cambia (teoricamente) mai, indipendentemente da dove ci si trovi.

1.2 Indirizzo IP (Indirizzo Logico)
L'Internet Protocol (IP) address è un'etichetta numerica assegnata dinamicamente o staticamente a un
dispositivo connesso a una rete informatica.
• Livello OSI: Lavora al Livello 3 (Network).
• Formato (IPv4): 32 bit, espresso in 4 numeri decimali (ottetti) separati da punti, che vanno da
0 a 255 (es. 192.168.1.50).
• Funzione: Viene utilizzato per il routing, ovvero per far viaggiare i pacchetti (Datagrammi) tra
reti diverse (es. da casa tua a un server di Google).
• Analogia: È come il tuo indirizzo di residenza (Via, CAP, Città). Cambia se ti trasferisci in
un'altra rete.

2. Host Configuration: I tre pilastri
Affinché un computer possa navigare in Internet o comunicare in una rete complessa, deve avere tre
parametri fondamentali configurati correttamente: Indirizzo IP, Subnet Mask e Default Gateway.

2.1 Indirizzo IP
Identifica in modo univoco l'host all'interno della sua rete attuale.

2.2 Subnet Mask (Maschera di Sottorete)
L'indirizzo IP da solo non basta. Il computer deve sapere "quanto è grande" la sua rete locale per capire
se il destinatario di un messaggio è un suo vicino di casa o se vive in un'altra città. La Subnet Mask
divide l'indirizzo IP in due parti:
1. Network ID: Identifica la rete.
2. Host ID: Identifica lo specifico dispositivo in quella rete.
• Notazione Decimale: 255.255.255.0
• Notazione CIDR (Moderna): /24 (indica che i primi 24 bit dell'IP sono bloccati per la rete).

2.3 Default Gateway (Gateway Predefinito)
È l'indirizzo IP del Router. Quando un computer capisce (grazie alla Subnet Mask) che l'indirizzo IP di
destinazione non si trova nella sua rete locale (es. stai cercando di contattare l'IP 8.8.8.8 di Google),
invia il pacchetto al Default Gateway. Il router si prenderà in carico il compito di trovare la strada
(routing) verso Internet.

3. Come avviene la comunicazione?
Ecco il flusso logico quando il Computer A (es. 192.168.1.10) vuole parlare con il Computer B:
Caso 1: Comunicazione Locale (B è nella stessa rete, es. 192.168.1.20)
1. A confronta il suo IP e la sua Subnet Mask con l'IP di B. Capisce che B è nella sua stessa rete.
2. A ha bisogno del MAC Address di B per inviare il pacchetto tramite lo Switch.
3. A usa il protocollo ARP (Address Resolution Protocol) per "urlare" nella rete: "Chi ha l'IP
192.168.1.20? Dimmi il tuo MAC!"
4. B risponde con il suo MAC Address.
5. La comunicazione fisica (Layer 2) avviene direttamente.
Caso 2: Comunicazione Remota (B è su Internet, es. 8.8.8.8)
1. A confronta le reti e capisce che B è fuori dalla sua LAN.

2. A ignora il MAC Address di B. Impacchetta il messaggio e chiede (tramite ARP) il MAC
Address del proprio Default Gateway (il router).
3. A invia il pacchetto al Router.
4. Il Router analizza l'IP di destinazione (8.8.8.8) e lo inoltra al router successivo, passando di
nodo in nodo fino alla destinazione finale.

4. Strumenti di Networking in Linux (CLI)
Storicamente si utilizzava il comando ifconfig, ma oggi lo standard moderno in Linux è la suite
iproute2, gestita tramite il comando ip.

4.1 Verificare la configurazione (IP e MAC)
Per vedere tutte le interfacce di rete (NIC) e i relativi indirizzi IP e MAC:
Bash
ip addr show

(Oppure la forma abbreviata: ip a)
• lo (Loopback): Interfaccia virtuale interna (indirizzo 127.0.0.1). Serve al computer per
parlare con se stesso.
• eth0, ens33, enp0s3: Nomi tipici delle schede di rete fisiche o virtuali (Ethernet). Qui
troverai il tuo IP (indicato dopo la parola inet) e il tuo MAC address (indicato dopo
link/ether).

4.2 Verificare il Default Gateway (Tabella di Routing)
Per scoprire qual è l'IP del router che ti fornisce accesso a Internet:
Bash
ip route

(Cerca la riga che inizia con default via [Indirizzo IP]).

4.3 Testare la Connettività
Il comando principale per verificare se un host è raggiungibile è ping, che usa il protocollo ICMP per
inviare una richiesta "Echo" e attendere una risposta.
Bash
ping 8.8.8.8

(Su Linux il ping continua all'infinito. Premi CTRL+C per fermarlo e leggere le statistiche di perdita
pacchetti).

4.4 Risoluzione dei Nomi (DNS Base)
Noi umani ricordiamo i nomi (es. google.com), non gli IP. Quando digiti un nome, Linux deve
tradurlo in un IP.
1. DNS Esterno: La traduzione avviene tramite server specializzati configurati (storicamente) nel
file /etc/resolv.conf.
2. Risoluzione Locale: Prima di interrogare Internet, Linux controlla un file locale chiamato
/etc/hosts. Questo file permette al SysAdmin di forzare manualmente la traduzione di un
nome in un IP specifico, aggirando il DNS. È utilissimo in fase di sviluppo.
Per vedere o modificare le risoluzioni locali:
Bash
sudo nano /etc/hosts

Sintassi: [Indirizzo IP] [Nome Host] (es. 192.168.1.50 server-database)

5. Livello Applicativo: IP, Porte e Servizi
Abbiamo visto che l'indirizzo IP porta il pacchetto fino al computer corretto. Ma una volta dentro, a
quale programma è destinato? Al server web? Al server di posta? Qui entrano in gioco le Porte (Ports)
(Livello 4 - Trasporto).
• Indirizzo IP: È l'indirizzo del palazzo.
• Porta: È il numero dell'interno (l'appartamento) dove risiede uno specifico servizio.
Le porte vanno da 1 a 65535. Alcune sono standardizzate (Well-Known Ports):
• 80 (HTTP): Traffico web in chiaro.
• 443 (HTTPS): Traffico web criptato.
• 22 (SSH): Accesso remoto sicuro al terminale.

6. Laboratorio Pratico: Il Web Server Istantaneo (Python)
Obiettivo: Dimostrare come un'applicazione si mette in "ascolto" (bind) su un IP e una Porta.
Python (preinstallato su quasi tutte le distribuzioni Linux) possiede un modulo per trasformare
istantaneamente qualsiasi cartella in un sito web.
1. Crea una cartella e un file HTML di prova:

Bash
mkdir /tmp/sito_test
cd /tmp/sito_test
echo "<h1>Benvenuti nel server ITS di $(whoami)</h1>" > index.html

2. Avvia il web server Python sulla porta 8000:
Bash
python3 -m http.server 8000

3. Test dal tuo PC Host (Windows/Mac): Scopri l'IP della tua VM Linux (es. 192.168.1.50).
Apri il browser sul tuo computer reale e digita: http://192.168.1.50:8000
4. Nel terminale Linux vedrai i log (le richieste HTTP GET) apparire in tempo reale.
5. Ferma il server premendo CTRL+C.

7. I Giganti del Web: Apache vs Nginx
Per i siti in produzione non usiamo Python, ma software progettati per gestire migliaia di connessioni
simultanee in sicurezza.

7.1 Apache HTTP Server
Il server storico che ha costruito il web. È basato su processi e offre un'enorme flessibilità grazie a
moduli dinamici e al file .htaccess (che permette di sovrascrivere configurazioni a livello di
singola cartella).
• Installazione: sudo apt install apache2
• Avvio/Verifica: sudo systemctl status apache2

7.2 Nginx (Si pronuncia "Engine-X")
Moderno, leggerissimo e basato su eventi (Event-Driven). Eccelle nel servire file statici (immagini,
CSS) a velocità estreme e funziona perfettamente come Reverse Proxy (un vigile urbano che smista il
traffico a vari server interni).
• Installazione: sudo apt install nginx
• Avvio/Verifica: sudo systemctl status nginx
(Attenzione: Non possono girare entrambi contemporaneamente sulla stessa porta 80. Se ne installi
uno, fermalo prima di avviare l'altro).

8. Showcase Extra: Deploy di una WebApp (LAMP Stack +
Cache)
Dimostrazione Live per l'Istruttore: Come si assembla un'infrastruttura completa bare-metal, unendo
Networking, Gestione Pacchetti (APT) e Permessi.
Implementeremo lo stack web più famoso al mondo: WordPress, supportato da un Database
(MariaDB/MySQL) e da un sistema di Caching in RAM (Redis), tutto sulla stessa VM.

Step 1: Installazione delle dipendenze (Lo Stack)
Aggiorniamo il sistema e installiamo Apache (Web), MariaDB (DB), PHP (Logica) e Redis (Cache),
inclusi i moduli di collegamento.
Bash
sudo apt update
sudo apt install -y apache2 mariadb-server php libapache2-mod-php php-mysql redisserver php-redis wget unzip

Step 2: Configurazione del Database (MariaDB)
Dobbiamo creare un database isolato e un utente per WordPress. Accedi alla console SQL come root:
Bash
sudo mysql

Esegui le seguenti query SQL per preparare il DB:
SQL
CREATE DATABASE wordpress_db;
CREATE USER 'wp_user'@'localhost' IDENTIFIED BY 'PasswordSicura123!';
GRANT ALL PRIVILEGES ON wordpress_db.* TO 'wp_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;

Step 3: Download e Deploy dell'Applicazione
Scarichiamo WordPress ufficiale e lo posizioniamo nella "Document Root" di Apache
(/var/www/html).
Bash
cd /tmp
wget https://wordpress.org/latest.zip
unzip latest.zip

sudo mv wordpress/* /var/www/html/

Step 4: Gestione Permessi (Cruciale!)
Ricordate la Lezione 2? Apache gira sotto un utente di sistema speciale chiamato www-data. Se non
gli diamo la proprietà dei file, WordPress non potrà installare plugin o caricare immagini.
Bash
# Elimina il file di default di Apache
sudo rm /var/www/html/index.html

# Assegna la proprietà della cartella all'utente del web server
sudo chown -R www-data:www-data /var/www/html/

# Imposta i permessi corretti (755 cartelle, 644 file)
sudo find /var/www/html/ -type d -exec chmod 755 {} \;
sudo find /var/www/html/ -type f -exec chmod 644 {} \;

Step 5: Test Finale e Setup
1. Scopri l'IP della tua VM (ip a).
2. Apri il browser sul PC Host e vai su http://<IP_DELLA_VM>.
3. Apparirà la schermata di benvenuto di WordPress!
4. Inserisci i dati creati allo Step 2:
• Nome DB: wordpress_db
• Utente: wp_user
• Password: PasswordSicura123!
• Host DB: localhost
Cosa abbiamo dimostrato? Senza usare interfacce grafiche o container pre-confezionati (come
Docker), abbiamo fatto comunicare:
1. Il browser (tramite IP e Porta 80).
2. Il web server (Apache), che ha passato il codice a PHP.
3. PHP, che si è connesso sulla porta interna 3306 a MariaDB per salvare i dati.
4. (Dietro le quinte) Redis è pronto sulla porta 6379 per memorizzare in RAM le query più
frequenti, alleggerendo il database.

