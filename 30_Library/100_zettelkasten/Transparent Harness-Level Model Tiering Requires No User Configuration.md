---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-29T09:36:07+00:00
permalink: llmeon/30-library/100-zettelkasten/transparent-harness-level-model-tiering-requires-no-user-configuration
proposition: Model and sub-agent tiering by task complexity can happen automatically
  inside the harness itself, transparently, with zero user configuration or even awareness
  — a harness can route simple tasks (e.g. reading files) to a small subagent and
  'complex tasks to a larger one "out of the box," rather than requiring the user or'
  engineer to deliberately design and configure the tiering strategy.
tags: [domain/llm, topic/agent-architecture, topic/cost-optimization, topic/harness-design]
title: Transparent Harness-Level Model Tiering Requires No User Configuration
type: claim
---

## Transparent Harness-Level Model Tiering Requires No User Configuration

Every existing tiering argument in this vault treats stratification as something a human designs: an engineer decides which tasks are routine, which model handles them, and wires that routing up deliberately. This note describes a different mode entirely: the harness itself makes that routing decision, automatically, without the user ever configuring anything or even knowing the mechanism exists. During autonomous execution, if the orchestrator needs to read files, it silently dispatches to a smaller, cheaper subagent; if it judges the action complex, it dispatches to a larger one—all invisibly, as a built-in behavior of the tool rather than a deliberate architecture decision by whoever is using it.

This matters because it changes who bears responsibility for good tiering: if it's transparent and automatic, the harness vendor's default routing logic determines cost and quality outcomes for every user of that harness, rather than each individual engineer having to get their own tiering strategy right.

### Scope & Conditions

Applies specifically to harnesses that implement this routing as a built-in, opaque behavior. Users of such harnesses get the benefits of tiering without effort, but also lose visibility and control—they can't easily audit or override which tasks get routed to which model tier unless the harness exposes that configuration explicitly (which some do, via custom agents/instructions, as an optional override on top of the default automatic behavior).

### Evidence

Source: "The harness is all you need (mostly)" (github.blog, GitHub Copilot team). "GitHub Copilot will automatically act as an orchestrator during this phase. If it needs to read files in the codebase, it will use the 'Explore' subagent with a small model. If it deems an action relatively complex, it will likely choose the 'General Purpose' subagent with a larger model. While you can get fine-grained control over orchestration in GitHub Copilot with custom agents and instructions, you don't need to do anything special to get the advantages of subagents and multimodel workflows. This works out of the box, even if you did not know that any of these things existed."

### Implications

- This is a distinct delivery mode for a principle the vault already endorses on other grounds: [[Token Smarter Concentrates Human Oversight at Architectural Leverage Points While Tiering Models by Task]], [[Small Models Should Execute Structured Tool Calls, Large Models Complex Reasoning]], and [[API Quota Limits, Not Just Cost, Drive Model Stratification in Agentic Workflows]] all argue _for_ tiering, but all three assume a human deliberately designs and executes the strategy. This note shows the same principle can be delivered as an invisible harness default instead of a manual practice—a materially different claim about where the tiering decision lives.
- It lowers the bar for benefiting from tiering, at the cost of auditability: engineers using a harness with this behavior get cost/quality benefits without having to learn or apply the vault's existing manual-tiering guidance—but they also can't easily verify the harness's routing choices are actually correct for their specific workload, unlike a deliberately-designed strategy they control directly.
- It's a specific instance of the inner-harness/outer-harness split already in the vault: [[Harness Engineering Splits into an Inner Harness and an Outer Harness]] distinguishes tools/APIs (inner) from surrounding dev environment (outer); automatic model routing is squarely an inner-harness behavior—it shapes what the model itself can access and how, invisibly to the user.

### Related

- [[Token Smarter Concentrates Human Oversight at Architectural Leverage Points While Tiering Models by Task]]—contrast: manually-designed tiering strategy vs. this note's automatic, harness-default tiering.
- [[Small Models Should Execute Structured Tool Calls, Large Models Complex Reasoning]]—contrast: same relationship—the principle delivered as a deliberate practice there, as an opaque default here.
- [[Harness Engineering Splits into an Inner Harness and an Outer Harness]]—extends: automatic model routing is a concrete inner-harness behavior.
- [[API Quota Limits, Not Just Cost, Drive Model Stratification in Agentic Workflows]]—related: automatic tiering would also help conserve quota, though the source doesn't discuss quota specifically.

### See Also

- [[Full-Autonomy Agent Execution Requires Sandboxing for Safety and Data Privacy, Not Just Concurrency]]

%%[extends:: [[Token Smarter Concentrates Human Oversight at Architectural Leverage Points While Tiering Models by Task]], strength=2, confidence=low]%%
