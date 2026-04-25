Dispensa ITS: Storage Management & Backup
Strategies
Modulo: Linux System Administration - Lezione 3
Obiettivo: Gestire dischi, partizioni, file system e implementare strategie di backup sicure.

1. Architettura dello Storage in Linux
A differenza di Windows, che assegna lettere di unità (C:, D:), Linux gestisce i dispositivi di
archiviazione come file speciali situati nella directory /dev.
+1

1.1 Naming Convention (Nomenclatura)
Il Kernel assegna i nomi in base al tipo di interfaccia:
Nome Device
/dev/sdX
/dev/sdXN

Descrizione
SATA/SCSI/USB Device. La 'X' è una lettera
progressiva (a, b, c...).
Partizione. La 'N' è un numero.

/dev/
NVMe SSD. Dischi moderni ad alta velocità.
nvme0n1
/dev/sr0
CD/DVD ROM.
Esporta in Fogli

Esempio
/dev/sda (1° disco), /dev/sdb
(2° disco)
/dev/sda1 (1ª partizione del 1°
disco)
/dev/nvme0n1p1 (Partizione 1)
-

2. Guida Pratica: Aggiungere un Disco in VirtualBox
Prima di poter partizionare un disco, dobbiamo collegarlo fisicamente (o virtualmente) alla macchina.
Ecco la procedura passo-passo per simulare l'inserimento di un secondo Hard Disk (HDD) nella vostra
VM Ubuntu.
Procedura (A VM Spenta):
1. Apri VirtualBox e seleziona la tua VM Ubuntu dalla lista a sinistra.
2. Clicca su Impostazioni (Settings) -> Archiviazione (Storage).
3. Nell'albero "Dispositivi di archiviazione", seleziona il Controller: SATA.
4. Clicca sull'icona "Aggiunge disco rigido" (quella con il + verde sopra l'icona del disco, non
quella del CD).

5. Nella finestra che si apre, clicca su Crea (Create).
6. Tipo di file: Seleziona VDI (VirtualBox Disk Image) -> Avanti.
7. Archiviazione: Seleziona Allocato dinamicamente (Occupa spazio solo se lo riempi) ->
Avanti.
8. Nome e Dimensione:
• Nome: Disco_Dati (o simile).
• Dimensione: 5 GB (sufficienti per l'esercizio).
9. Clicca su Fine.
10.Ora vedrai il nuovo disco nella lista "Not Attached". Selezionalo e clicca su Scegli (Choose).
11.Clicca OK per chiudere le impostazioni e avvia la VM.
Verifica in Linux: Una volta avviata la VM, apri il terminale e digita:
Bash
lsblk

Dovresti vedere un nuovo dispositivo (probabilmente sdb) di circa 5GB senza partizioni sotto di esso.

3. Partizionamento e File System
Un disco grezzo non è utilizzabile. Deve essere partizionato e formattato.

3.1 MBR vs GPT
Esistono due standard per la tabella delle partizioni:
Caratteristica
MBR (Master Boot Record)
GPT (GUID Partition Table)
Limite Dimensione Max 2 TB
Fino a 9.4 Zettabyte (praticamente illimitato)
Partizioni
Max 4 Primarie
Fino a 128 partizioni
Robustezza
Singola copia all'inizio del disco Copia di backup alla fine del disco
Utilizzo
Legacy / BIOS vecchi
Standard moderno / UEFI
Esporta in Fogli

3.2 Strumenti di Partizionamento
Utilizzeremo fdisk (più comune per script/MBR) o cfdisk (interfaccia grafica testuale, più
semplice).
Esempio con fdisk (su /dev/sdb):
Bash

sudo fdisk /dev/sdb

• m: Mostra il menu di aiuto.
• n: Nuova partizione.
• p: Primaria.
• w: Scrivi le modifiche ed esci.

3.3 Formattazione (Creazione File System)
Dopo aver creato la partizione (es. /dev/sdb1), dobbiamo decidere "come" scriverci i dati. Linux
usa principalmente ext4 (Fourth Extended Filesystem).
Comando per formattare:
Bash
sudo mkfs.ext4 /dev/sdb1

Attenzione: mkfs cancella irreversibilmente tutti i dati nella partizione specificata!

4. Mounting: Accedere ai Dati
In Linux, per accedere a un disco formattato, devi "montarlo" su una cartella esistente.

4.1 Mount Temporaneo
1. Crea il punto di mount (una cartella vuota):
Bash
sudo mkdir /mnt/dati

2. Collega la partizione alla cartella:
Bash
sudo mount /dev/sdb1 /mnt/dati

3. Verifica:
Bash
df -h

Nota: Al riavvio, questo collegamento andrà perso.

4.2 Mount Permanente (/etc/fstab)
Per rendere il mount automatico all'avvio, dobbiamo modificare il file /etc/fstab.

1. Ottieni l'UUID (codice univoco) del disco (è più sicuro usare l'UUID che il nome /dev/sdb1,
perché i nomi possono cambiare se sposti i cavi):
Bash
sudo blkid

Copia la stringa UUID relativa a /dev/sdb1.
2. Modifica il file fstab:
Bash
sudo nano /etc/fstab

3. Aggiungi una riga alla fine con questa sintassi: [Device] [Mount Point]
[Filesystem] [Options] [Dump] [Pass]
Esempio:
Plaintext
UUID=1234-5678-abcd

/mnt/dati

ext4

defaults

0

2

ATTENZIONE: Un errore di sintassi in /etc/fstab può impedire l'avvio del sistema.
Verificare sempre con sudo mount -a prima di riavviare.

5. Strategie di Backup
Il backup non è solo "copiare file", ma pianificare il recupero (Restore).
5.1 Tipologie di Backup
Tipo

Descrizione
Copia completa di tutti i
Full
dati selezionati.
Copia solo i dati
modificati dall'ultimo
Incrementale
backup (di qualsiasi
tipo).
Copia i dati modificati
Differenziale
dall'ultimo Full Backup.
Esporta in Fogli

Pro (Vantaggi)
Contro (Svantaggi)
Restore velocissimo (basta Lento da eseguire, occupa
l'ultimo file).
tantissimo spazio.
Restore lento e complesso (serve
Backup rapidissimo, poco
il Full + tutti gli incrementali
spazio occupato.
successivi).
Via di mezzo. Restore più Occupa progressivamente più
veloce dell'incrementale. spazio dell'incrementale.

5.2 La Regola del 3-2-1
La strategia standard industriale per la sicurezza dei dati:
1. Mantenere 3 copie dei dati (1 originale + 2 backup).

2. Salvare su 2 tipi di supporto diversi (es. Disco locale + NAS, oppure Disco + Cloud).
3. Conservare 1 copia Off-site (fuori sede, per proteggersi da incendi/furti fisici).

6. Strumenti di Backup Linux
6.1 Tar (Tape Archive)
Storico strumento per impacchettare file. Utile per backup completi (Full) o archiviazione "a freddo".
• Creare un archivio compresso (gzip):
Bash
tar -czvf backup_home.tar.gz /home/studente

• -c: Create
• -z: Gzip compression
• -v: Verbose (mostra i file)
• -f: File (nome del file di output)
• Estrarre (Restore):
Bash
tar -xzvf backup_home.tar.gz -C /tmp/restore

6.2 Rsync (Remote Sync)
Lo strumento più potente per backup incrementali e sincronizzazione. Copia solo i "delta" (le
differenze), risparmiando banda e tempo.
• Sintassi base:
Bash
rsync -av /sorgente /destinazione

• -a (Archive): Mantiene permessi, date, link simbolici, utenti (ricorsivo).
• -v (Verbose): Mostra dettagli.
• Backup speculare (Mirroring):
Bash
rsync -av --delete /home/studente/progetti /mnt/backup/

• --delete: Attenzione! Cancella nella destinazione i file che non esistono più nella
sorgente. Crea una copia esatta 1:1.

