---
aliases: ["Hardware Sympathy", "Mechanical Empathy"]
confidence: "5/5"
created: 2026-01-07T00:00:00Z
epistemic: "Mindset"
last_reviewed: 
modified: 2026-01-08T10:49:42+00:00
purpose: "To define the mindset of designing software that cooperates with, rather than fights against, the underlying hardware."
review_interval: "1 year"
see_also:
  - "[[MOC - Data-Oriented Design]]"
source_of_truth: []
status: "Stable"
tags: ["hardware", "mindset", "performance"]
title: SoT - Mechanical Sympathy
type: "SoT"
uid: 
updated: 
---

> "You don't have to be an engineer to be a racing driver, but you have to have **Mechanical Sympathy**."—**Jackie Stewart**

## 1. The Definition

Mechanical Sympathy is the understanding of how the underlying system operates and designing solutions that work _with_ that design, not against it.

## 2. In Software

It means accepting that **Abstraction is not Free**.

- **Virtual Functions:** Cost a cache miss.
- **Garbage Collection:** Costs a pause.
- **Threads:** Cost a context switch.

## 3. The Practice

- **Design for the Grain:** Write code that flows with the CPU pipeline (Branch Prediction).
- **Respect the Cache:** Pack data tightly.
- **Avoid the Supermarket:** Minimize Main Memory access.
