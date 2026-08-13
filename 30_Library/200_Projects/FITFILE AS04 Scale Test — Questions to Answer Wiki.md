---
created: 2026-07-13T15:45:51+00:00
modified: 2026-08-13T10:53:20+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-13-2026-4-45pm-1
tags: [2, 4]
title: FITFILE AS04 Scale Test — Questions to Answer Wiki
type: note
---

## FITFILE AS04 Scale Test—Questions to Answer Wiki

This is a working wiki to resolve the ambiguity in the AS04 - Perform Scale Test requirement, pulling together the Teams thread interpretation debate with what's already documented in your LTM (Confluence design docs, Jira, and Laura Clarke's review email).

### The Requirement, Verbatim

> "Execute a scale test with synthetic data generating a project cohort from five or more data providers, where at least two have OMOP measurement tables with 500 million rows or more."

This sits inside the [FITFILE Stress Testing Synthetic Data Strategy](https://fitfile.atlassian.net/wiki/spaces/~712020a5830ffled484bb2b0dd9c7abeba35d0/pages/2896068618/FITFILE+Stress+Testing+Synthetic+Data+-+version+1.1.0) document (version 1.1.0), whose background states it "outlines FITFILE's planned approach to stress testing a scaled-up system in accordance with the parameters agreed with the EE SDE using synthetic data… focuses on the implementation strategy for AS04… AS05 remains the reference point for next steps once stress testing is complete."

### Open Questions the Team is Trying to Resolve (From tOday's tEams tHread)

1. Does "500 million rows" describe the source data at the node, or the extract size?
   Today's thread converges on: source data. The recurring articulation is `"Two of the data providers must have 500m rows in their source data (before query)"` and `"The extract can contain less than 500m rows — otherwise the query has to be 'all rows'"`. One participant states it most explicitly: `"the 500 million rows describes the source data at the nodes, not the extract size. So the extract can contain less records based on the cohort we will select. The 500M figure is a scale constraint on the synthetic data, not on what gets pulled out."`

2. What defines a "reasonable" extract query, since AS04 doesn't specify extract size?
   This is flagged directly: `"it's the 'reasonable query' bit we are trying to define?"` and `"IMHO it is one that either we have seen before; or that has reasonable outputs — or this forms the expectation of 'scale'"`. This is the single largest unresolved gap blocking query design.

3. Does AS04 require extracting tables beyond `measurement` (`observation`, `condition_occurrence`, `drug_exposure`, etc.)?
   The thread's answer: `"The extract does not define how many measurements it should include, or any other table."`—i.e. AS04 as worded is silent on this; it isn't excluded, just unspecified.

4. What's a realistic extract size per cohort tier (100K / 500K / 1M)?
   Directly blocking query design per the thread: `"without knowing what a realistic extract is for each size of cohort we are testing (100K, 500K, 1M), I can't properly design the queries."` The distinction being drawn: source-data size stresses the _database_ (query processing load); extract size is what stress-tests the FITFILE system itself (downstream ingestion/transfer).

5. Is Synthea's US-basis a real risk for a UK stress test?
   Per Laura Clarke's email (relayed in the thread): `"Keiran has left a comment asking how you will ensure the synthetic data is realistic for UK data, as Synthea is primarily a US-based resource. It would be great to understand how we ensure the data scale matches expected distributions."` The team's counter-position in the thread: `"Keiran's point about Synthea being US-based shouldn't be a problem under the context of stress testing,"` citing [this JAMIA article on the Synthea dataset generation methodology](https://academic.oup.com/jamia/article/25/3/230/4098271).

6. Should the team ask SDE directly to clarify "the numbers"?
   Still open—`"Let me know if we want to ask SDE anything regarding the 'numbers'"`—with a caveat noted: `"I know Robin said no on Thursday but floating this"`, implying Robin Mofakham previously pushed back on escalating to SDE for clarification.

### What LTM Already Tells Us about the Numbers in Play

Cross-referencing the live debate against artifacts already in your workstream memory:

- Stress test scale parameters (from a shared browser session on the [FFNode Stress Testing Design](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281?assignee=633ae2b9fedc6169aed8f601) page, `Oliver Rushton, Robin Mofakham, Weronika Jastrzebska` chat, 9 Jul): `2.7M patients (584M measurements)`, with `person_source_value` overlap set at `9% overlap with 2 or more hospitals, 1.35% three or more`.
- Permutation grid for cohort/extract testing: `Cohort size: 100K, 500K, 1M`, `Number of nodes: 1, 3, 5`, `Privacy: ON/OFF`, results sent to S3. This aligns exactly with the "100K, 500K, 1M" tiers referenced in today's thread as the cohort sizes needing realistic extract-volume estimates.
- FFNode Stress Testing Design Document v5 describes a "structured subset of the 432-case grid" across six variable dimensions: C (Cohort size: 100k/500K/1M), S (Selection scope: S1/S2/S3), E (Extract cap: Uncapped), P (Privacy treatment On/Off), S3 (S3 export On/Off), L (Linkage scenario). Notably, this doc states `"Variable E (Extract cap — Capped) is not independently exercised by any wave… under Position B (stop at AS05) the primary concern is uncapped query performance."` This is a documented design decision that may directly resolve open question 4—worth surfacing to the thread.
- Jira `FTFL-728` ("Phase 0c: Cohort Design + Creation for Permutation Parameters") ties cohort design work explicitly to "the C (Cohort size) dimension of the six-variable permutation grid defined in the FFNode Stress Testing Design Document v5 §8.1 (FTFL-480)."
- A cost-per-query test-metrics table already exists in the v1.1.0 doc, e.g. `ABC.01 | 3m 54s | 500k patients, 2m related records | 1 Node, 62% CPU, 47% Mem, 20GB Disk | €3.17`, `ABC.02 | 8m 12s | 800k patients, 5m related records | …`—this is direct precedent for what "reasonable" extract volumes have looked like historically, relevant to question 2.
- Test runner status: per today's message, `"Currently, I'm working on the test runner. Once we have this working, we can run a few queries and I can show you rough volumes we are getting in the extract."`—the concrete unblock for question 4 is in progress but not yet delivered.

### Governance / Timeline Context

Per Laura Clarke's email today (`laura.clarke@healthinnovationeast.co.uk`, 13 Jul 15:00, subject "Node testing"): she added `20260710_FITFILEStressTestingSynthData_v1.1.17.docx` to SharePoint for review, noted Keiran's comment on Synthea realism, and flagged `"The Data team will aim to review this document by the end of next week, but depending on progress with MKUH and NNUH, there may be a delay."` This puts a soft external deadline on resolving these interpretation questions—the review clock is already running on a document version (`v1.1.17`) that may not yet reflect today's clarified interpretation.

### Recommended next Actions (Synthesized, not yet dEcided by the tEam)

- Formalize the agreed interpretation (source-data-scale, not extract-scale) back into the v1.1.0/v1.1.17 doc so it isn't re-litigated at each review.
- Cross-check whether FFNode Design Doc v5's "Extract cap: Uncapped" decision already answers the "what's a reasonable query" question, or whether AS04 needs its own explicit extract-size definition distinct from the v5 permutation grid.
- Wait on Oliver Rushton's test runner output for concrete extract volumes at 100K/500K/1M before finalizing query design—this is the fastest path to an evidence-based answer to question 4.
- Resolve internally (per Robin's Thursday position) before deciding whether to escalate "the numbers" to SDE—the thread suggests this is still contested, not settled.
- Decide whether to respond to Keiran's Synthea/UK-realism comment with the JAMIA methodology citation as-is, or supplement it with FITFILE's own distribution-matching evidence, given Laura's email frames it as an open governance question, not just a technical one.
