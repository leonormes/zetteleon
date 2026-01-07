---
aliases: []
alias: []
confidence: 5/5
created: 2025-12-22T00:00:00Z
epistemic: architecture
last_reviewed: 2026-01-01
modified: 2026-01-03T10:18:56+00:00
purpose: ">-"
review_interval: 6 months
see_also: ["[[SoT - Rust Type Mechanics]]", "[[SoT - Rust Language]]", "[[SoT - Data-Oriented Programming (DOP)]]"]
source_of_truth: []
status: stable
tags: [data-centric, dod, systems-programming, go, rust]
title: SoT - Data-Centric Software Engineering
type: SoT
uid:
updated:
---

## 1. Definitive Statement

> [!definition] The Core Philosophy
> "Bad programmers worry about the code. Good programmers worry about data structures and their relationships."—**Linus Torvalds**
>
> **Data-Centric Software Engineering** is the discipline of treating **Data Structures** as the primary source of truth and complexity in a system, rendering the **Code** (Logic) as a trivial derivation of that structure.

### 1.1 The Conservation Law of Complexity

Software complexity obeys a conservation law: it must reside either in the procedural logic (the Code) or the structural representation (the Data).

* **Code-Centric:** Complexity is handled by imperative logic (nested `if`, flags, loops). Result: Fragile, hard to test.
* **Data-Centric:** Complexity is encoded in the schema (Graph, Map, Table). Result: "Dumb" code that merely traverses the "Smart" structure.

### 1.2 The Consensus of the Masters

The industry's most impactful architects share a consensus: **Data Dominates Code**.

| Architect | Mental Model | The Core Tenet |
| --- | --- | --- |
| **Linus Torvalds** | **Data-Centric** | "Bad programmers worry about code. Good programmers worry about data structures." |
| **Fred Brooks** | **Table-Driven** | "Show me your tables, and I won't usually need your flowcharts; they'll be obvious." |
| **Rob Pike** | **Structural** | "Data dominates. If you've chosen the right data structures... the algorithms will almost always be self-evident." |
| **Mike Acton** | **Data-Oriented** | "The purpose of all programs is to transform data from one form to another." (Hardware sympathy). |
| **Andrew Kelley** | **Layout-First** | "Modern performance is governed by memory latency, not instruction speed." |

### 1.3 Case Study: The "Good Taste" of Linked Lists

Torvalds distinguishes "bad taste" from "good taste" by how a developer handles edge cases. If the data model is correct, the edge case vanishes.

* **Bad Taste:** Treating the "head" pointer and "next" pointers differently, requiring `if` statements to handle the list start.
* **Good Taste:** Using indirect pointers (pointer-to-pointer) to treat the address of any "incoming link" uniformly. The edge case is topologically identical to the standard case.

> **Insight:** Complexity in code is a symptom of an insufficient understanding of the data topology.

---

## 2. The Structural Logic (10 Pillars)

These ten principles form the structural backbone of the Data-Centric methodology, synthesizing the wisdom of the masters into a unified discipline.

### 1. Data Dominates Code (Torvalds/Pike)

Algorithms are ephemeral; data structures are foundational. If you choose the right data structures, the algorithms will be self-evident. Complexity in code is a failure of data modeling.

### 2. Mechanical Sympathy (Acton/Kelley)

Hardware is the platform, not the language. Software must respect the physical reality of the machine: cache lines, memory alignment, and instruction pipelines. Design for the hardware, not the "abstract machine."

### 3. The Conservation of Complexity

Complexity cannot be destroyed, only displaced. Shift complexity from procedural logic (fragile, hard to test) to structural schema (robust, easy to query). Smart data, dumb code.

### 4. Table-Driven Logic (Brooks)

Replace cyclomatic complexity (nested `if`/`else` logic) with data lookups. Control flow should be determined by traversing a data structure (tables, state machines), not by hard-coded branches.

### 5. Parse, Don't Validate (Wlaschin)

Use the type system to make invalid states unrepresentable. Do not check for validity deep in the code; parse data at the boundary into strict types that prove their own validity.

### 6. Value Semantics (The Stack)

Prefer immutable values (copies) over mutable references (pointers). Value semantics guarantee local reasoning, thread safety, and cache locality. Pointers introduce action-at-a-distance and aliasing bugs.

### 7. Semantic Compression (Muratori)

Avoid premature abstraction. Write the specific, concrete solution first. Only when patterns physically repeat should you "compress" them into a function. DRY (Don't Repeat Yourself) is a result, not a goal.

### 8. The Error Kernel (Armstrong)

Reliability comes from isolation, not defensive coding. Partition systems into a "Kernel" (must be correct) and "User Space" (allowed to crash). Supervision hierarchies manage failure; they do not prevent it.

### 9. Simplicity vs. Easy (Hickey)

Simplicity is the absence of interleaving (decomplected). "Easy" is merely familiarity. Strive for Simple (unbraided state), even if it is not Easy (requires learning).

### 10. Specification First (Lamport)

Coding is the final, trivial step. Understanding the problem is the work. Model the system's state space and invariants mathematically (or rigorously) before writing a single line of implementation.

---

## 3. The Hardware Reality: Data-Oriented Design (DoD)

Data-centricity is not just logical elegance; it is a physical requirement of modern hardware. The CPU does not see "Objects"; it sees **Structure** and **Stride**.

### 3.1 Mike Acton and the "Three Big Lies"

Modern software is often bogged down by abstraction layers that ignore reality. Mike Acton (Unity) identifies three pervasive industry lies:

1. **"Software is the platform."**
    * *The Lie:* We write code for Java, C#, or Python.
    * *The Reality:* **Hardware is the platform.** Reasoning about software independent of hardware is a denial of engineering reality.
2. **"Code is designed around the model of the world."**
    * *The Lie:* We should model a "Dog" class because dogs exist in the real world.
    * *The Reality:* **Code is designed to transform data.** The CPU does not know what a "Dog" is; it only processes streams of bytes.
3. **"Code is more important than data."**
    * *The Lie:* We study syntax, patterns, and hierarchies.
    * *The Reality:* **Data is paramount.** Code only exists to manipulate data. If you don't understand the data layout, you cannot understand the performance.

> **Hardware Context:** To understand the specific platform you are deploying to (AWS/Azure), consult **[[MOC - Cloud Hardware Architecture]]**.

### 3.2 The Physics of Computing (Mental Models)

To engineer for the machine, we must internalize its physical constraints.

#### A. The Kitchen Analogy (Nic Barker)

* **The Chef (CPU):** Can chop vegetables (process instructions) incredibly fast.
* **The Counter (L1 Cache):** Holds a small amount of ingredients right in front of the chef. Access is instant (~3 cycles).
* **The Supermarket (Main RAM):** Where all the ingredients live.
* **The Problem:** Going to the supermarket takes **~200-300 cycles**.
* **The Consequence:** If your data is scattered (pointers/objects), you are driving to the supermarket to buy *one single onion* for every chop. The Chef spends 99% of their time waiting for the truck.

#### B. The Cache Line (The Truck)

* **The Unit of Transfer:** Memory is not fetched byte-by-byte; it is fetched in **64-byte chunks** (Cache Lines).
* **The Efficiency Rule:** Every byte fetched into the cache line *must* be used.
* **The OOP Failure:** Standard objects are "Swiss Cheese" in memory—data + vtables + padding + pointers. You fetch 64 bytes to use 4 bytes. This is **~90% bandwidth waste**.

#### C. Observability (Linux CLI)
You can verify your hardware's architecture immediately using these tools:

*   **Inspect Hardware:** `lscpu | grep -i cache` (Look for L1d cache size).
*   **Query Line Size:** `getconf LEVEL1_DCACHE_LINESIZE` (Usually 64).
*   **Profile Cache Misses:**
    *   **Perf (Real HW):** `perf stat -e L1-dcache-load-misses ./my_program`
    *   **Cachegrind (Sim):** `valgrind --tool=cachegrind ./my_program`

### 3.3 The DoD Optimisation Toolbox

To maximise "Cache Density" (packing the truck efficiently), we use specific structural patterns.

| Strategy | OOP Approach (The Anti-Pattern) | DoD Approach (The Solution) | Result |
|:--- |:--- |:--- |:--- |
| **Storage** | **Array of Structures (AoS).** `[Ball(x,y,c), Ball(x,y,c)]`. | **Structure of Arrays (SoA).** `[x,x,x]`, `[y,y,y]`. | **100% Cache Line Utilization.** The CPU processes homogeneous streams. |
| **State** | **Boolean Flags.** `if (obj.isActive) update()`. | **Existence-Based Predication.** Move "Active" objects to a separate array. | **Zero Branching.** Iterate linearly over the "Active" array. |
| **Polymorphism** | **Virtual Functions.** `shape.Area()`. Forces a pointer chase + vtable lookup. | **Tagged Unions (Enums).** `match shape { Circle, Rect }`. | **Instruction Locality.** Data is contiguous; branch prediction works. |
| **References** | **Pointers (8 bytes).** `*Object`. Latency spike on dereference. | **Indexes (4 bytes).** `u32` ID. | **Halved size.** Better cache density; verifiable safety. |

### 3.4 Constructive Realism: The Synthesis

**Thesis:** High-level Correctness (Logic/Type Theory) and Low-level Performance (Physics/Layout) are isomorphic.

* **The Conflict:** Engineers often choose between "Clean Code" (Abstractions) and "Fast Code" (Hacks).
* **The Synthesis:** Use **Type Theory** to rigorously define the **Data Layout**. The Type System becomes the "Compiler's Physics Engine," ensuring that logical impossibilities are physically unrepresentable.

#### Empirical Validation: The Cost of "Clean Code"

Casey Muratori demonstrated that adhering to "Clean Code" dogmas (Polymorphism, Encapsulation) degrades performance by **1.5x to 10x**.

* **The Cost:** A 10x loss erases ~12 years of hardware advancement. It effectively runs modern hardware at 2010 speeds.
* **The Fix:** Aligning the Logical Model (Enum/Switch) with the Physical Model (Contiguous Memory) restores the hardware's potential.

---

## 4. Minimum Viable Understanding (MVU)

### Table-Driven Methods

The "Code-Centric" developer writes a "Giant Switch Statement" to handle state. The "Data-Centric" developer uses a **Lookup Table**.

* **Code:** `if cmd == "SAVE": save()`
* **Data:** `commands = {"SAVE": save_fn}`. Logic becomes `commands[input]()`.
* **Benefit:** Cyclomatic complexity drops to 1. New commands are added to data, not code.

### The Transformation Pipeline (Stoyan Nikolov)

View software not as a collection of "Entities" (Objects) but as a **Data Transformation Pipeline**.

* **Input:** Homogeneous Streams (Tables).
* **Process:** Independent Systems (Transformers).
* **Output:** Mutation Tables (Decoupled State Changes).
* *Result:* Testable, parallelizable, and cache-friendly.

---

## 5. Applied Domains (The Pattern in Practice)

The Data-Centric philosophy is not limited to code; it applies to the entire stack.

### A. Version Control (Git)

* **Problem:** Merging divergent histories.
* **Code Solution (SVN):** Complex heuristics tracking line numbers.
* **Data Solution (Git):** A **Directed Acyclic Graph (DAG)** of immutable snapshots. Merging is simply a graph traversal to find a common ancestor. The complexity is in the Graph, not the Merge script.
* **Deep Dive:** [[SoT - The Data Architecture of Source Control (Git)]]

### B. Infrastructure (Terraform)

* **Concept:** Infrastructure is not a script; it is a **Data Schema**.
* **Application:** Treating `config.tf` as a database of "Desirable State" (Maps/Lists) and `main.tf` as the "Renderer" that transforms that state into API calls.
* **Deep Dive:** [[MOC - Data-Centric Infrastructure]]

### C. Shell Environment (Zsh/Chezmoi)

* **Concept:** The shell environment is a **Data Structure to be instantiated**, not a script to be executed.
* **Application:** Using Chezmoi as a "Compiler" to resolve Sum Types (OS variants) and Product Types (config structs) into a static environment.
* **Deep Dive:** [[SoT - Type-Driven Shell Architecture|Type-Driven Shell]]

---

## 6. The Methodology: The Torvalds Loop

To practice this discipline, resist the urge to write logic immediately. Follow this strict four-phase protocol: **Shape -> Access -> Invariants -> Logic**.

*See also:* [[SoT - Type-Driven Development (The Torvalds Loop)]]

### Phase 1: Shape (The Physical Reality)

*Goal: Maximise information density; minimise cache misses.*

Focus on the **layout of memory**. Before thinking about "objects" or "methods", define the raw data structures.

- **Action:** Optimise `struct` layouts for mechanical sympathy (CPU cache efficiency, alignment, and padding). Define types based on how hardware will consume them.

### Phase 2: Access (The Interface)

*Goal: Predictable memory pressure and clear ownership.*

Determine the **mechanics of interaction**. How does data move?

- **Decision:** **Value Semantics** (Copying) vs. **Pointer Semantics** (Sharing).
- **Action:** Choose receiver types (Go: `(t T)` vs `(t *T)`) to control stack vs. heap allocation.

### Phase 3: Invariants (The Integrity)

*Goal: Zero trust in the caller; absolute trust in the data.*

Define **validity constraints**. An invariant is a condition that must *always* be true.

- **Action:** Use factory functions and unexported fields to enforce constraints at the boundary. Ensure it is impossible to construct a "broken" Shape.

### Phase 4: Logic (The Transformation)

*Goal: Efficient transformation of valid inputs to valid outputs.*

Only now do you write the algorithms. Because the Shape is optimised and Invariants are enforced, the Logic is simple, linear, and performant.

---

## 7. Implementation Example (Go)

### Mechanical Sympathy & Escape Analysis

In the **Access** phase, hardware realities dictate choices:

1. **Value Semantics (Stack):** Preferred. Data is contiguous (Cache Friendly). Allocation/Deallocation is instant (Stack Pointer movement). Zero GC cost.
2. **Pointer Semantics (Heap):** Use only when necessary. Data is scattered (Cache Misses). Allocation requires finding free space; Deallocation requires Garbage Collection (GC Pause).

**Rule of Thumb:**
- **Sharing Down (Stack Safe):** Passing a pointer *into* a function keeps it on the stack.
- **Sharing Up (Heap Escape):** Returning a pointer *out* of a function forces a heap allocation.

### Code Example: High-Throughput Event System

```go
// PHASE 1: SHAPE
// Ordered by size to minimize padding.
type Event struct {
    ID        uint64
    Timestamp int64
    Payload   []byte // Contiguous memory
    Type      uint8  // Aligned
}

// PHASE 2: ACCESS
// Value Semantics for reading (Cheap copy, Thread-safe).
func (e Event) Bytes() []byte {
    return e.Payload
}

// Pointer Semantics for mutation.
func (e *Event) MarkProcessed() {
    e.Type = 0
}

// PHASE 3: INVARIANTS
// Factory enforces that ID and Payload must exist.
func NewEvent(id uint64, payload []byte) (Event, error) {
    if id == 0 {
        return Event{}, errors.New("invalid ID")
    }
    return Event{ID: id, Payload: payload}, nil
}

// PHASE 4: LOGIC
// The logic is pure transformation because data integrity is guaranteed.
func Process(events []Event) {
    for _, e := range events {
        // No null checks needed; Invariants guarantee validity.
        handle(e)
    }
}
```

---

## 8. The Architecture of Reliability (Joe Armstrong)

Reliability is not achieved through defensive programming, but through **Isolation** and **Supervision**.

### 8.1 The "Let It Crash" Philosophy

Instead of wrapping code in brittle `try/catch` blocks, allow processes to fail and restart from a known clean state. This prevents "zombie" systems that run in inconsistent states.

### 8.2 The Error Kernel Pattern

Partition the system into a minimal "Kernel" that *must* be correct and cannot crash, and outer layers where failure is expected and managed. The reliability of the system is defined by the robustness of the supervision hierarchy, not the absence of bugs.

---

## 9. The Discipline of Simplicity (Rich Hickey)

Simplicity is an objective property of a system, distinct from "Ease" (familiarity).

* **Simple vs. Easy:** A tool is "Easy" if it is near at hand or familiar. A tool is "Simple" if it is unentangled (**Decomplected**).
* **Value-Oriented Programming:** Treat data as **Values** (Immutable). State is not a value; it is an identity that changes over time. Immutability eliminates the need for locks and makes systems trivially testable.
* **Deep Dive:** [[SoT - Simple Made Easy (Rich Hickey)]]

---

## 10. Thinking Above the Code (Leslie Lamport)

Coding is the last and least important step of software engineering.

* **The Specification Mindset:** Model the system mathematically before writing a single line of code. Define the "State Space" and "Next State" relations.
* **Invariants and Liveness:** Use formal tools (like TLA+) to check for properties that must always be true and those that must eventually happen.

---

## 11. Strategic Modelling (Domain-Driven Design)

Before defining physical data structures, we must define the **Domain Model**. DDD bridges the gap between Business Intent and Engineering Reality.

### 11.1 Ubiquitous Language as Schema

The **Ubiquitous Language** is the shared vocabulary of the business. In Data-Centric Engineering, this vocabulary dictates the **Type Names** and **Field Names**.

* **Rule:** If the expert says "Invoice," the type is `Invoice`. The code must "speak" the language of the domain.
* **The Artifact:** Gherkin scenarios or Event Storming outputs become the blueprint for your struct definitions.

### 11.2 Bounded Contexts (The Scope of Validity)

A **Bounded Context** defines the logical boundary where a specific Data Model applies.

* **Separation of Concerns:** A `Product` in the *Sales Context* (Price, Description) is structurally different from a `Product` in the *Shipping Context* (Weight, Dimensions).
* **Data Implication:** Do not create a single "God Object." Create distinct, optimized structs for each context, mapping between them only at the edges.

---

## 12. Semantic Compression (Casey Muratori)

Avoid "Premature Abstraction." Abstractions should be born from necessity, not dogma.

* **Compression over DRY:** Write the specific logic first. Only once the semantics are fully understood should you "compress" repeating patterns into functions or utilities.
* **The Jungle of Dependencies:** Every external library is a "jungle" you must manage. Minimize dependencies to maintain total control and debugging capability.

---

## 13. Type System Rigor (Wlaschin / Rust)

The type system is a verification tool, not just a set of labels.

* **Make Invalid States Unrepresentable:** Design data structures such that it is mathematically impossible for them to hold nonsensical data.
* **Types over Tests:** If the structure itself enforces the business rule, there is no need for runtime validity checks.

---

## 14. Type-Driven API Design (Will Crichton / Rust)

A well-designed API should guide the user toward correctness by making invalid states unrepresentable and providing compile-time feedback.

### 14.1 Traits as Behavioral Specifications

Traits define what a type *can do* rather than what it *is*. This decouples data from implementation and enables retroactive abstraction via **Extension Traits** (adding methods to types you don't own).

### 14.2 The Type State Pattern

Encode the lifecycle of an object directly into the type system.

* **Logic:** Transitioning between states (e.g., `Unbounded` -> `Bounded`) returns a new type.
* **Result:** Methods relevant only to a specific state are physically unavailable in other states, turning documentation into compiler-enforced constraints.

### 14.3 Philosophical Root: Leibniz's Dream

The strict Type System is the practical realization of Gottfried Wilhelm Leibniz's **[[Characteristica Universalis (Leibniz)|Characteristica Universalis]]** (17th Century).

* **The Vision:** A universal formal language where ambiguity is impossible.
* **The Modern Reality:** When we "Make Invalid States Unrepresentable," we are fulfilling Leibniz's goal of resolving disputes (bugs) through calculation (compilation) rather than debate (debugging).

---

## 15. Case Study: The Transformation Pipeline (Azure ACR)

How to transcend "Mediocre" Object-Oriented Design (OOD) using Data-Centric principles.

### 15.1 The Shift: From "Managers" to "Pipelines"

* **Mediocre OOD:** A `ChartManager` object iterates through charts, calling `update()` on each.
    * *Problem:* **N+1 Latency** (network calls per chart), hidden state, fragile error handling.
* **Data-Centric:** A linear pipeline of **Batch Transformations**.
    * *Process:* `Ingest` -> `Parse` -> `Discovery` -> `Transform` -> `Apply`.
    * *Benefit:* **Latency Hiding** (batch network queries), **Debuggability** (dump the buffer at any stage), **Simplicity** (flat loops).

### 15.2 Making Invalid States Unrepresentable (Rust)

Use the Type System to enforce the pipeline stages. It should be impossible to "patch a chart" before the image is confirmed in the registry.

```rust
// STAGE 1: The Input (Tainted/External)
struct PublicImageRef {
    registry: String, // "docker.io"
    digest: Option<Digest>,
}

// STAGE 2: The Target (Safe/Internal)
// Cannot be constructed unless verified in ACR.
struct ACRImageRef {
    acr_domain: String,
    digest: Digest, // Mandatory for immutability
}

// STAGE 3: The Verified Transition
// This struct is the ONLY input accepted by the "Patch" function.
// It physically couples the Chart with the PROOF that the image is safe.
struct VerifiedMigration {
    chart_id: Uuid,
    replacements: HashMap<PublicImageRef, ACRImageRef>,
}

// The Final Transformation
fn patch_chart(tarball: Vec<u8>, migration: VerifiedMigration) -> Result<Vec<u8>>;
```

---

## 16. The Leakage of Abstraction (Cloud Reality)

In Cloud Computing, the "Abstraction" (vCPU, GiB) is a lie. To achieve true Data-Centric performance, you must pierce the veil of virtualization.

### 16.1 The Lie of the vCPU

A "vCPU" is not a core; it is a time-slice on a hyperthread.

* **Cache Pollution:** When the hypervisor schedules a noisy neighbor on your physical core, they evict your data from L1/L2 cache.
* **The Penalty:** You incur a ~200-cycle stall to fetch data back from RAM when your thread returns.
* **Mitigation:** Use **Guaranteed QoS** (Kubernetes) or **Dedicated Instances** (AWS.metal) to pin threads to physical silicon.

### 16.2 NUMA: The Hidden Network

On large instances (e.g., >64 vCPUs), your VM spans multiple physical sockets.

* **The Trap:** A process on Socket 0 accessing memory on Socket 1 incurs **QPI/UPI Interconnect latency** (2x slower).
* **The Fix:** Use `topologyManagerPolicy: single-numa-node` in Kubernetes to force alignment.

---

## 17. Summary: The Table of Transcendence

| Domain | Mediocre Mental Model | Transcendental Mental Model (The Masters) |
|:---- |:---- |:---- |
| **Foundation** | **Code-Centric:** Focus on algorithms and syntax. | **Data-Centric:** Focus on topology and state. |
| **Reality** | **Modeling the World:** "Nouns"/Objects. | **Transformation:** Data streams and pipelines. |
| **Reliability** | **Defensive:** Try/Catch, null checks. | **Isolation:** Error Kernels, "Let it Crash". |
| **Complexity** | **Easy:** Familiarity, massive frameworks. | **Simple:** Unbraided, immutable values. |
| **Design** | **Abstraction:** Premature patterns. | **Compression:** Empirical abstraction. |
| **Verification** | **Testing:** Happy path checking. | **Specification/Typing:** Formal logic, state constraints. |
| **Performance** | **Cycles:** Optimizing instructions. | **Physics:** Optimizing memory layout. |
