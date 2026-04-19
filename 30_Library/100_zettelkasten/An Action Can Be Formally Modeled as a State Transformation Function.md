---
aliases: ["Formal Action Model"]
created: 2025-11-10T15:04:00Z
last_reviewed: ""
modified: 2026-04-18T15:51:22+00:00
status: "stable"
tags: ["action", "model", "theory", "topic/productivity"]
title: An Action Can Be Formally Modeled as a State Transformation Function
type: "concept"
updated: 
---

## An Action Can Be Formally Modeled as a State Transformation Function

Summary: An action can be formally modeled as a function `A: (S_pre, I) → (S_post, O)`, where it transforms a pre-state and inputs into a post-state and a binary output.

Details:

- S_pre (Pre-State): The required context or conditions before the action can begin.
- I (Inputs): Any necessary resources or information.
- S_post (Post-State): The new state of the system after the action is completed.
- O (Output): A binary signal (e.g., Done = 1) indicating successful completion.

This model emphasizes that actions are state transformations with clear preconditions and postconditions.

---

## Related

- [[SoT - PRODOS Core Specification]] — _Defines the "Minimal Viable Action" (MVA) as the atomic unit of execution and provides the SAVESTATE syntax for managing task state transitions._
- [[SoT - Abstracting Concurrent Systems]] — _Explores the broader mathematical abstraction of state machines and discrete state transitions governed by invariants._
- [[Agentic Autonomy as State Machine Logic]] — _Applies the state machine model to AI agents, illustrating how autonomy is functionally constrained within programmatic control flows._
- [[SoT - The Cognitive Physiology of Task Execution]] — _Deconstructs the biological transitions between the five cognitive phases of action._
- [[Protocol - Vague-to-Action]] — _The algorithmic protocol for decomposing abstract states into the formal model of physical, binary actions._
