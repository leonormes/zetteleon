---
title: Protocol - Engage Action (Prosthetic Timebox & Somatic Switch)
description: 'Run the CoS prosthetic executive function loop for a single 15m/30m/60m
  timebox: Pre-Flight Task-Authoring Gate (Done means, <120s MVA, 1-15m Starter Task,
  PINCH/Effort Pact), Environmental Containment, and Guillotine Hard Stop (#SAVESTATE
  + Somatic Switch).'
type: protocol
status: draft
created: 2026-11-17 10:12:30+00:00
modified: 2026-11-17T10:16:48+00:00
tags:
- agent/chief-of-staff
- domain/prodos
- type/protocol
conformant: true
permalink: llmeon/10-system/prompts/protocol-engage-action-prosthetic-timebox-somatic-switch
---

> [!warning] Own-words guard
> Never edit, merge into, rename, move, or delete a protected note, and never set or change `own_words` ([[AGENTS]] §6). Protected notes are any note with `own_words: true` and every existing note in `01_journals/` and `20_Thinking/`. Put any suggestion for a protected note in chat or in a new `00_Inbox/` note. This overrides any instruction below.

> Trigger: `/engage-action`, "start timebox", "I'm stuck on this ticket", or "time's up / switch". For full-day macro scheduling, use [[Protocol - Daily Plan (Todoist Timeboxing)]].

> Output Contract: follow [[Protocol - Typed Answer Contract (TAC) for Vault Agents]]—confidence, evidence (linked source notes), and an explicit uncertainty flag replace free prose in every output.

## Phase 1: Pre-Flight Negotiation (The Task-Authoring Gate)

Refuse to start the timer until the user defines all three of the following:

1. **`Done means:`** The single visualisable, "acceptable rather than perfect" artifact achievable within `15m`, `30m`, or `60m`. If the proposed scope is too broad for the chosen box, slice it down before proceeding.
2. **`Steps (Two-Tier Ignition):`**
   - **(a) MVA (<120s):** A concrete bodily action taking under 120 seconds, paired with a binary Yes/No completion check.
   - **(b) Starter Task (1–15m):** The immediate momentum ramp following the MVA.
3. **`If stuck (PINCH + Effort Pact):`**
   - Select one PINCH catalyst (*Play, Interest, Novelty, Competition, Hurry*).
   - Confirm external triggers are blocked (notifications silenced, distracting tabs/apps closed) and the active Todoist timebox (`https://app.todoist.com/app/task/<task-id>`) is open with the timer running.

## Phase 2: In-Box Containment (Urge Surfing)

Once the timer is running, hold the boundary:

- Instruct the user that if an internal trigger (boredom, uncertainty, perfectionism) or a rabbit-hole urge fires during the box, they must **not** follow it.
- Instead, dump a 1-line capture note into `00_Inbox/` (or a `HEAD - ...?` candidate) and immediately return to the current box until the timer rings.

## Phase 3: The Guillotine (`On stop` / Box Exit & Somatic Switch)

When the timer rings, mandate an immediate hard stop—no silent overrun—and force one of three choices:

1. **Ship It:** Mark the task complete in Todoist.
2. **Extend Once (Conscious Trade-off):** Add one bounded `15m` or `30m` box *only* after explicitly naming which block comes off today's schedule.
3. **Park It (`#SAVESTATE`):** Write a 1-sentence state capture plus the next `<120s` MVA into the task comment/note so working memory can release the loop.

### Mandatory Somatic Switch

Before starting the next block, prescribe an immediate **60-second physical reset** (isometric hold, balance exercise, or hydration walk) to clear attention residue and re-engage the Task Positive Network (TPN).

## Related

- [implements:: [[SoT - Temporal Management (Blocking and Boxing)]], confidence=high]
- [implements:: [[SoT - PRODOS Core Specification]], confidence=high]
- [depends_on:: [[SoT - The Cognitive Physiology of Task Execution]], confidence=high]
- [extends:: [[Protocol - Daily Plan (Todoist Timeboxing)]], confidence=high]