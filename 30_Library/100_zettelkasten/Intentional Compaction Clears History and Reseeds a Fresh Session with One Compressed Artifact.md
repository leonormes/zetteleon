---
created: 2026-07-28T10:27:27+00:00
epistemic_status: medium
modified: 2026-08-29T09:36:02+00:00
permalink: llmeon/30-library/100-zettelkasten/intentional-compaction-clears-history-and-reseeds-a-fresh-session-with-one-compressed-artifact
tags: [domain/llm, topic/context-management, topic/workflow-design]
title: Intentional Compaction Clears History and Reseeds a Fresh Session with One Compressed Artifact
type: claim
---

## Intentional Compaction Clears History and Reseeds a Fresh Session with One Compressed Artifact

The instinct when a task runs long is to let the conversation accumulate—every tool call, every intermediate result, every dead end stays in context because it might still matter. Intentional compaction rejects that instinct: at a deliberate checkpoint, the engineer has the LLM distill everything relevant into a single artifact (a research summary, a design doc), then throws away the conversation that produced it and opens a brand new session with only that artifact as input.

The key word is _discontinuous_. This isn't a scratchpad that grows and gets carried forward step by step within one ongoing process—it's a hard reset. The old context, including all its accumulated noise and any degradation from having spent time deep in the "dumb zone," is gone. Only the deliberately-authored compression survives into the next phase of work.

### Scope & Conditions

Applies at natural phase boundaries in a long-running agentic task—e.g., moving from research/exploration into implementation—where the engineer can identify a clean handoff point and is willing to have the LLM commit to a single artifact as the complete summary of everything learned so far. Requires trusting that artifact to actually capture what matters; a poorly-written compression artifact loses information the fresh session can never recover.

### Evidence

Source: "Context engineering with Dex Horthy" (Gergely Orosz interviewing Dex Horthy, Human Layer). "Rather than maintaining massive, sprawling conversation histories, developers should force the LLM to output a condensed summary (e.g., a research or design document), clear the history, and feed only that compressed artifact into a fresh session" [01:06:47]. Framed as the practical technique for staying in the "smart zone"—the early segment of the context window (roughly first 100k-200k tokens) where the model reliably follows instructions, before context growth pushes operations into the "dumb zone" of erratic, unreliable behavior [01:10:18].

### Implications

- A lighter-weight variant of this practice exists without the artifact-forcing step: "The harness is all you need (mostly)" (github.blog, GitHub Copilot team) recommends simply starting a new chat session per topic—"I'd recommend starting a new chat session for anything you do next that doesn't have to do with this date picker. You can think of chat sessions as being topical; if you start to diverge too much from the main topic, it's probably time for a new session"—without the deliberate compression-artifact step this note describes. Topical session scoping gets some of the same benefit (a clean, uncluttered context) at lower overhead, but loses the guarantee that everything relevant from the old session survives into the new one; intentional compaction's artifact-forcing step is what makes the discard safe rather than lossy.
- This is a distinct mechanism from the vault's existing carried-forward-scratchpad pattern: [[Sequential Processing with Working Memory (Folding Operator)]] describes memory accumulating and being carried forward continuously within an ongoing sequence—never cleared, always growing. Intentional compaction is the opposite motion: a deliberate, complete discard followed by a clean restart from one artifact.
- It's the general mechanism behind an already-adopted specific practice: [[Low-Context Implementation Execution]] already applies fresh, low-context sessions to the Implementation phase of the RPI workflow specifically; this note names the general technique—forcing an output artifact as the compaction mechanism—that makes that specific practice work.
- It directly operationalizes the smart-zone/dumb-zone distinction already established in this vault: [[SoT - The RPI Workflow (Context Engineering)]] and [[Context Volume Plateau]] both already document that instruction-following degrades as context fills; this note adds the concrete technique for staying ahead of that degradation rather than managing it after the fact.

### Related

- [[Sequential Processing with Working Memory (Folding Operator)]]—contrast: continuous scratchpad accumulation vs. this note's discrete clear-and-reseed.
- [[Low-Context Implementation Execution]]—implements: that note's fresh-session practice is a specific application of this note's general compaction technique.
- [[SoT - The RPI Workflow (Context Engineering)]]—supports: this note operationalizes the smart-zone/dumb-zone distinction that source already defines.
- [[RLMs Avoid Context Bloat by Storing Intermediate State as Symbolic Variables, Not Context Tokens]]—related: both are architectural responses to keeping an LLM's effective working context small, via different mechanisms (external symbolic state vs. periodic compaction-and-reset).

### See Also

- [[Harness Engineering Splits into an Inner Harness and an Outer Harness]]

%%[implements:: [[Low-Context Implementation Execution]], strength=3, confidence=medium]%%

%%[supports:: [[SoT - The RPI Workflow (Context Engineering)]], strength=3, confidence=medium]%%
