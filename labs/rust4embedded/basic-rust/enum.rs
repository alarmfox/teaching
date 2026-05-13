// This enum has four variants.
// It is a "Sum Type" because a WebEvent is exactly ONE of these at a time.
enum WebEvent {
    PageLoad,                 // Variant 1: No data attached
    KeyPress(char),           // Variant 2: Holds a single character
    Click { x: i64, y: i64 }, // Variant 3: Holds an anonymous struct
}

fn handle_event(event: WebEvent) {
    // 3. Use 'match' to exhaustively check every possible variant.
    // Notice how we give variable names like 'c', 'x', and 'y' to pull
    // the data out of the variants right when we match them!
    match event {
        WebEvent::PageLoad => {
            println!("Action: The page has completely finished loading.");
        }
        WebEvent::KeyPress(c) => {
            println!("Action: The user pressed the '{}' key.", c);
        }
        WebEvent::Click { x, y } => {
            println!(
                "Action: The mouse was clicked at coordinates x={}, y={}.",
                x, y
            );
        }
    }
}

fn main() {
    // We instantiate different variants of the same enum type
    let event1 = WebEvent::PageLoad;
    let event2 = WebEvent::KeyPress('A');
    let event3 = WebEvent::Click { x: 100, y: 200 };

    handle_event(event1);
    handle_event(event2);
    handle_event(event3);
}

// This function might find a user, or it might not.
// It returns an Option, forcing the caller to handle the 'None' case.
fn find_user_name(id: u32) -> Option<String> {
    if id == 1 {
        Some(String::from("Alice")) // We found a value!
    } else {
        None // We didn't find a value. No null pointers here!
    }
}

fn main() {
    let user = find_user_name(2);

    // EXHAUSTIVE PATTERN MATCHING:
    // We use 'match' to check the variants. Rust will refuse to compile
    // if we forget to handle the 'None' case! This prevents crashes.
    match user {
        Some(name) => println!("Found user: {}", name),
        None => println!("User not found. Please try again."),
    }
}

// This function returns a Result.
// T (Success) is an f64. E (Error) is a String.
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err(String::from("Cannot divide by zero!")) // Returning the error as a value
    } else {
        Ok(a / b) // Returning the success value
    }
}

fn main() {
    let outcome = divide(10.0, 0.0);

    // EXHAUSTIVE PATTERN MATCHING:
    // Rust forces us to handle both the Ok and Err variants.
    // You cannot accidentally use the result of a failed calculation.
    match outcome {
        Ok(number) => println!("The result is {}", number),
        Err(error_msg) => println!("Calculation failed: {}", error_msg),
    }
}
