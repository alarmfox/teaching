#include <stdio.h>

/*
 * Disabilita la randomizzazione dello stack:
 *
 * sudo sysctl -w kernel.randomize_va_space=0
 *
 * Compila con:
 *  gcc -m32 -fno-stack-protector -z execstack -no-pie hello.c hello
 */

void hello() {
    char buffer[64];
    printf("Inserisci il tuo nome: ");
    // Vulnerabilità: gets non controlla la dimensione dell'input
    gets(buffer);
    printf("Ciao, %s!\n", buffer);
}

int main() {
    char *p = malloc(10000);

        free(p);
    hello();
    return 0;
}
