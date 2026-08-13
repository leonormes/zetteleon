---
aliases: [Task Decomposition Protocol, Vague-to-Action]
conformant: false
created: 2026-04-04T12:00:00+00:00
last-synthesis: 2026-04-04
modified: 2026-08-13T10:53:39+00:00
non_conformance_reason: "Bulk inferred type. Needs review."
permalink: llmeon/30-library/so-t/protocol-vague-to-action
status: evergreen
tags: [execution, prodos, protocol, task-decomposition]
title: Protocol - Vague-to-Action
type: protocol
---

## Objective

To convert "heavy" or undefined tasks that trigger avoidance into physical, binary actions that can be executed immediately.

---

## The Algorithm

### Phase 1: Define the Endpoint

1. Identify the Problem Statement: Write down the vague task exactly as captured (e.g., "Sort out taxes").
2. Define "Done": Describe a tangible, physical outcome that proves the task is finished (e.g., "A submitted PDF confirmation on the HMRC portal").
3. Name the Outcome: Give this outcome a clear project name in your system.

### Phase 2: Capture the Steps

1. Set a 5-Minute Timer: This reduces the perceived "bigness" of the planning phase.
2. Brain Dump: Write every question, idea, and micro-step without filtering.
3. Organize into Phases: Group the dump into 3-5 logical stages (e.g., Gather Docs, Data Entry, Review, Submit).

### Phase 3: Activate the MVA

1. Identify Phase 1: Look at the first group of steps.
2. Identify the MVA: What is the _very next physical action_?
    - It must be small, visible, and doable now (e.g., "Find the login password," "Create a folder named 'Taxes 2024'").
3. Commit: Write this single MVA on your 'Next Actions' list. The entire project is now represented by this one task.

---

## Unit Test

- Binary Outcome: Can you say "Yes/No" to whether the step is finished in < 120 seconds?
- No Planning: Does the step require further "thinking" or "deciding"? If yes, it is not an MVA.

---

## Related

- [[SoT - PRODOS Core Specification]]—_The kernel specification that defines the "Logic-Dopamine Mismatch" and provides the theoretical basis for the 120-second MVA loop._
- [[MOC - Action Management]]—_The central hub for ProdOS execution strategies, mapping this protocol to the broader goal of transforming intent into reality._
- [[SoT - The Cognitive Physiology of Task Execution]]—_Deconstructs why "heavy" tasks trigger avoidance and how mechanical execution of an MVA generates the necessary dopamine for momentum._
- [[Chaining Starter Tasks Creates a Momentum Ramp]]—_A complementary technique for building behavioral momentum using a sequence of low-cost wins._
- [[The Framework Solves Task Initiation Difficulties]]—_Explains how atomic decomposition removing ambiguity lowers the activation energy required to begin._
- [[An Action Can Be Formally Modeled as a State Transformation Function]]—_The formal mathematical model underpinning the transition from vague states to physical actions._
