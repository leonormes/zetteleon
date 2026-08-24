---
title: Needle 2 Integration — Local Tool Call Worker
type: note
permalink: llmeon/30-library/200-projects/needle-2-integration-local-tool-call-worker
---


## Needle 2 — Local Tool-Call Inference (Option 2)

### What
A 45M-parameter foundation model (14MB binary, 28MB RAM) purpose-built for tool calling and structured extraction. Grammar-constrained decoding, built-in tool retrieval head, confidence-gated responses. Runs entirely locally on Apple Silicon.

### How it fits
Option 2 — standalone tool-call worker for pure-mechanical queries:
- **Pure tool calls** (Jira lookups, dim lights, create ticket) → Needle runs the complete loop locally
- **Tool retrieval** narrows a 50+ tool catalogue to top-5 per turn, saving 5K-15K tokens per query from not shipping all schemas
- **Grammar-constrained** — physically cannot produce malformed JSON
- **Confidence-gated** — calibrated score per response; below threshold → escalate to main LLM

### Installation
Chezmoi-managed via `packages.yaml`:
```yaml
cactus-needle:
  tags: [ai, python, ml]
  common: { manager: uv, id: "cactus-needle[metal]" }
```
CLI: `needle` | Python: `import needle`

### Related
- [[Hermes Cost Optimisation - Free Model Routing Strategy]]
- [[route-task]] — Tiered Routing Matrix

### Smoke test (2026-08-22)
```python
@needle.tool
def get_weather(city: str):
    'Get the current weather for a city.'
    return {'city': city, 'temp_c': 27, 'sky': 'clear'}
agent = needle.Needle(tools=[get_weather])
result = agent.run("what is the weather in London?")
# → get_weather(city="London"), returned correct result, zero cloud tokens
```



## Needle Router Integration (2026-08-22)

### What was built
- **needle-router** — CLI + Python tool that runs Needle 2.complete() against a 26-tool MCP catalogue, returns compressed JSON (suggested_tool + args + confidence)
- **needle-generate-catalogue** — SSE-protocol fetcher for tool schemas from 1MCP
- **Static catalogue** — 26 tools across 6 servers (atlassian, obsidian x2, basic-memory, memory, todoist)

### Skill update
route-task v2.7.0:
- Pre-flight step 0: run Needle Router on MCP queries
- Tier 0.25 in definitions: tool_router
- Full Tier 0.25 protocol section with invocation/output rules
- Routing block includes needle_confidence
- 5K-15K tokens saved per query when confidence >= 0.6

### How to use
```
echo "get Jira FTFL-123" | needle-router
echo "search vault for typed edges" | needle-router --format prompt
```

### Architecture
Route-task loads ~/.hermes/tool-catalogue.json (static snapshot).
Needle 45M model does 2ms inference in ~50MB RAM.
No cloud tokens, all local Apple Silicon.

### Related skill
`custom/needle-worker` — manual invocation patterns
