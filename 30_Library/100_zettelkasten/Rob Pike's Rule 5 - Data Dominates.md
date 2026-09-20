---
conformant: true
created: 2026-09-19T15:24:45+00:00
created_utc: 2026-09-19 00:00:00+00:00
modified: 2026-09-19T15:44:42+00:00
permalink: llmeon/00-inbox/rob-pikes-rule-5-data-dominates
source_title: "The Conservation of Software Complexity: The Dichotomy of Data Structures and Control Flow (plus epistemic review/fact-check)"
source_url: unknown
status: seed
tags: [data-structures, programming-rules, rob-pike]
title: "Rob Pike's Rule 5 - Data Dominates"
type: claim
upstream: '[[Data Structures vs Control Flow]]'
---

## Rob Pike's Rule 5 - Data Dominates

Rob Pike's fifth rule of programming holds that once the right data structures are chosen and organised well, the algorithms needed to manipulate them are almost always self-evident, so data structures—not algorithms—should be the central design concern.

### Scope & Conditions

From Pike's 1989 "Notes on C Programming"; rules 3–5 address algorithm/data trade-offs.

### Evidence

> "Rule 5: Data dominates. If you've chosen the right data structures and organized things well, the algorithms will almost always be self-evident. Data structures, not algorithms, are central to programming."

### Implications

- Design effort should be front-loaded onto modelling the data correctly rather than onto algorithmic cleverness.

### Related

- [[SoT - The Data-Centric Philosophy]]—direct concept match: cites the identical Pike quote in its "Consensus of the Masters" table (§1).

### Tensions

- [[The Right Data Structure, Not a Smart One, Is Pike's Actual Rule]]—qualifies: Pike's own Rule 4 (simple algorithms _and_ simple data structures) bounds how far this rule should be pushed; see that atom for the falsifier.
