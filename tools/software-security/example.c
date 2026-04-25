#include <stdio.h>

/* Compila: gcc -std=c89 -O0 -g example.c */
int main() {
    /* Allocazione di un buffer di 10 byte sullo Stack */
    char buffer[10];

    printf("Inserisci l'input:\n");

    /* gets() legge da standard input fino a incontrare un newline */
    gets(buffer);

    printf("Hai inserito: %s\n", buffer);
    return 0;
}
