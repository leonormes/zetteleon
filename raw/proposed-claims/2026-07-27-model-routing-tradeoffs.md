---
title: Model Routing Should Match Task Type — Mechanical Operations to Free Models,
  Reasoning to Premium Models
type: claim-stub
status: proposed
created: 2026-07-27 19:40:00+01:00
source_raw:
- - raw/proposed-claims/2026-07-27-model-routing-tradeoffs
claim_statement: LLM operations partition cleanly into mechanical (gather, execute,
  validate) and reasoning (diagnose, plan, synthesise) phases. Free models should
  handle the former; premium models should be reserved for the latter. Routing by
  task type yields 3–5× cost reduction without quality loss.
steel_man: 'A sufficiently capable free model (Gemini Flash, Llama 405B) can execute
  any mechanical task reliably if given clear instructions — kubectl commands, grep
  operations, helm template validation. The risk is not execution quality but escalation
  discipline: the free model must recognise when it cannot diagnose and escalate cleanly
  rather than hallucinating.'
tags:
- claim-stub
- agent-proposed
- cost-optimisation
- llm-routing
- hermes
falsifiers: null
crux: null
confidence: null
counter_positions: null
permalink: llmeon/raw/proposed-claims/2026-07-27-model-routing-tradeoffs
---

This stub names a principle the vault has extensive operational evidence for but no claim node to hang it on.

**Evidence already present:**
- `wiki/projects/Hermes-Multi-Model-Routing-Strategy.md` — architectural design for Hermes's multi-model orchestration; desired architecture: free model for context gathering and CLI execution, premium model for complex reasoning
- `30_Library/200_Projects/Hermes Cost Optimisation - Free Model Routing Strategy.md` — detailed session analysis showing 60-70% of operations are mechanical Gather/Act phases, only ~15% is genuine Reasoning. Concrete routing rules with escalation signal heuristics
- `wiki/projects/Token-Usage.md` — token consumption tracking across sessions

**Orphan claims awaiting a parent:**
- `Small Models Should Execute Structured Tool Calls, Large Models Complex Reasoning` — the task-type partition principle
- `LLMs Exhibit Divergent Strengths Across Development Lifecycle Phases` — different models for different phases
- `Continuous Autonomous Agent Loops Incur Significant API Cost` — the cost driver that makes routing necessary

**The unstated premise:** The Gather/Reason/Act cycle is universal across LLM-aided debugging workflows. If routing rules are designed for the general case (rather than task-specific heuristics), the pattern applies beyond Hermes's specific toolchain to any agentic debugging loop.

**Consequence for the P5 router:** The router's classification step (Step 2 — duplicate/supporting/refining/contradicting/genuinely-new) maps directly onto the Reason phase. If a free model handles the Gather phase (locate nearest notes via semantic or lexical search), the router's classification could be a single premium-model call per ingest cycle — the same 3-5× cost reduction pattern described in the Free Model Routing Strategy document.