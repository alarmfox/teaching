#![no_std]
#![no_main]

use core::panic::PanicInfo;

#[panic_handler]
fn panic(_info: &'_ PanicInfo) -> ! {
    loop {}
}

#[unsafe(naked)]
#[unsafe(no_mangle)]
extern "C" fn _init() -> ! {
    core::arch::naked_asm!(
        // 1. Setup Stack Pointer
        // We use the LLVM assembler pseudo-instruction '=' to load the address
        // of the external linker symbol `_stack_top` into r0, then move it to sp.
        "ldr r0, =_stack_top",
        "mov sp, r0",

        // 2. Clear / Reset general-purpose registers (r0-r12)
        // Loading 0 into r0, then moving r0 into the rest is the most efficient way.
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

        // Clear the Link Register (lr). This is helpful for debuggers so they
        // know they have reached the bottom of the call stack.
        "mov lr, r0",

        // 3. Jump to main
        // We use Rust's `sym` to resolve the address of the main function safely
        "b {main}",
        main = sym main,
    )
}

fn main() -> ! {
    loop {}
}
