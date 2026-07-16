---
aliases: [Agentic AI Workflows, Agentic Workflow Taxonomy, AI Agent Patterns]
created: 2026-04-05T12:00:00+00:00
modified: 2026-07-13T08:52:43+00:00
permalink: llmeon/30-library/so-t/so-t-agentic-ai-design-patterns
tags: [agents, ai, architecture, design-patterns, llm, sot]
title: SoT - Agentic AI Design Patterns
type: sot
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## 1. Minimum Viable Understanding (MVU)

Agentic AI Design Patterns are modular architectural strategies that move beyond simple "Prompt-Response" loops toward autonomous, iterative, and tool-augmented workflows. By decomposing complex tasks into structured agentic patterns, systems achieve higher reliability, better reasoning, and more efficient resource usage.

---

## 2. Taxonomy of Agentic Patterns

### A. Workflow & Control Flow

- Prompt Chaining: Breaking large tasks into sequential, validated sub-steps.
- Routing: Classifying requests to dispatch them to specialized agents.
- Parallelisation: Processing independent task chunks simultaneously then merging.
- Planning: Breaking goals into milestones and checking constraints before execution.
- Prioritisation: Scoring tasks by value/urgency in dynamic environments.

### B. Cognitive & Reasoning

- Reflection: Using a "critic" agent to review and refine drafts iteratively.
- Reasoning Techniques: Using structures like Chain of Thought (CoT) or Tree of Thought (ToT) to explore solution paths.
- Exploration & Discovery: Using research agents to scan, cluster, and extract insights from broad knowledge spaces.

### C. Action & Execution

- Tool Use: Autonomous discovery, permission verification, and calling of external APIs/tools.
- Human in the Loop: Triggering human review for high-stakes decisions or edge cases.
- Goal Setting & Monitoring: Defining measurable targets and adjusting the approach if the system drifts.

### D. System Architecture

- Multi-Agent Collaboration: Specialized agents working together via a central manager and shared memory.
- Memory Management: Categorizing info into Short-term, Episodic, or Long-term storage.
- Inter-Agent Communication: Structured messaging protocols with tracking and conflict resolution.
- Resource-Aware Optimisation: Routing simple tasks to cheaper models and complex ones to reasoning models.
- Exception Handling & Recovery: Classifying runtime errors to trigger retries, fallbacks, or alerts.

### E. Quality, Safety & Learning

- Knowledge Retrieval (RAG): Indexing and retrieving grounded context from document databases. _Limitation_: standard RAG is stateless—nothing accumulates across sessions. See [[SoT - LLM Wiki Pattern]] for the stateful evolution of this pattern.
- Learning & Adaptation: Collecting feedback and outcomes to update system prompts or policies.
- Evaluation & Monitoring: Using quality gates and test suites to track performance drift and regressions.
- Guardrails & Safety: Sanitizing inputs (injection detection) and moderating output risk.

---

## 3. Implementation in ProdOS

- Tooling: Leverages MCP (Model Context Protocol) for Tool Use and Knowledge Retrieval.
- Efficiency: Use Resource-Aware Optimisation by delegating surgical tasks to local/fast models and synthesis to frontier models.
- Reliability: Apply Reflection and Prompt Chaining to high-stakes knowledge synthesis (Chronos Synthesis).

---

## Related Knowledge

- [[SoT - AI Agent Skill Architecture]]
- [[SoT - Machine Learning Foundations (Neural Networks)]]
- [[MOC - Computer Science Foundations]]
- [[SoT - PRODOS Core Specification]]
