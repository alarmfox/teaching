Andrea BIONDO
Università di Padova

Software Security 1
1

https://cybersecnatlab.it

License & Disclaimer
2

License Information

Disclaimer

This presentation is licensed under the
Creative Commons BY-NC License

To view a copy of the license, visit:
http://creativecommons.org/licenses/by-nc/3.0/legalcode

© CINI – 2021

➢

We disclaim any warranties or representations
as to the accuracy or completeness of this
material.

➢

Materials are provided “as is” without
warranty of any kind, either express or
implied, including without limitation,
warranties of merchantability, fitness for a
particular purpose, and non-infringement.

➢

Under no circumstances shall we be liable for
any loss, damage, liability or expense incurred
or suffered which is claimed to have resulted
from use of this material.

Rel. 22.03.2021

Obiettivi
3

Comprensione della memoria a basso livello
➢ Conoscenza di base dei buffer overflows
➢ Conoscenze di base di reverse engineering
➢

© CINI – 2021

Rel. 22.03.2021

Prerequisiti
4

➢

Sistemi di numerazione
➢ Esadecimale

➢

Conoscenza di base del linguaggio C
➢ Tipi primitivi e strutturati, puntatori
➢ Funzioni di I/O

© CINI – 2021

Rel. 22.03.2021

Argomenti
5

Spazio di memoria
➢ Reverse engineering
➢ Buffer overflows
➢

© CINI – 2021

Rel. 22.03.2021

Argomenti
6

Spazio di memoria
➢ Reverse engineering
➢ Buffer overflows
➢

© CINI – 2021

Rel. 22.03.2021

Cos’è la memoria?
7

Per un programmatore potrebbe essere un insieme
di variabili tipate
➢ Per un ingegnere elettronico potrebbe essere un
insieme di celle bistabili
➢ Dobbiamo scegliere un livello di astrazione
➢

© CINI – 2021

Rel. 22.03.2021

Astrazioni di memoria
8

Dati tipati (variabili)

Visione interpretata dei byte

Linguaggio di programmazione
Sequenza di byte indirizzabili
Spazio indipendente per-processo
Solo alcune aree sono mappate

Memoria virtuale
Sistema operativo

Memoria fisica
© CINI – 2021

Sequenza di byte indirizzabili

Rel. 22.03.2021

Memoria virtuale
9

Spazio virtuale di dimensione fissata (4GB / 256TB)
➢ Mapping fra aree di memoria virtuale e fisica
➢ Flag di protezione degli accessi
➢

➢ Read, write, execute

© CINI – 2021

Rel. 22.03.2021

Spazio virtuale Linux userspace
10

Indirizzi

Binario
Text

Codice

Data

Dati globali inizializzati

BSS

Dati globali azzerati

Heap

Allocazioni dinamiche

Librerie

Binari delle librerie dinamiche

Stack

Variabili locali, record di attivazione

© CINI – 2021

Rel. 22.03.2021

Spazio virtuale Linux userspace
11

© CINI – 2021

Rel. 22.03.2021

Rappresentazione di interi
12

➢

unsigned int: intero a 32 bit senza segno
➢ Numero in [0, 4294967295]

➢

Esempio: valore 100.000.000
➢ Esadecimale: 0x05F5E100
+0

Big-endian

+1

0x05
+0

Little-endian

+2

0xF5
+1

0x00

+3

0xE1
+2

0xE1

0x00
+3

0xF5

© CINI – 2021

0x05
Rel. 22.03.2021

x86 usa LE

Rappresentazione di tipi C (x86)
13

➢

Interi little-endian
➢ Interi con segno rappresentati secondo la notazione

complemento a due
➢ char, int, short, long, enum: interi a varie lunghezze

float e double: IEEE 754
➢ I puntatori sono interi unsigned
➢

➢ Il loro valore è l’indirizzo puntato
➢ 32/64 bit (per indirizzare intero spazio virtuale)

© CINI – 2021

Rel. 22.03.2021

Rappresentazione di tipi C (x86)
14

➢

Array
➢ Elementi disposti sequenzialmente
➢ [i] @ base array + i * size elemento

➢

Strutture
➢ Campi disposti sequenzialmente in ordine di dichiarazione
➢ Campo @ base struct + somma size campi precedenti
➢ (Il compilatore potrebbe introdurre del padding)
© CINI – 2021

Rel. 22.03.2021

Corruzione di memoria
15

Modificare la memoria di un processo in un modo
diverso da quello previsto dal programmatore
➢ Controllare la memoria = controllare il processo!
➢

© CINI – 2021

Rel. 22.03.2021

Corruzione di memoria in the wild
16

➢

Malware
➢ Morris worm (1988!), Blaster, Sasser, Conficker, …
➢ Più recentemente, StuxNet e WannaCry

➢

Servizi remoti e applicazioni utente
➢ Attacchi su server e browser

➢

Sbloccaggio di dispositivi
➢ Root Android, jailbreak iOS, console per videogiochi

© CINI – 2021

Rel. 22.03.2021

Argomenti
17

Spazio di memoria
➢ Reverse engineering
➢ Buffer overflows
➢

© CINI – 2021

Rel. 22.03.2021

Reverse engineering
18

“Analizzare un sistema per creare rappresentazioni ad
alto livello di astrazione”
(Chikofsky, Cross 1990)

Prodotto finito
(eseguibile compilato)

© CINI – 2021

Informazioni
progettuali
(architettura, sorgente)

Rel. 22.03.2021

Reverse engineering
19

➢

Molte ragioni per fare reversing
➢ Recupero di codice sorgente
➢ Documentazione mancante o insufficiente
➢ Analisi di prodotti concorrenti
➢ “Aprire” piattaforme proprietarie
➢ Auditing di sicurezza
➢ Curiosità
© CINI – 2021

Rel. 22.03.2021

La vita di un programma
20

Sorgente

Perdita di informazioni
ad alto livello

Compilatore

Analisi dinamica

File oggetto

Processo

Linker

Eseguibile

Lib. statiche

Loader
Linker dinamico
Lib. dinamiche

Analisi statica
© CINI – 2021

Rel. 22.03.2021

Eseguibili
21

➢

Molti formati, a seconda dell’OS
➢ PE (Windows), Mach-O (MacOS, iOS), ELF (*nix), …

➢

Divisi in varie sezioni/segmenti mappabili
➢ Cioè che diventano aree di memoria virtuale a runtime

© CINI – 2021

Rel. 22.03.2021

Gli strumenti
22

➢

Analisi statica
➢ Disassemblatori, decompilatori (e.g., Ghidra)
➢ Avanzati: interpretazione astratta, esecuzione simbolica, …

➢

Analisi dinamica
➢ Debugger (e.g., GDB)
➢ Avanzati: tracer, instrumentazione dinamica, …

© CINI – 2021

Rel. 22.03.2021

Assembly x86_64
23

La CPU ha una piccola memoria locale composta da
registri
➢ Ogni istruzione assembly ha degli operandi
➢

➢ Registri: rax, ebx, r13d, …
➢ Memoria: [rax+4]
➢

Notazione Intel: <op> <destinazione>, <sorgente>
© CINI – 2021

Rel. 22.03.2021

Registri x86_64
24

Estesi da x86: r{a,b,c,d}x
➢ Program counter: rip
➢ Gestione stack
➢

➢ rsp (stack pointer)
➢ rbp (frame pointer)
➢

Generici: r8-r15
© CINI – 2021

Rel. 22.03.2021

Registri x86_64
25

RAX

EAX

AX

AH

AL

8

8

16
32
64

© CINI – 2021

Rel. 22.03.2021

Alcune istruzioni di base
26

MOV <dst>, <src>
➢ PUSH <src> / POP <dst>
➢ ADD/SUB <dst>, <src>
➢ CALL <pc> / RET
➢

© CINI – 2021

Rel. 22.03.2021

Salti condizionali
27

➢

CMP <opnd1>, <opnd2>
➢ Confronta due valori e imposta delle flag

➢

J<condizione> <pc>
➢ Salta a <pc> se le flag matchano <condizione>

➢

Salta se rax != 15:
➢ CMP rax, 15

➢ JNE …

© CINI – 2021

Rel. 22.03.2021

Reversing statico con Ghidra
28

© CINI – 2021

Rel. 22.03.2021

Argomenti
29

Spazio di memoria
➢ Reverse engineering
➢ Buffer overflows
➢

© CINI – 2021

Rel. 22.03.2021

Buffer overflows
30

char name[100];
printf("Come ti chiami? ");
scanf("%s", name);
printf("Ciao, %s!\n", name);

© CINI – 2021

Rel. 22.03.2021

Buffer overflows
31

➢

Cosa succede se l’utente ha un nome più lungo di
100 caratteri?
➢ O se è malevolo e vuole dare più di 100 caratteri in input...

➢

scanf (in questo caso) non controlla i bound
➢ Continuerà a scrivere caratteri oltre la fine di name,

sovrascrivendo la memoria che lo segue

© CINI – 2021

Rel. 22.03.2021

Buffer overflows
32

➢

Si ha un buffer overflow quando il programma scrive
oltre la fine di un buffer
➢ Perché i dati sono più lunghi del buffer

➢

Classica vulnerabilità di corruzione della memoria
➢ Scriviamo dati dall’attaccante (input utente) in posizioni di

memoria che il programmatore non aveva previsto
potessero essere modificate (oltre la fine del buffer)
© CINI – 2021

Rel. 22.03.2021

Conseguenze del buffer overflow
33

Le garanzie di correttezza cadono completamente
➢ Se corrompiamo abilmente la memoria, possiamo
ottenere il controllo completo del processo
➢

➢ Arbitrary code execution

© CINI – 2021

Rel. 22.03.2021

Accessi out-of-bounds
34

struct {
int a[2];
int b[3];
};

a[0]
a[1]
b[0]
b[1]
b[2]

Questo è anche a[2]!

a[2] = 42;
printf("%d\n", b[0]);
/* stampa 42 */
© CINI – 2021

Rel. 22.03.2021

Accessi out-of-bounds
35

Nessun bound
check!
Scritture OOB

© CINI – 2021

Rel. 22.03.2021

Accessi out-of-bounds
36

Nessun bound
check!

Scritture OOB

© CINI – 2021

Rel. 22.03.2021

Pattern pericolosi
37

➢

Senza bound checking
➢ gets, scanf %s, sprint, strcpy

➢

Bound checking usato impropriamente
➢ fgets, (f)read, snprintf, memcpy, strncpy, …

➢

Manipolazioni manuali
➢ Loop di copia, accessi ad array, …

© CINI – 2021

Rel. 22.03.2021

Un primo overflow
38

Nessun bound
check!

Overflow dei
caratteri 89

© CINI – 2021

Rel. 22.03.2021

Andrea BIONDO
Università di Padova

Software Security 1
39

https://cybersecnatlab.it

