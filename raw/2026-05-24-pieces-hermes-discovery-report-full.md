---
created: 2026-05-24T18:11:44+00:00
modified: 2026-05-26T11:43:31+00:00
pieces_ids: [c8c5de20-42b9-45d4-a2b4-07c43e6c83fc]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-24-pieces-hermes-discovery-report-full
---

## Hermes Agent Discovery Report—Full Configuration Audit

Pieces capture from 2026-05-24T18:11:44 UTC.

Both pagination cursors are now exhausted or have yielded sufficient additional evidence. Here are the two missing closing sections:

---

### 6. External References & Benchmarks

#### Documentation Consulted

- [Hermes Agent Quickstart — Ollama Docs](https://docs.ollama.com/integrations/hermes)—referenced during initial setup (27 Apr 2026); used to configure the `ollama launch hermes` flow and understand the Ollama-native provider onboarding.
- [OpenRouter × Hermes Integration guide](https://openrouter.ai/docs/cookbook/coding-agents/hermes-integration)—accessed 19 May 2026; used to configure OpenRouter as primary cloud provider and understand `hermes model` selector flow.
- Hermes Agent official website / Nous Research portal—accessed 24 May 2026 at [https://portal.nousresearch.com/login](https://portal.nousresearch.com/login); referenced for release notes and current version status.
- [Hermes Agent - Ollama integration page](https://docs.ollama.com/integrations/hermes)—multiple visits; used for manual `config.yaml` structure, provider routing syntax, and common errors (401/403, context length).
- [SAGE for Hermes Agent Architecture — Gemini session](https://gemini.google.com/app/cda485f937f19a0a)—18 May 2026; external consultant-style session used to design the brain-mcp cognitive layer upgrade and the "single point of discovery" mcp-proxy architecture. Key architectural principle cited: _"By updating the proxy instead of Hermes, every other LLM or agent in your system also gains access."_
- [Hermes Config: Intelligent Model Routing — Gemini session](https://gemini.google.com/app)—19 May 2026; used to plan OpenRouter latency-sorted routing, data-collection deny policy, and auxiliary slot optimisation.
- [Hermes: Cost-Optimizing AI Orchestration — Gemini](https://gemini.google.com/app/c38430bdcd504c9a)—19 May 2026; architectural framing for "master controller → lowest-cost model per task" design intent.
- [Orchestrating LLMs with CLIs — Gemini](https://gemini.google.com/app/de7a8fa29b794105)—7 May 2026; referenced for SOUL.md tiered-routing design (apfel as Tier 0 local brain, delegating to Claude Code / Gemini CLI / OpenRouter).
- Hermes Agent docs (built-in)—`hermes --version`, `hermes doctor`, `hermes config show`, `hermes mcp list` outputs consulted throughout; version progression tracked from `v0.11.0 (2026.4.23)` → `v0.12.0 (2026.4.30)` → `v0.13.0 (2026.5.7)` → `v0.14.0 (2026.5.16)`.

#### Comparative Agents / Projects Benchmarked

- OpenClaw (Claude Code)—primary comparison target. Multiple sessions (May 9–11, 2026) reviewed the YouTube video _"Hermes Agent might have just killed OpenClaw"_ by Alex Finn (81k–115k views); Gemini and Claude used to synthesise a structured review. Key friction identified: at the time of comparison, context length was 64k (Hermes) vs. 128k recommended; multi-agent parallel delegation was not yet performing.
- PRAXIS v0.7.0—mentioned in YouTube browsing session (18 May 2026) alongside Hermes Agent use cases; no deeper benchmarking captured.
- Codex / OpenCode—appear in the skills directory (`~/.hermes/skills/autonomous-agents/`) as delegated sub-agents; used as benchmarks for coding delegation quality in the SOUL.md routing tiers.
- apfel (Apple Foundation Model wrapper, v1.3.3)—tested as Tier 0 local provider on 7 May 2026; failed: 4,096-token context window is below Hermes's 64k minimum, causing `Failed to initialize agent` errors. Abandoned in favour of Ollama + qwen3.5.
- Gemini CLI, Claude Code CLI—positioned as Tier 1 delegation targets in the routing hierarchy (Tier 1A = Claude Code for coding; Tier 1B = Gemini CLI for research). Not benchmarked head-to-head; routing decisions are rule-based.

#### Success Criteria / Evaluation Benchmarks Mentioned

- `hermes --tui` startup target: under 10 seconds—explicitly set as the acceptance criterion in the TUI slow-startup `/goal` prompt (23 May 2026). Baseline at time of diagnosis: 30–40 seconds (timing out after 15s in test).
- `hermes doctor` issues: reduce to 0 or 1—used as the validation gate for the May 23 config audit; result was _"reduced from 2 to 1 (remaining item: pre-existing missing API keys)"_.
- `_config_version: 22 → 23`—config schema migration used as a completeness marker for the May 23 audit.
- Token cost reduction—qualitative objective driving the `private_config.yaml` "Clean Slate" refactor (18 May 2026): strip personality bloat, route auxiliary slots to `google/gemini-3-flash`, enforce `sort: latency` + `data_collection: deny` on OpenRouter.
- Context length ≥ 128k—cited as the target following the OpenClaw comparison review (11 May 2026): _"Current model context length: 64,000. Recommended: 128,000 or higher."_ Addressed by switching primary model to `qwen/qwen3.5-plus-20260420` (1M context, May 23).
- `max_turns: 30`—set as a functional threshold for long-running agentic tasks after repeated 10/10 freeze complaints (May 16–18); `max_turns` (main loop) and `max_iterations` (delegation) distinguished as separate parameters after debugging.

---

### Confidence & Gaps

High confidence (grounded in multiple independent tool results):

- Version history: `v0.11.0` → `v0.14.0`, all with specific dates and upstream commit hashes confirmed via terminal and GitKraken events.
- Core file paths: `~/.local/share/chezmoi/private_dot_hermes/private_config.yaml`, `SOUL.md`, `~/.hermes/config.yaml`, `~/.hermes/hermes-agent/`—confirmed by filesystem_search_paths and multiple vision/clipboard captures.
- Config architecture (chezmoi source → `chezmoi apply --force` → live `~/.hermes/`)—confirmed by 10+ independent session transcripts.
- Primary model evolution and the OpenRouter provider switch—confirmed by GitKraken commit messages, terminal diffs, and ask_memory narrative.
- Known bugs: TUI 30–40s startup, `qwen/qwen3.5:cloud` invalid model ID, `pieces (stdio) - failed` MCP connection, `/clear` freeze, `max_turns`/`max_iterations` confusion—all confirmed by raw terminal and Obsidian wiki captures with specific dates and error text.
- SOUL.md §1.5 (Pre-Task Context Rule) and §1.6 (Delegation Decision Tree)—content confirmed verbatim from audit transcripts.

Medium confidence (single-source or partially reconstructed):

- The exact current state of `private_config.yaml` at time of this report—last confirmed snapshot is the May 23 audit (`_config_version: 23`), but 4+ commits have occurred since; live state may differ.
- Profiles inventory (`cowork.yaml`, `ops.yaml`, `research.yaml`, `thin.yaml`, `creative.yaml`, `infra.yaml`, `pkm.yaml`)—confirmed by GitKraken and chezmoi file-explorer captures, but contents of most profiles were not captured in full.
- Custom skills list—confirmed by directory listing (28 Apr 2026) and GitKraken staged-file lists, but `SKILL.md` content for most skills not captured; `route-task.md` content partially seen.
- Honcho integration state—was configured (May 18), then explicitly removed in the "Clean Slate" refactor. Current status uncertain: one May 19 audit shows `honcho: {}` (disabled/empty), another shows `memory_provider: ''`. Contradictory.

Thin / gaps:

- Repo URL—no public or GitLab URL for the chezmoi repo was captured. Path: `~/.local/share/chezmoi`, branch: `development`. Remote `origin` inferred but URL not observed.
- AGENTS.md content—referenced multiple times as a Hermes rulebook, but full content not captured.
- Full `private_config.yaml` content—never read in a single complete capture; synthesised from partial diffs, walkthrough notes, and audit outputs. Risk of omission for less-touched sections.
- Test / eval coverage—no automated tests, evals, or benchmarking scripts found in any source. No CI pipeline for the Hermes config was observed.
- `mission.md` content—referenced as a Hormozi-12 mission definition file at `~/.local/share/chezmoi/private_dot_hermes/assets/context/mission.md`; added in the 15 May commit, but content not captured.
- Brain-mcp integration—proposed in a May 18 Gemini session as a future upgrade; no evidence it was ever implemented.
- Voice-capture skill—discussed as a planned enhancement on 23 May 2026; no evidence of implementation.
