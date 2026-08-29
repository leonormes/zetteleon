---
created: 2026-07-28T09:44:23+00:00
modified: 2026-08-29T09:36:07+00:00
permalink: llmeon/30-library/100-zettelkasten/the-slow-loop-pattern-constrained-off-hours-agent-loops-produce-a-single-pr-for-async-human-review
title: The Slow Loop Pattern - Constrained Off-Hours Agent Loops Produce a Single PR for Async Human Review
---

---

created: 2026-07-28T00:00:00+00:00
modified: 2026-07-28T00:00:00+00:00
title: The Slow Loop Pattern - Constrained Off-Hours Agent Loops Produce a Single PR for Async Human Review
type: claim
epistemic_status: medium
tags: [domain/llm, topic/agent-architecture, topic/workflow-design, topic/best-practice]
proposition: The pragmatic, working version of loop engineering is a "slow loop": a constrained, deterministic agent loop run off-hours—for example, a nightly cron job directing an agent to fix one specific anti-pattern or bug—culminating in a single pull request for human review the next morning. Human review happens once per loop cycle, asynchronously, rather than continuously or not at all.
---

## The Slow Loop Pattern - Constrained Off-Hours Agent Loops Produce a Single PR for Async Human Review

The slow loop sits between two failure modes: the dark factory (no human review anywhere in the loop) and the tight synchronous loop (an engineer babysitting every iteration). It gets its safety from three constraints working together: the scope is narrow (one specific anti-pattern or bug, not an open-ended mandate), the timing is off-hours (a nightly cron job, not a live session competing for the engineer's attention), and the output is singular (one PR, not a stream of incremental commits)—which means exactly one human review checkpoint per cycle, positioned at a natural, low-friction moment (morning standup, first coffee) rather than demanding real-time supervision.

This is presented as the pragmatic middle path: loop engineering's promise (an LLM verifying its own work against linters, compilers, or tests until a goal is met) without loop engineering's danger (drifting into full autonomy with no review boundary at all).

### Scope & Conditions

Applies to well-scoped, narrow maintenance tasks (a specific anti-pattern, a specific known bug class) where a single PR is a natural unit of review. Not presented as a general substitute for broader agentic workflows—it's specifically the pattern for extracting safe value from unattended, off-hours agent time.

### Evidence

Source: "Context engineering with Dex Horthy" (Gergely Orosz interviewing Dex Horthy, Human Layer). "The most pragmatic use of loop engineering is running constrained, deterministic loops off-hours. For example, a nightly cron job that directs an agent to fix one specific anti-pattern or bug, culminating in a single pull request for human review by morning" [36:58].

### Implications

- This is the working countermeasure to the dark-factory failure mode: [[Dark Factories Fail Within Months Because LLMs Lack Long-Term Architectural Intuition]] describes what happens when the review checkpoint is removed entirely; the slow loop is presented by the same source as the sustainable alternative that keeps a checkpoint while still capturing unattended-time value.
- It's a concrete instance of the engineer-at-the-boundaries pattern: [[Engineer Involvement Compresses to Planning and Review as Agentic Workflows Mature]] describes engineer involvement compressing to planning and review bookends generally; the slow loop is a specific, narrow-scope implementation of exactly that shape, with the review boundary made asynchronous and time-boxed to once per cycle.
- Narrow scope is doing the safety work, not just the async timing: a slow loop applied to a broad, ambiguous mandate would lose its safety properties even with the same off-hours/single-PR structure—the scope constraint and the review-cadence constraint are both load-bearing, not just one or the other.

### Related

- [[Dark Factories Fail Within Months Because LLMs Lack Long-Term Architectural Intuition]]—contrast: the cautionary failure mode this pattern is explicitly designed to avoid.
- [[Engineer Involvement Compresses to Planning and Review as Agentic Workflows Mature]]—implements: a specific, narrowly-scoped instance of the general boundary-compression pattern.
- [[Autonomous Self-Correction Loops Without Review Produce Overcomplex Code]]—related: both concern the risk/safety trade-off of unsupervised agent loops; this note is the pattern that avoids that note's failure mode.
- [[Mandatory Manual Code Review Before Deployment]]—supports: the slow loop is a concrete mechanism that satisfies this existing mandate even for off-hours, unattended work.

### See Also

- [[Software Factory Pattern - Specialized Sandboxed Agents Autonomously Own Feature, Bugfix, and Incident Lifecycles]]

%%[implements:: [[Engineer Involvement Compresses to Planning and Review as Agentic Workflows Mature]], strength=3, confidence=medium]%%

%%[supports:: [[Mandatory Manual Code Review Before Deployment]], strength=3, confidence=medium]%%
