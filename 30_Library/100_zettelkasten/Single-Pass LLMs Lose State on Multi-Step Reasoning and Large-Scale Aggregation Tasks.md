---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-13T10:56:59+00:00
permalink: llmeon/30-library/100-zettelkasten/single-pass-llms-lose-state-on-multi-step-reasoning-and-large-scale-aggregation-tasks
proposition: A simple LLM call — prompt and context fed directly into a single forward
  'pass predicting the next token — reliably handles simple lookups (e.g. "what is'
  '2+2?") but fails at multi-step reasoning or large-scale counting/aggregation tasks,'
  because a single forward pass has no persistent structure in which to hold and update
  intermediate state as the task proceeds. The failure is architectural, not a matter
  'of the model needing to "try harder" or be scaled up.'
tags: [domain/llm, topic/llm-behavior, topic/reliability, topic/rlm]
title: Single-Pass LLMs Lose State on Multi-Step Reasoning and Large-Scale Aggregation Tasks
  Tasks
type: claim
---

## Single-Pass LLMs Lose State on Multi-Step Reasoning and Large-Scale Aggregation Tasks

The gap between "what is 2+2?" and "categorize these five hundred questions into categories and tell me which category is most frequent" isn't a difference in difficulty the model can just push through with more capability—it's a difference in kind. The first task requires no persistent state: the answer is derivable in one shot. The second requires tracking category assignments across hundreds of items and then aggregating them correctly, and a single forward pass has nowhere to durably hold that running state as it goes. The model has to reconstruct its sense of "where it is" in the task from the accumulated text alone, which becomes increasingly unreliable as the task's working state grows.

This is presented as the specific architectural motivation for RLMs: rather than trying to make the single-pass architecture hold more state more reliably, an RLM sidesteps the problem by giving the task an external structure (the REPL environment) to hold state in, so the LLM itself never has to.

### Scope & Conditions

Describes a limitation of the single-pass, prompt-in/prediction-out architecture specifically—not a claim that all LLM usage fails at multi-step tasks, since chain-of-thought prompting, tool use, and agentic architectures (including RLMs) are all responses to this exact limitation. The claim is about the _base_ architecture's failure mode, which motivates those responses.

### Evidence

Source: "From RLMs to Agent Harnesses" (Still Broken AI). "Simple LLMs: You input a prompt and context directly, and the model predicts the next word in a single pass. This works well for simple tasks (like 'What is 2+2?') but fails on multi-step reasoning or complex counting tasks across large datasets because the model loses track of state and memory" [08:07–08:14].

### Implications

- This is the general architectural cause behind a symptom already documented in the vault: [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]] documents the same failure pattern (entity-fragmentation, aggregation breakdown) as it manifests in a specific DocETL pipeline context; this note names the underlying architectural cause—no persistent state in a single forward pass—that produces that symptom.
- It's the motivating problem the entire RLM architecture is a response to: [[Recursive Language Models Load Context as Environment Variables, Not Prompt Tokens]] and [[RLMs Avoid Context Bloat by Storing Intermediate State as Symbolic Variables, Not Context Tokens]] both directly address this failure mode by giving the task an external place to hold state.
- It cautions against treating multi-step task failures as a prompting problem alone: if the root cause is architectural (no persistent state), better prompting can help but cannot fully resolve the failure—the fix requires giving the system some form of externalized state, whether via REPL variables, tool calls, or explicit scratchpad mechanisms.

### Related

- [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]]—generalizes: this note is the architectural-cause version of that note's pipeline-specific symptom.
- [[Recursive Language Models Load Context as Environment Variables, Not Prompt Tokens]]—related: that architecture is a direct response to the failure mode this note describes.
- [[Sequential Processing with Working Memory (Folding Operator)]]—related: another response to the same underlying problem, using a carried-forward scratchpad rather than an external environment.
- [[Auto-Regressive Generation Reprocesses the Entire Context on Every Token]]—related: both describe fundamental mechanics of single-pass/auto-regressive generation that motivate more elaborate architectures to work around.

### See Also

- [[RLMs Dynamically Chunk Data at Runtime, Unlike RAG's Static Pre-Defined Chunking]]

%%[supports:: [[LLM Pipeline Accuracy Degrades with Document Length and Task Complexity]], strength=3, confidence=medium]%%
