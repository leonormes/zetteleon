---
aliases: [Note Maturity, Status Progression]
confidence: 0.93
created: 2025-10-31T08:20:00Z
epistemic: principle
last_reviewed: 2025-10-31
modified: 2025-11-01T09:43:58Z
purpose: "Defines the lifecycle of a note's status and the criteria for advancement from seedling to evergreen."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [quality, workflow, zettelkasten]
title: Note Status Lifecycle
type: concept
uid: 2025-10-31T08:20:00Z
updated: 2025-10-31T08:20:00Z
---

## Note Status Lifecycle

**Summary:** Each atomic note progresses through three status stages—seedling, growing, and evergreen—based on completeness, integration into the vault, and epistemic confidence.

**Details:**

**Seedling:** Initial state for all new notes. A seedling note has a summary and details, but may not be fully integrated or reviewed by the author. LLM-generated notes are always created at seedling status. Seedlings are drafts; they lack the rigor and review of more mature notes.

**Growing:** A seedling becomes growing once it:
- Has a summary (one sentence) and details (2–4 sentences)
- Has at least 1 inbound link from a structural note (evidence of integration)
- Has been reviewed by the author for accuracy and framing

**Evergreen:** A growing note becomes evergreen once it:
- Has at least 2 inbound links from structural notes (evidence of multiple contexts where it is useful)
- Has a clearly articulated `purpose` field
- Has a justified `confidence` score
- Has 1–3 related `see_also` links to other atomic notes
- Has been reviewed within the specified `review_interval`

Evergreen notes are the backbone of a zettelkasten. They are treated as reliable facts, and they appear in queries and MOCs with high confidence.

The `review_interval` field (default 90 days) triggers reminders to revisit notes and confirm their accuracy and relevance remain valid.
