---
title: Agent Review Queue
created: 2026-06-29 00:00:00+00:00
modified: 2026-06-29 00:00:00+00:00
tags:
  - system
  - agents
  - inbox
type: index
permalink: llmeon/00-inbox/agent-review-queue
---

# Agent Review Queue

Open this at the start of a thinking session. Two sections: things that need a decision from you, and things Hermes touched recently that you may want to promote or discard.

---

## Claim stubs awaiting your review

These were proposed by Hermes during Ingest. Each needs you to fill in `falsifiers`, `crux`, `confidence`, and `counter_positions` before it can be promoted to `30_Library/`.

```dataview
TABLE
  claim_statement AS "Statement",
  steel_man AS "Steel man",
  source_raw AS "Source"
FROM "raw/proposed-claims"
WHERE type = "claim-stub" AND status = "proposed"
SORT file.mtime DESC
```

---

## Recent wiki updates (last 7 days)

Agent-maintained dossiers and concept pages touched in the last week. Scan for anything worth promoting to a `30_Library/SoT/` note or linking into the zettelkasten.

```dataview
TABLE
  file.mtime AS "Modified",
  wiki_type AS "Type",
  entity_kind AS "Kind"
FROM "wiki"
WHERE file.mtime >= date(today) - dur(7 days)
  AND file.name != "README"
  AND file.name != "index"
SORT file.mtime DESC
```

---

## How to act on a claim stub

1. Open the stub from the table above.
2. Fill in `falsifiers` — what evidence would make this wrong?
3. Fill in `crux` — the single load-bearing assumption.
4. Add `confidence: <0–100%> as of <date>` to frontmatter.
5. Change `status: proposed` → `status: reviewed`.
6. If the claim holds up: copy it to `30_Library/100_zettelkasten/Claim - <title>.md`, set `type: claim`, add typed links (`related_to`, `contrasts_with`).
7. Delete or archive the stub in `raw/proposed-claims/`.