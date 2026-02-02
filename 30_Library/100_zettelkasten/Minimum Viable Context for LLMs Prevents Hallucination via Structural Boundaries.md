---
tags: [domain/ai, concept/mvc, governance]
status: evergreen
---

# Minimum Viable Context for LLMs Prevents Hallucination via Structural Boundaries

Minimum Viable Context (MVC) is the smallest set of structural information that prevents an LLM from inventing relationships while still enabling correct action.

### The MVC Components
For an LLM to reason accurately without "context rot," it requires three specific structural anchors:
1.  **Identity:** What entities exist? (Names, Kinds, Boundaries).
2.  **Constraint:** What must not break? (Invariants, Roles, Manifestos).
3.  **Reachability:** What is affected? (Callers, dependents, Blast Radius).

### MVC vs. Full Context
MVC is a **stop condition**, not a token count. 
- **Exclude:** Function bodies, implementation details, historical logs, and "how it works" prose. These belong in the "Surgery" phase, not the "Planning" phase.
- **Include:** Skeletons, dependency graphs, and type definitions.

### The MVC Test
The boundary of MVC is discovered by removing information until the model first begins to hallucinate a dependency or relationship, then adding back only the specific structural anchor that prevents it.

---
rel:: operationalizes [[LLM Reasoning Efficiency is Proportional to Structural Constraint]]
rel:: enforced-by [[MVC Enforcement Structural Gates for LLM Agents]]
