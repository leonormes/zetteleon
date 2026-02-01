---
aliases: ["Generational Arena", "Generational Indices", "Safe Indices", "Slot Map"]
created: 2025-12-31T00:00:00Z
last_reviewed: "2025-12-31"
modified: 2026-02-01T15:07:52+00:00
status: "stable"
tags: ["data_structures", "memory_safety", "performance", "rust", "typescript"]
title: SoT - Slot Map (Generational Arena)
type: "SoT"
updated: 
---

## 1. Definitive Statement

> [!definition] The Concept
> A Slot Map (or Generational Arena) is a container that solves the "Dangling Pointer" problem without Garbage Collection.
>
> It issues Stable IDs (Keys) composed of an `Index` and a `Generation`. If the data at the `Index` is deleted and reused, the `Generation` increments, invalidating all old Keys held by other parts of the system.

## 2. The Core Problems Solved

1. Dangling Pointers: In standard arrays, if you delete item 5 and move item 99 to slot 5 (swap-remove), any variable pointing to index 5 now points to the wrong object.
2. Memory Reuse: In systems like games or high-frequency trading, you cannot afford to allocate/deallocate memory constantly. You must reuse the "holes" left by deleted entities.

## 3. The Algorithm: Index + Generation

We do not give out a raw `index`. We give out a "Key" (Ticket).

- Index: Where the data lives in the array (Physical Location).
- Generation: A version counter for that slot (Logical Identity).

The Check:

When accessing `map.get(key)`:

```typescript
if (map.generations[key.index] !== key.generation) return null; // Stale Key
```

---

## 4. Implementation: TypeScript

In TypeScript/JavaScript, we maintain an explicit "Free List" stack to track empty slots.

```typescript
// The "Handle" - Safe to hold onto, even if the object dies
type EntityId = {
    index: number;
    generation: number;
}

class SlotMap<T> {
    // 1. The Data (Sparse)
    private data: (T | null)[] = [];
    
    // 2. The Meta-Data (Dense)
    // Tracks the "version" of each slot. Starts at 0.
    private generations: number[] = [];
    
    // 3. The Free List (Embedded Linked List / Stack)
    // A stack of indices that are currently empty.
    private freeIndices: number[] = [];

    insert(value: T): EntityId {
        let index: number;

        // Strategy: Reuse a hole if one exists, otherwise grow the array
        if (this.freeIndices.length > 0) {
            index = this.freeIndices.pop()!;
        } else {
            index = this.data.length;
            this.generations.push(0); // New slot, gen 0
            this.data.push(null);     // Placeholder
        }

        this.data[index] = value;

        // Return the Ticket
        return { index, generation: this.generations[index] };
    }

    get(id: EntityId): T | null {
        // SAFETY CHECK: This is the magic.
        if (id.index >= this.generations.length) return null; // Out of bounds
        if (this.generations[id.index] !== id.generation) return null; // Stale Key

        return this.data[id.index];
    }

    remove(id: EntityId): boolean {
        // Same safety check
        if (id.index >= this.generations.length) return false;
        if (this.generations[id.index] !== id.generation) return false;

        // 1. Increment generation so all existing IDs become invalid
        this.generations[id.index]++;
        
        // 2. Clear data to help Garbage Collector
        this.data[id.index] = null;

        // 3. Add this index to the "Free List" for reuse
        this.freeIndices.push(id.index);
        
        return true;
    }
}
```

---

## 5. Implementation: Rust

In Rust, this pattern is critical because it satisfies the Borrow Checker. The `SlotMap` owns the data; the rest of the program just holds `Key` structs (integers). We use an Implicit Free List woven into the `Slot` enum to save memory.

```rust
use std::num::NonZeroU32;

// The Handle. Lightweight (Copy, Clone).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Key {
    index: u32,
    generation: u32,
}

// Internal storage state for a slot
enum Slot<T> {
    Occupied(T),
    Free { next_free: Option<usize> },
}

pub struct SlotMap<T> {
    slots: Vec<Slot<T>>,
    generations: Vec<u32>,
    free_head: Option<usize>, // Index of first free slot
}

impl<T> SlotMap<T> {
    pub fn new() -> Self {
        Self {
            slots: Vec::new(),
            generations: Vec::new(),
            free_head: None,
        }
    }

    pub fn insert(&mut self, value: T) -> Key {
        if let Some(free_idx) = self.free_head {
            // REUSE STRATEGY: Pop from free list
            
            // 1. Get the slot (we know it's Free variant)
            let next_free = match &self.slots[free_idx] {
                Slot::Free { next_free } => next_free,
                _ => panic!("Corrupt free list"),
            };

            // 2. Update head
            self.free_head = next_free;

            // 3. Place data
            self.slots[free_idx] = Slot::Occupied(value);
            
            // 4. Return Key (Generation is already correct from previous increment)
            Key {
                index: free_idx as u32,
                generation: self.generations[free_idx],
            }

        } else {
            // APPEND STRATEGY: Grow vector
            let index = self.slots.len();
            self.slots.push(Slot::Occupied(value));
            self.generations.push(0);

            Key {
                index: index as u32,
                generation: 0,
            }
        }
    }

    pub fn get(&self, key: Key) -> Option<&T> {
        let idx = key.index as usize;
        
        // Bounds Check
        if idx >= self.generations.len() {
            return None;
        }

        // Generation Check (The "Stale" Protection)
        if self.generations[idx] != key.generation {
            return None;
        }

        // Return Data
        match &self.slots[idx] {
            Slot::Occupied(val) => Some(val),
            Slot::Free { .. } => None, // Should be unreachable if gen matches
        }
    }

    pub fn remove(&mut self, key: Key) -> Option<T> {
        let idx = key.index as usize;

        if idx >= self.generations.len() || self.generations[idx] != key.generation {
            return None;
        }

        // 1. Increment generation (Invalidates all existing Keys)
        self.generations[idx] += 1;

        // 2. Swap data out and replace with Free marker
        // Point this slot to the OLD free_head, then make this the NEW free_head.
        let old_head = self.free_head;
        self.free_head = Some(idx);

        // 3. Extract data to return it
        let old_slot = std::mem::replace(
            &mut self.slots[idx], 
            Slot::Free { next_free: old_head }
        );

        match old_slot {
            Slot::Occupied(val) => Some(val),
            Slot::Free { .. } => unreachable!(),
        }
    }
}
```

## 6. Advanced: Iteration

Iterating over a Slot Map requires skipping the "holes" (Free slots).

### TypeScript (Generator)

```typescript
public *iter(): IterableIterator<{ id: EntityId; value: T }> {
    for (let i = 0; i < this.data.length; i++) {
        if (this.data[i] !== null) {
            const id = { index: i, generation: this.generations[i] };
            yield { id, value: this.data[i]! };
        }
    }
}
```

### Rust (Iterator Trait)

Custom iterators in Rust optimize this by removing the bounds check and inlining the `next()` call.

```rust
impl<'a, T> Iterator for Iter<'a, T> {
    type Item = (Key, &'a T);

    fn next(&mut self) -> Option<Self::Item> {
        while self.index < self.map.slots.len() {
            let current_index = self.index;
            self.index += 1;

            if let Slot::Occupied(val) = &self.map.slots[current_index] {
                let key = Key {
                    index: current_index as u32,
                    generation: self.map.generations[current_index],
                };
                return Some((key, val));
            }
        }
        None
    }
}
```
