---
aliases:
- Hardware Sympathy
- Mechanical Empathy
created: 2026-01-07 00:00:00+00:00
last_reviewed: null
modified: 2026-02-01 15:07:55+00:00
status: Stable
tags:
- hardware
- mindset
- performance
title: SoT - Mechanical Sympathy
type: SoT
updated: null
permalink: llmeon/30-library/so-t/so-t-mechanical-sympathy
---

> "You don't have to be an engineer to be a racing driver, but you have to have Mechanical Sympathy."—Jackie Stewart

## 1. The Definition

Mechanical Sympathy is the understanding of how the underlying system operates and designing solutions that work _with_ that design, not against it.

## 2. In Software

It means accepting that Abstraction is not Free.

- Virtual Functions: Cost a cache miss.
- Garbage Collection: Costs a pause.
- Threads: Cost a context switch.

## 3. The Practice

- Design for the Grain: Write code that flows with the CPU pipeline (Branch Prediction).
- Respect the Cache: Pack data tightly.
- Avoid the Supermarket: Minimize Main Memory access.

## 4. The Scale of Latency (Mental Model)

To understand _why_ we avoid main memory or disk, we scale CPU cycles to human time.

Baseline: Accessing L1 Cache = 1 Second.

| Memory Level | Raw Latency | Scaled Time (Human) | Conceptual Distance |
|:--- |:--- |:--- |:--- |
| L1 Cache | ~0.5 ns | 1 second | Thought in your head. |
| L2 Cache | ~3 ns | ~5 seconds | Picking up a pen. |
| L3 Cache | ~10 ns | ~30 seconds | Walking to a bookshelf. |
| RAM (DDR) | ~100 ns | ~3 minutes | Walking to the kitchen. |
| NVMe SSD | ~10 µs | ~10 hours | Cross-country flight. |
| HDD (Disk) | ~10 ms | ~4 months | Shipping a container by sea. |
| Network (WAN)| ~150 ms | ~5 years | A manned mission to Mars. |

> Insight: When a CPU hits a cache miss and goes to RAM, it is effectively "idling in the kitchen" for 3 minutes. If it goes to Disk, the entire session is over.