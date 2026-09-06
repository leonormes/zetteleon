---
axiom: true
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-29T09:35:58+00:00
permalink: llmeon/30-library/100-zettelkasten/canaries-precise-trigger-alarms-reduce-false-positive-security-noise
proposition: A canary is a security alarm scoped to trigger only on exact, highly
  specific identifiers (e.g., an exact sensitive filename) rather than broad pattern
  matching. This precision reduces false-positive noise, making the alarm signal trustworthy
  enough that a real trigger is treated as a genuine breach rather than routine background
  noise.
tags: [domain/llm, topic/monitoring, topic/pkm, topic/privacy, topic/safety]
title: Canaries - Precise Trigger Alarms Reduce False-Positive Security Noise
type: claim
---

## Canaries - Precise Trigger Alarms Reduce False-Positive Security Noise

A broad security rule ("alert if any file containing 'tax' is accessed") generates constant false positives in a working vault—innocuous notes about tax policy, articles referencing taxes, and so on all trigger it. Eventually the alarm is ignored.

A canary inverts this: it is scoped to an exact, narrow trigger—typically one specific filename or identifier that has no legitimate reason to ever be accessed by the agent. Because the canary almost never fires under normal operation, a trigger is unambiguous: it means the boundary was actually crossed.

### Scope & Conditions

Effective when:

1. You can name the exact sensitive artifact in advance (a specific filename, a specific string)
2. False positives would otherwise erode trust in the alarm system
3. The cost of a missed real breach outweighs the cost of building precise, narrow rules

Less effective for:

- Detecting novel or unanticipated breach vectors (canaries only catch what they're tuned for)
- Broad categories of sensitive content where exact identifiers can't be enumerated

### Evidence

Source: "I Built Karpathy's LLM Wiki in Claude Code (No Vector DB)" (Achuth G. Ramesh). Quote: "To prevent leaks, specific alarms were set up to trigger only if exact, highly sensitive file names were ever accessed, reducing the noise of false alarms" [09:32].

### Implications

- Signal-to-noise as a trust mechanism: An alarm that never cries wolf is an alarm people actually act on when it fires.
- Requires upfront enumeration: You must know what to protect in advance; canaries don't generalise to unknown-unknowns.
- Complementary to broad rules, not a replacement: Canaries catch the "should never happen" case; broader heuristics still have a role for less certain risks.

### Related

- [[Privacy Tombstones Mark Sensitive Files as Off-Limits to AI Agents]]—complementary: tombstones prevent access structurally; canaries detect if prevention failed.
- [[Reasoning Loops Require Explicit Stopping Conditions (End-Loop Guardrails)]]—analogous: both are precision-tuned control mechanisms that trade generality for reliability.
- [[Trace Logging and Event Trees for Agent Observability]]—related: canary triggers are a specialised case of observability, tuned for maximum signal.

### See Also

- [[SoT - LLM Wiki Pattern]]

[supports:: [[Privacy Tombstones Mark Sensitive Files as Off-Limits to AI Agents]], strength=3, confidence=medium]
