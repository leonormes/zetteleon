---
aliases: []
confidence: ""
created: 2026-01-01T18:58:13+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-23T18:09:32+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: ""
tags: []
title: planning-learning-system-prompt
type: ""
---

## Prompt for Gemini Pro: Architecting the ProdOS Learning Engine

**Context:**
I am a developer with ADHD using "ProdOS," an Obsidian-based system designed for "Action over Collection." I currently have scattered notes containing curriculums and learning paths, but I lack a cohesive system to manage them. I struggle with focus and need a system that enforces working on **one learning project at a time** while allowing me to easily pick up where I left off.

**My Constraints:**
1. **Single Threaded:** I can only have ONE "Active Learning Project" at a time.
2. **Gamified:** I want to treat learning like a game (Levels, Missions, Boss Fights).
3. **Practical:** Theory is useless without a "Boss Fight" (a concrete project proving knowledge).
4. **Low Friction:** It must be easy to switch contexts if I _must_, but the system should discourage it.

**Existing Assets:**
I already have a `Template - Learning Project` that looks like this:

```markdown
# Project: Learn {{Topic}} (The Path)
> [!abstract] The "Why"
> **Goal:** {{What can you DO after learning this?}}
> **The "Boss Fight":** {{A concrete project that proves you know it.}}

## 1. The Map (Curriculum)
### Level 1: The Basics
- [ ] **Mission 1:** Hello World / Setup.
- [ ] **Mission 2:** The Core Concept.
- [ ] **Boss Fight 1:** A simple toy program.

### Level 2: The Struggle
- [ ] **Boss Fight 2:** A useful tool.

## 2. Active Quest (The Workbench)
- **Current Focus:** [[HEAD - Current Struggle]]

## 3. The Loot (Source of Truth)
- [[SoT - Key Concept]]
```

**Your Task:**
Act as a **Systems Architect**. Design the "Learning Engine" module for ProdOS. Please provide:

1. **The Registry Structure (MOC):** Design a `MOC - Learning Registry` note. How should it organize "Active," "Queued," and "Finished" curriculums? usage of Dataview queries is encouraged.
2. **The "Boss Fight" Protocol:** Explain how to convert a dry "curriculum list" (e.g., "Chapter 1: Pointers") into a "Boss Fight" (e.g., "Mission: Write a memory leak detector").
3. **The Activation Ritual:** A step-by-step checklist for when I want to start learning a new topic. (e.g., "1. Clone Template, 2. Define Final Boss, 3. Move to Active…").
4. **The Save-State Protocol:** How do I "pause" a learning project so I can resume it 3 months later without losing context? (e.g., Specific metadata, a "Next Action" log).

**Output Format:**
Provide the Markdown content for the `MOC - Learning Registry` and the `Protocol - Learning Engine` notes.
