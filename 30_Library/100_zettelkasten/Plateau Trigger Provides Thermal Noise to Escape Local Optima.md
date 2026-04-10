---
created: 2026-04-10T12:00:00+00:00
modified: 2026-04-10T16:52:03+00:00
tags: [exploration, heuristics, optimization, problem-solving]
title: Plateau Trigger Provides Thermal Noise to Escape Local Optima
---

## Plateau Trigger Provides Thermal Noise to Escape Local Optima

When a CORAL agent's performance plateaus, the Heartbeat Protocol fires a plateau trigger commanding the agent to attempt a completely orthogonal mathematical approach. This "thermal noise" impulse pushes the agent out of the attractor basin it has converged on, mimicking the role of temperature in simulated annealing: controlled random perturbation to escape local minima.

### Scope & Conditions

Activated by the Heartbeat Intervention Protocol when an agent's measured progress stalls below a defined threshold. Specific to mathematical research optimisation in CORAL; the underlying principle—force orthogonal exploration when convergence fails—is domain-agnostic. Effectiveness depends on the orthogonality of the commanded approach being genuinely different, not just a surface variation.

### Evidence

> "Plateau Triggers: If an agent reaches a dead end, it is commanded to attempt a completely orthogonal mathematical approach, providing a 'thermal noise' impulse to push it into new territory" [06:46]

### Implications

- Forces divergence in reasoning precisely when the agent's natural tendency is to converge more tightly on a failing strategy.
- Formalises the simulated annealing principle as an agentic workflow heuristic: scheduled perturbation as a first-class design element rather than an ad-hoc escape.

### Related

- [[Divergent Thinking Outperforms Narrow Specialization]]—shared mechanism: both prescribe switching to broader, orthogonal thinking when convergent approaches stall; the plateau trigger is an automated, operationalised form of the same cognitive shift described in that note.
- [[Automated Optimization Loops Degrade Beyond 15 Iterations]]—extends: the degradation heuristic establishes that long loops produce diminishing returns; the plateau trigger is the active intervention that fires before that ceiling is reached, making the two notes a complementary loop-management protocol.
