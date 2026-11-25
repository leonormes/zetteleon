---
aliases:
  - ADHD Lab
  - ADHD Strategy Experiments
  - Protocol Testing
conformant: true
created: 2025-12-16T12:00:00+00:00
entry_points:
  - "[[HEAD - Do 75m Deep Dive Sessions Outperform Granular Next Actions for ADHD?]]"
  - "[[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]]"
  - "[[The Clarification Ritual (Stuff to Action)]]"
  - "[[Chaining Starter Tasks Creates a Momentum Ramp]]"
  - "[[SoT - ADHD Neurology & Core Concepts]]"
  - "[[Protocol - Weekly Command Centre]]"
modified: 2026-11-18T06:55:13+00:00
permalink: llmeon/30-library/mo-c/moc-adhd-experiments-protocols
status: evergreen
tags:
  - experiments
  - hypothesis
  - prodos/moc
  - protocols
  - TheHuman/Health/ADHD
  - topic/productivity
  - type/moc
title: MOC - ADHD Experiments & Protocols
type: map
---

## 1. The Laboratory Mandate

> [!abstract] Reality as a Unit Test
> A note in the vault is useless until it is tested in reality. We do not collect "good ideas"; we curate validated protocols.
>
> Lifecycle in ProdOS:
> `Candidate (Draft Claim/Procedure) -> Active Experiment (HEAD Question in 20_Thinking/21_Workbench/) -> Outcome (Stable Claim/Evidence or Protocol) or Retired (Archived/Superseded)`

---

## 2. The CoS-Integrated Experiment Loop

Instead of a standalone 1-week manual logging ritual, experiments plug directly into existing Chief of Staff (CoS) and Weekly Command Centre loops:

1. **Frame (`HEAD` Question):** Promote a candidate idea to a `HEAD - <question>?` (`type: question`, `status: open`, `tags: [experiment, TheHuman/Health/ADHD]`) in `20_Thinking/21_Workbench/` with a `## What Would Settle It` section. CoS (`work-review-launchpad`) and `02_bases/Thinking.base` surface it automatically.
2. **Execute (Todoist Runway):** Schedule a single `<=15m` physical-verb starter or `/daily-plan` timebox in Todoist. Do not maintain a daily results table in Zettelkasten.
3. **Close (Weekly Command Centre / Daily Note):** Capture any raw observation in `01_journals/Dailies/` or as the single *One Friction Fix* line in Friday's `[[Protocol - Weekly Command Centre]]` (Move 4). When settled, promote the finding to a `claim`/`evidence` or `protocol` (`status: seed` → `evergreen`), mark the `HEAD` note `status: resolved`, and archive via `[[Protocol - Workbench Compliance Sweep]]`.

---

## 3. Active Experiments (The Workbench)

_Open `HEAD` questions in `20_Thinking/21_Workbench/` surfaced by CoS and `Thinking.base`._

```base
filters:
  and:
    - 'file.inFolder("20_Thinking/21_Workbench")'
    - 'type == "question"'
    - 'status == "open" || status == "thinking"'
    - 'tags.contains("TheHuman/Health/ADHD") || tags.contains("experiment")'
views:
  - type: table
    name: Active Experiments
    order:
      - file.name
      - status
      - closing_condition
      - file.mtime
    sort:
      - property: file.mtime
        direction: DESC
```

---

## 4. Candidate Ideas & Hypotheses (The Backlog)

_Draft notes in `30_Library/100_zettelkasten/` tagged `hypothesis` or `experiment` awaiting promotion to a `HEAD` test._

```base
filters:
  and:
    - 'file.inFolder("30_Library/100_zettelkasten")'
    - 'status == "draft"'
    - 'tags.contains("hypothesis") || tags.contains("experiment")'
views:
  - type: table
    name: Candidate Hypotheses
    order:
      - file.name
      - type
      - status
      - file.mtime
    sort:
      - property: file.mtime
        direction: DESC
```

---

## 5. Active & Validated ADHD Protocols & SoTs

_Stable or evergreen `protocol`, `sot`, and `procedure` notes for `TheHuman/Health/ADHD`._

```base
filters:
  and:
    - 'type == "protocol" || type == "sot" || type == "procedure"'
    - 'tags.contains("TheHuman/Health/ADHD")'
    - 'status == "stable" || status == "evergreen"'
views:
  - type: table
    name: Validated Protocols & SoTs
    order:
      - file.name
      - type
      - status
      - file.mtime
    sort:
      - property: type
        direction: ASC
      - property: file.name
        direction: ASC
```

---

## 6. Retired & Superseded (The Graveyard)

_Archived or superseded ADHD/experiment notes retained for historical reference._

```base
filters:
  and:
    - 'status == "archived" || status == "superseded"'
    - 'tags.contains("TheHuman/Health/ADHD") || tags.contains("experiment")'
views:
  - type: table
    name: Retired & Superseded
    order:
      - file.name
      - type
      - status
      - superseded_by
    sort:
      - property: file.mtime
        direction: DESC
```

---

## 7. Tracked Experiments & Core References (Graph Entry Points)

- [[HEAD - Do 75m Deep Dive Sessions Outperform Granular Next Actions for ADHD?]]—_Active workbench experiment testing whether 60–75m project blocks outperform granular Next Actions._
- [[Deep Dive Sessions for ADHD (Adapted GTD Next Actions)]]—_Source procedure/proposal for 75m project Deep Dive blocks._
- [[The Clarification Ritual (Stuff to Action)]]—_Candidate 15m daily shutdown clarification ritual._
- [[Chaining Starter Tasks Creates a Momentum Ramp]]—_Candidate claim on chaining micro starter tasks to build initiation momentum._
- [[SoT - ADHD Neurology & Core Concepts]]—_Canonical synthesis of ADHD neurology and cognitive mechanisms._
- [[Protocol - Weekly Command Centre]]—_10-minute Friday review floor whose Move 4 ("One Friction Fix") feeds experiment closure._
