#![no_main]
#![no_std]

use hello_arm_hal as _; // global logger + panicking-behavior + memory layout

use core::cell::RefCell;

use cortex_m::{asm, peripheral::NVIC};

use critical_section::Mutex;
use stm32f3xx_hal::{
    gpio::{self, Edge, Input, Output, PushPull},
    interrupt, pac,
    prelude::*,
    timer::{Event, Timer},
};

// --- Button LED Setup (PE9) ---
type LedPin = gpio::PE9<Output<PushPull>>;
static LED: Mutex<RefCell<Option<LedPin>>> = Mutex::new(RefCell::new(None));

// --- Button Setup (PA0) ---
type ButtonPin = gpio::PA0<Input>;
static BUTTON: Mutex<RefCell<Option<ButtonPin>>> = Mutex::new(RefCell::new(None));

// --- Timer Blinking LED Setup (PE10) ---
type BlinkLedPin = gpio::PE10<Output<PushPull>>;
static BLINK_LED: Mutex<RefCell<Option<BlinkLedPin>>> = Mutex::new(RefCell::new(None));

// --- Timer Setup (TIM2) ---
type BlinkTimer = Timer<pac::TIM2>;
static TIMER: Mutex<RefCell<Option<BlinkTimer>>> = Mutex::new(RefCell::new(None));

// When the user button is pressed. The north LED will toggle.
#[cortex_m_rt::entry]
fn main() -> ! {
    // Getting access to registers we will need for configuration.
    let device_peripherals = pac::Peripherals::take().unwrap();

    let mut rcc = device_peripherals.RCC.constrain();
    let mut syscfg = device_peripherals.SYSCFG.constrain(&mut rcc.apb2);
    let mut exti = device_peripherals.EXTI;
    let mut gpioe = device_peripherals.GPIOE.split(&mut rcc.ahb);
    let mut gpioa = device_peripherals.GPIOA.split(&mut rcc.ahb);
    let clocks = rcc
        .cfgr
        .freeze(&mut device_peripherals.FLASH.constrain().acr);

    let mut led = gpioe
        .pe9
        .into_push_pull_output(&mut gpioe.moder, &mut gpioe.otyper);
    // Turn the led on so we know the configuration step occurred.
    led.toggle().expect("unable to toggle led in configuration");

    // Move the ownership of the led to the global LED
    critical_section::with(|cs| *(LED.borrow(cs).borrow_mut()) = Some(led));

    let mut led = gpioe
        .pe10
        .into_push_pull_output(&mut gpioe.moder, &mut gpioe.otyper);
    // Turn the led on so we know the configuration step occurred.
    led.toggle().expect("unable to toggle led in configuration");
    // Move the ownership of the led to the global LED
    critical_section::with(|cs| BLINK_LED.borrow(cs).replace(Some(led)));

    // Configuring the user button to trigger an interrupt when the button is pressed.
    let mut user_button = gpioa
        .pa0
        .into_pull_down_input(&mut gpioa.moder, &mut gpioa.pupdr);
    syscfg.select_exti_interrupt_source(&user_button);
    user_button.trigger_on_edge(&mut exti, Edge::Rising);
    user_button.enable_interrupt(&mut exti);
    let interrupt_num = user_button.interrupt(); // hal::pac::Interrupt::EXTI0

    // Moving ownership to the global BUTTON so we can clear the interrupt pending bit.
    critical_section::with(|cs| *BUTTON.borrow(cs).borrow_mut() = Some(user_button));

    // 4. CONFIGURE TIMER (TIM2)
    // ==========================================
    let mut timer = Timer::new(device_peripherals.TIM2, clocks, &mut rcc.apb1);

    unsafe {
        NVIC::unmask(interrupt_num);
        NVIC::unmask(timer.interrupt());
    };

    timer.enable_interrupt(Event::Update);
    // Start a timer which fires regularly to wake up from `asm::wfi`
    timer.start(500.milliseconds());
    // Put the timer in the global context.
    critical_section::with(|cs| {
        TIMER.borrow(cs).replace(Some(timer));
    });

    loop {
        asm::wfi();
    }
}

// Button Pressed interrupt.
// The exti# maps to the pin number that is being used as an external interrupt.
// See page 295 of the stm32f303 reference manual for proof:
// http://www.st.com/resource/en/reference_manual/dm00043574.pdf
//
// This may be called more than once per button press from the user since the button may not be debounced.
#[interrupt]
fn EXTI0() {
    defmt::println!("Button Pressed!");
    critical_section::with(|cs| {
        // Toggle the LED
        LED.borrow(cs)
            .borrow_mut()
            .as_mut()
            .unwrap()
            .toggle()
            .unwrap();

        // Clear the interrupt pending bit so we don't infinitely call this routine
        BUTTON
            .borrow(cs)
            .borrow_mut()
            .as_mut()
            .unwrap()
            .clear_interrupt();
    })
}

#[interrupt]
fn TIM2() {
    critical_section::with(|cs| {
        // 1. Toggle the blinking LED
        BLINK_LED
            .borrow(cs)
            .borrow_mut()
            .as_mut()
            .unwrap()
            .toggle()
            .unwrap();

        // 2. Clear the timer's update event flag
        // If we don't do this, the interrupt will continuously fire, starving the main loop!
        TIMER
            .borrow(cs)
            .borrow_mut()
            .as_mut()
            .unwrap()
            .clear_event(Event::Update);
    })
}
