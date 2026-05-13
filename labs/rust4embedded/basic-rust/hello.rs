fn main() {
    let a: &str = "Hello world";
    let n: i32 = 10;

    println!("{} {}", a, n); // Prints hello world and 10

    /* We can rename variables. The one with the closer scope wins */
    let n: String = String::from(a);

    /* The type of copy will be automatically inferred by the the rust compiler (String) */
    let copy = n.clone();

    /* function ending in ! are not functions but macros. Rust has a meta-language */
    println!("{} {}", a, n); // Prints hello world twice
}
