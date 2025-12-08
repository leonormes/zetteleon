---
aliases: []
confidence: 
created: 2025-12-08T00:00:00Z
epistemic: 
last_reviewed: 
modified: 2025-12-08T11:11:32Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: defined
tags: [head, prodos, quality, thinking]
title: HEAD - ProdOS Action Quality Assurance
type: 
uid: 
updated: 
---

## HEAD - ProdOS Action Quality Assurance

### The Spark

Derived from ProdOS Task: "ProdOS should identify poorly defined next actions".

I often find tasks in my list like "Think about X" or "Project Y", which are not actionable. These cause procrastination because the "next physical step" is undefined.

### My Current Model

The system (ProdOS) currently accepts any input I give it. It assumes I am an expert at GTD definition, which I am not (especially when tired/ADHD).

The "Action Linter" concept: The system should act as a coach, rejecting or flagging vague inputs.

### The Tension
- **Friction vs. Quality:** If the system rejects my quick capture, I might stop capturing (high friction).
- **Automation:** How can the LLM identify "poor definition" reliably?
- **Correction:** Should it auto-fix it (guess) or ask me?

### The Next Test
- [ ] Create a "Linter Prompt" that takes a list of tasks and identifies ones missing a concrete verb or specific object.
- [ ] Run this prompt against my current `ProdOS.csv` export to see if it correctly identifies "bad" tasks.
