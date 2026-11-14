---
name: defuddle-knap
description: >-
  Extract clean, clutter-free Markdown and metadata from web URLs using Defuddle CLI and
  render TAC-compliant ProdOS notes or staging files using Knap CLI templates. Use when
  the user shares a URL to capture into 00_Inbox/, wants a web article turned into a
  tmp_atoms file for the Atomic Signal Extractor, or wants batch Markdown generation
  from JSON/CSV data with safe YAML quoting.
---

# Defuddle + Knap Skill (ProdOS Web Capture & Templating)

## Overview

Combines two official Obsidian CLI utilities to automate Stage 0 capture into `00_Inbox/` before running `[[Prompt - Vault Ingest Router]]` or `[[Atomic Signal Extractor → Write TMP file]]`:

1. **`defuddle`** (`npm install -g defuddle` or `npx defuddle`): strips web page navigation, ads, and boilerplate into clean Markdown + structured JSON metadata (`title`, `author`, `domain`, `description`, `published`, `content`).
2. **`knap`** (`npm install -g knap` or `npx knap`): renders Markdown templates from JSON or CSV data using `yaml_property` filters that guarantee safe YAML frontmatter quoting (preventing the unescaped `: `, quote, and apostrophe errors that break the Obsidian Linter).

## Pre-flight Check

Check availability before running:

```bash
defuddle --help
knap --help
```

If missing, run via `__NPX__` / `npx` or ask the user to install globally (`npm install -g defuddle knap`). Never fabricate extracted web content if the command fails.

## Workflow 1: Clean Web Extraction (`defuddle`)

Extract clean Markdown and metadata for `[[Prompt - Vault Ingest Router]]` or `[[Atomic Signal Extractor → Write TMP file]]`:

```bash
# Markdown body only (saves tokens vs raw HTML)
defuddle parse "<url>" --md

# Full JSON payload (title, author, published, description, domain, content)
defuddle parse "<url>" --md --json -o /tmp/capture.json
```

Extract a single metadata field:

```bash
defuddle parse "<url>" -p title
defuddle parse "<url>" -p author
```

## Workflow 2: Render Safe ProdOS Frontmatter (`defuddle` → `knap`)

Pipe `defuddle parse <url> --md --json` directly into `knap render` to stage a raw capture in `00_Inbox/` without YAML syntax errors:

```bash
defuddle parse "<url>" --md --json \
  | knap render -t '---
{{ title | yaml_property:"source_title" }}
{{ author | yaml_property:"author" }}
{{ domain | yaml_property:"domain" }}
status: tmp
---

# {{ title | trim }}

{{ content }}
' --data - -o "00_Inbox/capture_staged.md"
```

> **ProdOS Workbench Rule (`[[SoT - HEAD Note Contract (The Workbench)]] §1.2`):** Web captures NEVER go into `20_Thinking/21_Workbench/`. Always stage captures in `00_Inbox/`, then run `[[Atomic Signal Extractor → Write TMP file]]` → `[[Atomic Linker → Promote & Connect]]`.

## Workflow 3: Batch Note Generation (`knap batch`)

When converting structured JSON arrays or CSV exports into notes in `00_Inbox/`:

```bash
# Always validate the template and run --dry-run first
knap validate template.md
knap batch template.md --data items.json --output-dir 00_Inbox \
  --filename '{{ title | safe_name }}.md' --dry-run
```

## ProdOS Frontmatter Contract Reminders

When authoring a Knap template for permanent ProdOS notes:
- Always use `yaml_property` for string/list properties (`{{ title | yaml_property:"title" }}`).
- Include the mandatory TAC envelope (`title`, `type`, `tags`, `conformant`, `created`, `modified`, and `non_conformance_reason` when `conformant: false`).
- For `claim` notes in `30_Library/100_zettelkasten/`, follow `[[SoT - Atomic Note Standard (The Proposition Card)]]` (`## <Title>` H2, no H1, no `prodos` key, and K-Plex `[<rel>:: [[<target>]]]` typed edges under `### Related` / `### Tensions`).
