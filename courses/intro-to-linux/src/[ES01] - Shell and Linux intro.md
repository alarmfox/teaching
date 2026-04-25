Laboratorio Pratico: Consolidamento Lezione 1
Obiettivo: Padroneggiare la navigazione nel filesystem, la manipolazione di file/directory e l'uso
dell'autodocumentazione (man pages).
Prerequisiti: Macchina Virtuale Ubuntu avviata e terminale aperto.

Esercizio 1: Il Navigatore
Obiettivo: Prendere confidenza con i percorsi (path) assoluti e relativi.
1. Apri il terminale. Assicurati di essere nella tua Home Directory (/home/tuonome).
2. Crea una cartella chiamata Laboratorio_Ripasso.
3. Entra nella cartella appena creata.
4. Crea tre sottocartelle: Documenti, Immagini, Script.
5. Entra in Documenti.
6. Senza usare cd .. o cd /home..., prova a tornare alla cartella
Laboratorio_Ripasso usando un solo comando.
• Suggerimento: Ricorda cosa significano i due punti ...
7. Verifica la tua posizione con pwd.
Verifica: Il comando ls -R (dalla tua home) dovrebbe mostrarti la struttura ad albero creata.

Esercizio 2: Gestione File e "File Nascosti"
Obiettivo: Creare, rinominare e comprendere i file nascosti.
1. Spostati nella cartella Laboratorio_Ripasso/Script.
2. Crea un file vuoto chiamato mioprog.sh.
3. Crea un altro file chiamato .configurazione (fai attenzione al punto iniziale).
4. Esegui il comando ls. Vedi entrambi i file?
5. Trova il comando (o la "flag") giusta per vedere tutti i file, inclusi quelli nascosti.
6. Rinomina mioprog.sh in backup_prog.sh.

7. Sposta backup_prog.sh nella cartella ../Documenti (senza uscire dalla cartella in cui
sei).
Domanda per lo studente: Perché il file .configurazione non si vedeva all'inizio? A cosa
servono i file che iniziano con un punto in Linux?

Esercizio 3: RTFM (Read The Manual)
Obiettivo: Imparare a usare man per scoprire opzioni non spiegate a lezione.
Sei un sysadmin e devi creare una struttura di directory profonda, ma sei pigro e non vuoi fare mkdir
tre volte.
1. Apri il manuale di mkdir digitando man mkdir.
2. Cerca l'opzione (flag) che permette di creare directory "parent" (genitori) automaticamente se
non esistono.
• Indizio: Cerca la parola "parents".
3. Una volta trovata l'opzione, crea questa struttura con un solo comando:
Laboratorio_Ripasso/ProgettoA/Sorgenti/Codice (Nota: Le cartelle
ProgettoA e Sorgenti non esistono ancora).
4. Usa il comando tree (se installato) o ls -R per verificare il successo.

Esercizio 4: Manipolazione Ricorsiva (Attenzione!)
Obiettivo: Copiare e cancellare intere directory. Questo è il punto dove spesso si fanno errori.
1. Torna nella cartella Laboratorio_Ripasso.
2. Crea un file di testo leggimi.txt dentro la cartella ProgettoA (creata nell'esercizio 3).
3. Prova a copiare l'intera cartella ProgettoA dentro Documenti usando cp ProgettoA
Documenti/.
• Osserva l'errore: Il terminale ti dirà che stai omettendo una directory.
4. Usa man cp per trovare l'opzione "recursive" (ricorsiva).
5. Riprova il comando aggiungendo la flag corretta.
6. Ora prova a cancellare la cartella originale ProgettoA con rm.
• Osserva l'errore: Anche qui, rm si rifiuta di cancellare una cartella piena.

7. Trova l'opzione per cancellare ricorsivamente e rimuovi ProgettoA.
Attenzione: Quando usi rm con le opzioni ricorsive, fai molta attenzione a dove ti trovi!

Esercizio 5: Il "Disaster Recovery" (Challenge Finale)
Scenario: Un collega distratto ha creato dei file importanti ma li ha nominati male e messi nel posto
sbagliato. Devi sistemare tutto.
Setup (Esegui questi comandi per creare il "disastro"):
Bash
cd ~/Laboratorio_Ripasso
mkdir -p Disastro/Temp
touch Disastro/Temp/file_imporante.txt # (Notare l'errore di battitura)
touch Disastro/Temp/RELAZIONE_FINALE.doc
touch Disastro/NON_TOCCARE.txt

La tua Missione:
1. Sposta RELAZIONE_FINALE.doc nella cartella Documenti (che hai creato nell'Ex 1).
2. Entra in Disastro/Temp.
3. Correggi il nome di file_imporante.txt in file_importante.txt.
4. Copia file_importante.txt nella tua Home directory (~).
5. Torna alla radice di Laboratorio_Ripasso.
6. Elimina interamente la cartella Disastro e tutto il suo contenuto.
Controllo Finale: Alla fine, dentro Laboratorio_Ripasso dovresti avere solo le cartelle
Documenti, Immagini, Script e la struttura interna pulita.

