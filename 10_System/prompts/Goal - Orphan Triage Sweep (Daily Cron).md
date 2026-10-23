---
aliases: []
created: 2026-07-11T00:00:00+00:00
description: "Recurring daily cron protocol that triages 10 orphan notes at a time (proposals only — LINK/MERGE/ARCHIVE/UNSURE), draining the vault's orphan queue without ever editing a note directly. Human promotes proposals from the dated report."
modified: 2026-10-22T15:11:08+00:00
permalink: llmeon/10-system/prompts/goal-orphan-triage-sweep-daily-cron
tags: [prodos/prompt, sweep, topic/pkm, type/protocol]
title: Goal - Orphan Triage Sweep (Daily Cron)
type: prompt
---

## /goal—Orphan Triage Sweep (Daily cRon, 10 notes/day)

> Trigger: a recurring, proposal-only queue drain, 10 orphans a day. To position ONE orphan and apply the edges in a single supervised run use [[Orphan Note Positioning & Thread Audit]]; to route new content use [[Prompt - Vault Ingest Router]].
>
> Output Contract: follow [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]—confidence, evidence (linked source notes), and an explicit uncertainty flag replace free prose in every output.

You are running a proposal-only orphan-repair sweep. Baseline measured 2026-07-11 (re-measure on the first run; the figures are stale): 543 vault-wide full orphans (no inbound, no outbound links); 88 inside `100_zettelkasten/`. Your job is to drain this queue at 10 notes per day, by proposal only.

### Territory Rules (Absolute)

- This sweep is proposal-only by design, not because of the vault's write rules. You never edit an orphan note directly, and protected notes ([[AGENTS]] §6) are never write targets.
- All output goes to ONE file per run: `90_Audits/YYYY-MM-DD-orphan-triage.md`.

### Queue Construction

1. Build the orphan set: markdown notes with zero inbound `[[wikilinks]]` AND zero outbound `[[wikilinks]]`. Exclude: `.trash/`, `Templates/`, `assets/`, `AGENTS.md`, `CLAUDE.md`, everything in `01_journals/` and `20_Thinking/`, and any note already listed in a previous triage report (track via the reports themselves).
2. Maintain state in `90_Audits/_orphan-queue.md`: full remaining list, updated each run. Create it on first run.
3. Take the next 10, prioritising: (a) `100_zettelkasten/` first, (b) then `30_Library/` generally, (c) then everything else.

### Per-orphan triage—pick Exactly One Verdict

For each note, read it fully, then search the vault (MoCs first, then title/alias/content similarity) and issue ONE of:

- LINK—the note has standalone value. Propose 2–4 candidate connections, each formatted as: `[[candidate note]]` + one sentence of rationale + the suggested direction (which note should mention which). Always check whether an existing `MOC - *` should list it.
- MERGE—the note duplicates or near-duplicates another note. Name the survivor, quote the unique content worth carrying over (verbatim, minimal).
- ARCHIVE—superseded, trivial, or a stale fragment. One sentence of justification. Suggested destination: `99_Archive/`. Never default to ARCHIVE because a note is about PKM or productivity; judge it on content.
- UNSURE—genuinely ambiguous. Say why in one sentence. Max 2 UNSURE per run; force a verdict otherwise.

### Report Format

```
## Orphan Triage — YYYY-MM-DD
Queue: N remaining of 543 baseline

### 1. [[note title]] — VERDICT
(rationale / proposed links / survivor / destination)
...

### Human action block
- [ ] For each LINK proposal, write one line in your own words on why the two notes connect, then add the link: ...
- [ ] Merges to perform: ...
- [ ] Moves to 99_Archive: ...
```

The human action block must be a checklist of _physical_ actions, each completable in under two minutes, so the daily review costs five minutes total.

### Hard Rules

- Proposals only. No file moves, no link insertion, no deletions—ever.
- Never propose linking two orphans to each other as the sole repair (that creates an orphan island, not integration).
- When the queue reaches zero, report it, propose disabling this cron, and stop.
- End every report with `Confidence: <high | medium | low>` and `UNSURE: <verdicts you could not support, or None>`.
