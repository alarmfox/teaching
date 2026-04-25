1. I Prossimi Passi (Cosa studiare ora?)
Se vuoi diventare un SysAdmin completo o puntare verso il mondo DevOps / Cloud, ecco gli
argomenti successivi da affrontare:

A. Bash Scripting (Automazione)
Smetti di scrivere gli stessi comandi a mano. Impara a scrivere script in Bash (il linguaggio del
terminale) per automatizzare backup, creazione di utenti o monitoraggio.
• Concetti chiave: Variabili, cicli for/while, istruzioni condizionali if/else, espressioni
regolari (Regex) e comandi come awk e sed.

B. Containerization (Docker)
Nel corso abbiamo installato i software direttamente sul sistema operativo (Bare-Metal). Oggi
l'industria usa i Container: pacchetti leggeri che contengono l'applicazione e tutte le sue dipendenze,
isolati dal resto del sistema.
• Cosa studiare: Installazione di Docker, concetti di Immagini e Container, scrittura di un
Dockerfile, orchestrazione base con Docker Compose.

C. Version Control (Git)
Come SysAdmin, i tuoi file di configurazione (es. script, regole firewall) sono codice. Git ti permette di
tenere traccia delle modifiche, tornare indietro in caso di errori e lavorare in team.
• Comandi base: git init, git add, git commit, git push.

D. Infrastructure as Code (Ansible)
Immagina di dover configurare 50 server Linux identici a quello che hai preparato nell'ultima lezione.
Farlo a mano è impensabile. Ansible ti permette di scrivere un file di testo (Playbook) descrivendo
come deve essere il server, e lui lo configurerà in automatico via SSH.

2. Risorse di Studio Gratuite
Metti questi link tra i preferiti. Saranno i tuoi migliori amici:
• Linux Journey (Italiano/Inglese) Il miglior sito in assoluto per ripassare tutto ciò che abbiamo
visto nel corso e andare oltre. È strutturato a moduli, partendo da zero fino al routing di rete
avanzato.
• OverTheWire - Bandit (Inglese) Un "Wargame" a livelli. Ti colleghi via SSH ai loro server e
devi risolvere degli enigmi usando comandi Linux per trovare la password del livello
successivo. È il modo più divertente ed efficace per diventare dei "ninja" della riga di comando.

• Arch Wiki (Inglese) La "Bibbia" di Linux. Anche se usi Ubuntu o Debian, la Wiki di Arch
Linux contiene le spiegazioni più dettagliate e precise su come funziona qualsiasi software o
componente di Linux.
• ExplainShell (Inglese) Hai trovato un comando lunghissimo e incomprensibile su internet (es.
tar -czvf file.tar.gz /cartella | grep "errore")? Incollalo qui, e il sito
esploderà visivamente il comando spiegandoti cosa fa ogni singolo flag e lettera.

3. Canali YouTube Consigliati
La community Linux su YouTube è gigantesca e produce contenuti di altissima qualità:
1. NetworkChuck: Stile molto "americano", caffè alla mano, ma eccezionale per capire concetti
complessi come reti, Docker, Linux base e Cloud in modo divertente ed entusiasta.
2. Learn Linux TV: Canale istituzionale, perfetto. Centinaia di tutorial passo-passo (es. corso
completo su Bash Scripting o su Ansible).
3. Morrolinux (Italiano): Il punto di riferimento italiano per il mondo Linux. Fa recensioni,
tutorial tecnici e spiegazioni approfondite sull'architettura dei sistemi open source.

4. Il Consiglio d'Oro del SysAdmin
"Non imparare a memoria i comandi, impara a leggere i log e la documentazione."
Nella tua carriera dimenticherai la sintassi di migliaia di comandi. Non importa. Un buon sistemista
non è quello che ricorda tutto a memoria, ma quello che:
1. Sa usare il comando man [nome_comando] o --help.
2. Sa leggere in fondo a /var/log/syslog per capire perché un servizio è crashato.
3. Sa cercare l'errore esatto su Google o StackOverflow.
Ecco un'eccellente integrazione per la Dispensa Extra. Le certificazioni sono il modo migliore per
dimostrare alle aziende (e soprattutto ai recruiter delle Risorse Umane) che le competenze acquisite non
sono solo teoriche.
Puoi copiare e incollare questa sezione direttamente in coda al documento precedente, aggiungendola
come punto 5.

5. Certificazioni IT: Dimostrare le proprie competenze
Nel mercato del lavoro IT, l'esperienza pratica è fondamentale, ma le certificazioni ufficiali sono il
"passaporto" che ti permette di superare i filtri dei recruiter e ottenere i primi colloqui.

Se vuoi certificare le competenze acquisite in questo corso e in quelli futuri, ecco i percorsi più
riconosciuti a livello internazionale:

A. Il Livello Base (Per iniziare)
Se vuoi consolidare le fondamenta e avere un certificato entry-level da mettere subito a curriculum:
• LPI Linux Essentials: È il primissimo gradino offerto dal Linux Professional Institute. Copre
esattamente i concetti base della riga di comando, file, script semplici e licenze Open Source. È
facile, accessibile e non ha scadenza.
• CompTIA Linux+: Una certificazione "vendor-neutral" (non legata a una specifica
distribuzione come Ubuntu o Red Hat) molto rispettata. Dimostra che sai amministrare sistemi,
gestire la sicurezza base e fare troubleshooting. L'esame è a risposta multipla e scenari simulati.

B. Il Livello Intermedio (Il vero SysAdmin)
Queste sono le certificazioni che ti qualificano ufficialmente come Amministratore di Sistema Linux
Junior/Mid-level.
• LPIC-1 (Linux Administrator): Il logico passo successivo al Linux Essentials. È composta da
due esami e certifica che sei in grado di installare, configurare e mantenere una postazione
Linux o un server base connesso in rete.
• RHCSA (Red Hat Certified System Administrator): Il "Gold Standard" assoluto. A
differenza delle altre, questo esame è 100% pratico. Ti mettono davanti a un terminale rotto e
hai 3 ore per ripararlo, partizionare dischi, configurare LVM, utenti e servizi di rete (su base
Red Hat/CentOS). Se hai questa certificazione nel CV, le aziende sanno che sai davvero mettere
le mani in console. È dura, ma vale ogni sforzo.

C. Lo Sguardo al Futuro (Cloud & DevOps)
Una volta che padroneggi Linux, il passo successivo è scalare l'infrastruttura. I server fisici o le singole
VM oggi si gestiscono in massa.
• AWS Certified Cloud Practitioner: Per capire come Amazon Web Services (il cloud provider
più grande al mondo) usa Linux per ospitare milioni di server virtuali.
• LFCS (Linux Foundation Certified IT System Administrator): Simile alla RHCSA, è un
esame puramente pratico erogato direttamente dalla fondazione che gestisce il Kernel Linux.
Ottima per ambienti cloud-native.
💡 Il consiglio di carriera: Non fare l'errore di accumulare certificazioni senza aver mai
"rotto" un server vero. Usa VirtualBox, crea laboratori domestici, distruggi macchine
virtuali e riparale. Le certificazioni ti fanno ottenere il colloquio, ma i laboratori pratici
ti fanno superare la prova tecnica.

