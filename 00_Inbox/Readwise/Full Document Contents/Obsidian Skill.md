---
created: 2026-03-14T09:50:16+00:00
modified: 2026-03-14T11:09:05+00:00
tags: [articles]
title: Obsidian Skill
---

## Obsidian Skill

![rw-book-cover](https://mcp-obsidian.org/og-image.jpg)

### Metadata

- Author: [[Mauricio Wolff (bitbonsai)]]
- Full Title: Obsidian Skill
- Category: articles
- Summary: The Obsidian Skill routes note operations to the right backend for safety and efficiency. It uses MCP for safe file edits, Obsidian CLI for app-specific tasks, and Git for syncing and backups. This ensures secure, atomic note management without needing Obsidian Sync.
- URL: <https://mcp-obsidian.org/skill/>

### Full Document

Combines MCP server safety with Obsidian CLI context.
 One skill that routes each operation to the right backend.

#### Routing Matrix

Each operation maps to exactly one backend. The skill picks the right one automatically.

| Operation | MCP | Obsidian CLI | Git | Notes |
| --- | --- | --- | --- | --- |
| Read note |  ✓  |—|—| Safe, sandboxed read via MCP |
| Write / patch note |  ✓  |—|—| Atomic writes with validation |
| Search vault |  ✓  |—|—| BM25-ranked full-text search |
| Manage tags / frontmatter |  ✓  |—|—| Safe YAML merge |
| Move / rename files |  ✓  |—|—| Path-confirmed moves |
| Open note in Obsidian |—|  ✓  |—| Requires the desktop app running |
| Trigger plugin commands |—|  ✓  |—| Workspace actions, plugin APIs |
| Export to PDF |—|  ✓  |—| App-level rendering pipeline |
| Sync vault across devices |—|—|  ✓  | Plain git—no Obsidian Sync needed |
| Automated backup |—|—|  ✓  | Cron / launchd, no UI needed |

#### Flow Cheat Sheet

The skill routes by intent. MCP is the safe default for vault edits, Obsidian context is used for app-specific actions, and Git CLI handles sync/backup.

##### Intent Routing

#### What It Is

Handles all file I/O: reading, writing, searching, patching, and organizing notes. Enforces path sandboxing, validates inputs, and performs atomic operations. The safe default for any vault mutation.

Bridges the gap for operations that need the running desktop app: opening notes in the editor, triggering plugin commands, exporting to PDF via Obsidian URI schemes.

Plain git for vault syncing across devices. No Obsidian Sync subscription required. Works headlessly via cron, launchd, or CI—no app needs to be running.

#### When To Use

##### Trigger Phrases

#### Workflow Patterns

Three patterns for combining MCP and Obsidian in a single session.

Chain MCP reads into app actions. Search for a note via MCP, then open it in Obsidian for visual editing.

The skill picks the right backend automatically. File operations route through MCP; app-context actions use Obsidian URI schemes.

#### Safety Defaults

All file mutations go through the MCP server, which validates paths, confirms targets, and performs atomic writes.

Commands use structured arguments, never string-interpolated shell input. No injection vectors.

Install the skill to teach your AI assistant the Obsidian workflow.

```
.claude/
  skills/
    obsidian/
      SKILL.md                  # Gotchas, error recovery, index
      resources/
        tool-patterns.md        # Per-tool response shapes and recipes
        obsidian-conventions.md # Vault structure, wikilinks, tags
        git-sync.md             # Git backup/sync workflows
```

```
---
name: obsidian
description: >
  Activate when the user mentions their
  Obsidian vault, notes, tags, frontmatter,
  daily notes, backup, or sync. Route
  operations across MCP, Obsidian CLI/app
  actions, and git sync with safe defaults.
metadata:
  version: "2.0"
  author: bitbonsai
---
```
