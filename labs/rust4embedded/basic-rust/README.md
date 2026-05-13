# Basic Rust Examples

This directory contains fundamental Rust programming examples, covering core concepts such as variables, ownership, borrowing, enums, and scope. These examples are designed to be simple and illustrative, helping beginners understand the basic syntax and behavior of Rust.

## Examples

-   **`hello.rs`**: The classic "Hello, World!" program.
    -   **Compilation**: `rustc hello.rs`
    -   **Execution**: `./hello`

-   **`scope.rs`**: Demonstrates variable scope and how variables are dropped when they go out of scope.
    -   **Compilation**: `rustc scope.rs`
    -   **Execution**: `./scope`

-   **`borrow.rs`**: Illustrates Rust's ownership and borrowing rules, including mutable and immutable references.
    -   **Compilation**: `rustc borrow.rs`
    -   **Execution**: `./borrow`

-   **`enum.rs`**: Shows how to define and use enums, including pattern matching with `match`.
    -   **Compilation**: `rustc enum.rs`
    -   **Execution**: `./enum`

## General Compilation and Execution

To compile a single Rust file (`.rs`):

```bash
rustc your_file.rs
```

This will produce an executable binary in the same directory. To run it:

```bash
./your_file
```
