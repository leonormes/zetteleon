---
aliases: [Engineering Management, Project Planning, Software Estimation, Stakeholder Management]
conformant: false
created: 2025-12-27T20:38:44+00:00
modified: 2026-08-13T10:53:49+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/so-t-software-estimation-and-management
tags: [career, estimation, leadership, management]
title: SoT - Software Estimation and Management
type: sot
---

## 1. Definitive Statement

> [!definition] The Estimation Mandate
> Estimation is a business tool for decision-making, not a comfort mechanism.
> Your professional duty is to provide the Truth (ranges, probabilities, risks) so the business can allocate resources effectively, rather than providing "lies" (arbitrary dates) to purchase temporary emotional comfort.

## 2. The Trap: The Logic of Failure

Providing a Single Point Estimate (e.g., "It will be done in 2 weeks") for an undefined problem is "Professional Suicide."

- The Mechanism: Developers estimate based on a "Best Case Scenario" (perfect code, no interruptions).
- The Reality: Entropy exists. Requirements change, bugs appear, and systems break.
- The Result: When the fantasy deadline is missed, the developer owns the liability. This leads to burnout, technical debt (cutting corners), and loss of trust.

## 3. The Framework: Truth-Based Estimation

To maintain professional integrity and career longevity, adhere to these three rules:

### Rule 1: Never Give a Single Date

Protocol: Always provide a Range.

- _Bad:_ "Friday."
- _Good:_ "3 to 6 weeks, depending on the complexity of the legacy integration."
- _Logic:_ As information increases, the cone of uncertainty narrows, but it never reaches zero until the work is done.

### Rule 2: Request a Discovery Phase

Protocol: If precision is demanded, buy it with time.

- _Script:_ "I cannot give you a responsible date right now. Give me 2 days to investigate the code, and I will come back with a tight range."
- _Logic:_ An estimate based on zero research is a guess. A guess is a lie.

### Rule 3: Reframe the Problem

Protocol: Shift focus from "The Output" (The App) to "The Outcome" (The Business Value).

- _Script:_ "If we need this by Friday, we can't build the full feature. But we can solve the core customer problem by doing X."
- _Logic:_ This turns the conversation from a hostage negotiation ("Do this impossible thing") into a collaborative trade-off ("Here are our options").

## 4. Operational Scripts (Mental Models)

| Scenario | The Pushback | The Professional Response |
|:--- |:--- |:--- |
| "I need a date." | "Give me a single date." | "I can give you a date, but it will be a lie based on 'nothing going wrong'. Do you want the happy path date (30% chance) or the realistic range (90% chance)?" |
| "That's too long." | "Can't you do it faster?" | "I can't change the complexity of the math. But we can change the scope. What features can we cut to hit that date?" |
| "Just guess." | "I won't hold you to it." | "Experience shows that guesses become deadlines. I will take 2 hours to research this and give you a real answer." |

## 5. Minimum Viable Understanding (MVU)

1. Ranges, Not Dates: Uncertainty is a fact of physics. Represent it.
2. Discovery is Work: You cannot estimate what you do not understand.
3. Trade-offs, Not Magic: Time, Scope, Quality. You can only pick two.

## Related

- [[Value Stream Analysis via LLM — Feasibility + Source Map + Prompt]]
- [[SoT - Pragmatism vs Rigour in Software]]
- [[Shift to Architectural Oversight]]
- [[SoT - Accelerate & DORA]]
