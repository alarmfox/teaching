use core::arch::asm;
use core::fmt::{self, Write};

/// An empty struct we will use to implement the Write trait
pub struct HostSerial;

impl Write for HostSerial {
    fn write_str(&mut self, s: &str) -> fmt::Result {
        // The semihosting operation code for printing a single character
        const SYS_WRITEC: usize = 0x03;

        for byte in s.bytes() {
            unsafe {
                // r0 holds the semihosting command
                // r1 holds a POINTER to the character we want to print
                asm!(
                    "bkpt 0xAB",
                    inout("r0") SYS_WRITEC => _,
                    in("r1") core::ptr::addr_of!(byte),
                    options(nostack, readonly, preserves_flags)
                );
            }
        }
        Ok(())
    }
}
