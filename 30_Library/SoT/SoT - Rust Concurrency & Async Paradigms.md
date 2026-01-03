---
source_of_truth: []
aliases: ["Async Rust", "Rust Concurrency", "Shared-Nothing Architecture", "Structured Concurrency"]
confidence: "5/5"
created: 2026-01-02T14:30:00Z
epistemic: "knowledge"
last_reviewed: "2026-01-02"
modified: 2026-01-03T10:18:48+00:00
purpose: "To define the architectural paradigms of Concurrency and Async in Rust, contrasting standard defaults with high-performance alternatives."
review_interval: "6 months"
see_also: ["[[MOC - Rust Programming Language]]", "[[SoT - Rust Language]]", "[[SoT - Rust High-Performance Computing (HPC) Optimization]]"]
status: "stable"
tags: ["rust", "concurrency", "async", "architecture", "performance"]
title: SoT - Rust Concurrency & Async Paradigms
type: "SoT"
---

## 1. The Core Tension: Work-Stealing vs. Shared-Nothing

Modern Rust Concurrency is defined by the trade-off between **General Purpose Flexibility** and **High-Performance Determinism**.

| Feature | Work-Stealing (Tokio Default) | Shared-Nothing (Thread-per-Core) |
|:--- |:--- |:--- |
| **Logic** | Tasks migrate between threads to balance load. | Tasks are pinned to a specific core for their lifetime. |
| **Constraints** | Requires `Send` + `Sync` + `'static` (Arc/Mutex boilerplate). | Allows `!Send` data (Rc/RefCell). No locks required. |
| **Performance** | High context switching; potential cache thrashing. | Maximum Cache Locality; Zero-cost borrows. |
| **Node.js Analogy** | A managed thread pool. | Running multiple independent Event Loops (one per core). |

### 1.1 The `'static` Requirement

In standard `tokio::spawn`, tasks are "fire and forget" and may outlive the parent scope. This forces the compiler to mandate `'static` lifetimes, preventing simple borrowing and necessitating `Arc<T>`.

---

## 2. Paradigm Shift: Structured Concurrency

Structured Concurrency binds the lifetime of child tasks to a parent scope, ensuring children complete before the parent exits.

* **Benefit:** Allows child tasks to hold references (`&T`) to the parent's data instead of owning/cloning it.
* **Implementation:**
    * **Low-Level:** `futures::stream::FuturesUnordered`.
    * **High-Level:** Libraries like `moro` (async scopes) or `tokio::task::JoinSet`.

---

## 3. Paradigm Shift: Shared-Nothing (Thread-per-Core)

Used for stateful, high-throughput systems (databases, storage engines, compute kernels) where hardware alignment is critical.

* **Logic:** One executor is pinned to one physical CPU core. Data stays in the L1/L2 cache of that core.
* **Benefit:** Eliminates the synchronization overhead of atomic counters (`Arc`) and locks (`Mutex`).
* **Runtimes:** `Glommio`, `Datadog's internal runtime`, or a single-threaded Tokio configuration.

---

## 4. The I/O Revolution: io_uring & Direct I/O

Standard I/O uses buffered kernel page caches, leading to memory pollution and CPU waste (memcpy).

* **Direct I/O (O_DIRECT):** Bypasses kernel cache, moving data from Disk to User Buffer via DMA.
* **io_uring:** Linux's high-performance asynchronous interface for submission/completion rings.
* **Data-Oriented View:** The architect, not the OS, decides what to cache in userspace.

---

## 5. Architectural Takeaway for Node.js Developers

Node.js achieved the correct **Concurrency Model** (Event Loops) but utilized a suboptimal **I/O Model** (Buffered I/O). High-performance Rust allows you to pair the Event Loop architecture (Thread-per-Core) with a superior I/O model (io_uring).
