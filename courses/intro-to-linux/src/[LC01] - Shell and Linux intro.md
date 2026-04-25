Introduzione all'Ambiente Linux
Modulo: Sistemi Operativi Linux – Lezione 1
Obiettivo: Analisi dell'architettura Linux, configurazione dell'ambiente di virtualizzazione e
interazione con la Shell.

1. Architettura del Sistema
Quando si parla di "Linux" in ambito tecnico, è necessario fare una distinzione tra il Kernel e il sistema
operativo completo.

1.1 Il Kernel Linux
Linux è un Kernel monolitico open source (GPLv2), creato inizialmente da Linus Torvalds nel 1991. Il
Kernel è il componente centrale del sistema operativo che risiede in memoria ed è responsabile
dell'interfaccia tra l'hardware della macchina e il software applicativo.
Le sue funzioni primarie includono:
• Process Management: Scheduling dei processi e gestione del multitasking.
• Memory Management: Gestione della RAM, paginazione e memoria virtuale.
• Hardware Abstraction: Fornitura di driver per interagire con le periferiche (I/O).
• System Calls: Interfaccia che permette ai programmi in User Space di richiedere servizi al
Kernel.

1.2 GNU/Linux (User Space)
Un Kernel da solo non è utilizzabile dall'utente finale. Il sistema operativo completo è costituito
dall'unione del Kernel Linux con il software di sistema del progetto GNU (GNU's Not Unix), che
fornisce librerie, compilatori e la shell.

2. Ecosistema delle Distribuzioni
Una Distribuzione Linux (Distro) è un sistema operativo completo che integra il Kernel, il set di
strumenti GNU, un sistema di gestione dei pacchetti (Package Manager) e, spesso, un Desktop
Environment.
Le distribuzioni si differenziano principalmente per:

1

1. Gestione dei Pacchetti: Il formato dei file di installazione e il software che risolve le
dipendenze.
2. Ciclo di Rilascio: Rolling release (aggiornamenti continui) vs Fixed release (versioni stabili
periodiche).

Famiglie Principali
• Debian/Ubuntu: Utilizza il formato .deb e il package manager apt. Nota per la stabilità e
l'ampia adozione sia desktop che server. È la distribuzione di riferimento per questo corso.
• RHEL (Red Hat Enterprise Linux) / Fedora: Utilizza .rpm e dnf/yum. È lo standard de
facto per le infrastrutture enterprise aziendali.
• Arch Linux: Adotta un approccio "minimalista" e rolling release. Richiede una configurazione
manuale approfondita.

3. Virtualizzazione (Lab Setup)
Per l'ambiente di laboratorio utilizzeremo una soluzione di Virtualizzazione di Tipo 2 (Hosted).

3.1 Concetti Chiave
• Host OS: Il sistema operativo fisico (Windows/macOS) su cui è installato l'hardware.
• Hypervisor: Il software (es. VirtualBox, VMware Workstation) che astrae le risorse hardware
dell'Host per assegnarle alle macchine virtuali.
• Guest OS: Il sistema operativo virtualizzato (nel nostro caso, Ubuntu).

3.2 Vantaggi in ambiente di sviluppo
L'uso di VM permette l'isolamento dei processi (sandbox). Eventuali errori di configurazione critica o
compromissioni di sicurezza nel Guest non impattano l'Host. Inoltre, la funzionalità di Snapshot
permette di salvare lo stato della memoria e del disco per ripristinare il sistema a una condizione
precedente in caso di errore.

4. Interazione con la Shell (CLI)
La CLI (Command Line Interface) è l'interfaccia primaria per l'amministrazione di sistema
(SysAdmin). In ambiente Linux, la shell predefinita è solitamente Bash (Bourne Again SHell).
La CLI offre vantaggi sostanziali rispetto alla GUI:
• Granularità: Accesso diretto alle System Call e configurazioni di basso livello.

• Automazione: Possibilità di scripting per task ripetitivi.
• Remote Management: Gestione di server remoti tramite protocollo SSH, essenziale in
architetture Cloud/Headless.

4.1 Navigazione del Filesystem
Il filesystem Linux segue lo standard FHS (Filesystem Hierarchy Standard) ed è strutturato ad albero
rovesciato, partendo dalla radice / (root).
• Path Assoluto: Percorso completo dalla root (es. /home/studente/progetti).
• Path Relativo: Percorso riferito alla directory corrente (es. ./progetti).
Comandi di Navigazione
Comando Descrizione tecnica
Sintassi comune
Print Working Directory. Restituisce il path assoluto pwd
pwd
della directory corrente.
ls -la (mostra dettagli e file
ls
List. Elenca il contenuto di una directory.
nascosti/dotfiles)
cd /path/to/dir o cd ..
Change Directory. Modifica la working directory
cd
corrente.
(parent directory)

4.2 Manipolazione File e Directory
Comando Descrizione tecnica
mkdir Make Directory. Crea una nuova directory.
touch Aggiorna il timestamp di un file o ne crea uno vuoto
se non esiste.
Copy. Copia file o directory (con flag -r per
cp
ricorsivo).
Move. Sposta o rinomina file/directory (inode
mv
operation).
rm

Remove. Rimuove file (unlink). Non esiste cestino.

Sintassi comune
mkdir nome_dir
touch file.txt
cp source dest
mv old_name new_name
rm file o rm -rf dir (force
recursive)

5. Risorse e Riferimenti Tecnici
Per l'approfondimento e l'esercitazione pratica pre-lab:
• Linux Journey (linuxjourney.com): Consultare la sezione Grasshopper per la sintassi dei
comandi.
• Bandit Wargame (overthewire.org): Esercizi di sicurezza e amministrazione via SSH.
3

• ExplainShell (explainshell.com): Tool per l'analisi visiva degli argomenti dei comandi (parsing
delle man pages).
• Man Pages: Il manuale di sistema integrato. Utilizzare man [comando] (es. man ls) per la
documentazione ufficiale POSIX.

