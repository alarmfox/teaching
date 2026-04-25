Andrea BIONDO
Università di Padova

Paolo Prinetto
President of CINI
Paolo.Prinetto@polito.it
Mob. +39 335 227529

Software Security 2
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

Rel. 15.03.2021

Obiettivi
3

Comprensione delle metodologie di debugging con GDB
➢ Conoscenza di base degli stack overflows e mitigazioni
➢ Conoscenza di ulteriori attacchi avanzati e relative mitigazioni
➢

© CINI – 2021

Rel. 15.03.2021

Prerequisiti
4

➢

Modulo SS_1 – Software Security 1

© CINI – 2021

Rel. 15.03.2021

Argomenti
5

Debugging
➢ Stack overflows
➢ Altri attacchi e difese
➢

© CINI – 2021

Rel. 15.03.2021

Argomenti
6

Debugging
➢ Stack overflows
➢ Altri attacchi e difese
➢

© CINI – 2021

Rel. 15.03.2021

Debugging
7

Il processo di trovare e risolvere bug
➢ Debugger: programma che permette di ispezionare e
modificare lo stato interno di un programma target
➢

➢ Si presta anche all’analisi a fini di reversing ed exploitation
➢ In senso esteso, debugging = uso del debugger come

strumento di analisi, non solo per risolvere bug

© CINI – 2021

Rel. 15.03.2021

Funzioni di un debugger
8

➢

Gestione del control flow
➢ Breaking, stepping, continuing, jumping

➢

Intercettazione di eventi
➢ Breakpoints, catchpoints, watchpoints, eccezioni, …

➢

Ispezione e modifica dello stato
➢ Variabili, registri, stack, memoria, codice

➢ Valutazione di espressioni

© CINI – 2021

Rel. 15.03.2021

GNU Debugger (GDB)
9

➢

Molto diffuso in ambiente Linux
➢ Alternativa: LLDB (LLVM Project)
➢ rr (Mozilla) offre record/replay sopra GDB

Interfaccia a riga di comando
➢ Supporto per plugin (GDB script, Python)
➢

➢ pwndbg per reversing/exploitation

© CINI – 2021

Rel. 15.03.2021

GDB: avviare una sessione
10

$ gdb <programma>
➢ $ gdb –p <pid>
➢ (gdb) r[un] [args…]
➢ (gdb) q[uit]
➢

© CINI – 2021

Rel. 15.03.2021

GDB: controllo di flusso
11

➢

b[reak] <simbolo/linea/*indirizzo>
➢ Imposta un breakpoint

➢

c[ontinue]
➢ Riprende l’esecuzione

➢

s[tep] / n[ext]
➢ Continua fino alla prossima linea di codice (next passa

sopra alle chiamate a funzione)
© CINI – 2021

Rel. 15.03.2021

GDB: controllo di flusso
12

➢

s[tep]i / n[ext]i
➢ Come step/next, ma a livello di istruzioni macchina

➢

i[nfo] b[reakpoints]
➢ Mostra i breakpoint

➢

d[elete] <numero BP>
➢ Elimina un breakpoint

© CINI – 2021

Rel. 15.03.2021

GDB: ispezione dello stato
13

➢

i[nfo] r[egisters]
➢ Mostra i registri

➢

i[nfo] locals
➢ Mostra le variabili locali

➢

b[ack]t[race]
➢ Mostra backtrace dello stack di chiamate

© CINI – 2021

Rel. 15.03.2021

GDB: valutazione di espressioni
14

➢

p[rint] <espressione C-like>
➢ p 100 + 23 stampa 123
➢ p foo stampa il valore del simbolo foo
➢ p *(int *)0x1234 stampa un int letto dall’indirizzo 0x1234
➢ p $rax stampa il registro rax
➢ p/x = hex, p/d = decimale

© CINI – 2021

Rel. 15.03.2021

GDB: ispezione della memoria
15

➢

x/nfu <addr>
➢ n = numero di word da stampare
➢ f = formato di visualizzazione (x = hex, d = decimale, i =

istruzione)
➢ u = dimensione word (b = 1b, h = 2b, w = 4b, g = 8b)
➢ addr = espressione per l’indirizzo a cui leggere
➢ x/16xg 0x1234 stampa 16 quadword in hex da 0x1234
© CINI – 2021

Rel. 15.03.2021

GDB: modifica dello stato
16

set variable foo = 42
➢ set *(int *)0x1234 = 42
➢

© CINI – 2021

Rel. 15.03.2021

Una prima challenge con GDB
17

© CINI – 2021

Rel. 15.03.2021

Argomenti
18

Debugging
➢ Stack overflows
➢ Altri attacchi e difese
➢

© CINI – 2021

Rel. 15.03.2021

Buffer overflows su stack
19

➢

Un buffer overflow è utile se ci sono dati interessanti
da corrompere dopo il buffer
➢ Dipende dal programma

➢

Stack overflow: overflow di buffer allocato su stack
➢ Lo stack contiene dati chiave per il control flow, nascosti al

programmatore e sempre presenti in ogni programma!

© CINI – 2021

Rel. 15.03.2021

Lo stack x86
Indirizzi di memoria

20

void bar() {
char baz[32];
/* … */
}
void foo() {
int abc, def;
bar();
/* … */
}

SP
Variabili locali
BP

Saved BP

Frame
di foo

Return address

int main() {
foo();
/* … */
}
© CINI – 2021

Rel. 15.03.2021

Lo stack x86
Indirizzi di memoria

21

void bar() {
char baz[32];
/* … */
}
SP

void foo() {
int abc, def;
bar();
/* … */
}

Return address
Variabili locali

BP

Saved BP

Frame
di foo

Return address

int main() {
foo();
/* … */
}
© CINI – 2021

Rel. 15.03.2021

Lo stack x86
Indirizzi di memoria

22

SP, BP

void bar() {
char baz[32];
/* … */
}
Saved BP
void foo() {
int abc, def;
bar();
/* … */
}

Return address
Variabili locali
Saved BP

Frame
di foo

Return address

int main() {
foo();
/* … */
}
© CINI – 2021

Rel. 15.03.2021

Lo stack x86
23

void bar() {
char baz[32];
/* … */
}

SP

Indirizzi di memoria

Variabili locali
BP

Saved BP

Frame
di bar

void foo() {
int abc, def;
bar();
/* … */
}

Return address
Variabili locali
Saved BP

Frame
di foo

Return address

int main() {
foo();
/* … */
}
© CINI – 2021

Rel. 15.03.2021

Lo stack x86
Indirizzi di memoria

24

SP, BP

void bar() {
char baz[32];
/* … */
}
Saved BP
void foo() {
int abc, def;
bar();
/* … */
}

Return address
Variabili locali
Saved BP

Frame
di foo

Return address

int main() {
foo();
/* … */
}
© CINI – 2021

Rel. 15.03.2021

Lo stack x86
Indirizzi di memoria

25

void bar() {
char baz[32];
/* … */
}
SP

void foo() {
int abc, def;
bar();
/* … */
}

Return address
Variabili locali

BP

Saved BP

Frame
di foo

Return address

int main() {
foo();
/* … */
}
© CINI – 2021

Rel. 15.03.2021

Lo stack x86
Indirizzi di memoria

26

void bar() {
char baz[32];
/* … */
}
void foo() {
int abc, def;
bar();
/* … */
}

SP
Variabili locali
BP

Saved BP

Frame
di foo

Return address

int main() {
foo();
/* … */
}
© CINI – 2021

Rel. 15.03.2021

Lo stack visto da GDB
27

© CINI – 2021

Rel. 15.03.2021

Stack overflow
28

Buffer
Sv. BP
Retaddr

?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
c3 90 8b 00 ff 7f 00 00
d5 e0 7b 30 b2 55 00 00

Input: 32 ‘A’

Ritorna a 0x55b2307be0d5

© CINI – 2021

41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
c3 90 8b 00 ff 7f 00 00
d5 e0 7b 30 b2 55 00 00
Ritorna a 0x55b2307be0d5

Rel. 15.03.2021

Stack overflow
29

Buffer
Sv. BP
Retaddr

?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
c3 90 8b 00 ff 7f 00 00
d5 e0 7b 30 b2 55 00 00

Input: 40 ‘A’

Ritorna a 0x55b2307be0d5

© CINI – 2021

41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
d5 e0 7b 30 b2 55 00 00
Ritorna a 0x55b2307be0d5

Rel. 15.03.2021

Stack overflow
30

Buffer
Sv. BP
Retaddr

?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
c3 90 8b 00 ff 7f 00 00
d5 e0 7b 30 b2 55 00 00

Input: 46 ‘A’

Ritorna a 0x55b2307be0d5

© CINI – 2021

41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
41 41 41 41 41 41 00 00
Ritorna a 0x414141414141
Controllo instruction pointer!

Rel. 15.03.2021

Implicazioni dello stack overflow
31

➢

Possiamo far saltare il programma dove vogliamo
➢ Se il programma contiene codice “interessante”, possiamo

eseguirlo
➢ Se siamo in grado di iniettare codice arbitrario da qualche
parte in memoria, possiamo eseguirlo
➢ Arbitrary code execution

➢

Tecniche applicabili ad ogni programma vulnerabile
© CINI – 2021

Rel. 15.03.2021

Challenge con stack overflow
32

© CINI – 2021

Rel. 15.03.2021

Argomenti
33

Debugging
➢ Stack overflows
➢ Altri attacchi e difese
➢

© CINI – 2021

Rel. 15.03.2021

Stack overflow con shellcode
34

➢

Shellcode: codice macchina standalone scritto
dall’attaccante, che fa qualcosa di “interessante”
➢ E.g., aprire una shell

➢

Idea: iniettare shellcode nella memoria del
programma, poi usare stack overflow per eseguirlo
➢ Shellcode iniettato a 0x1234
➢ Sovrascriviamo retaddr con 0x1234
© CINI – 2021

Rel. 15.03.2021

Stack overflow con shellcode
35

Buffer @ 0x7fff008b9070
Buffer
Sv. BP
Retaddr

?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
c3 90 8b 00 ff 7f 00 00
d5 e0 7b 30 b2 55 00 00

31 f6 48 bb 2f 62 69 6e
2f 2f 73 68 56 53 54 5f
6a 3b 58 31 d2 0f 05 90
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
70 90 8b 00 ff 7f 00 00

Ritorna a 0x55b2307be0d5

© CINI – 2021

Rel. 15.03.2021

Shellcode
Padding
Indirizzo buffer

Stack overflow con shellcode
36

Buffer @ 0x7fff008b9070
Buffer
Sv. BP
Retaddr

?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
?? ?? ?? ?? ?? ?? ?? ??
c3 90 8b 00 ff 7f 00 00
d5 e0 7b 30 b2 55 00 00

31 f6 48 bb 2f 62 69 6e
2f 2f 73 68 56 53 54 5f
6a 3b 58 31 d2 0f 05 90
41 41 41 41 41 41 41 41
41 41 41 41 41 41 41 41
70 90 8b 00 ff 7f 00 00

Ritorna a 0x55b2307be0d5

Ritorna a 0x7fff008b9070

© CINI – 2021

Rel. 15.03.2021

Shellcode
Padding
Indirizzo buffer

Mitigazioni
37

➢

Come ci difendiamo?
➢ Fixando i bug
➢ Rendendo difficile l’exploitation

➢

Le mitigazioni seguono il secondo approccio

© CINI – 2021

Rel. 15.03.2021

Mitigazioni
38

➢

Di cosa ha bisogno l’attaccante?
➢ Deve poter iniettare codice
➢ Deve conoscere l’indirizzo del codice
➢ Deve poter sovrascrivere il retaddr

➢

Rendiamogli la vita difficile!

© CINI – 2021

Rel. 15.03.2021

W⊕X / NX / DEP
39

Write XOR eXecute: ogni mapping è o scrivibile o
eseguibile, mai entrambi assieme
➢ Aree dati non eseguibili
➢

➢ Posso iniettare codice come dati, ma se ci salto la CPU si

rifiuta di eseguirlo
➢

Aree di codice non scrivibili
➢ Non posso sovrascrivere codice esistente
© CINI – 2021

Rel. 15.03.2021

Bypass W⊕X / NX / DEP
40

➢

Code reuse: riusare codice esistente (e.g., ROP Return-oriented programming)

© CINI – 2021

Rel. 15.03.2021

ASLR
41

Address Space Layout Randomization: il layout virtuale
(= indirizzi) è randomizzato all’avvio del processo
➢ Quattro basi randomizzate:
➢

➢ Base dell’eseguibile
➢ Base dell’heap
➢ Base delle librerie

➢ Base (limite alto) dello stack

© CINI – 2021

Rel. 15.03.2021

Bypass ASLR
42

Information leak: vulnerabilità che fornisce
informazioni (in questo caso, indirizzi)
➢ ASLR randomizza solo la base
➢

➢ Offset relativi sono costanti!
➢ E.g., leako 0x5623 = base + 0x123
➢ Base = 0x5623 - 0x123 = 0x5500

➢ A = base + 0x42 = 0x5500 + 0x42 = 0x5542

© CINI – 2021

Rel. 15.03.2021

Stack canaries
43

➢

Stack canary: valore segreto sullo stack dopo variabili
locali ma prima del retaddr
➢ Randomizzato all’avvio del processo
➢ Inserito nel prologo, controllato nell’epilogo

➢

Prima di retaddr → siamo costretti a sovrascriverlo
➢ Non lo conosciamo, quindi il controllo nell’epilogo fallisce

© CINI – 2021

Rel. 15.03.2021

Bypass stack canaries
44

➢

Canary randomizzata all’avvio del processo
➢ Costante durante l’esecuzione

➢

Infoleak della canary da un qualunque stack frame
➢ Possiamo sovrascrivere con il valore corretto nell’overflow

© CINI – 2021

Rel. 15.03.2021

Exploit engineering
45

Spesso non abbiamo una vulnerabilità
immediatamente exploitabile
➢ Esempio: bug nel calcolo della size di un buffer
➢

➢ Gli facciamo calcolare una size errata
➢ Ci copia dei dati → buffer overflow

© CINI – 2021

Rel. 15.03.2021

Exploit engineering
46

➢

Esempio: programma tiene ptr a cui legge/scrive dati
utente, c’è overflow su buffer prima del ptr
➢ Usiamo overflow per sovrascrivere il ptr
➢ Il programma legge/scrive un indirizzo arbitrario!
➢ Arbitrary address read/write

© CINI – 2021

Rel. 15.03.2021

Exploit engineering
47

➢

Stiamo usando un bug per indurre una nuova
vulnerabilità che ci è più comoda per exploitation
➢ Una sorta di domino di bug

➢

Se “inscatolo” un pezzo di exploitation che mi
permette di fare una certa cosa, ho una primitiva
➢ Posso usarla senza più pensare a come funziona
➢ PC control, arbitrary R/W, leak dell’addr di un oggetto, …
© CINI – 2021

Rel. 15.03.2021

Andrea BIONDO
Università di Padova

Paolo Prinetto
President of CINI
Paolo.Prinetto@polito.it
Mob. +39 335 227529

Software Security 2
48

https://cybersecnatlab.it

