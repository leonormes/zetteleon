---
aliases: []
confidence: ""
created: 2026-01-07T17:59:36+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:50:02+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: Active
tags: ["SoftwareEngineering/Architecture", "TheHuman/Philosophy", head]
title: 2026-01-07-1225-HEAD - Simple vs Easy
type: ""
---

## The Spark

Derived from "Simple vs. Easy: A Programmer's Guide to Better Choices" (Rich Hickey influence).

**Core Concept:** "Simple" = Untangled (Simplex). "Easy" = Familiar/Nearby (Adjacent).

**The Trap:** Choosing what is "Easy" (familiar tools/shortcuts) often builds "Complex" (tangled/complected) systems that fail over time.

## My Current Model (ProdOS Alignment)

| Concept | Simple (One Fold) | Easy (Adjacent/Tangled) |
|:--- |:--- |:--- |
| **Note Strategy** | `HEAD` (Volatile) separated from `SoT` (Stable). | One big folder where everything is mixed ("it's easy to just save it here"). |
| **Action Strategy** | `MVA` (Indivisible/Atomic). | "Work on Project X" (Tangles planning, doing, and testing). |
| **Tooling** | Specialized MCP tools for specific tasks. | Using a single big prompt for everything ("Easy to type, hard to debug"). |

## The Tension

- **Familiarity Bias:** I often default to "Easy" workflows (e.g., standard RAG) instead of "Simple" ones (e.g., highly specialized context files).
- **Complecting:** Am I braiding "Thinking" and "Storage" too much in my current Vault?

## The Next Test

- [ ] **Simplicity Audit:** Review the `10_System/templates` or `fileClasses`. Are they doing one thing, or are they complected?
- [ ] **Protocol Check:** Does the "MVA" in my tasks strictly follow the "one-fold" rule (atomic and binary)?
