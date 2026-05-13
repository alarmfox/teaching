# Hello ARM - LED Blink & Semihosting

This project builds upon the bare-metal setup of `hello-arm` by adding practical embedded functionalities: blinking an LED and printing messages to the debugger console using semihosting. It demonstrates direct hardware interaction in Rust while maintaining memory safety through careful abstraction.

## Key Concepts

-   **Vector Table**: Explicitly defines and places the ARM Cortex-M vector table in Flash memory for proper startup.
-   **Direct Register Access**: Demonstrates how to directly manipulate microcontroller registers (e.g., GPIO, RCC) using raw pointers and `unsafe` blocks.
-   **Safe Abstraction over `unsafe`**: Encapsulates unsafe hardware access within safe Rust structs and methods (e.g., the `Led` struct).
-   **Semihosting**: A mechanism that allows code running on a target system to communicate with and use the I/O facilities of a host computer, enabling `println!`-like debugging on bare-metal.
-   **Busy-Wait Delay**: Simple delay loops using `asm!("nop")` for basic timing without timers.

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

-   `.cargo/config.toml`: Configures Cargo for the ARM target and linker script.
-   `build.rs`: Copies `memory.x` and sets linker search paths.
-   `memory.x`: The custom linker script for FLASH and RAM, including vector table placement.
-   `openocd.cfg`: OpenOCD configuration for ST-Link/V2 and STM32F303VC.
-   `src/main.rs`: The main application, containing the vector table, `_init`, `panic_handler`, and the LED blinking logic.
-   `src/led.rs`: Defines the `Led` struct and methods for safe GPIO manipulation.
-   `src/serial.rs`: Implements `core::fmt::Write` for semihosting-based serial output.

## How to Build

Navigate to the `hello-arm-blink` directory and build the project:

```bash
cd hello-arm-blink
cargo build --target thumbv7em-none-eabihf
```

This will produce an ELF executable in `target/thumbv7em-none-eabihf/debug/hello-arm-blink`.

## How to Inspect the Binary

You can inspect the generated ELF file using `cargo-objdump`:

```bash
cargo objdump --target thumbv7em-none-eabihf --bin hello-arm-blink -- -d -j .text
```

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
                     target/thumbv7em-none-eabihf/debug/hello-arm-blink
    ```
    This sequence connects GDB to OpenOCD, resets the target, loads the compiled binary, and then resumes execution.

    You should observe LED3 and LED4 on your board blinking. Additionally, if your debugger console is configured to display semihosting output (e.g., in `minicom` or your IDE's debug console), you will see "Hello from bare-metal Rust!" messages.
