---
aliases: []
confidence: "1"
created: 2026-01-03T18:24:19+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-23T18:09:18+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: stable
tags: []
title: SoT - Rust Vec Data Structure
type: SoT
---

## SoT - Rust Vec Data Structure

### Overview

Synthesized knowledge from **"A Common-Sense Guide to Data Structures and Algorithms"** (Theory) and **"The Rust Programming Language"** (Implementation).

---

### Syllabus: Understanding Rust `Vec<T>`

#### Phase 1: Physical Data Layout (Theory)

_Source: Wengrow, Ch. 1 & 14_

- **Contiguous Memory:** Learn how `Vec` stores data in adjacent memory slots on the heap.
- **The Array Foundation:** Understand why `Vec` is technically a "Dynamic Array."
- **O(1) Reading:** Why calculating the memory address `base_address + (index * size_of_T)` allows instant access.

#### Phase 2: Basic Operations in Rust

_Source: The Book, Ch. 8.1_

- **Creation & Inference:** Using `Vec::new()` vs the `vec![]` macro.
- **Growth (The `push` method):** Understanding how `Vec` handles adding items.
- **Accessing Data:** The difference between `&v[index]` (panics on out-of-bounds) and `v.get(index)` (returns `Option<&T>`).

#### Phase 3: Ownership & The Borrow Checker

_Source: The Book, Ch. 8.1 & Ch. 4_

- **Reallocation Risks:** Why adding an item to a `Vec` can invalidate existing references (memory is moved if the current heap block is too small).
- **Simultaneous Borrows:** Understanding why you can't push to a `Vec` while holding a reference to one of its elements.

#### Phase 4: Performance & Optimization

_Source: Wengrow, Ch. 19_

- **Space Complexity:** The "Capacity vs. Length" trade-off.
- **Time Complexity:** Why `pop()` is O(1) but `remove(0)` is O(n) (shifting elements).

---

### Practical Code Examples

#### 1. Creation, Growth, and Indexing

This example shows how Rust infers types and how `Vec` provides safe access to contiguous memory.

```rust
fn main() {
    // Theory: Wengrow Ch 1 - The Array Foundation
    // Rust: The Book 8.1 - Creating and Updating
    
    let mut v = Vec::new(); // Initial capacity is 0
    v.push(10); // Amortized O(1) - Might trigger a reallocation
    v.push(20);
    v.push(30);

    // Safe reading using .get (O(1) time complexity)
    match v.get(1) {
        Some(val) => println!("The second element is {val}"),
        None => println!("Element not found"),
    }

    // Direct indexing (will panic if out of bounds!)
    let third = &v[2]; 
    println!("The third is {third}");
}
```

#### 2. The Borrow Checker vs. Data Layout

This example demonstrates the "shifting memory" problem described in both books.

```rust
fn main() {
    let mut v = vec![1, 2, 3];

    // We take a reference to the first element
    let first = &v[0]; 

    // ERROR: This won't compile!
    // Why? Wengrow explains that pushing might move the whole 
    // array to a new memory location if it needs more space.
    // The reference 'first' would then point to "deallocated memory."
    
    // v.push(4); 

    println!("The first is: {first}");
}
```

#### 3. Efficiency: Iteration and Cache Locality

Iterating over a `Vec` is extremely fast because the data is physically next to each other in memory (Cache Locality).

```rust
fn main() {
    let mut v = vec![100, 200, 300];

    // Theory: Wengrow Ch 1 - Linear search/iteration
    // Implementation: The Book 8.1 - Iterating
    for i in &mut v {
        *i += 50; // Dereference to modify the value in place
    }

    for i in &v {
        println!("{i}");
    }
}
```

#### 4. Handling Multiple Types (Advanced Data Layout)

Rust `Vec` can only hold one type. To hold "different" types, we use an Enum to make them look like one type.

```rust
enum DataCell {
    Integer(i32),
    Text(String),
    Float(f64),
}

fn main() {
    // Theory: Every element in a contiguous array must be the same size.
    // Rust: Enum variants are sized to the largest variant, ensuring O(1) indexing works.
    let row = vec![
        DataCell::Integer(3),
        DataCell::Text(String::from("Rust")),
        DataCell::Float(10.5),
    ];

    for cell in row {
        match cell {
            DataCell::Integer(i) => println!("Int: {i}"),
            DataCell::Text(s) => println!("String: {s}"),
            DataCell::Float(f) => println!("Float: {f}"),
        }
    }
}
```
