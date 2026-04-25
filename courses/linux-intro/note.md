**Corso:** Linux Livello ITS  
**Obiettivo:** Comprendere l'ecosistema Linux, prendere confidenza con la CLI via browser e preparare l'ambiente di virtualizzazione.

---

# 1. Il File System (FHS): La Mappa del Tesoro (30 min)

**Obiettivo:** Spiegare che non esiste il disco `C:` e che *tutto è un file*.

## Concetti Chiave da Trasmettere

- **La Radice (`/`)**  
  L’inizio di tutto l’albero del filesystem.

- **Mount Point**  
  Se inserisci una USB, non diventa `E:` ma una *cartella*  
  (solitamente in `/media` o `/mnt`).

- **Case Sensitivity**  
  `File.txt` ≠ `file.txt`  
  👉 Fai fare un test pratico: è uno degli errori più comuni.

## Tour Guidato (Live Demo)

Apri il terminale e naviga con `cd`, mostrando queste directory:

- **`/bin` & `/sbin`**  
  I binari (eseguibili).  
  Qui vivono comandi come `ls`, `cp`, `ip`.

- **`/etc`**  
  Configurazione del sistema.  
  Mnemonico: **Editable Text Configuration**  
  Qui vive l’anima del sistema.

- **`/home`**  
  Le cartelle degli utenti standard.

- **`/root`**  
  La home dell’amministratore (spesso inaccessibile senza permessi).

- **`/var`**  
  Dati variabili: log, spool di stampa, database, siti web.

- **`/tmp`**  
  File temporanei (di solito si svuota al riavvio).

- **`/dev`**  
  I file device (es. `/dev/null`, il buco nero).

---

# 2. Editing di Testo: Nano vs Vim (30 min)

**Obiettivo:** Configurare server senza interfaccia grafica.

## Nano (La scelta sicura)

Editor immediato per principianti.  
I comandi sono visibili in basso.

### Comandi base

- `nano file.txt` → apre/crea il file
- `CTRL + O` → salva (Write Out)
- `CTRL + X` → esce

## Vim (Il “Mostro Finale” – Opzionale)

Mostralo solo se c’è tempo o curiosità.  
È **modale** (Insert vs Command).

### Panic Button
Se qualcuno entra per sbaglio e non sa uscire:

ESC -> :q! -> INVIO
---

# 3. Utenti e Superpoteri: sudo (45 min)

**Obiettivo:** Capire la gestione multi-utente e la sicurezza.

## Concetti

- **Root**  
  L’amministratore supremo.

- **User**  
  L’utente limitato (quello che usano loro).

- **Sudo**  
  *SuperUser DO* → permesso temporaneo per agire come root.

## Demo: I file degli utenti

Gli utenti sono solo righe di testo in un file.

- `cat /etc/passwd`  
  Lista utenti pubblica.  
  Spiegare i campi:  
  **User – UID – GID – Home – Shell**

- `cat /etc/shadow`  
  Password hashate (file privato).

### Prova pratica

```sh
cat /etc/shadow
```
**Permesso negato**

```sh
sudo cat /etc/shadow
```

→ **Funziona**

---

# 4. Permessi e Proprietà (1 ora – Cruciale)

**Obiettivo:** Decifrare `ls -l`.

## La Triade: `rwx`

Usa `ls -l` su un file e spiega la prima colonna  
(es. `-rwxr-xr--`).

### Struttura

- **Tipo**
  - `-` file
  - `d` directory

- **User (u)**  
  Proprietario del file

- **Group (g)**  
  Gruppo assegnato

- **Others (o)**  
  Tutti gli altri

### Significato dei permessi

- **r (Read)**  
  - File: leggere  
  - Directory: listare contenuto

- **w (Write)**  
  - File: modificare  
  - Directory: creare/cancellare file

- **x (Execute)**  
  - File: eseguire  
  - Directory: entrarci (`cd`)

## Comandi Lab

### `chmod` (Change Mode)

- **Simbolico**
```sh
chmod u+x script.sh
```

- **Ottale**
```sh 
chmod 755 script.sh # script standard
chmod 644 file.txt # file standard
```

⚠️ **Warning:** evitare `777` se non per test disperati.

### `chown` (Change Owner)

```sh
sudo chown utente:gruppo file
```
---

# 5. Gestione Pacchetti: APT (45 min)

**Obiettivo:** Installare software in modo professionale.

## Concetti

- **Repository**  
  Il “magazzino” ufficiale del software.

- **Dipendenze**  
  APT scarica automaticamente le librerie necessarie.

## Il Flusso Sacro
```sh
sudo apt update
```

Aggiorna la **lista** dei pacchetti (non il software).

```sh
sudo apt upgrade
```
Aggiorna i pacchetti installati.


```sh
sudo apt install nome
```

Installa un programma (es. `htop`, `neofetch`).


```sh
sudo apt remove nome
```
Rimuove il programma (mantiene i file di config).


```sh
sudo apt purge nome
```

Rimuove tutto.

## Lab “Gratificazione Immediata”

Installare:

- `cmatrix` → effetto Matrix
- `sl` → locomotiva se sbagliano `ls`
- `htop` → monitor risorse colorato

---

# 6. Note Mentali per l’Istruttore

- **Il TAB è tuo amico**  
  Insistere sull’autocompletamento.  
  Scrivere i percorsi a mano = frustrazione garantita.

- **Root vs Permessi**  
  Root ignora i permessi.  
  Un file `chmod 000` può essere letto da root.

- **Disclaimer `rm -rf`**  
  Quando spieghi la cancellazione ricorsiva con `sudo`,  
  fai un avviso enorme:  
  *“Da grandi poteri derivano grandi responsabilità.”*

---

# 7. Link e Risorse Extra (per gli studenti)

- **Chmod Calculator**  
  Per visualizzare e capire i permessi ottali.

- **Linux FHS Official**  
  Documentazione ufficiale della gerarchia filesystem.

- **Vim Adventures**  
  Gioco per imparare Vim divertendosi.
