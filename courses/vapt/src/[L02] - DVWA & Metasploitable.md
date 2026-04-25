# Dispensa Lezione 2: Web Fuzzing, Shell e Attacchi in Laboratorio

## 1. Introduzione alla Lezione

Questa seconda lezione è divisa in due fasi. Nella prima parte
analizzeremo insieme la compromissione completa di due macchine target
sulla piattaforma HackTheBox. Vedremo come combinare l\'enumerazione dei
servizi web, lo sfruttamento di vulnerabilità specifiche e
l\'ottenimento di privilegi di amministratore.

Nella seconda parte, vi dividerete in due Red Team autonomi per
attaccare due ambienti distinti: il primo focalizzato sulla sicurezza
Web (DVWA) e il secondo sulla sicurezza di sistema (Metasploitable). Al
termine, ogni team dovrà rendicontare il proprio lavoro all\'altro
gruppo.

## 2. Strumenti e Concetti (Fase Dimostrativa)

Durante la dimostrazione pratica, utilizzeremo i seguenti strumenti e
concetti fondamentali per il Penetration Testing moderno.

### 2.1 Enumeration: Nmap e FFUF

La fase di ricognizione è il cuore dell\'attacco.

Nmap: Lo utilizzeremo per mappare le porte aperte e identificare la
superficie di attacco.

FFUF (Fuzz Faster U Fool): Quando identifichiamo un server web (es.
porta 80 o 443), non basta navigare il sito tramite browser. FFUF è un
web fuzzer scritto in Go, estremamente veloce, che ci permette di
scoprire directory nascoste, file non linkati e parametri invisibili
testando migliaia di parole (prese da una wordlist) contro l\'URL
target.

Sintassi base: ffuf -w /usr/share/wordlists/dirb/common.txt -u
http://\<IP_TARGET\>/FUZZ

La parola FUZZ nell\'URL agisce da segnaposto: FFUF la sostituirà con
ogni parola della wordlist.

### 2.2 Exploitation: Il protocollo MCP

Nel nostro scenario d\'esempio, l\'enumerazione rivelerà l\'utilizzo del
protocollo MCP. Esamineremo come l\'implementazione o la configurazione
di determinati protocolli (spesso legati ad applicazioni di terze parti
o sistemi di gestione) possa presentare vulnerabilità sfruttabili per
l\'esecuzione di codice remoto (RCE). L\'obiettivo è capire che
qualsiasi servizio esposto, non solo i classici web o database,
rappresenta un potenziale vettore di ingresso.

2.3 Post-Exploitation: Bind Shell vs Reverse Shell

Una volta trovata una vulnerabilità che permette l\'esecuzione di
comandi (RCE), il nostro obiettivo è ottenere una Shell interattiva sul
sistema bersaglio. Esistono due tipologie principali:

Bind Shell: Il payload malevolo apre una porta in ascolto sulla macchina
bersaglio (es. porta 4444) e lega a essa una shell (come /bin/bash o
cmd.exe). L\'attaccante si connette poi dal proprio computer a quella
porta.

Svantaggio: I firewall moderni bloccano quasi sempre le connessioni in
ingresso su porte non standard.

Reverse Shell: È la tecnica più utilizzata. L\'attaccante apre una porta
in ascolto sulla propria macchina (tramite Netcat: nc -lvnp 9001). Il
payload eseguito sulla macchina bersaglio stabilisce una connessione in
uscita verso il computer dell\'attaccante, consegnandogli la shell.

Vantaggio: I firewall sono generalmente molto più permissivi sul
traffico in uscita, permettendo al payload di \"chiamare casa\" senza
essere bloccato.

### 2.4 Privilege Escalation: LinPEAS

Ottenuto l\'accesso iniziale, spesso ci ritroveremo con privilegi bassi
(es. utente www-data). Per diventare amministratori (root), dobbiamo
cercare falle interne al sistema.

LinPEAS (Linux Privilege Escalation Awesome Script) è uno script bash
che automatizza la ricerca di vettori di Privilege Escalation. Analizza
permessi errati, file SUID, cronjob mal configurati, password in chiaro
nei log e kernel vulnerabili, evidenziando i risultati con un sistema a
colori per facilitarne la lettura.

## 3. Attività di Laboratorio (Red Teaming)

La classe viene ora divisa in due gruppi. Ogni gruppo ha l\'obiettivo di
compromettere il proprio target, fare più danni possibili (simulando un
attacco reale), documentare i passaggi e preparare una presentazione
tecnica per i colleghi.

#### Gruppo 1: Web Application Hacking (DVWA)

Target: Damn Vulnerable Web App (DVWA)

Focus: OWASP Top 10, SQL Injection, Command Injection, XSS, File Upload.

Setup (Docker Compose): Creerete un ambiente effimero tramite container.

Create una cartella: mkdir lab_dvwa && cd lab_dvwa

Create un file docker-compose.yml e inserite le istruzioni standard per
l\'immagine di DVWA (es. vulnerables/web-dvwa).

Avviate l\'infrastruttura con il comando:

Bash

docker compose up -d

Accedete all\'IP locale di Kali sulla porta 80 tramite browser. Login di
default: admin / password.

Obiettivo: Affrontare le sfide presenti nel menu laterale, partendo dal
livello di sicurezza \"Low\". Cercate di estrarre il database tramite
SQLi e di ottenere una reverse shell tramite Command Injection.
Consultate guide online e la documentazione OWASP in caso di blocco.

Ripristino Ambiente: Se compromettete il sistema al punto da renderlo
instabile, potete resettarlo azzerando il container:

Bash

docker compose down

docker compose up -d

#### Gruppo 2: Infrastructure & System Hacking (Metasploitable)

Target: Metasploitable 2

Focus: Enumerazione dei servizi, sfruttamento di software obsoleto (FTP,
Samba, distccd, SSH), Privilege Escalation.

Setup (Snapshot di Sicurezza): La macchina è già configurata su
VirtualBox. Poiché il vostro obiettivo è compromettere a fondo il
sistema (modificando file di configurazione, aggiungendo utenti root,
ecc.), è obbligatorio creare uno Snapshot prima di iniziare.

Su VirtualBox, selezionate la VM Metasploitable -\> \"Istantanee\" -\>
\"Cattura\".

Questo vi permetterà di riportare la macchina allo stato originario con
un click alla fine dell\'esercitazione o nel caso in cui \"rompiate\" il
sistema operativo.

Obiettivo: Partite da zero con Nmap. Identificate i servizi in ascolto e
cercate exploit noti (potete usare searchsploit su Kali o cercare le CVE
online). Puntate a ottenere l\'accesso come utente root in almeno 3 modi
diversi sfruttando 3 servizi differenti.
