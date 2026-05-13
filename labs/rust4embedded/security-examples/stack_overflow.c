#include <stdio.h>
#include <string.h>

/* Compile this program with
 *
 * gcc -std=c89 -g -O0 -fno-stack-protector stack_overflow.c -o stack-overflow
 *
 * Generate 8 'A':  python -c 'print("A" * 8)'
 *
 * Use "AAAAAAAA!" as input
 * */
int main() {
    /* Memory layout: 'is_admin' is often placed right next to 'password' on the stack */
    int is_admin = 0;
    char password[8];

    printf("Enter password: ");
    /* VULNERABILITY: gets() doesn't check the length of the input! */
    gets(password);

    if (strcmp(password, "secret") == 0) {
        is_admin = 1;
    }

    if (is_admin) {
        printf("Access Granted! Admin privileges unlocked.\n");
    } else {
        printf("Access Denied.\n");
    }
    return 0;
}
