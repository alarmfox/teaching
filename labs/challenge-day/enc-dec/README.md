# DTLab Challenge: Encryption and Decryption

## Overview
This challenge is designed to be completed in approximately 90 minutes. It requires students to conduct independent research to solve problems related to cryptography and network security.

**Goal:** Reconstruct a private key to decrypt a message in `decryptme.txt`. An optional component involves utilizing exploits to gather system information.

**Flags:** 2.6, 3.5

## Phase 1: Network Discovery (8 pts)
Conduct reconnaissance to understand the target network infrastructure.

### Flag 1.1: Asset Enumeration (2 pts)
Determine your current network address and netmask.

### Flag 1.2: Host Identification (2 pts)
Identify the number of active hosts (excluding your local machine) within the network.

### Flag 1.3: Asset Details (3 pts) - Optional
Provide details regarding the operating systems of the identified assets.

### Flag 1.4: Network Infrastructure (1 pt)
What is the IP address of the switch?

## Phase 2: Network Credentials (14 pts)
Analyze network traffic to identify potential leaks and gain unauthorized access to a network device.

### Flag 2.1: Traffic Analysis (2 pts)
Exclude networking protocols. Identify any application-level traffic, its transport protocol, and the port number in use.

### Flag 2.2: Communication Analysis (1 pt) - Optional
Identify the sender and receiver of the message.

### Flag 2.3: Data Exfiltration (4 pts)
Examine the application message and derive the secret.

### Flag 2.4: Network Access (4 pts)
Utilize the secret discovered to gain access to a network device. Identify the user password and determine the hashing algorithm employed.

### Flag 2.5: Network Configuration (2 pts) - Optional
Identify the VLAN ID currently in use.

### Flag 2.6: Device Configuration (2 pts)
Retrieve the description of interface `f0/23`.

## Phase 3: Exploitation (15 pts)
Perform a vulnerability assessment and exploit a service on the target server to recover the second part of the key.

### Flag 3.1: Server Identification (1 pt)
What is the IP address of the server?

### Flag 3.2: Service Discovery (2 pts)
Enumerate the services running on the server.

### Flag 3.3: System Access (5 pts)
Identify a vulnerability in one of the services and establish a shell on the server. What is the content of `imin.txt`?

### Flag 3.4: Password Cracking (4 pts)
The hash found in `imin.txt` may correspond to the current user's password. Attempt to crack it.

### Flag 3.5: File Decryption (3 pts)
Locate and crack the password-protected file to reveal its contents.

## Technical Resources

### Cracking ZIP Files
```bash
fcrackzip -vul 1-4 <zip_file>
```

### Cryptographic Operations
**Generate RSA Key Pair:**
```bash
openssl genrsa -out private.key 4096
openssl rsa -in private.key -pubout -out public.key
```

**Encrypting Data:**
```bash
openssl pkeyutl -encrypt -pubin -inkey public.key -in plaintext.txt -out encrypted.txt
```

**Decrypting Data:**
```bash
openssl pkeyutl -decrypt -inkey private.key -in encrypted.txt -out decrypted.txt
```
