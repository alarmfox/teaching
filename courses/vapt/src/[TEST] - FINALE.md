Nome e Cognome: _____________________________________________________
Data: ___________________

Punteggio: _____/20

1. Qual è l'obiettivo principale della Binary Exploitation?
A) Alterare il codice sorgente originale del programma
B) Aggiornare le difese del sistema operativo
C) Manipolare il flusso di esecuzione tramite input malformati per ottenere l'Arbitrary Code
Execution
D) Crittografare i file sensibili sul server bersaglio
2. Nella memoria virtuale di un processo, quale area è specificamente dedicata all'allocazione
dinamica (ad esempio quando si utilizzano funzioni come malloc())?
A) Stack
B) Heap
C) Text
D) BSS
3. Per quale motivo strutturale il linguaggio C è particolarmente esposto alla vulnerabilità di
Buffer Overflow?
A) Perché la memoria viene gestita da un Garbage Collector troppo lento
B) Perché non effettua alcun controllo automatico dei limiti (bounds checking) sulle allocazioni
C) Perché richiede permessi di root per ogni esecuzione
D) Perché non supporta l'utilizzo dei registri della CPU
4. Qual è la dimensione standard di un Indirizzo Fisico (MAC Address)?
A) 32 bit
B) 48 bit
C) 64 bit
D) 128 bit
5. Come si comporta uno switch di rete quando riceve un frame con un MAC Address di
destinazione non presente nella sua tabella (Unknown Unicast)?
A) Scarta immediatamente il frame per sicurezza
B) Rimanda il frame al mittente con un messaggio di errore

Nome e Cognome: _____________________________________________________
Data: ___________________

Punteggio: _____/20

C) Effettua il Flooding, inoltrando il frame su tutte le porte attive tranne quella di origine
D) Mette il frame in coda aspettando che il destinatario si presenti
6. Quale debolezza architetturale fondamentale del protocollo ARP viene sfruttata nell'attacco di
ARP Spoofing?
A) La mancanza di qualsiasi meccanismo di autenticazione per i messaggi inviati
B) L'uso di chiavi crittografiche deboli a 56-bit
C) La lentezza intrinseca nella propagazione dei pacchetti broadcast
D) La frammentazione dei pacchetti a livello 3
7. Qual è uno dei principali impatti di un attacco di ARP Spoofing (o Poisoning) riuscito?
A) La corruzione del firmware del router
B) L'esecuzione di uno shellcode remoto
C) L'intercettazione del traffico tramite una posizione di Man-in-the-Middle (MitM)
D) La cancellazione della MAC Address Table dello switch
8. Cosa può accadere se un attaccante riesce a sovrascrivere illegalmente il "Return Address"
salvato nello Stack?
A) Il sistema formatta automaticamente la memoria per prevenire danni
B) L'attaccante può deviare il flusso del programma verso un indirizzo di sua scelta
C) Il router isola l'host compromesso dalla rete
D) Il programma viene ricompilato in modalità sicura
9. In ambito di Network Security, quale intervento rappresenta una "mitigazione operativa"
(seppur non scalabile) contro l'ARP Spoofing?
A) L'uso di cavi schermati
B) L'impostazione manuale di Tabelle ARP Statiche sugli host critici
C) Il riavvio periodico dello switch
D) La disabilitazione della porta 80

Nome e Cognome: _____________________________________________________
Data: ___________________

Punteggio: _____/20

10. In ambito di Network Security, in cosa cosa consiste la Dynamic ARP Inspection? ?
A) Bloccare l’ARP per permettere alla rete di funzionare solo a livello 3
B) Riconoscere il MAC address del gateway dinamicamente
C) Utilizzo di richieste DHCP snooping per mantenere associazione tra MAC-Address e IP address
D) Abilitare la comunicazione tra host wireless e wired
11. Cos'è un attacco di tipo "Rogue DHCP"?
A) Un server DHCP legittimo che esaurisce improvvisamente gli indirizzi IP disponibili
B) Un malware che disabilita il servizio DHCP sul router principale dell'azienda
C) L'introduzione nella rete di un server DHCP non autorizzato, che assegna configurazioni IP
malevole (es. gateway e DNS errati) agli ignari client
D) Una tecnica crittografica per nascondere il traffico DHCP agli sniffer di rete
12. Qual è l'obiettivo primario di un attacco di "DHCP Starvation"?
A) Bloccare la porta 80 del server web aziendale
B) Esaurire tutti gli indirizzi IP disponibili nel pool del server DHCP legittimo inviando continue e
false richieste di assegnazione
C) Rubare le password di amministratore memorizzate nel server DHCP
D) Forzare il server DHCP a fare il downgrade del protocollo alla versione precedente
13. Come funziona tipicamente un attacco di "DNS Spoofing" (o DNS Poisoning) all'interno di
una rete locale?
A) Inviando milioni di pacchetti ICMP (ping) al server DNS per farlo crashare
B) Sfruttando un Buffer Overflow nel browser della vittima
C) Rispondendo alle richieste DNS della vittima con indirizzi IP falsificati, reindirizzando così il suo
traffico web verso un server controllato dall'attaccante
D) Cancellando fisicamente il file hosts sul computer del bersaglio
14. Durante l'analisi di un'applicazione web, qual è lo scopo principale dell'utilizzo di un tool
come FFUF per la "Directory e Domain Enumeration"?
A) Decifrare le password degli utenti tramite un attacco a forza bruta sul form di login

Nome e Cognome: _____________________________________________________
Data: ___________________

Punteggio: _____/20

B) Scoprire cartelle, file nascosti o sottodomini non pubblici sul server web inviando rapidamente
migliaia di richieste automatizzate basate su un dizionario
C) Intercettare in chiaro il traffico di rete tra il client e il server web
D) Eseguire comandi di amministrazione direttamente sul database del sito
15. Quale delle seguenti definizioni descrive meglio una vulnerabilità di "SQL Injection" (SQLi)?
A) L'inserimento di input utente non filtrato all'interno di una query diretta al database, che
permette all'attaccante di manipolare la richiesta o estrarre dati sensibili
B) L'inserimento di codice JavaScript maligno che verrà eseguito nel browser degli altri visitatori
del sito
C) Un difetto di configurazione del server web che permette l'accesso alle cartelle senza password
D) Un attacco DoS (Denial of Service) che satura la banda di rete del server database
16. In ambito di Penetration Testing, qual è la caratteristica distintiva di una "Reverse Shell"
rispetto a una shell tradizionale (Bind Shell)?
A) La Reverse Shell è un'interfaccia grafica, mentre la Bind Shell è solo a riga di comando
B) La Reverse Shell si può utilizzare solo su sistemi operativi Linux
C) Nella Reverse Shell è il sistema vittima (compromesso) che avvia attivamente la connessione
verso l'indirizzo IP della macchina dell'attaccante in ascolto
D) La Reverse Shell richiede sempre l'inserimento di una password di root
17. In un MAC Address, a cosa servono i primi 24 bit (chiamati OUI)?
A) A identificare univocamente la singola scheda di rete prodotta
B) A stabilire la classe dell'indirizzo IP associato
C) A identificare il vendor (produttore) dell'interfaccia di rete
D) A determinare la priorità del traffico VLAN
18. Nella segmentazione della memoria di un processo, cosa contiene la sezione "Text" (o
Code)?
A) I file di testo aperti dall'utente
B) L'allocazione dinamica degli oggetti
C) Le istruzioni macchina eseguibili del programma, tipicamente in sola lettura
D) I messaggi di errore del compilatore

Nome e Cognome: _____________________________________________________
Data: ___________________

Punteggio: _____/20

19. Qual è lo scopo primario del protocollo ARP (Address Resolution Protocol)?
A) Risolvere i nomi a dominio nel corrispondente indirizzo IP
B) Assegnare un indirizzo IP dinamico a un nuovo host
C) Crittografare la comunicazione locale tra due switch
D) Conoscere il MAC Address di una macchina di cui si conosce già l'indirizzo
20. Nei processori con architettura x86 a 32-bit, qual è il registro critico che contiene l'indirizzo di
memoria della prossima istruzione che la CPU dovrà eseguire?
A) EAX
B) EBP
C) ESP
D) EIP

