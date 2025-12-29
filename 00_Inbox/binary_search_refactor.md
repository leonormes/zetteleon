---
aliases: []
tags: []
title: "Refactoring: `src/strategies/binary_search.rs`"
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2025-12-28T09:19:43+00:00
modified: 2025-12-29T09:48:14+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# Refactoring: `src/strategies/binary_search.rs`

## 👃 Code Smell Report

**1. The "Torvalds Loop" Violation: Representing "Jobs" with Primitive Tuples**
The current implementation manages state using a `VecDeque<(isize, isize, isize, isize)>`.
* **Critique:** This is "Stringly/Numberly Typed". `(0, 10, 5, 20)` has no semantic meaning. It requires manual unwrapping and index arithmetic that is prone to off-by-one errors (hence the `isize` usage).
* **Better Data Shape:** A `Job` struct with proper `Range<usize>` or `Slice` references.

**2. The "Trinity" Violation: Implicit Invariants (The "Sorted" Assumption)**
The algorithm implements a "Divide and Conquer" intersection (splitting the target list `g_n` based on a match). This logic **only works if `g_n` is sorted**.
* **Critique:** The function signature `fn binary_search(..., g_n: &Vec<T>)` accepts *any* vector. If an unsorted vector is passed, the algorithm silently drops data (as seen in the `[A, Z]` vs `[Z, A]` counter-example).
* **Better Type System:** Accept `SortedSlice<T>` or similar wrapper that proves the data is sorted.

**3. The "Node.js" Legacy: Callbacks & Dynamic Types**
The use of `mut cb: F` where `F: FnMut(...)` is a classic JavaScript pattern.
* **Critique:** In Rust, we use Traits (`Ord`, `PartialEq`) to define comparability, or iterators. Passing a closure to "find an item in a slice" abstracts away the one thing that needs to be efficient (the search).
* **Better Logic:** Use `std::cmp::Ord`.

## 🔧 The Refactor Proposal

We will replace the entire "Divide and Conquer with Linear Scan" approach with a **Data-Oriented Merge Join**.

Since both inputs must be sorted for the original logic to behave correctly, we can use a linear scan $O(N+M)$ which is cache-friendly and strictly faster than the current implementation.

### Step 1: Define the Data (Data-Oriented)

First, we define a type that guarantees our invariant.

```rust
use std::ops::Deref;

/// A wrapper type that enforces the invariant that the inner data is sorted.
/// This prevents passing unsorted data to algorithms that require it.
#[derive(Debug)]
pub struct SortedSlice<'a, T>(&'a [T]);

impl<'a, T: Ord> SortedSlice<'a, T> {
   /// profoundly unsafe if data is not sorted, but we are in the boundary
   pub fn new_unchecked(data: &'a [T]) -> Self {
       Self(data)
   }
   
   pub fn as_slice(&self) -> &'a [T] {
       self.0
   }
}
```

### Step 2: Implement the "Arrow" (Logic)

Refactor `binary_search` to `intersect_sorted`.

```rust
use std::cmp::Ordering;

/// Computes the intersection of two sorted collections.
/// Returns a map of IndexInLeft -> Value.
/// 
/// Complexity: O(N + M)
pub fn intersect_sorted<T>(
    left: SortedSlice<String>, 
    right: SortedSlice<T>,
    extractor: impl Fn(&T) -> &String
) -> HashMap<usize, String>  
where T: Clone
{
    let mut matches = HashMap::new();
    let mut l_iter = left.as_slice().iter().enumerate();
    let mut r_iter = right.as_slice().iter();
    
    let mut l_current = l_iter.next();
    let mut r_current = r_iter.next();

    while let (Some((l_idx, l_val)), Some(r_val)) = (l_current, r_current) {
        let r_key = extractor(r_val);
        match l_val.cmp(r_key) {
            Ordering::Less => {
                // Left is smaller, advance Left
                l_current = l_iter.next();
            },
            Ordering::Greater => {
                // Right is smaller, advance Right
                r_current = r_iter.next();
            },
            Ordering::Equal => {
                // Match! Record it.
                // Note: If we need to handle duplicates in Right, we need to peek ahead.
                // Assuming unique keys in Right for now based on `IndexSet` usage in caller.
                matches.insert(l_idx, l_val.clone());
                
                // Advance Left (Standard Merge Join)
                // If we want M:N join, logic needs slightly more state.
                l_current = l_iter.next();
            }
        }
    }

    matches
}
```

## ⚠️ Breaking Change Warning

The caller (`basic_reidentification.rs`) currently **does not sort** `g_n` (the tokens).

* `read_tokens` returns a `Vec<String>` from an `IndexSet` (Insertion Order).
* We **MUST** update `read_tokens` to sort the vector before returning, or sort it at the call site.

## Proposed New File Content (`src/strategies/binary_search.rs`)

```rust
use std::collections::HashMap;
use std::fmt::Debug;
use std::cmp::Ordering;

/// Input wrapper to enforce sorted invariant
pub struct SortedSlice<'a, T>(pub &'a [T]);

/// Computes the intersection of two sorted slices.
/// 
/// This replaces the complex stack-based divide-and-conquer strategy with a 
/// cache-friendly linear Merge Join.
/// 
/// # Preconditions
/// * `left` MUST be sorted.
/// * `right` MUST be sorted.
pub fn intersect_sorted<T, K, F>(
    left: &[K], 
    right: &[T], 
    key_extractor: F
) -> HashMap<usize, K>
where
    K: Ord + Clone + Debug,
    F: Fn(&T) -> &K,
{
    let mut intersection = HashMap::new();
    let mut left_iter = left.iter().enumerate();
    let mut right_iter = right.iter().peekable();

    let mut left_curr = left_iter.next();

    while let Some((l_idx, l_val)) = left_curr {
        // Advance right until r_val >= l_val
        while let Some(r_val) = right_iter.peek() {
            if key_extractor(r_val) < l_val {
                right_iter.next();
            } else {
                break;
            }
        }

        // Check if we have a match
        if let Some(r_val) = right_iter.peek() {
            if key_extractor(r_val) == l_val {
                intersection.insert(l_idx, l_val.clone());
            }
        }

        left_curr = left_iter.next();
    }

    intersection
}
```

This solution removes the recursion, the stack allocation, the `isize` casting, and the callback complexity. It leverages `Iterator` and `Peekable` for safe, clean traversal.
