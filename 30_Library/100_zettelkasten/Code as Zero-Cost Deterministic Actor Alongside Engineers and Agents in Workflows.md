---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-08T10:29:16+00:00
permalink: llmeon/30-library/100-zettelkasten/code-as-zero-cost-deterministic-actor-alongside-engineers-and-agents-in-workflows
proposition: In an AI-assisted development workflow there are three distinct actors
  — engineers, agents, and plain deterministic code — and code is the most underused
  of the three despite being the only one that executes near-instantly, behaves with
  perfect consistency, and costs zero LLM tokens. Wherever a task is genuinely deterministic
  (routing, tests, formatting, validation), moving it out of the agent and into code
  is a direct win on speed, cost, and reliability simultaneously.
tags: [domain/llm, topic/agent-architecture, topic/cost-optimization, topic/workflow-design]
title: Code as Zero-Cost Deterministic Actor Alongside Engineers and Agents in Workflows
type: claim
---

## Code as Zero-Cost Deterministic Actor Alongside Engineers and Agents in Workflows

Discussions of agentic workflows tend to frame the design space as a choice between human effort and agent effort. That framing skips a third actor that's present in every real workflow and doesn't get named: plain code. Code executes at machine speed, produces the same output for the same input every time, and—unlike an agent call—consumes no tokens at all.

The practical implication is a simple sorting rule: for any given step in a workflow, ask whether it's actually deterministic. If it is—a routing decision, a test suite, a formatter, a schema check—putting it in an agent call is strictly worse on every axis (slower, costlier, less reliable) than writing it as code. Agents should be reserved for the genuinely non-deterministic parts of the task: the parts that require judgment, synthesis, or handling ambiguity that code cannot resolve on its own.

### Scope & Conditions

Applies to workflow design decisions where a task's determinism is known or knowable in advance. Does not apply to tasks that are only apparently deterministic but actually require contextual judgment (e.g. "is this test failure a real regression or a flaky test" often isn't purely deterministic). The rule is a sorting heuristic, not a blanket argument against agent usage generally.

### Evidence

Source: "FORGET Loop Engineering. Agentic Engineering is about THIS" (IndyDevDan). Code is described as "the unsung hero" of agentic workflows—it "executes at the speed of light, is consistently reliable, and costs zero tokens" [04:10]. The video's closing advice reinforces this directly: "don't over-leverage agents… move deterministic tasks (like routing and testing) into pure code to increase speed, reduce token costs, and guarantee reliability" [30:13].

### Implications

- This is the actionable, general-purpose version of a narrower existing principle: [[Evaluation Pipelines Should Distinguish LLM Judges from Deterministic Scripts]] already applies this exact logic to the specific case of evaluation harnesses; this note generalizes it to workflow design as a whole.
- It reframes "agent harness" architecture as an economic choice, not just a control choice: [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]] describes wrapping agents in deterministic controls for reliability; this note adds that the same substitution is also a cost-and-latency optimization, not solely a safety one.
- It sets an upper bound on how much of a workflow should ever touch an agent: [[Agentic Autonomy Accelerates Fastest in Domains Where Success Is Verifiable]] shows agents excel specifically in verifiable domains—verifiable is close to "expressible as deterministic code," so the overlap between where agents excel and where code should be used instead is worth noticing as a design tension.

### Related

- [[Evaluation Pipelines Should Distinguish LLM Judges from Deterministic Scripts]]—instance: the evaluation-specific case of this general sorting rule.
- [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]]—extends: this note adds a cost/speed rationale to the harness's existing reliability rationale.
- [[Error Handling and Retry Pipelines for LLM Failures]]—related: retry pipelines are themselves an instance of deterministic code doing work an agent shouldn't have to redo.
- [[Unsustainable Agent Token Costs Are Driving a Shift from Flat-Fee to Usage-Based Pricing]]—supports: every task moved from agent to code directly reduces the token-cost pressure that note describes.

### See Also

- [[Software Factory Pattern - Specialized Sandboxed Agents Autonomously Own Feature, Bugfix, and Incident Lifecycles]]

%%[extends:: [[Agent Harness - Wrapping LLMs in Deterministic Software Controls]], strength=3, confidence=medium]%%

%%[supports:: [[Unsustainable Agent Token Costs Are Driving a Shift from Flat-Fee to Usage-Based Pricing]], strength=3, confidence=medium]%%
