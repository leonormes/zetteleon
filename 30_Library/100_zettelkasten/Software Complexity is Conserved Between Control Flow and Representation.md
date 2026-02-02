---
tags: [domain/software-engineering, concept/complexity, law]
status: evergreen
---

# Software Complexity is Conserved Between Control Flow and Representation

Software complexity obeys a conservation law: it cannot be destroyed, only relocated. In any non-trivial system, complexity must reside in one of two primary containers:
1.  **Control Flow (Code/Time):** Logic, branches, loops, and temporal sequences.
2.  **Representation (Data/Space):** Schemas, types, graphs, and static structures.

### The Trade-off
When a developer "worries about data structures" (Torvalds/Pike), they are moving complexity out of the **procedural** layer and into the **structural** layer. 

- **Smart Structures ⇒ Dumb Code:** If the data model perfectly mirrors the problem domain's constraints, the algorithms required to manipulate that data become trivial, often reducing to simple traversals or lookups.
- **Dumb Structures ⇒ Brittle Code:** If the data model is a "flat bucket" or lacks internal constraints, the code must compensate with defensive null-checks, complex `if/else` ladders, and state-tracking flags.

### Cognitive and Computational Implications
- **Static vs. Dynamic:** Humans and machines find it easier to reason about static topology (what things are) than dynamic execution (how things change over time).
- **Schema Debt:** Because data structures often "ossify" (become hard to change once shared or at scale), failing to encode complexity in structure early leads to "interest" paid in the form of increasingly complex and fragile code.

### Relation to LLMs
This law is the foundation for the [[LLM Reasoning Efficiency is Proportional to Structural Constraint|LLM Corollary]], as LLMs are significantly more effective at traversing structure than simulating execution.

---
rel:: supports [[SoT - Complexity Conservation]]
source:: [[Code vs Data Structures (Torvalds Essay)]]
