#include <stdio.h>

/*
 * Disable stack randomization:
 *
 * sudo sysctl -w kernel.randomize_va_space=0
 *
 * Compila con:
 *  gcc -O0 -g -std=c89 -m32 -fno-stack-protector -z execstack -no-pie hello.c -o hello
 *
 * Trigger segmentation fault:
 *
 * python3 -c "print('A' * 80)" | ./hello
 */
void hello() {
    char buffer[64];
    printf("Inserisci il tuo nome: ");
    /* Vulnerabilità: gets non controlla la dimensione dell'input */
    gets(buffer);
    printf("Ciao, %s!\n", buffer);
}

int main() {
    hello();
    return 0;
}
