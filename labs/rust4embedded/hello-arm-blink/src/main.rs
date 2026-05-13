#![no_std]
#![no_main]

use core::fmt::Write;

mod led;
mod serial;

use core::panic::PanicInfo;

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}

// Import the stack top symbol from our linker script
unsafe extern "C" {
    static _stack_top: u32;
}

// Define the structure of the bare minimum Vector Table
//  GDB look at the vector table x/2xw 0x08000000
#[repr(C)]
struct VectorTable {
    initial_sp: &'static u32,
    reset_handler: unsafe extern "C" fn() -> !,
}

// Create the vector table and force it into the ".vector_table" section
#[unsafe(link_section = ".vector_table")]
#[unsafe(no_mangle)]
static VECTOR_TABLE: VectorTable = VectorTable {
    // We take the address of the linker symbol to give the hardware the stack top
    initial_sp: unsafe { &_stack_top },
    // We point the hardware directly to our initialization function
    reset_handler: _init,
};

// Our reset handler can now be a normal text section.
#[unsafe(link_section = ".text")]
#[unsafe(naked)]
#[unsafe(no_mangle)]
extern "C" fn _init() -> ! {
    core::arch::naked_asm!(
        // Notice we REMOVED the stack pointer setup here.
        // The Cortex-M hardware already did it by reading VECTOR_TABLE[0]!

        // 1. Clear / Reset general-purpose registers
        "movs r0, #0",
        "mov r1, r0",
        "mov r2, r0",
        "mov r3, r0",
        "mov r4, r0",
        "mov r5, r0",
        "mov r6, r0",
        "mov r7, r0",
        "mov r8, r0",
        "mov r9, r0",
        "mov r10, r0",
        "mov r11, r0",
        "mov r12, r0",
        "mov lr, r0",

        // 2. Jump to main
        "b {main}",
        main = sym main,
    )
}

#[unsafe(no_mangle)]
fn main() -> ! {
    let mut serial = serial::HostSerial;
    let a = 2 + 2;

    // Use the standard core::fmt macro to print strings and formatted numbers
    let _ = writeln!(serial, "Hello from bare-metal Rust! 2 + 2 = {}", a);

    // We instantiate LED3 (which is on pin 9).
    // This safely calls all the initialization code.
    let led3 = led::Led::new(9);

    // We can even initialize another LED easily now! (LED4 is on pin 8)
    let led4 = led::Led::new(8);
    loop {
        // Look how clean our main loop is now! No unsafe blocks required here.
        led3.toggle();
        led4.toggle();

        for _ in 0..100_000 {
            unsafe { core::arch::asm!("nop") };
        }
    }
}
