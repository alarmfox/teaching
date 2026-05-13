use std::io;

fn main() {
    let mut is_admin = false;
    // Rust's String is dynamically sized and heap-allocated
    let mut password = String::new();

    println!("Enter password: ");
    // read_line automatically grows the String to fit the input safely
    io::stdin().read_line(&mut password).unwrap();

    if password.trim() == "secret" {
        is_admin = true;
    }

    if is_admin {
        println!("Access Granted! Admin privileges unlocked.");
    } else {
        println!("Access Denied.");
    }
}
