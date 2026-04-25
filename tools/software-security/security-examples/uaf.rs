struct User {
    name: String,
    action: fn(),
}

fn regular_greet() {
    println!("Hello, user! Welcome back.");
}

fn drop_shell() {
    println!("[!] Hijacked execution flow! Dropping shell...");
    // Rust can call system commands via std::process::Command,
    // but we won't even get that far.
}

fn main() {
    let user = User {
        name: String::from("Alice"),
        action: regular_greet,
    };

    // We explicitly free the memory by dropping the variable.
    // In Rust, `drop` takes ownership of `user`.
    drop(user);

    // Attempt to invoke the function pointer after the memory is freed.
    (user.action)();
}
