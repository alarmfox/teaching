# Password Manager

This directory contains a Rust project implementing a secure command-line password manager. It demonstrates several key Rust concepts including type states for enhanced security, robust error handling, and `clap` for command-line interface parsing. This tool uses `argon2` for master password hashing and `chacha20poly1305` for symmetric encryption of stored passwords.

## Features

-   **Secure Master Password**: Uses Argon2 for strong master password hashing.
-   **Encrypted Storage**: Passwords are encrypted using ChaCha20Poly1305 before being written to disk.
-   **Typestate Pattern**: Demonstrates how Rust's type system can enforce security invariants at compile time (e.g., preventing access to decrypted passwords without explicit unlocking).
-   **CLI Interface**: Easy-to-use command-line interface for managing passwords.

## Project Structure

-   `Cargo.toml`: The Cargo manifest file, defining project metadata and dependencies.
-   `src/main.rs`: The main source file containing all the password manager's logic, including CLI parsing, encryption/decryption, and password management.

## How to Use

First, navigate to the `password-manager` directory:

```bash
cd password-manager
```

### 1. Build the Project

Compile the project using Cargo:

```bash
cargo build
```

This will create an executable named `passman` (as defined in `Cargo.toml` and `main.rs`) in the `target/debug/` directory. For an optimized release build, use `cargo build --release`.

### 2. Initialize a New Password Store

Before you can add passwords, you need to initialize a new password database. This command will prompt you to set a master password.

```bash
cargo run -- init
```

**Example:**
```bash
cargo run -- init --file my_passwords.db
# Insert master password: [type your master password]
# Confirm master password: [re-type your master password]
# Database initialized successfully.
```

By default, the database file will be `password.db` in the current directory. You can specify a different file path using the `--file` (or `-f`) option.

### 3. Add a Password

To add a new password for a service or account, use the `add` command. You will be prompted for your master password and then for the new password.

```bash
cargo run -- add --key <service_name>
```

**Example:**
```bash
cargo run -- add --key google
# Insert master password: [your master password]
# Insert password for 'google': [your google password]
# Confirm password for 'google': [re-type your google password]
# Added password for 'google'.
```

Use the `--file` option if your database is not `password.db`.

### 4. List Passwords

#### List Keys Only

To see a list of all stored service names (keys) without revealing the passwords, use the `list` command without the `--show` flag. This does not require your master password.

```bash
cargo run -- list
```

**Example:**
```bash
cargo run -- list
# google: ********
# github: ********
```

#### List Keys and Passwords

To view both the service names and their corresponding passwords, use the `list` command with the `--show` flag. This will prompt you for your master password to decrypt the entries.

```bash
cargo run -- list --show
```

**Example:**
```bash
cargo run -- list --show
# Insert master password: [your master password]
# google: mysecretgooglepass
# github: mygithubpass123
```

### 5. Delete a Password

To remove a password entry, use the `delete` command. You will be prompted for your master password.

```bash
cargo run -- delete --key <service_name>
```

**Example:**
```bash
cargo run -- delete --key google
# Insert master password: [your master password]
# Deleted password for 'google'.
```

### 6. Count Stored Passwords

To get a count of how many password entries are stored in your database, use the `count` command. This does not require your master password.

```bash
cargo run -- count
```

**Example:**
```bash
cargo run -- count
# Stored passwords: 2
```

## Key Concepts Demonstrated

-   **`clap` crate**: Powerful and easy-to-use library for parsing command-line arguments.
-   **`rpassword` crate**: Securely prompts for passwords without echoing input to the terminal.
-   **`argon2` crate**: Industry-standard password hashing algorithm for secure storage of the master password.
-   **`chacha20poly1305` crate**: A modern authenticated encryption algorithm used to encrypt and decrypt stored passwords.
-   **Typestates**: The `PasswordManager` struct is designed with typestates (`Locked` and `Unlocked`) to ensure that sensitive operations (like decrypting and listing cleartext passwords) can only be performed when the manager is explicitly in the `Unlocked` state.
