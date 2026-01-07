---
aliases: []
tags:
  - head
  - ai
  - mcp
  - rag
created: 2026-01-07T12:00:00
status: Active
---

# The Spark
Derived from "MCP-powered RAG Over Complex Docs" (EyelevelAI / Daily Dose of Data Science).
**Core Concept:** Use Cursor IDE as MCP client -> Local MCP Server (FastMCP) -> GroundX API for parsing/search.
**Goal:** Enable RAG over "complex" documents (tables, images, charts) which standard text parsers fail at.

## Resources
- **Repo:** https://github.com/patchy631/ai-engineering-hub/tree/main/eyelevel-mcp-rag
- **GroundX:** https://eyelevel.ai/

# My Current Model
- **Hypothesis:** GroundX handles parsing better than local unstructured loaders.
- **Architecture:** 
    - Client: Cursor IDE
    - Server: Python FastMCP
    - Backend: GroundX API
- **Gap:** I haven't tested if the latency/cost of GroundX is worth it vs local embeddings.

# The Tension
- Is this better than my current Vault RAG?
- Does GroundX have a generous free tier for testing?

# The Next Test
- [ ] **Setup:** Clone repo and get GroundX API Key.
- [ ] **Ingest:** Feed it one "complex" PDF (e.g., a datasheet or financial report).
- [ ] **Verify:** Ask a specific question about a table in that PDF via Cursor.
