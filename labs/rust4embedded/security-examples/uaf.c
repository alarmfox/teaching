#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// The function we WANT to run
void regular_greet() {
    printf("Hello, user! Welcome back.\n");
}

// The function the ATTACKER wants to run
// In a real word attack, this function can be byte encoded in a malicious payload.
// There tools to do this for example "msfvenom".
void drop_shell() {
    printf("[!] Hijacked execution flow! Dropping shell...\n");
    system("/bin/sh");
}

// The victim struct containing a function pointer
struct User {
    char name[32];
    void (*action)(); // Function pointer
};

int main() {
    // 1. Normal program execution
    struct User *user = malloc(sizeof(struct User));
    strcpy(user->name, "Alice");
    user->action = regular_greet;

    /* Things happen and the pointer is not needed anymore. */
    user->action();

    free(user);
    user = NULL;

    printf("Free happened");

    // 2. THE ATTACK: An attacker triggers an allocation of the exact same size.
    // In a real-world scenario
    // The memory allocator will likely reuse the exact block we just freed.
    long *attacker_data = malloc(sizeof(struct User));

    // The attacker fills the memory chunk.
    // The struct is 40 bytes (32 bytes for name, 8 bytes for pointer on 64-bit).
    // They put garbage in the first 32 bytes, and the address of `drop_shell` at the end.
    attacker_data[0] = 0x41414141; // 'AAAA'
    attacker_data[1] = 0x41414141; // 'AAAA'
    attacker_data[2] = 0x41414141; // 'AAAA'
    attacker_data[3] = 0x41414141; // 'AAAA'
    attacker_data[4] = (long)drop_shell; // OVERWRITE THE FUNCTION POINTER!

    // 3. VULNERABILITY TRIPPED: The dangling pointer is used
    printf("Executing user action...\n");
    user->action(); // The program blindly jumps to drop_shell!

    return 0;
}

void regular_greet() {
    printf("Hello, user! Welcome back.\n");
}

struct User {
    char name[32];
    void (*action)(); // Function pointer
};

int main() {
    struct User *user = malloc(sizeof(struct User));
    strcpy(user->name, "Alice");
    user->action = regular_greet;

    user->action();

    free(user);

    /* For simplicity this is placed here. But the allocation can be
     * triggered in another part of the program (far away) */
    long *attacker_data = malloc(sizeof(struct User));

    attacker_data[0] = 0x41414141; // 'AAAA'
    attacker_data[1] = 0x41414141; // 'AAAA'
    attacker_data[2] = 0x41414141; // 'AAAA'
    attacker_data[3] = 0x41414141; // 'AAAA'
    attacker_data[4] = (long)drop_shell; // OVERWRITE THE FUNCTION POINTER!

    /* The program uses the same pointer to call action after calling free */
    printf("Executing user action...\n");
    user->action(); // The program blindly jumps to drop_shell!

    return 0;
}
