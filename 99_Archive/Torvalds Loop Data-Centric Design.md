---
aliases: []
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2025-12-27T20:40:52+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
title: Torvalds Loop Data-Centric Design
source: "https://gemini.google.com/share/c1da0e2cb739"
author:
  - "[[Gemini]]"
published:
created: 2025-12-27T20:17:41+00:00
description: "Created with Gemini"
tags:
  - "clippings"
---

I came across this definition;

The Torvalds Loop:\*\* A four-phase design protocol: Shape -> Access -> Invariants -> Logic.

Describe it in more detail and align it with a data centric perspective towards programming. Give examples in go

The "Torvalds Loop" is a mental model that enforces **Data-Oriented Design (DOD)** over Object-Oriented Design. It operationalises Linus Torvalds' core philosophy:

> *"Bad programmers worry about the code. Good programmers worry about data structures and their relationships."*—Linus Torvalds

In this protocol, code (Logic) is the *last* consideration, not the first. You design the physical reality of the data first, then the rules that govern it, and finally the behaviour.

Here is the breakdown of the loop aligned with a data-centric perspective and Go implementation.

---

### The Framework: Shape Access Invariants Logic

#### 1\. Shape (The Physical Reality)

This phase focuses on the **layout of memory**. Before thinking about "objects" or "methods", you define the raw data structures. In Go, this means optimising `struct` layouts for mechanical sympathy (CPU cache efficiency, alignment, and padding).

- **Goal:** Maximise information density; minimise cache misses.
- **Action:** Define types based on how hardware will consume them, not how humans categorise them.

#### 2\. Access (The Interface)

This phase determines **mechanics of interaction**. How does data move? Do we share data (pointers) or copy data (values)? In Go, this is the decision between **Value Semantics** and **Pointer Semantics**.

- **Goal:** predictable memory pressure and clear ownership.
- **Action:** Choose receiver types (`(t T)` vs `(t *T)`) and function signatures to control heap vs. stack allocation.

#### 3\. Invariants (The Integrity)

This phase defines **validity constraints**. An invariant is a condition that must always be true for the data to be valid. You must ensure that it is impossible for a user to construct a "broken" version of your Shape.

- **Goal:** Zero trust in the caller; absolute trust in the data.
- **Action:** Use factory functions and unexported fields to enforce constraints at the boundary.

#### 4\. Logic (The Transformation)

Only now do you write the algorithms. This is the **transformation of state**. Because the Shape is optimised and Invariants are enforced, the Logic becomes simple, linear, and performant.

- **Goal:** Efficient transformation of valid inputs to valid outputs.
- **Action:** Write the business logic functions.

---

### Go Implementation Example: A High-Throughput Event System

We will apply the Torvalds Loop to design a system for processing network events.

#### Phase 1: Shape

We define the struct. We order fields by size to minimise padding (memory alignment) and group related fields to maximise spatial locality.

#### Phase 2: Access

We decide on semantics. Events are immutable facts that flow through the system.

- **Decision:** Use **Value Semantics** for movement (copying is cheap for 48 bytes and safer for concurrency).
- **Decision:** Use **Pointer Semantics** only when mutating state (decoding into the event).

Go

```markdown
// Reader: Uses Value Semantics (copies the Event).
// Safe for concurrent reads without locks.
func (e Event) Bytes() []byte {
    return e.Payload
}

// Mutator: Uses Pointer Semantics (modifies the Event).
func (e *Event) MarkProcessed() {
    e.Type = 0 // Hypothetical 'processed' state
}
```

#### Phase 3: Invariants

We ensure an `Event` cannot exist without a valid ID and Timestamp. We use an unexported struct or a factory function to enforce this.

Go

```markdown
// NewEvent enforces the invariant: No event can exist without an ID and Time.
// It returns a value, maintaining our Value Semantics decision.
func NewEvent(id uint64, payload []byte) (Event, error) {
    if id == 0 {
        return Event{}, errors.New("invalid ID: zero value not allowed")
    }
    if len(payload) == 0 {
        return Event{}, errors.New("invalid payload: empty")
    }

    return Event{
        ID:        id,
        Timestamp: time.Now().UnixNano(),
        Payload:   payload,
        Type:      1, // Default type
        Priority:  0,
    }, nil
}
```

#### Phase 4: Logic

Finally, we write the processing logic. Because we know the Shape is cache-friendly and Invariants are checked at creation, the Logic is pure data transformation.

Go

```markdown
type Processor struct {
    // ...
}

// ProcessBatch takes a slice of Events (linear memory access).
// The logic is simplified because we trust the data integrity.
func (p *Processor) ProcessBatch(events []Event) {
    for _, e := range events {
        // We know ID is non-zero and Payload is present.
        // We operate on local copies (stack-allocated if possible).
        if e.Priority > 10 {
            p.handleHighPriority(e)
        } else {
            p.handleStandard(e)
        }
    }
}
```

### Summary of Alignment

| Phase | OOD Perspective (Typical) | Data-Centric Perspective (Torvalds Loop) |
| --- | --- | --- |
| **Shape** | Classes modelling "real world" concepts. | Structs modelling memory layout and hardware access. |
| **Access** | Getters/Setters, Encapsulation. | Semantic consistency (Value vs Pointer), API boundaries. |
| **Invariants** | Often checked inside every method or ignored. | Checked at the boundary (Construction); assumed true internally. |
| **Logic** | The primary focus; complex state management. | The final step; simple transformations of trusted data. |

**Next Step:** Would you like me to expand on the **Access** phase specifically regarding "Mechanical Sympathy" and how Go's escape analysis dictates the choice between pointers and values?

Yes

This expansion focuses on the **Access** phase through the lens of **Mechanical Sympathy**, detailing how hardware realities and the Go compiler's Escape Analysis dictate your architectural choices.

### 1\. Mechanical Sympathy: The Cost of Indirection

Mechanical Sympathy asserts that software designs must respect the underlying hardware. In the context of "Access" (deciding between Values and Pointers), the primary constraints are **Latency** and **Cache Locality**.

#### The Hardware Reality

Modern CPUs are incredibly fast, but memory (RAM) is comparatively slow. To bridge this gap, CPUs use caches (L1, L2, L3).

- **Value Semantics (Contiguous Data):** When you use values (arrays, slices of structs), data is laid out linearly in memory. The CPU's "prefetcher" can predict the next read, pulling data into the L1 cache before your code even asks for it.
- **Pointer Semantics (Scattered Data):** A pointer is a memory address. To read the data, the CPU must fetch the address, wait, then fetch the data at that address. If that address points to a random location in the heap, you likely trigger a **Cache Miss**, forcing a slow fetch from main RAM.

**The Mental Model:**

- **Value Access:** Reading a book page by page.
- **Pointer Access:** Reading a "Choose Your Own Adventure" book, constantly flipping to random page numbers.

#### Go Example: Cache Efficiency

Consider processing a list of `Pixel` objects.

Go

```markdown
// BAD: Pointer Semantics (Linked List style)
// Creates 'pointer chasing'. Data is scattered across the heap.
// High probability of Cache Misses.
type PixelNode struct {
    R, G, B uint8
    Next    *PixelNode
}

// GOOD: Value Semantics (Slice of Structs)
// Contiguous memory. One cache line fetch loads multiple Pixels.
// The CPU prefetcher can devour this data.
type Pixel struct {
    R, G, B uint8
}
pixels := []Pixel{{...}, {...}}
```

### 2\. Escape Analysis: The Cost of Allocation

In Go, "Access" decisions directly control **where** data lives: the **Stack** or the **Heap**.

- **The Stack:** Fast, self-cleaning scratchpad. Allocation is just moving a pointer. Deallocation happens automatically when the function returns. **Zero Garbage Collector (GC) cost.**
- **The Heap:** A messy warehouse. Allocation requires finding free space. Deallocation requires the Garbage Collector to stop the world (or burn CPU cycles) to sweep it. **High GC cost.**

**Escape Analysis** is the compiler pass that decides: *"Can I safely keep this variable on the Stack, or must I move it to the Heap?"*

#### The "Sharing" Mental Model

To master Access in Go, use these rules of thumb regarding data movement:

**1\. Sharing Down (Stack Safe)** Passing a pointer *down* into a function call usually keeps data on the stack. The compiler knows the data outlives the function call.

Go

```markdown
func main() {
    u := User{Name: "Architect"} // Allocated on Stack
    // We pass a pointer DOWN.
    // 'u' stays on the main stack frame. No GC pressure.
    printUser(&u) 
}

func printUser(u *User) {
    fmt.Println(u.Name)
}
```

**2\. Sharing Up (Heap Escape)** Returning a pointer *up* out of a function forces an escape. The stack frame dies when the function returns, so the data *must* survive in the Heap.

Go

```markdown
func NewUser() *User {
    u := User{Name: "Architect"}
    // We return a pointer UP.
    // The compiler MUST move 'u' to the Heap.
    // This creates GC pressure.
    return &u 
}
```

### 3\. The Access Decision Matrix

When applying the **Access** phase of the Torvalds Loop, apply this logic:

### Summary for the Architect

In the Torvalds Loop, **Access** is not just about API design; it is about **resource management**.

1. **Default to Values:** Optimise for the CPU cache and Stack allocation.
2. **Opt-in to Pointers:** Only when you strictly need shared mutation or the data structure is physically too large to copy efficiently.
3. **Think in Cache Lines:** A cache miss costs ~200 clock cycles. A copy of a small struct costs ~3 cycles. Do the math.

**Next Step:** Would you like to walk through the **Invariants** phase to see how unexported fields and factory patterns in Go can eliminate defensive coding checks in your business logic?

Google Account

Leon Ormes

leonormes@gmail.com
