---
aliases: []
confidence: ""
created: 2026-01-07T17:58:44+00:00
epistemic: ""
last_reviewed: ""
modified: 2026-01-08T10:50:02+00:00
purpose: ""
review_interval: ""
see_also: []
source_of_truth: []
status: Active
tags: [ai, head, mcp, rag]
title: 2026-01-07-1200-HEAD - MCP GroundX Experiment
type: ""
---

## The Spark

Derived from "MCP-powered RAG Over Complex Docs" (EyelevelAI / Daily Dose of Data Science).

**Core Concept:** Use Cursor IDE as MCP client -> Local MCP Server (FastMCP) -> GroundX API for parsing/search.

**Goal:** Enable RAG over "complex" documents (tables, images, charts) which standard text parsers fail at.

### Resources

- **Repo:** https://github.com/patchy631/ai-engineering-hub/tree/main/eyelevel-mcp-rag
- **GroundX:** https://eyelevel.ai/

## My Current Model

- **Hypothesis:** GroundX handles parsing better than local unstructured loaders.
- **Architecture:**
    - Client: Cursor IDE
    - Server: Python FastMCP
    - Backend: GroundX API
- **Gap:** I haven't tested if the latency/cost of GroundX is worth it vs local embeddings.

## The Tension

- Is this better than my current Vault RAG?
- Does GroundX have a generous free tier for testing?

## The Next Test

- [ ] **Setup:** Clone repo and get GroundX API Key.
- [ ] **Ingest:** Feed it one "complex" PDF (e.g., a datasheet or financial report).
- [ ] **Verify:** Ask a specific question about a table in that PDF via Cursor.
