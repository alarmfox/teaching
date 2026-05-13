fn main() {
    // 1. s1 is created and becomes the owner of the String "hello"
    let s1 = String::from("hello");

    // 2. We assign s1 to s2.
    // In Rust, this means ownership MOVES from s1 to s2.
    // s1 is now considered empty/invalid.
    let s2 = s1;

    // 3. If we try to print s1, Rust will throw a COMPILE ERROR!
    // println!("{}, world!", s1);

    // 4. We can only print s2, because s2 is the new owner.
    println!("{}, world!", s2);
}

fn main() {
    // 1. s1 is created and becomes the owner of the String "hello"
    let s1 = String::from("hello");

    // 2. Borrow s1. We take a read-only reference. s1 is still the owner
    let s2 = &s1;

    // or we can clone and create 2 distinct memory areas. s1 and s2 are both valid
    let s2 = s1.clone();

    // 3. Use the reference
    println!("{}, world!", s1);

    // 4. We can only print s2, because s2 is the new owner.
    println!("{}, world!", s2);
}

fn main() {
    let my_text = String::from("Hello");

    // We pass 'my_text' into the function. Ownership MOVES into the function.
    let returned_text = take_and_modify(my_text);

    // println!("{}", my_text); // COMPILE ERROR! my_text no longer owns the data.

    // We must use the returned variable because it is the new owner.
    println!("Final result: {}", returned_text);
}

// This function takes ownership of 's'. We make 's' mutable so we can change it.
fn take_and_modify(mut s: String) -> String {
    s.push_str(" World"); // Modifies the string

    s // We MUST return 's' to give ownership back to the caller!
}

fn main() {
    // We must declare the original variable as mutable (mut)
    let mut my_text = String::from("Hello");

    // We pass a MUTABLE REFERENCE to the function using '&mut'
    // Ownership does NOT move. The function is just borrowing it.
    modify_in_place(&mut my_text);

    // This works perfectly! We never lost ownership of my_text.
    println!("Final result: {}", my_text);
}

// This function takes a mutable reference to a String.
// It does not take ownership, and it doesn't need to return anything.
fn modify_in_place(s: &mut String) {
    s.push_str(" World"); // Modifies the original string directly
}

fn main() {
    // We must declare the original variable as mutable (mut)
    let mut my_text = String::from("Hello");

    // Create another temporary mutable reference
    let mut temp_ref = &mut my_text;

    // We pass a MUTABLE REFERENCE to the function using '&mut'
    // Ownership does NOT move. The function is just borrowing it.
    modify_in_place(&mut my_text);

    // Use the temporary reference created before here.
    // This gives an error: we have 2 mutable reference active
    temp_ref.push_str("aaaa");

    // This works perfectly! We never lost ownership of my_text.
    println!("Final result: {}", my_text);
}

// This function takes a mutable reference to a String.
// It does not take ownership, and it doesn't need to return anything.
fn modify_in_place(s: &mut String) {
    s.push_str(" World"); // Modifies the original string directly
}
