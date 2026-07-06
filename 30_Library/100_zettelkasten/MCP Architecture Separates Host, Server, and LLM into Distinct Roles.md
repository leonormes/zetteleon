---
created: 2026-04-10T13:00:00+00:00
modified: 2026-07-04T10:51:49+00:00
permalink: llmeon/30-library/100-zettelkasten/mcp-architecture-separates-host-server-and-llm-into-distinct-roles
tags: [agentic-ai, architecture, mcp, system-design]
title: MCP Architecture Separates Host, Server, and LLM into Distinct Roles
---

## MCP Architecture Separates Host, Server, and LLM into Distinct Roles

The MCP architecture decomposes a tool-augmented AI system into three distinct entities: the Host (the client application—e.g. Claude Code, Cursor—that mediates the user interaction), the Server (the component that exposes tools and resources to the LLM), and the LLM (the reasoning engine that decides which tools to call and how to interpret their results). Information flows: Host receives user input → LLM reasons and selects tools → Server executes tools and returns results → LLM synthesises a response → Host presents output.

### Scope & Conditions

Defines the conceptual model for any MCP-compliant implementation. Servers can be swapped or updated independently of the host—the protocol boundary is the interface. The LLM's role is pure reasoning; it never directly invokes infrastructure, it only names what to call.

### Evidence

> "interaction between the Host (client application), the Server (exposing tools/resources), and the LLM (reasoning engine) [Video 2]"

### Implications

- Clean separation of concerns enables modularity: a new tool server can be registered without modifying the host or retraining the LLM.
- The LLM as a "pure reasoner" is a deliberate constraint—isolating side effects to the Server layer makes agentic actions auditable and rollbackable.

### Related

- [[SoT - Extending Gemini CLI with MCP]]—extends: the Host/Server/LLM decomposition is the conceptual model behind the `.gemini/settings.json` configuration patterns in that SoT; the config file registers Server definitions for the Host to manage.
- [[SoT - Agentic Roles]]—shared mechanism: both define a role-separation model for AI systems; MCP's Host/Server/LLM maps structurally onto the Architect/Coder/Scout decomposition—reasoning, execution, and coordination as distinct responsibilities.
