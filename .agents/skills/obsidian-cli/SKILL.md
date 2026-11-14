---
name: obsidian-cli
description: >-
  Interact with the LLMeon Obsidian vault via the Obsidian CLI (Tier 2 fallback after
  obsidian-llmeon 1MCP tools) and debug/reload Obsidian plugins such as K-Plex. Use when
  1MCP tools are unreachable or when reloading plugins, inspecting DOM/console errors,
  or running CLI commands against vault="LLMeon".
---

# Obsidian CLI Skill (LLMeon / ProdOS Edition)

## ProdOS Tooling Tier Rule (`AGENTS.md` §9.1)

1. **Tier 1 (Preferred):** Always prefer `obsidian-llmeon_1mcp_*` tools via 1MCP (`_note_read`, `_note_patch`, `_note_create`, `_note_insert`, `_search_semantic`, `_search_text`, `_wikilinks`).
2. **Tier 2 (This Skill):** Use the `obsidian` CLI when 1MCP is unreachable, or for desktop app / plugin operations (`plugin:reload`, `dev:errors`, `dev:console`, `dev:screenshot`, `rename`, `move`).
3. **Hard Guard (`AGENTS.md` §6):** Never edit, move, rename, or delete a protected note (`own_words: true` or any existing note in `01_journals/` and `20_Thinking/`). Call `shale intent` before mutating any file and `shale done` afterwards.

## Critical Syntax Rules for `LLMeon`

1. **`vault="LLMeon"` MUST Be the First Argument:**
   Since the 2026-07-30 vault split (`LLMeon` vs `Hermes`), always pass `vault="LLMeon"` as the very first token. Anywhere else on the command line it is silently ignored!
   ```bash
   # CORRECT
   obsidian vault="LLMeon" read path="30_Library/100_zettelkasten/MOC - ProdOS.md"
   obsidian vault="LLMeon" search:context query="prosthetic executive function" limit=10

   # WRONG (vault= ignored when not first!)
   obsidian search query="test" vault="LLMeon"
   ```

2. **Double-Dash Output Flags Go LAST:**
   `--json`, `--md`, `--csv`, `--tsv`, and `--copy` only work **after** the command name. Putting them before `vault=` or the command fails (`Command "--json" not found`).
   ```bash
   obsidian vault="LLMeon" backlinks path="30_Library/100_zettelkasten/MOC - ProdOS.md" --json
   ```

3. **Zero Exit Code Trap:**
   The `obsidian` CLI exits with status `0` even when a command fails. Always inspect stdout/stderr before reporting success.

4. **`content=` Backslash & Size Trap:**
   In `create content=...` or `append content=...`, every `\n` and `\t` is converted to a newline/tab with no escaping, corrupting LaTeX (`\theta`, `\rightarrow`), regexes, or Windows paths. For notes with backslashes or bodies over ~4 KB, use `obsidian-llmeon_1mcp_note_create` / `_note_patch` or direct file writes after reading.

5. **Dots in Filenames:**
   A dot in `name=` or `to=` is parsed as the start of a file extension. Always append `.md` explicitly when a title contains a dot:
   ```bash
   obsidian vault="LLMeon" rename path="00_Inbox/draft.md" name="SoT - v1.2 Architecture.md"
   ```

## Common Vault Operations

```bash
obsidian vault="LLMeon" read path="30_Library/100_zettelkasten/SoT - PRODOS Core Specification.md"
obsidian vault="LLMeon" search:context query="choice architecture" limit=10
obsidian vault="LLMeon" backlinks path="30_Library/100_zettelkasten/SoT - Prosthetic Executive Function.md"
obsidian vault="LLMeon" unresolved
obsidian vault="LLMeon" rename path="30_Library/100_zettelkasten/Old Title.md" name="New Title.md"
obsidian vault="LLMeon" move path="00_Inbox/Promoted Note.md" to="30_Library/100_zettelkasten/"
```

> Use `obsidian vault="LLMeon" rename` or `move` (or `git mv` per workflow rules) so Obsidian's link updater rewrites inbound `[[wikilinks]]`.

## K-Plex & Plugin Reload / Debugging Workflow

For inspecting K-Plex ontology, directional neighbours, connection evidence (`frontmatter-overrides-body-ontology` overrides), and open canvases at runtime, load **`.agents/skills/kplex-obsidian-cli/SKILL.md`** and query `window.kplexApi.v1` via `obsidian vault="LLMeon" eval`:

```bash
# Quick K-Plex runtime probes (strip leading `=> ` before JSON.parse)
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.status())'
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.ontologyGuide({format:"markdown"}))'
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.neighbors({id:"30_Library/100_zettelkasten/SoT - The Extended Mind.md",role:"child",limit:40}))'
obsidian vault="LLMeon" eval 'code=JSON.stringify(window.kplexApi.v1.evidence({sourceId:"SOURCE_ID",targetId:"TARGET_ID",limit:128}))'
```

After editing `.obsidian/plugins/k-plex/data.json` or any plugin configuration (remember to reacquire `window.kplexApi.v1` after reload):

```bash
# 1. Enable debug capture (once per session)
obsidian vault="LLMeon" dev:debug on

# 2. Hot-reload K-Plex so it picks up the new data.json ontology/facets immediately
obsidian vault="LLMeon" plugin:reload id=k-plex

# 3. Check for runtime or ontology validation errors
obsidian vault="LLMeon" dev:errors
obsidian vault="LLMeon" dev:console level=error
```
