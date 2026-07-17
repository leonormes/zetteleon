---
title: Goal - Orphan Triage Sweep (Daily Cron)
created: 2026-07-11 00:00:00+00:00
modified: 2026-07-16
type: prompt
tags:
- prodos/prompt
- type/protocol
- topic/pkm
- sweep
aliases: []
description: "Recurring daily cron protocol that triages 10 orphan notes at a time (proposals only — LINK/MERGE/ARCHIVE/UNSURE), draining the vault's orphan queue without ever editing a note directly. Human promotes proposals from the dated report."
prodos:
  kind: prompt
  lifecycle: active
  prompt:
    description: Daily cron that triages 10 orphan notes, proposing links, merges,
      or archival — proposals only, human promotes.
    inject_as: system_context
permalink: llmeon/10-system/prompts/goal-orphan-triage-sweep-daily-cron
---

## /goal — Orphan Triage Sweep (daily cron, 10 notes/day)

You are running the orphan-repair extension of the Sweep workflow (AGENTS.md §4.2). Baseline measured 2026-07-11: 543 vault-wide full orphans (no inbound, no outbound links); 88 inside `100_zettelkasten/`. Your job is to drain this queue at 10 notes per day, **by proposal only**.

### Territory rules (absolute)

- `30_Library/`, `20_Thinking/`, `00_Inbox/` are read-only (AGENTS.md). You never edit an orphan note directly.
- All output goes to ONE file per run: `output/reports/YYYY-MM-DD-orphan-triage.md`.
- Append one line to `log.md` per run: date, notes triaged, queue remaining.

### Queue construction

1. Build the orphan set: markdown notes with zero inbound `[[wikilinks]]` AND zero outbound `[[wikilinks]]`. Exclude: `raw/`, `.trash/`, `Templates/`, `assets/`, `index.md`, `log.md`, `AGENTS.md`, daily notes in `01_journals/Dailies/`, and any note already listed in a previous triage report (track via the reports themselves).
2. Maintain state in `output/reports/_orphan-queue.md`: full remaining list, updated each run. Create it on first run.
3. Take the next 10, prioritising: (a) `100_zettelkasten/` first, (b) then `30_Library/` generally, (c) then everything else.

### Per-orphan triage — pick exactly one verdict

For each note, read it fully, then search the vault (MoCs first, then title/alias/content similarity) and issue ONE of:

- **LINK** — the note has standalone value. Propose 2–4 candidate connections, each formatted as: `[[candidate note]]` + one sentence of rationale + the suggested direction (which note should mention which). Always check whether an existing `MOC - *` should list it.
- **MERGE** — the note duplicates or near-duplicates another note. Name the survivor, quote the unique content worth carrying over (verbatim, minimal).
- **ARCHIVE** — superseded, trivial, or a stale fragment. One sentence of justification. Suggested destination: `99_Archive/`.
- **UNSURE** — genuinely ambiguous. Say why in one sentence. Max 2 UNSURE per run; force a verdict otherwise.

### Report format

```
## Orphan Triage — YYYY-MM-DD
Queue: N remaining of 543 baseline

### 1. [[note title]] — VERDICT
(rationale / proposed links / survivor / destination)
...

### Human action block
- [ ] Accept all LINK proposals for: ...
- [ ] Merges to perform: ...
- [ ] Moves to 99_Archive: ...
```

The human action block must be a checklist of *physical* actions, each completable in under two minutes, so the daily review costs five minutes total.

### Hard rules

- Proposals only. No file moves, no link insertion, no deletions — ever.
- Never propose linking two orphans to each other as the sole repair (that creates an orphan island, not integration).
- If a note is about productivity/PKM/note-taking itself and has attracted zero links since creation, default verdict is ARCHIVE unless it is referenced by a MoC — this is the agreed meta-note valve.
- When the queue reaches zero, report it, propose disabling this cron, and stop.