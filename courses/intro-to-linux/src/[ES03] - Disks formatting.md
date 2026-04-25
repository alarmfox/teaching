Laboratorio Pratico Lezione 3: Storage &
Backup Management
Scenario: Sei il nuovo Junior SysAdmin della "ITS Tech Solutions". Il CTO ti ha assegnato un nuovo
server (la tua VM) a cui è stato appena collegato un nuovo disco fisico. Il tuo compito è configurarlo
per ospitare i dati aziendali e impostare un sistema di backup automatico.
Tempo stimato: 90 minuti Prerequisiti: Macchina Virtuale spenta (inizialmente).

Parte 1: Hardware Provisioning (VirtualBox)
Obiettivo: Simulare l'inserimento fisico di un disco nel server.
1. Spegni la VM se è accesa.
2. Vai su Impostazioni -> Archiviazione.
3. Seleziona il Controller: SATA.
4. Clicca sull'icona "Aggiungi disco rigido" (icona disco con il +).
5. Seleziona Crea -> VDI -> Allocato dinamicamente.
6. Imposta la dimensione a 4 GB (o 5GB). Chiamalo Disco_Dati.
7. Conferma e avvia la VM.

Parte 2: Partizionamento (fdisk/cfdisk)
Obiettivo: Suddividere il disco per scopi diversi.
1. Apri il terminale e identifica il nuovo disco:
Bash
lsblk

(Dovresti vedere un device, probabilmente sdb, da 4GB senza partizioni).
2. Lancia l'utility di partizionamento:
Bash
sudo cfdisk /dev/sdb

(Se ti chiede il tipo di etichetta, scegli gpt).
3. Crea la seguente struttura:

• Partizione 1: 2 GB (Sarà usata per i "Dati Produzione").
• Partizione 2: 2 GB (Spazio rimanente, sarà usata per i "Backup Locali").
4. Seleziona [ Write ], digita yes per confermare e poi [ Quit ].
5. Verifica che le partizioni esistano:
Bash
lsblk

(Ora dovresti vedere sdb1 e sdb2).

Parte 3: Filesystem e Formattazione
Obiettivo: Rendere le partizioni utilizzabili.
1. Formatta entrambe le partizioni con il filesystem standard ext4:
Bash
sudo mkfs.ext4 /dev/sdb1
sudo mkfs.ext4 /dev/sdb2

Parte 4: Mounting Persistente (/etc/fstab)
Obiettivo: Configurare il server affinché i dischi siano pronti ad ogni riavvio.
1. Crea i punti di mount (le cartelle vuote):
Bash
sudo mkdir -p /mnt/produzione
sudo mkdir -p /mnt/backup_drive

2. Ottieni gli UUID delle partizioni (copiali su un blocco note o tienili pronti):
Bash
sudo blkid

3. Modifica il file /etc/fstab per rendere il mount permanente:
Bash
sudo nano /etc/fstab

4. Aggiungi in fondo al file queste due righe (sostituisci TUO_UUID_... con i codici reali):
Plaintext

# Mount point Dati Produzione
UUID=inserisci-uuid-sdb1

/mnt/produzione

ext4

defaults

0

2

/mnt/backup_drive

ext4

defaults

0

2

# Mount point Backup
UUID=inserisci-uuid-sdb2

5. TEST CRUCIALE: Prima di riavviare, verifica che non ci siano errori!
Bash
sudo mount -a

(Se il comando non restituisce output, è andato tutto bene. Se dà errore, correggi fstab o la VM
non partirà).
6. Verifica che siano montati:
Bash
df -h

7. Gestione Permessi: Di default, root possiede queste cartelle. Assegnale al tuo utente:
Bash
sudo chown -R $USER:$USER /mnt/produzione
sudo chown -R $USER:$USER /mnt/backup_drive

Parte 5: Simulazione Dati e Backup "Cold" (TAR)
Obiettivo: Creare un archivio compresso di salvataggio.
1. Generazione Dati: Crea una struttura di file finti in produzione:
Bash
mkdir /mnt/produzione/progetto_web
echo "Codice importante" > /mnt/produzione/progetto_web/index.html
echo "Configurazione segreta" > /mnt/produzione/progetto_web/config.php

2. Esecuzione Backup (Full): Crea un archivio .tar.gz di tutto il progetto e salvalo nel disco
di backup.
Bash
tar -czvf /mnt/backup_drive/backup_full_v1.tar.gz
/mnt/produzione/progetto_web

3. Simulazione Disastro: Un utente distratto cancella tutto!

Bash
rm -rf /mnt/produzione/progetto_web

4. Restore (Ripristino): Recupera i dati dall'archivio.
Bash
# Attenzione alla posizione: tar scompatta dove gli dici o nel percorso
assoluto se registrato
tar -xzvf /mnt/backup_drive/backup_full_v1.tar.gz -C /

(Nota: Abbiamo usato -C / perché il tar è stato creato con percorsi assoluti. Verifica se i file
sono tornati in /mnt/produzione).

Parte 6: Backup Incrementale e Sync (RSYNC)
Obiettivo: Mantenere una copia speculare (mirror) sempre aggiornata.
1. Crea una cartella per il mirror sul disco di backup:
Bash
mkdir /mnt/backup_drive/mirror_giornaliero

2. Lancia la prima sincronizzazione:
Bash
rsync -av /mnt/produzione/ /mnt/backup_drive/mirror_giornaliero/

(Nota lo slash finale / dopo produzione: significa "il contenuto di", non la cartella stessa).
3. Modifica Dati: Aggiungi un nuovo file in produzione.
Bash
touch /mnt/produzione/progetto_web/nuovo_file.txt

4. Sync Incrementale: Rilancia lo stesso comando rsync di prima.
• Osserva l'output: copierà solo nuovo_file.txt. Non ricopia tutto il resto. Questo è
il vantaggio di rsync!

Challenge Finale (Per chi finisce prima)
Obiettivo: Automatizzare il backup con Cron.
Configura il sistema affinché esegua il comando rsync (quello della Parte 6) automaticamente ogni
minuto (solo per test didattico).

1. Apri il crontab: crontab -e
2. Aggiungi la riga magica (cerca su Google "Crontab every minute syntax" se non la ricordi): *
* * * * rsync -av /mnt/produzione/
/mnt/backup_drive/mirror_giornaliero/ >> /tmp/backup.log
3. Crea un file in produzione, aspetta 60 secondi e controlla se appare magicamente nel backup.

Troubleshooting Rapido
• Errore "Permission Denied": Hai dimenticato il sudo chown nella Parte 4. Le cartelle
montate appartengono a root finché non le cambi.
• Errore "Device is busy" (quando smonti): Sei ancora dentro la cartella col terminale. Fai cd
~ e riprova.
• La VM va in Emergency Mode al riavvio: Hai sbagliato l'UUID in /etc/fstab.
• Soluzione: Inserisci la password di root, dai nano /etc/fstab, commenta (metti #)
davanti alle righe aggiunte, salva e riavvia. Poi riprova con calma.

