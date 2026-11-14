---
conformant: true
contrasts_with: ["[[Protocol - Action-First GTD (LLM Chief of Staff)]]"]
created: 2026-04-02T10:55:00+00:00
merged_from: ["[[SoT - Cognitive Engineering Protocols]]"]
modified: 2026-11-14T13:41:00+00:00
permalink: llmeon/30-library/so-t/so-t-prod-os-thinking-stream
project_category: prodos
see_also: ["[[SoT - HEAD Note Contract (The Workbench)]]", "[[SoT - Unified Writing to Think Process]]"]
status: stable
tags: [prodos, system/protocol, thinking, workflow]
tension: ["[[The Danger of Perpetual System-Building]]"]
title: SoT - ProdOS Thinking Stream
type: sot
upstream: ["[[MOC - ProdOS]]", "[[SoT - PRODOS Core Specification]]"]
---

## Minimum Viable Understanding (MVU)

The Thinking Stream is the "RAM" of the ProdOS system—a low-friction, high-throughput loop for converting raw mental noise into structured knowledge or physical action. It relies on the Rule of Zero Toil: if it feels like "organizing," stop. The goal is rapid context restoration and momentum generation.

## Working Knowledge

### 1. The Core Lifecycle (CRPE)

1. CAPTURE: Dump mental noise into the Daily Note. Raw text, no formatting, no judgment. Translating abstract feeling and unprocessed noise into linear syntax activates the Prefrontal Cortex (PFC), dampening Amygdala/Mid-Cingulate stress loops and freeing Working Memory RAM (Neuro-Synchronization). If the dump feels overwhelming, cap it at the top 10 loudest items and triage via [[Protocol - Action-First GTD (LLM Chief of Staff)]].
2. REFINE: If an idea is complex or "stuck" and leaves a question that needs your judgement, open a `HEAD - <question>?` note in `20_Thinking/21_Workbench/`. Admission rules are in [[SoT - HEAD Note Contract (The Workbench)]].
3. PROCESS (The 120s Loop):
    - Goal: What is the single, physical outcome desired?
    - Block: What is the exact friction preventing progress?
    - MVA: What is the next physical step that takes <120 seconds?
4. EXIT:
    - Action? $\rightarrow$ Move to Todoist (see [[gtd-action-system]]).
    - Fact? $\rightarrow$ Merge into a canonical `SoT -` note in `30_Library/100_zettelkasten/` via [[Prompt - ProdOS Chronos Synthesizer]], then archive the HEAD note (leave a tombstone if other notes cite it; see the HEAD Note Contract §3.1).
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

- Kernel: [[SoT - PRODOS Core Specification]] [implements:: [[SoT - PRODOS Core Specification]], confidence=high]
- Workbench: [[SoT - HEAD Note Contract (The Workbench)]] [depends_on:: [[SoT - HEAD Note Contract (The Workbench)]], confidence=medium]
- Philosophy: [[SoT - Processing IS the Work]] [implements:: [[SoT - Processing IS the Work]], confidence=high]
- Mechanism: [[Writing Acts as an External Working Memory]] [depends_on:: [[Writing Acts as an External Working Memory]], confidence=high]
- Writing pipeline: [[SoT - Unified Writing to Think Process]] [supports:: [[SoT - Unified Writing to Think Process]], confidence=high]
- Automation: [[Protocol - Action-First GTD (LLM Chief of Staff)]] (Mode B: agent-run)
