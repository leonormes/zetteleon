---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/70024f38abf3"
author:
  - "[[Gemini]]"
published:
created: 2026-01-05
description: "Created with Gemini"
tags:
  - "input"
---
https://youtu.be/HB5TrK7A4pI?si=\_Bk\_vPHBH8mZwiU9

This presentation by Gerald Sussman, "We Really Don't Know How to Compute!", argues that modern computing remains trapped in a paradigm of scarcity, prioritising low-level optimisation over the high-level flexibility and evolvability found in biological systems.

The following framework deconstructs Sussman's critique and his proposed mental models for a more resilient computing architecture.

### 1\. The Core Thesis: Obsolete Paradigms

Sussman posits that current programming languages and architectures are "obsolete" because they are designed to minimise CPU and memory usage—resources that are now effectively free \[[06:09](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=369)\]. The primary bottleneck is no longer hardware, but the **cost of programmers** and the **brittleness of code** \[[07:03](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=423)\].

### 2\. Biological Benchmarks for Computation

Sussman uses biological phenomena as a "proof of concept" for a superior computational model:

- **Concept Density & Flexibility:** The human genome (~1GB) is comparable in size to Microsoft Windows, yet it produces a vastly more complex, flexible, and evolvable machine \[[01:34](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=94)\].
- **Latency vs. Parallelism:** The human brain resolves complex visual illusions (like the Kanizsa triangle) in ~100ms, suggesting a massive parallel process with a depth of only 30-40 steps—a feat current software cannot replicate \[[01:16](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=76)\].
- **Regenerative Logic:** Biological systems, such as salamanders regrowing limbs, operate via local communication where cells "talk" to neighbours to resolve structural inconsistencies \[[04:09](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=249)\].

### 3\. Proposed Architectural Frameworks

#### Extensible Generic Operators

To achieve evolvability, software must support dynamic extension at runtime rather than just compile-time.

- **Function Overloading:** Operators should handle any type (integers, rationals, functions, matrices) without breaking the original system \[[10:45](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=645)\].
- **Automatic Differentiation:** By extending primitives to handle "hyper-real" numbers (x + dx), the chain rule is implemented automatically, enabling complex physics simulations with minimal code \[[16:20](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=980)\].

#### Propagator Networks

Sussman proposes moving away from the "expression tree" model (where data flows strictly upward) to a **Propagator Architecture**:

- **Autonomous Machines:** Computing is viewed as a network of independent propagators connected to "cells" \[[33:04](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=1984)\].
- **Monotonic Information Gain:** Cells do not just hold values; they merge information monotonically. As more propagators "observe" a cell, the precision of the value improves \[[34:03](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=2043)\].
- **Directional Independence:** Unlike standard functions, information can propagate in any direction (e.g., if you know the sum and one addend, you can deduce the other) \[[01:04:13](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=3853)\].

#### Truth Maintenance Systems (TMS) & Provenance

To handle real-world complexity, systems must manage **provenance** (the origin of data) and **inconsistency**:

- **Locally Consistent Sub-worlds:** Rather than a single "correct" state, a TMS allows the system to maintain multiple, even contradictory, worldviews simultaneously \[[50:27](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=3027)\].
- **Dependency-Directed Backtracking:** When a contradiction is found, the system uses provenance to pinpoint and prune only the relevant assumptions, rather than chronologically undoing all recent work \[[55:38](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=3338)\].

### 4\. Degeneracy as a Design Principle

Sussman advocates for **degeneracy** —the biological principle of having multiple, overlapping ways to achieve the same result \[[01:03:14](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=3794)\]. In software, this means using different mathematical formulations (Newtonian, Lagrangian, Hamiltonian) or programming styles (functional, imperative, logic-based) within the same problem space to reveal different insights and provide redundancy \[[39:18](http://www.youtube.com/watch?v=HB5TrK7A4pI&t=2358)\].

### Summary of Architectural Shift

| Feature | Current Paradigm | Proposed Paradigm |
| --- | --- | --- |
| **Primary Goal** | Correctness & Performance | Evolvable & Flexible |
| **Logic Structure** | Strict Expression Trees | Propagator Networks |
| **Data Integrity** | Global Consistency | Local Consistency (TMS) |
| **System State** | Destructive Updates | Monotonic Information Merging |

[https://youtu.be/HB5TrK7A4pI?si=\_Bk\_vPHBH8mZwiU9](https://youtu.be/HB5TrK7A4pI?si=_Bk_vPHBH8mZwiU9)

Google Account

Leon Ormes

leonormes@gmail.com