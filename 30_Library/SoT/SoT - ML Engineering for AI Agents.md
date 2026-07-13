---
aliases: [Agentic ML Workflow, ML Engineering for Agents, SuperML Pattern]
created: 2026-03-28T17:30:00+00:00
modified: 2026-07-13T08:45:17+00:00
permalink: llmeon/30-library/so-t/so-t-ml-engineering-for-ai-agents
tags: [agents, ai, devops, engineering, machine-learning, workflows]
title: SoT - ML Engineering for AI Agents
---

## Minimum Viable Understanding (MVU)

Machine Learning Engineering for AI Agents involves providing agents with specialized Skills and Memory to handle the ML lifecycle—planning runs, verifying configs, and debugging failures like OOM or NaN. By grounding an agent in a persistent experiment memory and a verified knowledge base (e.g., Leeroopedia), the agent moves from "probabilistic guessing" to "documented engineering."

---

## Working Knowledge

### 1. The Agentic ML Lifecycle

| Phase | Agent Skill | Objective |
|:---|:---|:---|
| Planning | `ml-plan` | Architect multi-step training pipelines against framework docs. |
| Verification | `ml-verify` | Catch config mistakes (e.g., QLoRA rank, learning rate) before burning GPU hours. |
| Debugging | `ml-debug` | Triage OOM, divergence, or crashes by root cause rather than guessing. |
| Iteration | `ml-iterate` | Provide ranked next steps when metrics plateau. |
| Memory | `ml-experiment` | Track hypotheses, results, and lessons learned across sessions. |

### 2. Persistent Memory (The ML Expert)

A persistent ML agent should maintain state across conversations:

- Hardware Profile: Awareness of available GPUs (e.g., 1xA100 80GB) and their limits.
- Experiment Log: Avoid repeating failed experiments by checking past results.
- Battle-Tested Defaults: Cite verified defaults for frameworks like vLLM, DeepSpeed, or LangChain.

_Note_: This is a domain-specific instance of the [[SoT - LLM Wiki Pattern]]—the Experiment Log is the "wiki layer" for ML engineering, maintained by the agent across sessions rather than rediscovered on each query.

### 3. Knowledge Grounding (Leeroopedia)

Agents should use MCP tools to look up documentation in real-time and cite their sources.

- Reference: 27k+ pages of ML/AI framework metadata.
- Benefit: Reduces hallucinations in training configs and loss masking patterns.

---

## Current Understanding

### The "Mirroring" Trap in ML

If an agent generates both the training script and the validation logic, it can replicate logical errors in data preprocessing that make validation results misleadingly high.

- Fix: Use independent verification scripts or isolated "Double-Blind" verifier agents.

### Benchmarked Outcomes

Empirical tests show that grounding agents in specialized ML skills improves functional correctness on tasks like QLoRA fine-tuning by over 50% (Avg score 13.2/15 with skills vs 8.3/15 without).

## Related Documentation

- [[SoT - AI Agent Skill Architecture]]
- [[SoT - Generative Intelligence]]
