---
aliases: ["Software Estimation", "Engineering Management", "Stakeholder Management", "Project Planning"]
confidence: "5/5"
created: 2025-12-27T20:38:44+00:00
epistemic: "pattern"
last_reviewed: "2025-12-27"
modified: 2025-12-27T20:40:43+00:00
purpose: "To define the principles and protocols for accurate software estimation and effective stakeholder management."
review_interval: "6 months"
see_also: ["[[SoT - Data-Centric Software Engineering]]", "[[SoT - PRODOS (System Architecture)]]"]
source_of_truth: []
status: "stable"
tags: ["management", "leadership", "estimation", "career"]
title: SoT - Software Estimation and Management
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] The Estimation Mandate
> **Estimation is a business tool for decision-making, not a comfort mechanism.**
> Your professional duty is to provide the **Truth** (ranges, probabilities, risks) so the business can allocate resources effectively, rather than providing "lies" (arbitrary dates) to purchase temporary emotional comfort.

## 2. The Trap: The Logic of Failure

Providing a **Single Point Estimate** (e.g., "It will be done in 2 weeks") for an undefined problem is "Professional Suicide."

- **The Mechanism:** Developers estimate based on a "Best Case Scenario" (perfect code, no interruptions).
- **The Reality:** Entropy exists. Requirements change, bugs appear, and systems break.
- **The Result:** When the fantasy deadline is missed, the developer owns the liability. This leads to burnout, technical debt (cutting corners), and loss of trust.

## 3. The Framework: Truth-Based Estimation

To maintain professional integrity and career longevity, adhere to these three rules:

### Rule 1: Never Give a Single Date

**Protocol:** Always provide a **Range**.
- *Bad:* "Friday."
- *Good:* "3 to 6 weeks, depending on the complexity of the legacy integration."
- *Logic:* As information increases, the cone of uncertainty narrows, but it never reaches zero until the work is done.

### Rule 2: Request a Discovery Phase

**Protocol:** If precision is demanded, buy it with time.
- *Script:* "I cannot give you a responsible date right now. Give me 2 days to investigate the code, and I will come back with a tight range."
- *Logic:* An estimate based on zero research is a guess. A guess is a lie.

### Rule 3: Reframe the Problem

**Protocol:** Shift focus from "The Output" (The App) to "The Outcome" (The Business Value).
- *Script:* "If we need this by Friday, we can't build the full feature. But we can solve the core customer problem by doing X."
- *Logic:* This turns the conversation from a hostage negotiation ("Do this impossible thing") into a collaborative trade-off ("Here are our options").

## 4. Operational Scripts (Mental Models)

| Scenario | The Pushback | The Professional Response |
|:--- |:--- |:--- |
| **"I need a date."** | "Give me a single date." | "I can give you a date, but it will be a lie based on 'nothing going wrong'. Do you want the happy path date (30% chance) or the realistic range (90% chance)?" |
| **"That's too long."** | "Can't you do it faster?" | "I can't change the complexity of the math. But we can change the scope. What features can we cut to hit that date?" |
| **"Just guess."** | "I won't hold you to it." | "Experience shows that guesses become deadlines. I will take 2 hours to research this and give you a real answer." |

## 5. Minimum Viable Understanding (MVU)

1. **Ranges, Not Dates:** Uncertainty is a fact of physics. Represent it.
2. **Discovery is Work:** You cannot estimate what you do not understand.
3. **Trade-offs, Not Magic:** Time, Scope, Quality. You can only pick two.
