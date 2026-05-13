# Hello ARM (Embedded Rust Bare-Metal)

This project is a minimal bare-metal "Hello, World!" for ARM Cortex-M microcontrollers using Rust. It demonstrates how to set up a basic embedded Rust project without relying on a Hardware Abstraction Layer (HAL) or standard library, focusing on the very core of embedded development.

## Key Concepts

-   **`no_std` and `no_main`**: Rust features for bare-metal development, indicating no standard library usage and a custom entry point.
-   **Linker Script (`memory.x`)**: Defines the memory layout of the target microcontroller, specifying RAM regions and stack configuration.
-   **Naked Assembly Entry Point (`_init`)**: Manually initializes the stack pointer and clears registers before jumping to the Rust `main` function, as required by the ARM architecture's calling convention.
-   **Panic Handler**: A mandatory function for `no_std` applications that defines what happens on a panic.
-   **Cargo Build Script (`build.rs`)**: Automates the inclusion of the custom linker script into the build process.
-   **Target Configuration (`.cargo/config.toml`)**: Specifies the ARM target and linker arguments.

## Prerequisites

1.  **Rust Toolchain**: Ensure you have Rust installed via `rustup`.
2.  **ARM Target**: Add the `thumbv7em-none-eabihf` target:
    ```bash
    rustup target add thumbv7em-none-eabihf
    ```
3.  **`cargo-binutils`**: For inspecting the compiled binary.
    ```bash
    cargo install cargo-binutils
    rustup component add llvm-tools-preview
    ```
4.  **OpenOCD**: For flashing and debugging your STM32 board with an ST-Link/V2.
    ```bash
    sudo apt-get install openocd
    ```
5.  **`arm-none-eabi-gdb`**: The GNU Debugger for ARM Cortex-M targets.
    ```bash
    sudo apt-get install build-essential gcc-arm-none-eabi
    ```

## Project Structure

-   `.cargo/config.toml`: Configures Cargo to use the ARM target and custom linker script.
-   `build.rs`: Copies `memory.x` and sets linker search paths.
-   `memory.x`: The custom linker script.
-   `openocd.cfg`: OpenOCD configuration for ST-Link/V2 and STM32F303VC.
-   `src/main.rs`: Contains the `_init` assembly entry point, `panic_handler`, and an infinite loop `main` function.

## How to Build

Navigate to the `hello-arm` directory and build the project:

```bash
cd hello-arm
cargo build --target thumbv7em-none-eabihf
```

This will produce an ELF executable in `target/thumbv7em-none-eabihf/debug/hello-arm`.

## How to Inspect the Binary

You can inspect the generated ELF file using `cargo-objdump` (from `cargo-binutils`):

```bash
cargo objdump --target thumbv7em-none-eabihf --bin hello-arm -- -d -j .text
```

Look for the `_init` and `main` functions to see the compiled assembly.

## How to Run (Flashing and Debugging with OpenOCD)

To run this on an actual STM32F303VC development board with an ST-Link/V2 debugger:

1.  **Connect your STM32F303VC board** to your computer via the ST-Link/V2.

2.  **Start OpenOCD** in a separate terminal using the provided configuration file:
    ```bash
    openocd -f openocd.cfg
    ```
    Ensure you see output indicating successful connection to the target.

3.  **Open a GDB session** in another terminal:
    ```bash
    arm-none-eabi-gdb -ex "target remote :3333" \ 
                     -ex "monitor reset halt" \ 
                     -ex "load" \ 
                     -ex "monitor resume" \ 
                     target/thumbv7em-none-eabihf/debug/hello-arm
    ```
    This sequence connects GDB to OpenOCD, resets the target, loads the compiled binary, and then resumes execution.

This `hello-arm` project will simply enter an infinite loop in the `main` function, effectively doing nothing but running on the microcontroller.
