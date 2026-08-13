---
created: 2026-07-28T00:00:00+00:00
epistemic_status: medium
modified: 2026-08-13T10:54:41+00:00
permalink: llmeon/30-library/100-zettelkasten/agent-ergonomic-clis-output-token-efficient-plaintext-instead-of-verbose-json-schemas
proposition: Current tool-integration protocols (including some MCP servers) rely
  on verbose JSON schemas for input/output, which are optimized for programmatic parsing
  rather than for LLM consumption. Engineering CLIs and tools to instead output token-efficient,
  semantically dense plaintext — rather than structured JSON meant for a traditional
  parser — drastically reduces token consumption, lowers latency, and improves the
  "agent's task success rate."
tags: [domain/llm, topic/cost-optimization, topic/harness-design, topic/tool-use]
title: Agent-Ergonomic CLIs Output Token-Efficient Plaintext Instead of Verbose JSON Schemas
  Schemas
type: claim
---

## Agent-Ergonomic CLIs Output Token-Efficient Plaintext Instead of Verbose JSON Schemas

JSON schemas earned their place in traditional software because a deterministic parser benefits from explicit structure: field names, types, nesting, all unambiguous and machine-checkable. An LLM consuming that same output pays a different cost: every brace, quote, key name, and nesting level is tokens spent on syntax rather than information, and the LLM has to do the work of extracting meaning from structure that was designed for a parser, not for it.

"Agent-ergonomic" design inverts the priority: since the consumer is now frequently an LLM rather than a traditional parser, the tool's output should be optimized for what an LLM actually needs—dense, readable, unambiguous plaintext that conveys the same information with far fewer tokens and no structural overhead. The claim isn't just about token savings in isolation; it's that this specifically improves task success rate, because less of the model's limited attention is spent parsing structure and more is available for reasoning about content.

### Scope & Conditions

Applies to designing or choosing tool/CLI interfaces specifically for LLM/agent consumption, as distinct from interfaces meant for traditional software integration. A tool serving both traditional software and LLM agents may need to offer both output modes, or accept the trade-off of optimizing for one consumer at the expense of the other.

### Evidence

Source: [video with "Axi" agent-ergonomic interface segment, exact title/channel not given in the summary]. "A core technical critique is levied against current integration protocols (such as some MCP servers) that rely on verbose JSON schemas. The speaker argues for engineering Command Line Interfaces (CLIs) to be 'agent-ergonomic.' By outputting token-efficient, semantically dense plaintext rather than structured data meant for programmatic parsing, developers can drastically reduce token consumption, lower latency, and improve the agent's success rate." Grounding note from the same source: "The critique of JSON bloat in agent tooling is highly accurate and empirically sound. Token efficiency is a primary bottleneck in LLM engineering. Stripping out unnecessary metadata and standardising inputs/outputs to plaintext is a recognised, effective method for optimising context windows and minimising API costs."

### Implications

- This is in tension with, not an instance of, the vault's existing structured-output-enforcement note: [[Structured Output Enforcement (JSON Schema and Function Calling)]] treats JSON schema as a positive reliability pattern for the _input_ side of tool calls (constraining what the model must produce to call a tool correctly); this note argues for plaintext specifically on the _output_ side (what a tool returns to the model to consume)—the two aren't strictly contradictory since they concern different directions of the interface, but the tension is worth naming: JSON structure is valuable when it constrains the model's own output, and costly when it's simply what the model has to read.
- It adds a design-level countermeasure to a decoding-level failure mode already in this vault: [[Grammar-Constrained Decoding Forces Hallucination When JSON Tool-Call Sampling Fails]] documents a specific failure where JSON-constrained output decoding can force hallucination; if a tool's _input_ schema can be simplified toward plaintext-like structures per this note's philosophy, the surface area for that decoding failure mode shrinks too, though this is an inference rather than something the source states directly.
- It gives MCP a specific, actionable critique rather than treating it as a settled standard: [[Model Context Protocol Standardises the LLM-to-Tool Interface]] establishes MCP as the standardization layer for tool integration; this note names a concrete weakness in how some MCP servers implement that standardization (verbose JSON overhead) rather than treating MCP adoption as unambiguously good.

### Related

- [[Structured Output Enforcement (JSON Schema and Function Calling)]]—contrast: JSON structure valuable for constraining model _output_ (input to tools); this note argues for the opposite on tool _output_ (input to the model).
- [[Grammar-Constrained Decoding Forces Hallucination When JSON Tool-Call Sampling Fails]]—related: a decoding-level failure mode this note's design philosophy plausibly reduces exposure to, without stating so directly.
- [[Model Context Protocol Standardises the LLM-to-Tool Interface]]—related: names a concrete implementation weakness (verbose JSON) in some MCP server implementations, without indicting the protocol itself.
- [[Rising Per-Task Cost of Newer Models Indicates Inflation in Problem-Solving Cost]]—supports: reducing per-call token overhead is a direct, controllable countermeasure to the token-cost pressure that note describes as an external trend.

### See Also

- [[API Quota Limits, Not Just Cost, Drive Model Stratification in Agentic Workflows]]

%%[supports:: [[Rising Per-Task Cost of Newer Models Indicates Inflation in Problem-Solving Cost]], strength=3, confidence=medium]%%
