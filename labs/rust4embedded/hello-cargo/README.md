# Hello Cargo

This directory demonstrates a basic Rust project managed by Cargo, Rust's build system and package manager. Cargo is essential for managing dependencies, compiling code, running tests, and generating documentation for Rust projects.

## Project Structure

-   `Cargo.toml`: The Cargo manifest file. It contains metadata about your project (name, version, authors, edition) and its dependencies.
## `src/main.rs`

This file introduces basic Rust concepts like types, variables, structs, and traits. 

**Note**: The file contains a commented-out section at the end titled "Incorrect code". This code is intentionally written to violate Rust's borrow checker rules and will not compile. It serves as an educational example of common ownership and borrowing errors.


## How to Use

1.  **Build the project**:
    ```bash
    cargo build
    ```
    This command compiles your project and creates an executable in the `target/debug/` directory.

2.  **Run the project**:
    ```bash
    cargo run
    ```
    This command compiles your project (if necessary) and then runs the executable.

3.  **Check for errors (without compiling)**:
    ```bash
    cargo check
    ```
    This command quickly checks your code for errors without producing an executable.

4.  **Build for release (optimized)**:
    ```bash
    cargo build --release
    ```
    This compiles your project with optimizations, producing a faster executable in `target/release/`.

## `Cargo.toml` Explained

```toml
[package]
name = "hello-cargo"
version = "0.1.0"
edition = "2024"

[dependencies]
# Add your project dependencies here
# For example:
# rand = "0.8.5"
```

-   `[package]`: Defines the package metadata.
-   `name`: The name of your package.
-   `version`: The current version of your package.
-   `edition`: The Rust edition to use for the package.
-   `[dependencies]`: Where you list external crates (libraries) that your project depends on. Cargo will automatically download and compile these dependencies.
