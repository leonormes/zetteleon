---
created: 2026-04-13T14:41:15+00:00
created_utc: 2026-04-13 11:20:00+00:00
kind: definition
modified: 2026-08-13T10:54:49+00:00
permalink: llmeon/30-library/100-zettelkasten/model-context-protocol-mcp
source_title: AI Agent Architecture and the Modern Tech Stack
source_url: https://gemini.google.com/app/509937047bd0b955
status: seed
tags: [interoperability, mcp, standards, tool-calling]
title: Model Context Protocol (MCP)
type: atom
upstream: '[[HEAD The Failure of Human-Centric Design]]'
---

## Model Context Protocol (MCP)

The Model Context Protocol (MCP) is a standardized communication interface that allows AI agents to interact with external tools and databases using a uniform schema. It functions as a universal "OpenAPI specification" for LLMs, enabling them to interpret and utilize tools without the need for bespoke integration code for every new capability.

### Scope & Conditions

Standardizes tool-calling across different platforms and LLMs. It reduces the technical debt associated with custom tool implementations.

### Evidence

> "A standardised communication interface… allows AI agents to interface with external tools… using a uniform protocol, bypassing the need for… bespoke integration code."

### Implications

- Standardises tool-calling across different LLMs and platforms.
- Reduces the friction of integrating new external capabilities into agentic systems.

### Related

- [[CLI Interoperability for Agents]]—shared mechanism: MCP provides the protocol layer for the interoperable tools described in the Unix philosophy parallel.
- [[MCP Token Noise]]—failure_mode: over-enabling MCP servers can introduce noise that degrades reasoning.
- [[MOC - AI Software Engineering]]—See Also.
