fn main() {
    /* Scope 1*/
    let b = 5;

    /* Ok */
    let c = {
        let a = 10;

        /* A block is an expression: it can produce a value
         * a + b is the result of this expression and is assigned to C
         *
         * This is ok because b leaves in an outer scope and a is local scoped.
         */
        a + b
    };
    println!("{}", c);

    /* Not ok: a is deallocated when its scope ends. This code does not compile */
    let mut c = a + b;
    c += 1;

    println!("{}", c);
}
