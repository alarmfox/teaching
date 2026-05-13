# Buffer Overflow Example

This directory contains a classic stack-based buffer overflow example in C and an exploit script in Python using `pwntools`.

## 1. Environment Setup

For this exploit to work, you need to disable Address Space Layout Randomization (ASLR) and allow core dumps. It is recommended to use a **Kali Linux VM**.

### Disable ASLR
```bash
sudo sysctl -w kernel.randomize_va_space=0
```

### Enable Core Dumps
```bash
ulimit -c unlimited
```

### Install Pwntools and Pwndbg
```bash
sudo apt-get update
sudo apt-get install python3-pwntools pwndbg
```

## 2. Compile the Vulnerable Program

Compile `hello.c` with flags that disable modern security protections (Stack Canary, NX Stack, PIE):

```bash
gcc -O0 -g -std=c89 -m32 -fno-stack-protector -z execstack -no-pie hello.c -o hello
```

## 3. Manual Investigation with `pwndbg` and `pwn cyclic`

You can use `pwndbg` (a GDB plugin) and the `pwn cyclic` utility to find the offset to the EIP.

1.  **Generate a cyclic pattern:**
    ```bash
    pwn cyclic 150
    # Copy the output, e.g., 'aaaabaaacaaadaaaeaaaf...'
    ```
2.  **Run in GDB:**
    ```bash
    gdb ./hello
    pwndbg> r
    # When prompted "Inserisci il tuo nome:", paste the cyclic pattern.
    ```
3.  **Find the offset:**
    When it crashes, look at the value in `EIP`. For example, if EIP is `0x61616161` (AAAA), use `pwn cyclic -l 0x61616161` to find the exact offset.

## 4. Understanding the Stack Layout

A successful buffer overflow often involves carefully crafting a payload to overwrite the return address on the stack. The diagram below illustrates the conceptual layout:

```
+------------------+  <-- Higher Address / Stack Top (Buffer grows downwards)
|      BUFFER      |
|    (e.g., 'A's)  |
|                  |
+------------------+
|     ...filler    |
|                  |
+------------------+
|   RETURN ADDRESS |  <-- This is what we overwrite!
+------------------+
|     NOP SLED     |  <-- NOP instructions (0x90) for reliability
|                  |
+------------------+
|    SHELLCODE     |  <-- Our malicious code (e.g., spawn a shell)
+------------------+  <-- Lower Address / Stack Bottom
```

## 5. Automated Exploit

The `exploit.py` script automates the process:
1.  Triggers a crash to locate the real Stack Pointer (ESP) from the core dump.
2.  Calculates the return address.
3.  Generates a payload containing a NOP sled and shellcode.
4.  Launches `/bin/sh`.

**Run the exploit:**
```bash
python3 exploit.py
```
