---
conformant: false
created: 2026-02-04T18:28:15+00:00
last-synthesis: 2026-02-04
modified: 2026-08-13T10:53:41+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-cynefin-framework
source_of_truth: true
tags: [domain/systems-thinking, framework/cynefin, type/SoT]
title: SoT - Cynefin Framework
type: sot
---

## Minimum Viable Understanding (MVU)

The Cynefin Framework is a sense-making model that categorizes problems into five domains based on the relationship between cause and effect. Its primary utility is distinguishing between Complicated systems (expert-solvable, predictable parts, like a watch) and Complex systems (emergent, retrospective understanding only, like a rainforest).

## Working Knowledge

### The Five Domains

| Domain | Characteristic | Cause & Effect | Approach | Example |
|:--- |:--- |:--- |:--- |:--- |
| Clear (Simple) | Known Knowns | Obvious to all | Sense → Categorize → Respond | Processing an invoice. |
| Complicated | Known Unknowns | Discoverable by analysis | Sense → Analyze → Respond | Repairing a mechanical watch. |
| Complex | Unknown Unknowns | Only clear in retrospect | Probe → Sense → Respond | Managing a team; Distributed Software. |
| Chaotic | Unknowable | Non-existent or shifting | Act → Sense → Respond | A house fire; A generic outage. |
| Confusion | Disorder | Unknown | N/A | The state of not knowing where you are. |

### The "Cliff" of Complacency

There is a catastrophic boundary between Clear and Chaotic. If a Complex system is treated as if it were Clear (rigid rules, no feedback loops), it will eventually collapse into Chaos when reality diverges from the model.

## Current Understanding: Software as a Complex System

### The Semantic Clash: "Code is Deterministic"

A common point of confusion is why software is labeled Complex when code is deterministic (Input A + Function B = Output C).

- Micro View (Complicated): A single script in a vacuum is complicated. It is predictable and reducible.
- Macro View (Complex): Modern software runs in a hostile environment (network latency, hardware faults, asynchronous user behavior).

### Emergence in Software

Complexity arises from the interaction of components, not the components themselves.

- _Example:_ A "Retry on Fail" logic is simple (Complicated).
- _Emergence:_ When 10,000 clients retry simultaneously, they create a "Thundering Herd" (Retry Storm) that destroys the system. This behavior exists only in the collective, not the individual script.

## Related Knowledge

- Parent: [[SoT - Systems Thinking]]
- Core Concept: [[SoT - Emergence]] (The defining trait of the Complex domain)
