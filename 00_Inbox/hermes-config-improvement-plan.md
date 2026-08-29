---
title: hermes-config-improvement-plan
type: note
permalink: llmeon/00-inbox/hermes-config-improvement-plan
---

# Hermes Config Improvement Plan — 2026-05-23

## Summary

Audit of the Hermes configuration (chezmoi source vs live) reveals the config is largely in sync — no file drift between source and live. However, 5 inconsistencies were found against the intended tiered architecture: the default model is set to a Tier 1.5 reasoning engine instead of a Tier 0 cheap flash model, the Pieces MCP server is missing entirely (despite SOUL.md referencing it), the memory provider is not set to `honcho`, `dialectic_cadence` is absent, and the config schema is one version behind.

## Inconsistencies Found

| ID | File | Key/Section | Current Value | Expected Value | Severity |
|----|------|-------------|---------------|----------------|----------|
| I-01 | `private_config.yaml` | `model.default` | `openrouter/owl-alpha` (Tier 1.5) | A Tier 0 cheap flash model (e.g. `qwen/qwen3.5:cloud` or `google/gemini-3-flash`) | **HIGH** |
| I-02 | `private_config.yaml` | `mcp_servers` | Missing Pieces MCP entry | Add Pieces MCP server at `http://localhost:39300/model_context_protocol/` with `transport: sse` | **HIGH** |
| I-03 | `private_config.yaml` | `memory.provider` | `''` (empty, built-in) | `honcho` | **MEDIUM** |
| I-04 | `private_config.yaml` | `dialectic_cadence` | Key does not exist | `2` | **MEDIUM** |
| I-05 | `private_config.yaml` | `_config_version` | `22` | `23` (run `hermes doctor --fix` to migrate) | **LOW** |

## Optimisation Goals

### G-01: Enforce Tiered Model Usage

**Objective:** Ensure cheap models handle context-building (Tier 0) and premium CLIs (Claude Code, Gemini CLI) are only invoked for coding/research tasks AFTER full context has been assembled by Tier 0.

**Current state:** `model.default` is `openrouter/owl-alpha` — a Tier 1.5 free reasoning engine with 1M context. This means every session starts with Owl Alpha consuming the full context window, even for trivial file reads and greps. The `goal_judge.model` is correctly set to `google/gemini-3-flash`.

**Target state:** Set `model.default` to a cheap cloud flash model like `qwen/qwen3.5:cloud` or keep `google/gemini-3-flash`. Owl Alpha remains available as Tier 1.5 via `/model openrouter/owl-alpha` for heavy reasoning, but is NOT the default.

**Files to change:**
- `private_dot_hermes/private_config.yaml`: set `model.default` to `qwen/qwen3.5:cloud` (or equivalent cheap flash)
- `private_dot_hermes/SOUL.md`: add explicit directive that Tier 0 = cheap flash for context-building; Tier 1.5 Owl Alpha for heavy reasoning only

**Rationale:** The mission spec explicitly states Tier 0 should use cheaper models for file reading, searching, and context-building. Owl Alpha is Tier 1.5 and should be invoked on-demand, not as the default.

### G-02: Register Pieces MCP Server

**Objective:** The SOUL.md references `ask_pieces_ltm` for semantic search, but no Pieces MCP server is configured. This means the tool is non-functional.

**Current state:** `mcp_servers` contains only `mcp-proxy` and `graphify`. No Pieces MCP entry.

**Target state:** Add a Pieces MCP server entry pointing to `http://localhost:39300/model_context_protocol/` with `transport: sse`.

**Files to change:**
- `private_dot_hermes/private_config.yaml`: add Pieces MCP server under `mcp_servers`

**Note:** This assumes the Pieces LTM server is running locally on port 39300. If it's not running, the MCP connection will fail — but the config should still be present so it connects when the server is available.

### G-03: Set Memory Provider to Honcho

**Objective:** Enable cross-session user modeling via Honcho as specified in the mission.

**Current state:** `memory.provider` is `''` (empty string), falling back to built-in memory.

**Target state:** Set `memory.provider` to `honcho`. Requires `HONCHO_API_KEY` in `.env` and `~/.honcho/config.json` with `enabled=true`.

**Files to change:**
- `private_dot_hermes/private_config.yaml`: set `memory.provider: honcho`
- `private_dot_hermes/private_dot_env`: add `HONCHO_API_KEY=<user_to_provide>`

**Note:** The user must provide the Honcho API key. This is a MEDIUM item — apply only after confirming the key is available.

### G-04: Add Dialectic Cadence Setting

**Objective:** Configure the dialectic cadence for memory nudges as specified.

**Current state:** `dialectic_cadence` key does not exist in config.

**Target state:** Add `dialectic_cadence: 2` under the `memory` section.

**Files to change:**
- `private_dot_hermes/private_config.yaml`: add `dialectic_cadence: 2` under `memory:`

### G-05: Migrate Config Schema to v23

**Objective:** Bring config schema up to date.

**Current state:** `_config_version: 22`, but v23 is available.

**Target state:** Run `hermes doctor --fix` to auto-migrate.

**Note:** This is LOW severity — new settings are available but not critical. Apply after other fixes.

## Next Actions (ordered)

1. **Fix I-01 (HIGH):** Edit `private_dot_hermes/private_config.yaml`, change `model.default` from `openrouter/owl-alpha` to `qwen/qwen3.5:cloud`
2. **Fix I-02 (HIGH):** Edit `private_dot_hermes/private_config.yaml`, add Pieces MCP server under `mcp_servers`
3. Run `chezmoi diff` to verify the delta
4. Run `chezmoi apply --force` to propagate changes
5. Run `hermes config` to verify new default model is live
6. Run `hermes mcp list` to verify Pieces MCP connects (or shows as configured)
7. **Fix I-03 (MEDIUM):** Set `memory.provider: honcho` — PENDING user providing Honcho API key
8. **Fix I-04 (MEDIUM):** Add `dialectic_cadence: 2` under `memory:` — PENDING confirmation
9. **Fix I-05 (LOW):** Run `hermes doctor --fix` to migrate config schema — PENDING

## Items Deferred for User Review

| ID | Item | Reason |
|----|------|--------|
| I-03 | Set `memory.provider: honcho` | Requires Honcho API key from user |
| I-04 | Add `dialectic_cadence: 2` | Low risk but should confirm intent |
| I-05 | Config schema migration | Non-critical; `hermes doctor --fix` handles it |

## Verification Steps (Post-Fix)

1. `hermes doctor` — should show clean (or fewer issues)
2. `hermes mcp list` — should show 3 servers (mcp-proxy, graphify, pieces)
3. `hermes config` — should show new default model
4. `chezmoi diff` — should show zero untracked drift
5. Test session: cheap model builds context → delegates one coding task to Claude Code CLI → confirm tier transition fires correctly