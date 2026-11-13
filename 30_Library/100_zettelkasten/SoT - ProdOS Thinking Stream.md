---
conformant: true
created: 2026-04-02T10:55:00+00:00
last-synthesis: 2026-04-02
modified: 2026-10-22T15:11:11+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/so-t/so-t-prod-os-thinking-stream
source_of_truth: true
project_category: prodos
tags: [prodos, system/protocol, thinking, type/SoT, workflow]
title: SoT - ProdOS Thinking Stream
type: sot
---

## Minimum Viable Understanding (MVU)

The Thinking Stream is the "RAM" of the ProdOS system—a low-friction, high-throughput loop for converting raw mental noise into structured knowledge or physical action. It relies on the Rule of Zero Toil: if it feels like "organizing," stop. The goal is rapid context restoration and momentum generation.

## Working Knowledge

### 1. The Core Lifecycle (CRPE)

1. CAPTURE: Dump mental noise into the Daily Note. Raw text, no formatting, no judgment.
2. REFINE: If an idea is complex or "stuck" and leaves a question that needs your judgement, open a `HEAD - <question>?` note in `20_Thinking/21_Workbench/`. Admission rules are in [[SoT - HEAD Note Contract (The Workbench)]].
3. PROCESS (The 120s Loop):
    - Goal: What is the single, physical outcome desired?
    - Block: What is the exact friction preventing progress?
    - MVA: What is the next physical step that takes <120 seconds?
4. EXIT:
    - Action? $\rightarrow$ Move to Todoist (see [[gtd-action-system]]).
    - Fact? $\rightarrow$ Merge into a canonical note in `30_Library/SoT/` via [[Prompt - ProdOS Chronos Synthesizer]], then archive the HEAD note (leave a tombstone if other notes cite it; see the HEAD Note Contract §3.1).
    - Skill/Project? $\rightarrow$ Move to the Hangar (Project Note).
    - Noise? $\rightarrow$ DELETE (raw captures only; never a HEAD note that is cited as `upstream`).

### 2. The Guardrails

- FLAT WORKBENCH: No sub-folders inside `20_Thinking/21_Workbench/`; it is a flat queue of questions.
- NO POLISHING: Clarity of thought is superior to aesthetics of layout.
- NO SILENT ROT: A thought that cannot name what would settle it is debt. Fix it in place, resolve it, or archive it per the HEAD Note Contract; do not leave it open by default.

## Current Understanding

### The "120s Loop" as Cognitive Defrag

The 120s loop is designed to bypass the "Dumb Zone" of over-deliberation. By focusing strictly on the Minimal Viable Action (MVA), we shift from "Logic Mode" (direction) to "Dopamine Mode" (fuel).

## Related Knowledge

- Kernel: [[SoT - PRODOS Core Specification]] [implements:: [[SoT - PRODOS Core Specification]], confidence=medium]
- Workbench: [[SoT - HEAD Note Contract (The Workbench)]] [depends_on:: [[SoT - HEAD Note Contract (The Workbench)]], confidence=medium]
- Philosophy: [[SoT - Processing IS the Work]]
- Automation: [[Protocol - Action-First GTD (LLM Chief of Staff)]] (Mode B: agent-run)
