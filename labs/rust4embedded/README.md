# Rust for Embedded Systems Workshop

Welcome to the Rust for Embedded Systems workshop! This repository contains a series of examples designed to introduce you to Rust programming, its application in embedded contexts, and fundamental security concepts.

Each subdirectory represents a distinct module or project, complete with its own `README.md` file that provides specific instructions, compilation commands, and explanations.

## Repository Structure

-   **`basic-rust/`**: Introduces fundamental Rust concepts such as variables, ownership, borrowing, and enums.
    -   [Read `basic-rust/README.md`](./basic-rust/README.md)

-   **`hello-cargo/`**: Demonstrates how to use Cargo, Rust's build system and package manager, for basic project management.
    -   [Read `hello-cargo/README.md`](./hello-cargo/README.md)

-   **`password-manager/`**: A practical command-line application showcasing Rust's features for building CLI tools.
    -   [Read `password-manager/README.md`](./password-manager/README.md)

-   **`hello-arm/`**: Your first steps into embedded Rust on ARM microcontrollers. Focuses on setting up a basic embedded project.
    -   [Read `hello-arm/README.md`](./hello-arm/README.md) *(To be created)*

-   **`hello-arm-blink/`**: Builds upon `hello-arm` to demonstrate basic GPIO manipulation for blinking an LED.
    -   [Read `hello-arm-blink/README.md`](./hello-arm-blink/README.md) *(To be created)*

-   **`hello-arm-hal/`**: Explores the use of Hardware Abstraction Layers (HALs) in embedded Rust for more ergonomic peripheral control.
    -   [Read `hello-arm-hal/README.md`](./hello-arm-hal/README.md) *(To be created)*

-   **`security-examples/`**: Contains various security vulnerability examples in C and Rust, highlighting common pitfalls and Rust's memory safety guarantees.
    -   [Read `security-examples/README.md`](./security-examples/README.md)

## General Workshop Guidance

### Rust Toolchain Installation

If you haven't already, install the Rust toolchain using `rustup`:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### Embedded Toolchain Setup (for `hello-arm*` projects)

For embedded projects, you will typically need additional targets and tools. Refer to the specific `README.md` files in the `hello-arm*` directories for detailed setup instructions, including `probe-rs` or `openocd`.

### Compiling and Running Rust Projects

-   **Single file (`.rs`):**
    ```bash
    rustc your_program.rs
    ./your_program
    ```

-   **Cargo project (with `Cargo.toml`):**
    ```bash
    cargo build       # Compile the project
    cargo run         # Compile and run the project
    cargo test        # Run tests
    cargo build --release # Build an optimized release version
    ```

### Compiling C Examples

For C examples, `gcc` is the standard compiler. Specific compilation flags are often provided within each example's `README.md` to demonstrate vulnerabilities by disabling modern security features.

```bash
gcc your_program.c -o your_program
./your_program
```

Enjoy the workshop!
