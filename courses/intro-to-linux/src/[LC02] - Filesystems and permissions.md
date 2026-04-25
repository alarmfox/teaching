Dispensa Tecnica: Amministrazione di Sistema
Linux (Modulo 1)
Corso: ITS Introduzione a Linux
Argomento: Filesystem Hierarchy Standard, Gestione Utenti, Permessi e Package Management.
Prerequisiti: Concetti base di Sistemi Operativi (Kernel, Shell, Processi).

1. Filesystem Hierarchy Standard (FHS)
A differenza dei sistemi Windows, che utilizzano lettere di unità (C:\, D:\) per identificare partizioni
e dischi, Linux adotta una struttura a singolo albero invertito. Tutto il sistema parte dalla directory
radice, indicata con / (Root).
Ogni dispositivo hardware, processo attivo o partizione è rappresentato come un file o una directory
all'interno di questo albero.

1.1 Directory Critiche di Sistema
La struttura delle directory è definita dallo standard FHS (Filesystem Hierarchy Standard). Ecco le
directory che un SysAdmin deve conoscere:
Directory
/
/bin &
/sbin
/etc
/home
/root
/var
/dev
/proc
/tmp

Contenuto e Funzione

Note Tecniche
Contiene solo le directory essenziali
Root. Il punto di montaggio primario.
per il boot.
Binaries. Eseguibili essenziali (es. ls, cp, /sbin contiene binari riservati a
ip).
root (es. fdisk).
Configuration. File di configurazione di
Mnemonico: Editable Text
sistema e applicazioni.
Configuration. Mai binari qui.
Ogni utente ha la sua (es.
Directory personali degli utenti standard.
/home/student).
Home directory dell'utente amministratore Separata da /home per garantire
(Root).
accesso in emergenza.
Variable. Dati che cambiano dimensione Critica per il monitoraggio
(/var/log).
nel tempo (Log, Spool, Cache).
Es. /dev/sda (disco), /dev/null
Devices. File speciali che puntano
all'hardware.
(bit bucket).
Process. Filesystem virtuale creato in RAMContiene info sui processi attivi (es.
/proc/cpuinfo).
dal Kernel.
Viene svuotata automaticamente al
Temporary. File volatili.
riavvio.

Nota Architetturale: In Linux, "montare" (mount) un dispositivo significa agganciare il
filesystem del dispositivo a una directory esistente dell'albero principale.

2. Editor di Testo (CLI)
In ambiente server (spesso headless, senza monitor), la modifica dei file di configurazione in /etc
avviene esclusivamente tramite terminale.

2.1 GNU Nano
Editor semplice e intuitivo, standard su molte distro.
• Sintassi: nano [percorso_file]
• Comandi: I comandi utilizzano il tasto CTRL (indicato come ^).
• ^O (Write Out): Salva le modifiche.
• ^X (Exit): Chiude l'editor.
• ^W (Where Is): Cerca nel testo.

2.2 Vi / Vim (Vi IMproved)
Editor modale, standard de facto per amministratori Unix/Linux. Opera in diverse modalità:
1. Command Mode (Default): I tasti eseguono comandi (copia, incolla, naviga).
2. Insert Mode: Si digita il testo (attivata premendo i).
3. Ex Mode: Comandi di salvataggio/uscita (attivata premendo :).
Comandi di sopravvivenza Vim:
• i : Entra in modalità inserimento.
• ESC : Torna in modalità comando.
• :w : Salva (Write).
• :q! : Esci senza salvare (Quit Force).
• :wq : Salva ed esci.

3. Gestione Utenti e Autenticazione
Linux è un sistema nativamente multi-utente. La gestione degli accessi si basa su UID (User ID) e
GID (Group ID).

3.1 Tipi di Utenti
• Root (UID 0): Il Superuser. Ha accesso illimitato a ogni risorsa. Ignora i permessi.
• System Users (UID 1-999): Utenti non interattivi creati per eseguire servizi (es. www-data
per Apache). Non hanno shell di login.
• Standard Users (UID 1000+): Utenti umani con permessi limitati.

3.2 File di Configurazione Utenti
File

Permessi

Contenuto
/etc/passwd 644 (Read All) Database utenti:
user:x:UID:GID:Comment:Home:Shell
/etc/shadow 640 (Root
Hash delle password e policy di scadenza.
Read)
/etc/group 644 (Read All) Definizione dei gruppi e membri.

3.3 SUDO (SuperUser DO)
Il comando sudo permette a un utente autorizzato (nel gruppo sudo o wheel) di elevare i propri
privilegi per eseguire un singolo comando come root.
• Principio di "Least Privilege": Si lavora sempre come utente standard, si diventa root solo
quando strettamente necessario.
• Audit: Ogni comando eseguito con sudo viene loggato in /var/log/auth.log.

4. Permessi e Access Control List (ACL)
Il modello di sicurezza di Linux si basa sui permessi POSIX. Ogni file possiede tre set di permessi per
tre categorie di soggetti.

4.1 La Struttura dei Permessi
Analizzando l'output di ls -l: drwxr-xr-- 2 student develop 4096 Oct 10 14:00
progetto
1. Tipo File (primo char): - (file), d (directory), l (link).

2. User (u): rwx (Il proprietario student ha pieni poteri).
3. Group (g): r-x (Il gruppo develop può leggere ed eseguire, ma non scrivere).
4. Others (o): r-- (Tutti gli altri possono solo leggere).

4.2 Notazione Simbolica vs Ottale
Permess Simbol Valore
o
o
Ottale
r
Read
4
w

2

Execute x

1

Write

Descrizione (File)

Descrizione (Directory)

Listare i file (ls).
Creare/Cancellare file nella
Modificare/Sovrascrivere.
cartella.
Eseguire come
Attraversare la cartella (cd).
programma.
Leggere il contenuto.

Esempi di calcolo ottale:
• rwx = 4 + 2 + 1 = 7
• r-x = 4 + 0 + 1 = 5
• r-- = 4 + 0 + 0 = 4
Comuni configurazioni:
• chmod 755 file (rwx r-x r-x): Script eseguibile da tutti, modificabile solo dal proprietario.
• chmod 644 file (rw- r-- r--): File di configurazione standard.
• chmod 600 file (rw- --- ---): File privato (es. chiavi SSH).

4.3 Comandi di Gestione
• chmod [modalità] [file]: Modifica i permessi (Change Mode).
• chown [utente]:[gruppo] [file]: Modifica la proprietà (Change Owner).
• Esempio: sudo chown mario:devs script.py

5. Advanced Package Tool (APT)
Nelle distribuzioni Debian-based (come Ubuntu), il software non si scarica dai siti web, ma dai
Repository ufficiali firmati digitalmente. APT gestisce automaticamente le dipendenze (librerie
necessarie).

Ciclo di vita del software
1. Aggiornamento Indici: sudo apt update Scarica l'elenco aggiornato dei pacchetti dai
repository. Non installa nulla.
2. Aggiornamento Sistema: sudo apt upgrade Confronta le versioni installate con l'elenco
scaricato e aggiorna i binari.
3. Installazione: sudo apt install [nome_pacchetto] Esempio: sudo apt
install git htop
4. Rimozione:
• sudo apt remove [pacchetto]: Rimuove il binario ma mantiene i file di
configurazione (in /etc).
• sudo apt purge [pacchetto]: Rimuove binario e configurazioni (pulizia
totale).
5. Pulizia: sudo apt autoremove Rimuove le dipendenze orfane non più necessarie.

🔗 Risorse e Riferimenti Bibliografici
• Man Pages: La documentazione primaria.
• Uso: man [comando] (es. man chmod, man hier).
• Debian Administrator's Handbook: debian-handbook.info (Testo sacro per sysadmin
Debian/Ubuntu).
• Linux Filesystem Hierarchy Standard (Official): refspecs.linuxfoundation.org.
• Explainshell: explainshell.com (Analizzatore visivo di argomenti della riga di comando).

