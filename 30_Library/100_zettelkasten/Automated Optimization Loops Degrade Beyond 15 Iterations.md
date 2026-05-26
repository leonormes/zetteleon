---
created: 2026-04-10T00:00:00+00:00
modified: 2026-05-26T11:44:36+00:00
tags: [iterations, optimization, quality-control, token-management]
title: Automated Optimization Loops Degrade Beyond 15 Iterations
---

## Automated Optimization Loops Degrade Beyond 15 Iterations

Effective automated optimization typically requires 5 to 10 iterations to converge on a quality result. Exceeding 15 iterations tends to degrade output quality and increase token costs without commensurate gain. The degradation likely reflects accumulated context drift—each iteration adds noise to the running context, and later passes optimize against a distorted signal rather than the original objective.

### Scope & Conditions

Applies when setting the loop count for recursive optimization tasks in agentic frameworks. The 5–10 / 15 heuristic is empirical guidance from a specific framework (Auto Research), not a universal law. The appropriate number may vary with task complexity and context window management strategies. The principle—that longer loops introduce diminishing returns and eventual quality regression—is the transferable insight.

### Evidence

> "recommends running 5 to 10 iterations; going beyond 15 can degrade the output and unnecessarily increase your token costs [17:00]"

### Implications

- Prevents quality "drift" or over-fitting in long agentic optimization loops.
- Functions as a primary cost-management constraint: token spend scales with iteration count, so a hard ceiling is both a quality and an economics control.

### Related

- [[SoT - Agentic AI Design Patterns]]—direct concept match: the "Reflection" pattern (iterative critic-refine loop) is the exact mechanism this heuristic governs; the atom provides a concrete bound for a pattern that the SoT describes structurally but does not constrain numerically.
- [[Shrinking the Loop Gathers Experiential Feedback Safely]]—shared mechanism: both advocate for bounded, controlled iteration over unlimited looping; the contexts differ (cognitive/ADHD overthinking vs. automated optimization), but the structural insight—that loop size must be constrained to avoid compounding noise—is shared.

### See Also

- [[Deep Agents for Long Horizon Planning]]
