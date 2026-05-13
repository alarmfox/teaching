# Security Examples

This directory contains various security vulnerability examples in C and Rust, demonstrating common pitfalls and how to exploit or prevent them. Each subdirectory has its own `README.md` with specific instructions.

## Subdirectories

-   **`buffer-overflow/`**: Demonstrates a classic stack-based buffer overflow in C and its exploitation using `pwntools`.
    -   [Read `buffer-overflow/README.md`](./buffer-overflow/README.md)

-   **`stack_overflow.c`**: A simple C program demonstrating how `gets()` can lead to a stack overflow, overwriting adjacent variables.
    -   **Compilation**: `gcc -std=c89 -g -O0 -fno-stack-protector stack_overflow.c -o stack-overflow`
    -   **Execution**: Run `./stack-overflow` and provide input longer than 8 characters (e.g., `AAAAAAAAA!`). Observe how `is_admin` can be set to 1.

-   **`stack_overflow.rs`**: A Rust example demonstrating how Rust's memory safety prevents the same stack overflow vulnerability found in the C example.
    -   **Compilation**: `rustc stack_overflow.rs`
    -   **Execution**: Run `./stack_overflow`. The program will safely handle input and prevent overwriting `is_admin`.

-   **`uaf.c`**: Demonstrates a Use-After-Free (UAF) vulnerability in C, where memory is accessed after being freed, potentially leading to arbitrary code execution.
    -   **Compilation**: `gcc -g uaf.c -o uaf`
    -   **Execution**: Run `./uaf`. Observe how the program's execution flow is hijacked to `drop_shell` after a free operation.

-   **`uaf.rs`**: A Rust example showing how Rust's ownership and borrowing system prevents Use-After-Free vulnerabilities at compile time.
    -   **Compilation**: `rustc uaf.rs`
    -   **Execution**: Attempting to compile `uaf.rs` will result in a compile-time error, preventing the UAF vulnerability.

## General Compilation for C Examples

For C examples, you typically use `gcc`. Basic compilation without specific security flags:

```bash
gcc your_program.c -o your_program
```

However, for security examples, specific flags are often used to disable modern protections (like `-fno-stack-protector`, `-z execstack`, `-no-pie`) to make the vulnerabilities easier to observe and exploit.

## General Compilation for Rust Examples

For Rust examples, you use the Rust compiler `rustc`:

```bash
rustc your_program.rs
```
