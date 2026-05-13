/* This code contains an introduction to Rust basics. Types, variables*/

/* Derive we are asking to the compiler to generate some code for us. For example, Debug and Clone
 * functions for this struct. The implementations will call recursively the same function for each
 * member */
#[derive(Debug, Clone)]
struct Player {
    name: String,
    age: u8,
    alive: bool,
}

/* Add operations on struct with "impl" blocks. Impl blocks can add simple operations or
 * implement a "trait" (like interfaces) */
impl Player {
    /* By default everything is private */
    fn hi(&self) {
        /* In rust everything is an expression that can generate a value.
         * Expressions MUST generate value of the same type */
        let str = if self.alive {
            /* Note no ";" */
            format!("{} - {}, alive", self.name, self.age)
        } else {
            /* Note no ";" */
            format!("{} - {}, dead", self.name, self.age)
        };

        println!("{}", str);
    }
}

/* Implement for example the Default trait */
impl Default for Player {
    fn default() -> Self {
        Self {
            name: Default::default(),
            age: 18,
            alive: true,
        }
    }
}

/* Functions and modules marked with test can be executed with cargo test*/
#[test]
fn test_default() {
    let p = Player::default();
    assert_eq!(p.name.len(), 0);
}

/* Correct main */
fn main() {
    let a = "i am a &str";
    let mut n = 10;

    println!("{} {}", a, n);
    dbg!(n);

    /* Cannot immutable by default*/
    n += 1;
    println!("{} {}", a, n);

    /* We can have a single mutable reference to an object*/
    let mut k = 10;
    k += 1;

    /* Try to compile this */
    let mut p = Player::default();
    p.name = String::from("Giuseppe");

    /* Take a reference of &p and try to modify "p" */
    let p1 = &p;
    let mut p2 = p.clone();

    p2.age += 1;

    dbg!(p2);

    p1.hi();
}

/* Incorrect code */
// fn main() {
//     let a = "i am a &str";
//     let n = 10;
//
//     /* Cannot immutable by default*/
//     n += 1;
//
//     /* Try to compile this */
//     let mut p = Player::default();
//     p.name = String::from("Giuseppe");
//
//     /* Take a reference of &p and try to modify "p" */
//     let p1 = &p;
//     let mut p2 = p.clone();
//     p2.age += 1;
//
//     dbg!(p2);
//
//     p.name = p.name.to_uppercase();
//
//     p1.hi();
// }
