---
aliases: []
confidence: ""
created: 2026-01-04T09:07:38+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:50:02+00:00
purpose: ""
review_interval: ""
see_also: []
source: "Database Internals by Alex Petrov"
source_of_truth: []
status: ""
tags: [data-modeling, database-internals, rust, storage-engines]
title: 2026-01-03-Database-Internals-Data-Layout
type: ""
---

## Data Layout: Row-Oriented vs. Column-Oriented

This note summarizes the physical data layout strategies discussed in Chapter 1 of _Database Internals_, with a focus on how these impact data modeling in Rust.

### 1. Row-Oriented Data Layout

Data is partitioned **horizontally**. Values belonging to the same row are stored contiguously on disk.

- **Spatial Locality:** Excellent for accessing entire records. Since disk I/O is block-wise, a single read usually fetches all fields for a record.
- **Use Cases:**
    - **OLTP (Online Transactional Processing):** User registrations, order processing, point lookups.
    - Scenarios where you mostly read/write the entire "struct" (e.g., `User { id, name, email }`).
- **Rust Analogy:**
    - A `struct` where fields are stored together in memory (especially with `#[repr(C)]`).
    - Storing a collection as `Vec<MyStruct>`.

### 2. Column-Oriented Data Layout

Data is partitioned **vertically**. Values for the same column are stored contiguously.

- **Computational Efficiency:**
    - **Cache Utilization:** Reading multiple values for the same column in one run improves CPU cache hits.
    - **Vectorization:** Allows for SIMD (Single Instruction Multiple Data) optimizations.
- **Compression:** Storing same-typed data together (e.g., all integers) allows for much higher compression ratios (using algorithms like Run-Length Encoding or Delta Encoding).
- **Use Cases:**
    - **OLAP (Online Analytical Processing):** Trend analysis, computing averages, stock market history.
    - Scenarios where you only need a subset of columns across millions of rows.
- **Rust Analogy:**
    - A "struct of arrays" (SoA) pattern.
    - Storing a collection as a `struct MyCollection { ids: Vec<u32>, names: Vec<String>, prices: Vec<f64> }`.

### Summary Comparison

| Feature | Row-Oriented | Column-Oriented |
|:--- |:--- |:--- |
| **Access Pattern** | Record-based (all columns) | Field-based (subset of columns) |
| **Locality** | Spatial (row-wise) | Spatial (column-wise) |
| **Efficiency** | Point queries / Range scans | Aggregates / Analytical queries |
| **Compression** | Lower | Higher (same-type proximity) |
| **Rust Pattern** | `Vec<Struct>` (AoS) | `Struct { Vec, Vec }` (SoA) |

### Implementation Considerations for Rust

- **Row-Oriented:** Use `#[repr(C)]` to maintain predictable binary offsets if serializing the whole struct to a `slotted page`.
- **Column-Oriented:** Consider crates like `arrow` (Apache Arrow) which provide an implementation of memory-efficient columnar formats in Rust.
- **Wide Column Stores:** (e.g., HBase/Cassandra) represent data as a multidimensional map; columns are grouped into families, and data within a family is stored row-wise.

---

**Next Action:** Review Chapter 3 (File Formats) for details on implementing Slotted Pages for variable-size data in Rust.
