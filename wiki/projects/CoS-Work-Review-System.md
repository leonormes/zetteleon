---
title: CoS Work-Review System
wiki_type: dossier
entity_kind: project
created: 2026-05-26 12:00:00+00:00
modified: 2026-05-26 12:00:00+00:00
tags:
- wiki
- dossier
sources:
- raw/2026-05-26-pieces-cos-work-review-jira.md
permalink: llmeon/wiki/projects/co-s-work-review-system
---

## Summary

The CoS (Chief of Staff) Work-Review System is an automated Hermes cron job that periodically queries Jira for open tickets, reviews them against Obsidian PKM data, and updates the Source of Truth with current work status. The system was built and validated on 2026-05-26, overcoming a critical Node.js `fetch()` proxy incompatibility on the FitFile corporate VPN by creating a `jira-fetch.js` curl-based workaround.

## Key Facts

- **Jira user ID**: `633ae2b9fedc6169aed8f601` — confirmed from Jira API via curl — [[raw/2026-05-26-pieces-cos-work-review-jira]] (Pieces: a248a154-ae91-4a21-b60f-4d92cc7056cc)
- **Jira URL**: `fitfile.atlassian.net`, project key `FTFL` — [[raw/2026-05-26-pieces-cos-work-review-jira]] (Pieces: 91514026-6fa3-40c3-8f39-5a93f61f1001)
- **Node.js `fetch()` proxy incompatibility**: `@aashari/mcp-server-atlassian-jira` is unusable on FitFile's corporate VPN because Node's native `fetch()` (undici) does not honour macOS system proxies. `curl` works because it reads the system proxy config. This makes the MCP server route a dead end on this machine — `jira-fetch.js` (curl-based) is the canonical path — [[raw/2026-05-26-pieces-cos-work-review-jira]] (Pieces: 94288a8e-651f-4e20-bbf6-900a87045b45)
- **1Password token retrieval fix**: The root cause of empty `$TOKEN` was `2>/dev/null` suppressing the 1Password interactive prompt. The fix requires either `2>&1` or using `--no-tty` flag — [[raw/2026-05-26-pieces-cos-work-review-jira]] (Pieces: 8720efc8-0a3b-451f-9eb5-205b57814cba)
- **CoS skill created**: `~/.hermes/skills/cos-work-review.md` — 80 lines, all 7 steps, YAML frontmatter — [[raw/2026-05-26-pieces-cos-work-review-jira]] (Pieces: 435c7268-168d-4c24-a0b2-af2cde06beef)
- **Cron jobs registered**: Morning Boot (08:15), plus additional schedule entries — [[raw/2026-05-26-pieces-cos-work-review-jira]] (Pieces: 435c7268-168d-4c24-a0b2-af2cde06beef)
- **First successful run**: Retrieved 5 open Jira tickets, identified 1 stale (FTFL-638 Grafana Monitoring going cold), updated Obsidian — [[raw/2026-05-26-pieces-cos-work-review-jira]] (Pieces: 34b0e586-ebd1-4a4a-bd93-5a5acfcea103)
- **zsh `%` escaping issue**: `zsh: % with no previous word matched` caused by `%3D` inside double quotes — fix is to use single quotes or escape with `\\%` — [[raw/2026-05-26-pieces-cos-work-review-jira]] (Pieces: b999c433-488f-4e46-9c03-158ea1322144)

## Reliability History

### 2026-06-04 — Cron enters stale failure streak

The CoS Work Review cron began producing stale data for **7–8 consecutive runs** (last fresh fetch: 2026-06-04). Two independent failure modes affected the Jira data pipeline:

1. **`gk whoami` returning "not authenticated"** — The `XDG_DATA_HOME` environment variable was missing from the Hermes gateway launchd plist (`~/Library/LaunchAgents/ai.hermes.gateway.plist`). The Jira sub-provider in `gk` requires this path to locate its credentials, which launchd services do not inherit from the user shell by default.

2. **`op run` timeout** — The 1Password CLI daemon socket becomes stale after the user desktop session's authentication expires. The cron job runs as a launchd service without a TTY, so `op run` cannot re-prompt the user for 1Password desktop app approval.

Fix applied **2026-06-09**: Injected `XDG_DATA_HOME=/Users/leon.ormes/.local/share` into the plist. Committed to chezmoi at `private_Library/LaunchAgents/ai.hermes.gateway.plist` (commit message: "fix: inject XDG_DATA_HOME into hermes gateway plist for gk cron auth"). Gateway PID `75103` verified authenticated immediately after restart.

### Durable fix direction (investigated 2026-06-10)

To eliminate the 1Password/GitKraken session dependency entirely, the planned fix is to provision a standalone **Jira Personal Access Token** and register it with `gk`:

```
gk provider add jira -t <new-token>
```

This removes the need for `op run` (1Password) or `gk OAuth session` (GitKraken) in cron context. The existing `lazyjira` Atlassian PAT (created 1 Apr 2026, expires 1 Apr 2027) is stored in 1Password at `op://ff/JIRA_API_TOKEN/credential` — a new distinct token would be created for the cron job to avoid confusion.

Key files: `~/.hermes/skills/custom/cos-work-review/SKILL.md` contains the cron skill logic; `~/.local/share/GitKrakenCLI/cli/gk_config.yaml` stores provider configs.

### Token audit: LazyJira Atlassian PAT

Verified 2026-06-10 from Atlassian API tokens page:
- Token name: **`lazyjira`** (this is the Atlassian PAT name, not the tool name)
- Created: 2026-04-01, Expires: 2027-04-01
- 1Password reference: `op://ff/JIRA_API_TOKEN/credential` in `chezmoidata.toml`
- The Hermes cron job will use a **separate** PAT (`hermes-cos-cron`) to avoid confusion with the existing token

## Timeline (continued)

- **2026-06-04** — Last fresh Jira data fetch before cron enters stale failure streak
- **2026-06-09 ~09:00 BST** — XDG_DATA_HOME fix applied, gateway restart verified
- **2026-06-10 07:51** — User reports cron still stale (2nd consecutive stale run since 09 June fix); new inquiry about PAT-based durable auth
- **2026-06-10 09:23** — FTFL-658 Jira comment drafted explaining change freeze & pipeline block for MKUH

##

- **2026-05-26 ~09:59–10:32** — CoS work-review system built, diagnosed, and validated end-to-end
- **2026-05-26 10:28** — First successful CoS run: 5 open tickets retrieved, Obsidian updated

## Connections

- [[wiki/projects/MCP Proxy Robustness and High Availability]] — mcp-proxy infrastructure that the CoS system depends on
- [[wiki/projects/Hermes-Agent]] — Hermes agent configuration and skills system
- [[wiki/projects/Obsidian-PKM]] — Obsidian as the Source of Truth updated by CoS runs
- [[wiki/projects/Grafana Alloy Monitoring — FTFL-638]] — FTFL-638 identified as stale in first CoS run

## Contradictions

_(none)_

## Open Questions

- Should the CoS system also query Microsoft Teams for meeting context, or is Jira-only sufficient for the initial version?
- What is the optimal cron frequency for CoS runs — every 4 hours, or twice daily?