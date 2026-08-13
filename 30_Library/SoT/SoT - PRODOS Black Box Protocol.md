---
aliases: [Black Box Thinking, Error Engine, Marginal Gains]
conformant: false
created: 2026-01-11T21:20:00+00:00
modified: 2026-08-13T10:53:47+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-prodos-black-box-protocol
tags: [adhd-tools, improvement-logic, prodos, system-architecture]
title: SoT - PRODOS Black Box Protocol
type: sot
---

## 1. The Core Philosophy

Failure is the only reliable source of high-fidelity data. In PRODOS, we move from Closed-Loop (ignoring errors) to Open-Loop (extracting logic from errors).

- Axiom: A mistake is only a "Failure of Ineptitude" if it happens twice.
- Objective: Turn "Cognitive Dissonance" (denial) into "Context Integration" (updates to the SoT).

---

## 2. The Feedback Loop (Data Ingest)

### 2.1 The Post-Mortem (The Trace)

Whenever an outcome $\neq$ Desired State ($S_d$), trigger a HEAD Note Trace:

1. The Gap: What was the delta between expectation and reality?
2. The Logic Flaw: Was this a "Failure of Ignorance" (missing data) or "Ineptitude" (failed execution)?
3. The Root Node: Use "The Five Whys" to find the system flaw, not the human flaw.

### 2.2 Marginal Gains (The Compounding Rule)

Break down the system into its smallest components. Improve one variable by 1% each week.

- PRODOS Strategy: Update one Instruction SoT (Checklist) after every failure to prevent re-entry of that specific error.

---

## 3. Pre-Mortem Protocol (The Defense)

Before launching a significant project (The "Capstone"), perform a Prospective Hindsight exercise.

1. The Scenario: Imagine it is 6 months from now and the project has failed catastrophically.
2. The Autopsy: List every reason _why_ it failed (e.g., "I lost focus," "The tech stack broke," "Assumptions were wrong").
3. The Mitigation: Create a Checklist Pause-Point for each identified risk.

---

## 4. Architectural Guardrails (ADHD Support)

### 4.1 Radical Transparency

To bypass the "Seniority Trap" or ego-driven denial, PRODOS operators must treat their HEAD notes as public-facing audits.

- Rule: If you are tempted to delete a record of a mistake, it MUST be logged in the `episodic/` cache instead.

### 4.2 The "Just Culture" Buffer

Distinguish between Complexity Errors (unpredictable) and Protocol Errors (ignoring the checklist).

- Action: If it's a Protocol Error, the MVA is to simplify the checklist until "Activation Energy ≈ 0."
