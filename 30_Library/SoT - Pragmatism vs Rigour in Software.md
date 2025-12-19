---
aliases: [Pragmatism vs Theory in Software, Rigour vs Velocity]
confidence: 5/5
confidence-gaps: []
created: 2025-12-19T13:09:01Z
decay-signals: []
epistemic: framework
last_reviewed: 2025-12-19
modified: 2025-12-19T13:09:01Z
purpose: "To define the fundamental conflict between building software that is theoretically 'correct' versus software that is 'good enough' and ships quickly."
quality-markers: [Defines the core trade-off, Establishes the two opposing philosophies.]
related-soTs: ["[[SoT - The \"Worse is Better\" Philosophy]]"]
resonance-score: 10
review_interval: 6 months
see_also: []
source_of_truth: true
status: stable
supersedes: []
tags: ["philosophy", "software-engineering", "mental-model"]
title: SoT - Pragmatism vs Rigour in Software
type: SoT
uid: 
updated:
---

## 1. Definitive Statement

> [!definition] Definition
> The **Pragmatism-Rigour Conflict** is the central tension in software engineering between two opposing value systems:
>
> 1. **Pragmatism (Velocity):** Values speed of implementation, adaptability, and delivering "good enough" solutions quickly. It prioritizes market adoption and iteration.
> 2. **Rigour (Correctness):** Values mathematical proof, theoretical purity, and building systems that are provably free of entire classes of errors. It prioritizes stability and long-term maintenance.

---

## 2. The Core Problem: A Spectrum of Trade-offs

The software industry exists on a spectrum between these two poles. Neither is inherently "better," but choosing a position on the spectrum has profound consequences for cost, speed, safety, and scalability. The core problem is that many teams make this choice unconsciously.

| Philosophy | Pragmatism (e.g., Python, JavaScript) | Rigour (e.g., Idris, Coq) |
| :--- | :--- | :--- |
| **Primary Goal** | Get a working product to market fast. | Build a verifiably correct and secure system. |
| **View on Errors** | Errors are inevitable and should be caught at runtime (testing, monitoring). | Errors are preventable and should be eliminated at compile time. |
| **Cost Model** | Low upfront cost (fast development), high long-term cost (maintenance, bug-fixing, security patches). | High upfront cost (slow, complex development), low long-term cost (fewer bugs, easier maintenance). |
| **Developer Pool** | Large. Lower barrier to entry. | Small. Requires specialized knowledge of formal methods. |
| **Dominant Principle** | [[SoT - The "Worse is Better" Philosophy]] | The "Correctness-by-Construction" Principle |

---

## 3. The Architecture of Each Approach

### A. The Pragmatic Architecture ("The Band-Aid Economy")

1. **Languages:** Use flexible, "padded-cell" languages that abstract away complexity.
2. **Safety Net:** Rely on a massive ecosystem of external tools to provide safety:
    - Extensive unit and integration test suites.
    - Static analysis and linters.
    - CI/CD pipelines for automated testing.
    - Observability and monitoring systems to catch runtime failures.
    - Web Application Firewalls (WAFs) and security scanners.
3. **Outcome:** Fragility masked by redundancy. We spend billions on runtime mitigation because we don't pay the upfront cost of compile-time proof.

### B. The Rigorous Architecture ("Correctness by Construction")

1. **Languages:** Use languages with powerful type systems, like [[SoT - Dependent Types in Software]], that can enforce invariants at compile time.
2. **Safety Net:** The compiler *is* the primary safety net. If the code compiles, it is guaranteed to be free of certain types of errors.
3. **Testing:** Testing focuses on high-level properties and logic, not on "did I forget a null check?"
4. **Outcome:** Provably correct, robust systems that are conceptually harder to build but far cheaper to maintain and secure.

---

## 4. Protocols & Implementation

### Protocol: Choosing Your Position on the Spectrum

*Use when starting a new project or defining team engineering principles.*

1. [ ] **Define the Cost of Failure:** What happens if this software fails? Is it a critical medical device (requires rigour) or a social media app (can tolerate pragmatism)?
2. [ ] **Estimate Project Lifespan:** Is this a short-lived prototype (favor pragmatism) or a 10-year platform (invest in rigour)?
3. [ ] **Assess Talent Availability:** Do you have access to developers skilled in formal methods, or do you need to hire from a broader, more pragmatic talent pool?
4. [ ] **Make a Conscious Choice:** Explicitly state your team's position on the spectrum. "We are a pragmatic team that values velocity, and we will mitigate risk with extensive testing." or "We are a rigour-focused team, and we accept a slower development pace in exchange for provable correctness."

---

## 5. Minimum Viable Understanding (MVU)

1. **Software design is a trade-off between moving fast (Pragmatism) and being correct (Rigour).**
2. **Pragmatism optimizes for low upfront cost and speed, but creates high long-term maintenance and security costs.**
3. **Rigour optimizes for long-term stability and safety, but has a high upfront cost in time and talent.**
4. **The most important step is to choose your position on this spectrum consciously, rather than by accident.**

---

## 6. Open Questions & Tensions

- **Tension:** Can we have both? The industry is constantly searching for a "holy grail" language or system that provides the safety of rigour with the ease of pragmatism. So far, this has proven elusive.
- **Tension:** The "Pragmatic Ceiling." A team that only ever operates in the pragmatic realm may find it impossible to build the kind of highly reliable, secure systems required for certain domains (aerospace, finance, etc.), hitting a ceiling on the impact they can have.

## 7. Related Components

- [[SoT - The "Worse is Better" Philosophy]]
- [[SoT - Dependent Types in Software]]
- [[SoT - Padded Cell vs Nanny Languages]]
- [[SoT - Runtime Guards vs Compile-Time Proofs]]
