---
created: 2026-01-16T10:50:09+00:00
modified: 2026-01-20T15:33:29+00:00
title: 'The Corrected Hierarchy (The "Type-Driven Onion")'
---

# The Corrected Hierarchy (The "Type-Driven Onion")

1. Layer 1 (The Core): Types & Invariants

- Industry Term: Domain Primitives / Value Objects.
- Definition: The fundamental "atoms" of your reality. (e.g., `struct UserId` vs `String`).
- Why First? If `UserId` creates itself, you don't need to check for security vulnerabilities in 50 different functions. The Type is the Security.
- Surgeon Tool: Librarian (`tree-sitter getsymbols`). It builds the `architectureskeleton.md` which lists only these Types. This is the "Source of Truth."
    
1. Layer 2: Data

- Industry Term: Aggregates / State.
- Definition: How those Types are combined into valid structures (e.g., `struct User { id: UserId, email: Email }`).
- Surgeon Tool: Librarian (`getast`). It maps how data is structured.
    
1. Layer 3: Data Transformations (The Logic)

- Industry Term: Pure Functions / Pipelines.
- Definition: deterministic A $\to$ B functions. No side effects.
- Surgeon Tool: Scout (`tree-sitter findusage`). This is where the Scout "traces" the call hierarchy. It understands flow by seeing who consumes the Data from Layer 2.
    
1. Layer 4: Security & Boundaries

- Industry Term: Interfaces / Ports & Adapters.
- Definition: Who is allowed to call whom? (Public vs Private). This is where "Security" happens in a Type-Driven system—at the edges.
- Surgeon Tool: Architect (Review Phase). The Architect specifically checks "Module Boundaries" and "Lifecycle Integrity."
    
1. Layer 5: Maintainability (Easy to Change)

- Definition: The result of the previous 4 layers being correct.
- Surgeon Tool: Specialist (Refactor). Because Layers 1-4 are enforced, the Specialist can change a Type in Layer 1, and the Compiler (and Scout) immediately highlights the exact blast radius in Layer 3.
