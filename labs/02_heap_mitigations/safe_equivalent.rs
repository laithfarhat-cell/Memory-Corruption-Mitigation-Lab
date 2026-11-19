fn report(value: &i32) { println!("{}", value); }
fn main() {
    let owner = Box::new(42);
    report(&owner);
    drop(owner);
    // report(&owner); // E0382: drop moved the Box; it cannot be borrowed again.
}
