// We hide the memory addresses inside the module so main() can't mess with them.
const RCC_AHBENR: *mut u32 = 0x4002_1014 as *mut u32;
const GPIOE_MODER: *mut u32 = 0x4800_1000 as *mut u32;
const GPIOE_ODR: *mut u32 = 0x4800_1014 as *mut u32;

// A struct to represent a single LED on Port E
pub struct Led {
    pin: u8,
}

impl Led {
    /// Initializes Port E and configures the specific pin as an output.
    pub fn new(pin: u8) -> Self {
        unsafe {
            // 1. Enable the clock for GPIO Port E
            let mut ahbenr = core::ptr::read_volatile(RCC_AHBENR);
            ahbenr |= 1 << 21;
            core::ptr::write_volatile(RCC_AHBENR, ahbenr);

            // 2. Configure the specific pin as an output (01)
            let mut moder = core::ptr::read_volatile(GPIOE_MODER);
            let shift = pin * 2; // Each pin takes 2 bits in MODER
            moder &= !(0b11 << shift); // Clear bits
            moder |= 0b01 << shift; // Set to output
            core::ptr::write_volatile(GPIOE_MODER, moder);
        }

        // Return the constructed Led struct
        Self { pin }
    }

    /// Toggles the LED on and off. Notice this function is completely SAFE!
    pub fn toggle(&self) {
        unsafe {
            let mut odr = core::ptr::read_volatile(GPIOE_ODR);
            odr ^= 1 << self.pin;
            core::ptr::write_volatile(GPIOE_ODR, odr);
        }
    }
}
