Test Finale: Introduzione a Linux
Nome e Cognome: _____________________________________________________
Data: ___________________

Punteggio: _____/20

1. Qual è la differenza tecnica tra "Linux" e una "Distribuzione" (es. Ubuntu)?
A. Linux è il sistema operativo completo, la distribuzione è solo l'interfaccia grafica.
B. Linux è il Kernel (il cuore che gestisce l'hardware), la distribuzione è il pacchetto completo di
software e strumenti.
C. Sono sinonimi, indicano la stessa cosa.
D. Linux è un software a pagamento, le distribuzioni sono sempre gratuite.
2. Quale comando utilizzi per visualizzare il percorso completo della directory in cui ti trovi (es.
/home/student)?
A. ls
B. cd
C. pwd
D. whoami
3. Devi rinominare il file bozza.txt in finale.txt. Quale comando utilizzi?
A. rn bozza.txt finale.txt
B. cp bozza.txt finale.txt
C. mv bozza.txt finale.txt
D. rm bozza.txt finale.txt
4. In un ambiente di virtualizzazione, cos'è l'"Hypervisor"?
A. Il sistema operativo installato dentro la macchina virtuale.
B. Il software che crea e gestisce le macchine virtuali (es. VirtualBox).
C. Un virus che colpisce solo i sistemi Linux.
D. L'amministratore di sistema con privilegi elevati.
5. Cosa succede se esegui cd ..?
A. Ti sposti nella directory Home dell'utente.

B. Cancelli la directory corrente.
C. Ti sposti nella directory di livello superiore (cartella genitore).
D. Il sistema ti chiede di confermare l'uscita dal terminale.
6. Secondo lo standard FHS, quale directory contiene i file di configurazione del sistema?
A. /bin
B. /home
C. /var
D. /etc
7. Cosa esegue esattamente il comando sudo apt update?
A. Aggiorna tutti i programmi installati all'ultima versione.
B. Scarica l'elenco aggiornato dei pacchetti dai repository (aggiorna l'indice).
C. Aggiorna il Kernel di Linux.
D. Rimuove i pacchetti non più necessari.
8. Analizzando i permessi drwxr-xr--, quali diritti hanno gli "Altri" (Others)?
A. Lettura ed Esecuzione.
B. Scrittura ed Esecuzione.
C. Sola Lettura.
D. Nessun permesso.
9. Vuoi assegnare permessi completi (rwx) al proprietario e solo lettura/esecuzione (r-x) a tutti gli
altri. Qual è il comando corretto (supponi il file abbia I seguenti permessi “r--r--r--”?
A. chmod u+wx,o+x,g+x file
B. chmod u+x,o-wrx,g-x file
C. chmod addx file
D. chmod default file
10. Qual è il file che contiene la lista degli utenti del sistema?
A. /etc/shadow
B. /etc/passwd

C. /etc/users
D. /home/list.txt
11. Come viene identificata la seconda partizione del primo disco SATA in Linux?
A. /dev/hda2
B. /dev/sdb1
C. D:\
D. /dev/sda2
12. Quale file devi modificare per rendere permanente il mount di un disco al riavvio del sistema?
A. /etc/mount
B. /etc/fstab
C. /dev/disk
D. /etc/modules
13. Prima di utilizzare una nuova partizione per salvarci dei dati, quale operazione è
obbligatoria?
A. Copiarci dentro un file di testo.
B. Creare un File System (Formattazione), ad esempio con mkfs.ext4.
C. Riavviare la macchina virtuale.
D. Installare il driver del disco.
14. Cos'è un "Backup Incrementale"?
A. Una copia completa di tutti i dati, fatta ogni giorno.
B. Una copia solo dei file modificati rispetto all'ultimo backup (di qualsiasi tipo).
C. Una copia che sovrascrive i dati originali.
D. Una copia dei soli file di sistema.
15. Quale comando è ideale per sincronizzare due cartelle copiando solo le differenze?
A. cp -r
B. tar -czvf
C. rsync -av
D. mv

16. Qual è il comando più moderno per visualizzare gli indirizzi IP delle interfacce di rete?
A. ipconfig
B. ifconfig
C. ip addr show (o ip a)
D. netstat
17. A quale livello opera un indirizzo MAC?
A. Livello 3 (IP / Routing).
B. Livello 2 (Fisico / Data Link – Switch).
C. Livello 4 (Porte / Trasporto).
D. Livello 7 (Applicazione).
18. Vuoi associare manualmente il nome server-test all'IP 192.168.1.50 senza usare un
DNS esterno. Quale file modifichi?
A. /etc/resolv.conf
B. /etc/hosts
C. /etc/network/interfaces
D. /etc/hostname
19. Qual è la porta standard per il traffico Web non criptato (HTTP)?
A. 22
B.443
C. 80
D. 8080
20. Qual è l'indirizzo IP di "Loopback" (che identifica sempre il computer stesso)?
A. 192.168.1.1
B. 127.0.0.1
C. 0.0.0.0
D. 10.0.0.1

Domanda Risposta Argomento Note Rapide
1

B

Intro

Kernel vs Distro

2

C

CLI

pwd = Print Working Directory

3

C

CLI

mv sposta o rinomina

4

B

Virt

Hypervisor gestisce le VM

5

C

CLI

.. = Directory genitore

6

D

Admin

/etc = Editable Text Config

7

B

APT

update aggiorna solo la lista

8

C

Permessi

r-- = Solo lettura (4)

9

A

Permessi

chmod u+wx,o+x,g+x

10

B

Utenti

passwd contiene gli utenti, shadow le psw

11

D

Storage

sda=Disco 1, 2=Partizione 2

12

B

Storage

fstab = Filesystem Table

13

B

Storage

Senza Filesystem non scrivi dati

14

B

Backup

Risparmia spazio e tempo

15

C

Backup

rsync è standard per sync differenziale

16

C

Network

ip sostituisce ifconfig

17

B

Network

MAC è indirizzo fisico (L2)

18

B

Network

/etc/hosts è il DNS locale

19

C

Network

80=HTTP, 443=HTTPS, 22=SSH

20

B

Network

Localhost standard

