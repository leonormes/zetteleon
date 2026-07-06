---
created: 2026-06-22T09:16:18+00:00
modified: 2026-07-04T10:52:05+00:00
permalink: llmeon/10-system/prompts/configure-basic-memory.prompt
title: configure-basic-memory.prompt
---

## Task: Configure Basic Memory for the LLMeon Zettelkasten (Chezmoi-managed, lOcal-first)

You are my engineering assistant on macOS. Configure Basic Memory (<https://docs.basicmemory.com>) as a shared, local Markdown memory layer, with my existing Obsidian vault as the single source of truth. Work through my chezmoi-managed dotfiles. Be idempotent, discover the real state of my system rather than assuming, and stop at the one DECISION POINT below before proceeding.

---

### Operating Constraints (Read First, Do not vIolate)

- chezmoi is the source of truth for config. Every persistent config change is made in the chezmoi source directory, then applied with `chezmoi apply`. Never hand-edit a target file (e.g. `~/.hermes/config.yaml`) directly—locate its source with `chezmoi source-path <target>` and edit that.
- Local-first. No cloud, no API keys. Embeddings run locally via `fastembed` (default). Do not enable `cloud_mode` or run any `bm cloud …` command.
- Never manage runtime-mutated or derived files in chezmoi (see §2). Doing so causes permanent `chezmoi diff` drift.
- British English in any note, comment, or doc you write.
- Idempotent + re-runnable. Assume this prompt may be run more than once.
- Report in micro-steps. After each numbered phase, give me a one-line status. Stop and ask at the DECISION POINT.

---

### 1. Context—what We Are Building

A single Markdown knowledge base, written and read by three consumers that all share the same files:

1. Hermes Agent (you)—via the first-party `hermes-basic-memory` plugin.
2. Claude Desktop—via an MCP server entry.
3. Claude Code—via an MCP server entry (or routed through my existing `mcp-proxy` on `:8000`).

Single source of truth (the vault): `/Volumes/DAL/Zettelkasten/LLMeon/`

This is an existing Obsidian vault on an external volume. Basic Memory treats the Markdown files as canonical; its SQLite index is a disposable, rebuildable cache. Obsidian needs no plugin—it simply opens the same folder.

Relevant facts about this machine:

- Hermes Agent is v0.14.0 (`_config_version 23`), primary model `openrouter/owl-alpha`, managed in chezmoi under `~/.local/share/chezmoi/private_dot_hermes/`.
- Existing MCP servers: `mcp-proxy` (streamable-http, `:8000`) and `pieces` (SSE, `:39300`).
- `uv` / `uvx` is available.

---

### 2. Hard Rules for Chezmoi (The Failure Modes to aVoid)

| File / path | Manage in chezmoi? | Why |
|---|---|---|
| `~/.basic-memory/config.json` | No | Basic Memory rewrites it at runtime (migration, `auto_update_last_checked_at`, `last_sync`). Register the project via the `run_onchange_` script in §5 instead. |
| `~/.basic-memory/*.db` (SQLite index) | No | Derived cache; rebuilt from the Markdown. Never commit. |
| `/Volumes/DAL/Zettelkasten/LLMeon/` (the vault) | No | This is _data_, not config; it is its own store. |
| `~/.hermes/config.yaml` | Yes | Declarative. Add the `memory.provider` block (§6). |
| `~/.hermes/basic-memory.json` (plugin config) | Yes, if used | Declarative settings _you_ choose (§7). Edit via chezmoi, not via `hermes memory setup` (that command would write the target and create drift). |

If any of the "No" paths fall inside a chezmoi-managed tree, add them to `.chezmoiignore`.

The `~/.basic-memory/config.json` mutation problem is the single most important constraint. The whole point of the `run_onchange_` script is to express the project registration _declaratively in chezmoi_ while letting the app own the mutable JSON.

---

### 3. Pre-flight—discover, Don't Assume (Run These, Report fIndings)

```bash
command -v uv && uv --version                      # uv must be on PATH
test -d /Volumes/DAL/Zettelkasten/LLMeon && echo "vault mounted" || echo "VAULT NOT MOUNTED"
chezmoi source-path                                # chezmoi source root
chezmoi source-path ~/.hermes/config.yaml          # where the Hermes config source lives
command -v bm || echo "basic-memory not yet installed"
hermes plugins list 2>/dev/null || true            # is the plugin already present?
```

Also locate (do not edit yet) my existing MCP client configs so §8 matches the pattern I already use:

- `mcp-proxy` config (the thing serving `:8000`)
- Claude Desktop: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Claude Code: `~/.claude.json` (user scope) and/or any project `.mcp.json`

If the vault is not mounted, stop and tell me—nothing below should run against an absent volume.

---

### 4. Install the Basic Memory CLI

```bash
uv tool install basic-memory      # idempotent; gives the `bm` command
bm --version
```

---

### 5. Register the Vault as a project—via a Chezmoi `run_onchange_` Script (NOT a Static Config fIle)

Create this in the chezmoi source directory (alongside other dotfiles, not inside `private_dot_hermes/`):

`run_onchange_after_configure-basic-memory.sh`

```bash
#!/usr/bin/env bash
# Registers the Basic Memory project for the LLMeon Zettelkasten.
# run_onchange: re-runs automatically if PROJECT or VAULT below changes.
set -euo pipefail

PROJECT="llmeon"
VAULT="/Volumes/DAL/Zettelkasten/LLMeon"

# Guard: external volume must be mounted — skip cleanly so `chezmoi apply` never fails.
if [ ! -d "$VAULT" ]; then
  echo "basic-memory: vault not mounted at $VAULT — skipping registration." >&2
  exit 0
fi

# Ensure the CLI exists (idempotent).
command -v bm >/dev/null 2>&1 || uv tool install basic-memory

# Register the project and make it the default for clients that don't pass one.
# NOTE: verify the exact syntax for the installed version first — older builds use
#   `bm project add <name> <path>` (positional); some use `--local-path`.
#   Run `bm project add --help` and adjust the next line if needed.
bm project add "$PROJECT" "$VAULT" 2>/dev/null || true
bm project default "$PROJECT"
bm project list
```

Then:

```bash
chmod +x <source>/run_onchange_after_configure-basic-memory.sh   # if your chezmoi setup needs it
chezmoi apply
```

> Why this pattern: putting the path inside the script means changing the path changes the script's content, which is exactly what re-triggers a `run_onchange_` script. The registration is therefore version-controlled and reproducible, while the mutable `config.json` stays machine-local.

_(Optional refinement, only if you want DRY: lift `VAULT`/`PROJECT` into `.chezmoidata.yaml` and make the script a `.tmpl`. Skip for now unless asked—it adds steps for little gain at one project.)_

---

### 6. Install and Activate the Hermes Plugin

This is the primary integration for _me_ (the agent) and is richer than a bare MCP entry—it adds search-before-answer recall and auto-capture.

```bash
hermes plugins install basicmachines-co/hermes-basic-memory
```

In the chezmoi source for `~/.hermes/config.yaml` (found in §3), merge in—do not clobber existing keys:

```yaml
memory:
  provider: basic-memory
```

Apply and bring the plugin up:

```bash
chezmoi apply
# Ensure the `mcp` python package is in the Hermes venv (the installer usually handles this):
uv pip install --python ~/.hermes/hermes-agent/venv/bin/python mcp   # only if `hermes memory status` complains
hermes gateway restart        # only if the gateway is running
hermes memory status          # expect: provider basic-memory, plugin installed ✓, available ✓
```

Version caveat—do not be surprised: on Hermes `v0.14.0` the native `/bm-*` slash commands will _not_ appear in gateway sessions (an upstream plugin-loading gap, not a plugin bug). The `bm_*` agent tools and auto-capture work regardless. The fix is the Hermes-side patch in the plugin's `MONKEYPATCH.md`. Treat that patch as a deferred, optional follow-up—flag it in your final report but do not apply it now without my say-so (it modifies upstream Hermes and I prefer incremental changes).

---

### 7. DECISION POINT—capture Policy (Protect the Zettelkasten)—STOP AND ASK ME

The plugin's auto-capture writes a running transcript every turn plus an end-of-session summary. By default it targets project `hermes-memory` at `~/hermes-memory/`. Raw transcripts do not belong in a curated Zettelkasten. Present me these three options and wait for my choice:

- Option A—Two projects (recommended).
  Leave the plugin on its defaults (`project: hermes-memory`, `project_path: ~/hermes-memory/`) so all noisy auto-capture stays _out_ of the vault. The vault project `llmeon` becomes a deliberate write target, reached via per-call routing (`bm_write(…, project="llmeon")`) only when I explicitly ask you to file something in the Zettelkasten. Lowest config, cleanest separation, vault stays pristine. _(If chosen, the plugin config file in §2 is optional—defaults suffice. Consider adding a one-line routing convention to my `SOUL.md`/`AGENTS.md`: "file durable, curated notes to `llmeon`; everything else stays in `hermes-memory`.")_

- Option B—One project, fenced capture.
  Point the plugin at the vault (`project: llmeon`, `project_path: /Volumes/DAL/Zettelkasten/LLMeon/`) but keep `capture_folder` as a clearly-named subfolder (e.g. `hermes-sessions/`) that I can exclude from Obsidian's graph and search. Everything in one place, at the cost of raw logs living inside the vault.

- Option C—One project, capture off.
  `project: llmeon`, `capture_per_turn: false`, `capture_session_end: false`. The vault stays purely curated; I only remember what you explicitly `bm_write`. Most conservative, loses the auto-memory benefit.

If I pick B or C, write the chosen settings to the chezmoi source for `~/.hermes/basic-memory.json` (managed per §2):

```json
{
  "mode": "local",
  "project": "llmeon",
  "project_path": "/Volumes/DAL/Zettelkasten/LLMeon/",
  "capture_per_turn": true,
  "capture_session_end": true,
  "capture_folder": "hermes-sessions",
  "remember_folder": "bm-remember"
}
```

(adjust the flags to match the option chosen), then `chezmoi apply`.

---

### 8. Wire the other Clients to the Same Vault (The "Shared bRain")

Register Basic Memory with Claude Desktop and Claude Code so they read/write the same `llmeon` vault (they should _not_ touch my agent's private `hermes-memory` log). Match my existing MCP config style from §3—if I aggregate through `mcp-proxy`, add it there once; otherwise add it to each client.

Canonical stdio entry:

```json
{
  "mcpServers": {
    "basic-memory": {
      "command": "uvx",
      "args": ["basic-memory", "mcp"],
      "env": { "BASIC_MEMORY_MCP_PROJECT": "llmeon" }
    }
  }
}
```

- `BASIC_MEMORY_MCP_PROJECT=llmeon` locks these clients to the vault regardless of the global default.
- If adding behind `mcp-proxy`, register Basic Memory as a stdio backend (`bm mcp` / `uvx basic-memory mcp`) in whatever format my existing proxy backends use.
- Restart each client after editing.

---

### 9. Verify End-to-end (Then Clean uP)

1. From a Hermes session: `bm_write` a throwaway note titled "Basic Memory smoke test" into `llmeon`.
2. Confirm the `.md` file appears under `/Volumes/DAL/Zettelkasten/LLMeon/` and opens in Obsidian (backlinks/graph render).
3. `bm_search "smoke test"` returns it; `bm_recent` lists it.
4. From Claude Desktop or Claude Code, confirm the same note is searchable (proves the shared store).
5. `bm_delete` the test note.
6. `chezmoi diff`—confirm no drift (managed files clean; mutable `config.json` / `*.db` ignored, not tracked).
7. Commit the chezmoi source: `chezmoi cd` → `git add -A && git commit -m "Add Basic Memory: LLMeon vault, Hermes plugin, MCP clients"` → exit.

---

### 10. Final Report to Me (Concise, Micro-step fOrmat)

- What changed, and which files are now in chezmoi vs intentionally excluded (and why).
- The capture option I chose and where auto-captured session notes land.
- Confirmation that `chezmoi diff` is clean.
- Deferred / optional: the `MONKEYPATCH.md` slash-command patch (v0.14.0), and any `SOUL.md`/`AGENTS.md` routing convention.
- Operational caveat to surface: memory is unavailable whenever the `/Volumes/DAL` volume is unmounted—the `run_onchange_` guard skips cleanly, but live recall/capture will fail until it's remounted.
