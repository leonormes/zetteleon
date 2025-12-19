---
aliases: ["Commit to Main", "Main-as-Default TBD", "Trunk Based Development SoT"]
confidence: 5/5
created: 2025-12-15T00:00:00Z
epistemic: Validated via 10-year longitudinal practice and DORA metrics.
last_reviewed: 2025-12-15
modified: 2025-12-19T10:12:35Z
purpose: To define "Main-as-Default Trunk Based Development" as the canonical software delivery methodology for ProdOS, optimizing for the smallest robust increments of change.
related-soTs: ["[[SoT - Process Primacy (Systems Over Goals)]]", "[[SoT - PRODOS (System Architecture)]]"]
review_interval: 1 year
see_also: []
source_of_truth: true
status: stable
tags: ["agile", "devops", "git", "software_engineering", "tbd"]
title: SoT - Main-as-Default Trunk Based Development
type: SoT
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition: Main-as-Default TBD
> **Main-as-Default Trunk Based Development** is a workflow where developers commit unfinished but safe work directly to the `main` branch, relying on small increments and feature flags rather than long-lived feature branches.
>
> The core hypothesis is: **"Optimizing for continually integrating and shipping the smallest robust increments of change will in itself ensure quality and stability."**

### The Core Protocol

1. **Commit Straight to Main:** Developers push directly to the trunk.
2. **Continuous Pipeline:** Every commit triggers build, test, and deployment to a test environment.
3. **Deployability:** Any developer *can* deploy to production at any time.
4. **Feedback:** Developers own the change until it is validated in production.

---

## 2. The Myth of Prerequisites

A common barrier to adoption is the belief that TBD requires an "elite" setup (100% test coverage, TDD, Mob Programming). Empirical data refutes this.

**You DO NOT need:**

- Complex automated test suites (at first).
- Strict Pair/Mob programming.
- Rigid TDD workflows.
- To "wait until the next greenfield project."

**You DO need:**

- **Small Increments:** The discipline to break work down into tiny, safe batches.
- **Feature Flags:** The ability to decouple "Deployment" (code on server) from "Release" (feature visible to user).
- **Mindset Shift:** Accepting that `main` is a place for *work in progress*, not just "finished" code.

> **The Insight:** High transaction costs (heavy PR process, manual QA) lead to *larger* batches, which actually *increases* risk. TBD lowers transaction costs, enabling smaller, safer steps.

---

## 3. Techniques for Safe Commits

How do you commit to main without breaking it?

1. **Feature Flags:** Wrap new logic in a toggle (`if (feature.enabled) { new() } else { old() }`).
2. **Branch by Abstraction:** Introduce an interface, route traffic to the old implementation, build the new one in parallel, then switch.
3. **Dark Launching:** Execute the new code path but discard the result (or log it) to validate performance without affecting users.
4. **UI-Last Development:** Build the backend API endpoints first. They are "live" but unreachable by users until the frontend is updated.
5. **Mocking the Frontend:** If building UI, mock the data response so frontend work can proceed before the backend is fully wired.

---

## 4. Empirical Evidence (Case Study Results)

A survey of a team using this method for 10 months revealed:

- **Adoption:** 9/10 comfort level with committing to main.

- **Stability:** "Main is often broken" scored **1/10** (Strongly Disagree).

- **Efficiency:** "Trunk-based development has made our delivery cycle faster" scored **8.5/10**.

- **Safety:** "I feel nervous when I deploy to production" scored **3/10**.

**The "Lift" Metaphor:**
Building software this way is like pouring concrete in **"lifts"** (small layers). Each layer settles and hardens, creating a stronger structure than trying to pour the entire building at once.

---

## 5. Addressing Common Objections

| Objection | Counter-Reality |
| :--- | :--- |
| **"Main will break constantly."** | Small, atomic commits are easier to fix/revert than massive merge bombs. Empirical data shows *increased* stability. |
| **"We need Pull Requests for quality."** | PRs often become "rubber stamps" or delay feedback. Post-commit review (or pairing) is faster and often more engaged. |
| **"It's too cowboy."** | It requires *more* discipline, not less. The safety comes from the small batch size, not the process gate. |

---

## 6. Implementation Strategy

To switch your team to TBD:

1. **Stop Branching:** Start committing small, safe changes to main today.
2. **Add a Toggle:** Introduce a simple config-based feature flag system.
3. **Decouple:** Separate the concept of "Deploying code" from "Releasing features."
4. **Refactor:** Don't wait for a rewrite. Apply "Strangler Fig" patterns to legacy code.
