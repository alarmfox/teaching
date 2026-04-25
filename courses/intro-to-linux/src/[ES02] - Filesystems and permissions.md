Laboratorio Pratico - Lezione 2: Admin
Fundamentals
Durata: 60 Minuti
Obiettivo: Consolidare la gestione dei permessi, l'installazione software e l'editing dei file di sistema.

Esercizio 1: L'Esploratore del Filesystem (10 min)
Obiettivo: Navigare nelle directory di sistema critiche e capire la differenza tra file temporanei e
persistenti.
1. Spostati nella directory radice (/).
2. Elenca il contenuto. Quante cartelle vedi?
3. Entra in /var/log.
4. Cerca il file syslog o auth.log. Prova a leggerne le ultime righe usando il comando tail
syslog (o cat).
• Domanda: Riesci a leggerlo? Se no, perché? (Controlla i permessi con ls -l).
5. Spostati in /tmp.
6. Crea un file chiamato test_volante.txt e scrivici dentro "Questo file sparirà".
7. Verifica i permessi di questo file. Chi è il proprietario?

Esercizio 2: Gestione Software con APT (15 min)
Obiettivo: Installare strumenti di monitoraggio e divertimento, comprendendo il ciclo di vita dei
pacchetti.
1. Aggiornamento: Esegui il comando per aggiornare la lista dei repository (non i programmi,
solo la lista!).
2. Monitoraggio: Cerca e installa il pacchetto htop.
• Lancialo digitando htop. Osserva l'utilizzo di RAM e CPU.
• Premi F10 o q per uscire.
3. Fun & Games: Installa il pacchetto cmatrix.

• Lancialo. (Per uscire: CTRL+C o q).
4. Pulizia: Rimuovi cmatrix ma mantieni i file di configurazione.
5. Pulizia profonda: Reinstalla cmatrix e poi rimuovilo completamente (inclusi i file di
configurazione) usando l'opzione purge.
6. Igiene: Esegui il comando per rimuovere le dipendenze orfane (pacchetti non più necessari).

Esercizio 3: Il "Messaggio del Giorno" (Sudo & Nano) (15 min)
Scenario: Sei l'amministratore e vuoi lasciare un messaggio di benvenuto a chiunque si colleghi al
server. Devi modificare un file di sistema protetto.
1. Prova a modificare il file /etc/motd (Message Of The Day) usando nano /etc/motd.
• Nota: Se il file non esiste (dipende dalla versione di Ubuntu), crea/modifica
/etc/issue.net o cerca dove Ubuntu salva il motd dinamico (/etc/updatemotd.d/).
2. Prova a salvare. Cosa succede? (Dovresti ricevere un errore di "Permesso negato").
3. Esci senza salvare (CTRL+X, poi N).
4. Riapri il file usando sudo.
5. Aggiungi il testo: "BENVENUTI NEL SERVER DI [TUO NOME] - ACCESSO
MONITORATO"
6. Salva ed esci.
7. Verifica che il contenuto sia cambiato usando cat.

Esercizio 4: Il Maestro dei Permessi (20 min - Cruciale)
Obiettivo: Gestire la sicurezza dei file tramite chmod (modalità ottale e simbolica).
Scenario A: Lo script pubblico
1. Torna nella tua Home (cd ~).
2. Crea un file chiamato mio_script.sh.
3. Scrivi dentro: echo "Funziona!".
4. Prova a eseguirlo: ./mio_script.sh. (Dovrebbe darti "Permesso negato").
5. Controlla i permessi attuali con ls -l.

6. Assegna il permesso di Esecuzione al proprietario (te stesso) usando la modalità simbolica
(u+...).
7. Esegui di nuovo lo script. Ora funziona?
Scenario B: Il file Top Secret
1. Crea un file chiamato password_segrete.txt.
2. Configura i permessi in modo che:
• Tu (User) puoi leggere e scrivere.
• Il Gruppo non può fare nulla.
• Gli Altri non possono fare nulla.
• Suggerimento: Usa la notazione ottale. Qual è il numero per rw- --- ---? (4+2=6,
0, 0).
3. Verifica con ls -l.
4. Prova a leggere il file (cat).
5. Cambia utente temporaneamente (o chiedi al compagno di provare a leggerlo se siete in rete,
altrimenti prova a leggerlo con un altro utente se creato, oppure fidati di ls -l).

Esercizio 5: La "Prova del Nove" (Multi-utente)
Obiettivo: Verificare empiricamente i permessi creando un utente di test ("dummy") e provando ad
accedere ai file protetti.
Scenario: Hai protetto il file password_segrete.txt nell'esercizio precedente. Ma sei sicuro che
funzioni? Per esserne certo, creerai un finto intruso.
1. Creazione dell'Intruso: Crea un nuovo utente chiamato "dummy" (fantoccio).
• Comando: sudo adduser dummy
• Compila la password (usa qualcosa di semplice tipo 1234) e premi INVIO per saltare i
dettagli anagrafici (Nome stanza, Telefono, ecc.).
2. Preparazione del Test: Poiché la tua Home Directory (/home/tuonome) potrebbe essere
bloccata agli estranei (a seconda della configurazione di Ubuntu), copiamo il file segreto in un
"terreno neutrale" per testare solo i permessi del file.
• Copia il file in /tmp: cp password_segrete.txt /tmp/segreto.txt
• Verifica di essere ancora il proprietario del file copiato: ls -l /tmp/segreto.txt

• Assicurati che i permessi siano blindati (solo tu leggi/scrivi): chmod 600
/tmp/segreto.txt
3. Cambio d'Identità (Switch User): Ora diventa l'utente dummy.
• Comando: su - dummy
• Inserisci la password di dummy.
• Nota: Il prompt del terminale cambierà (es. da student@vm a dummy@vm). Ora non
sei più tu.
4. Il Tentativo di Furto: Come utente dummy, prova a leggere il file segreto che appartiene
all'altro utente.
• Comando: cat /tmp/segreto.txt
• Risultato atteso: Permission denied. (Se lo leggi, hai sbagliato il chmod!).
5. Ritorno alla Base: Esci dall'identità di dummy per tornare te stesso.
• Comando: exit
• Verifica di essere tornato te stesso con whoami.
6. Pulizia: Ora che il test è finito, elimina l'utente di test per non lasciare "spazzatura" nel sistema.
• Comando: sudo deluser --remove-home dummy

Challenge Finale: "Disaster Recovery" (Extra)
Scenario: Un utente ha impostato permessi sbagliati su una cartella web.
1. Crea una cartella SitoWeb.
2. Dentro crea index.html.
3. Imposta i permessi della cartella a 000 (Nessun permesso).
4. Prova a entrare nella cartella (cd SitoWeb). Cosa succede?
5. Ripristina i permessi corretti affinché:
• Il proprietario possa fare tutto (7).
• Tutti gli altri possano solo leggere ed entrare (5).

