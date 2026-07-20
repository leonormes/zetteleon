---
created: 2026-04-24T07:22:57+00:00
modified: 2026-07-20T16:34:19+00:00
permalink: llmeon/30-library/200-projects/cuh-omop-database-slow-for-cohort-discovery-queries
project_category: omop
project_name: OMOP
project_status: active
title: CUH OMOP database slow for cohort discovery queries
type: null
---

Based on your long-term memories, the strongest evidence is the Mail thread you were viewing at 8:19 AM today about "RE: CUH OMOP database slow for cohort discovery queries", plus yesterday's related Slack/email activity. I don't see any relevant workspace files in the project context for this, so this summary is based on the email and chat trail.

## Conversation Summary

### What Happened

1. 12:04 PM yesterday (Thu 23 Apr)—Ollie emailed Jakub saying HDRUK had alerted FITFILE that cohort discovery queries were timing out, and that from the bunny logs the queries appeared to be stuck executing.
2. 12:29 PM yesterday—Jakub replied that nothing was currently running in bunny and suggested the request may have timed out while the web layer was still waiting.
3. 2:10 PM yesterday—Ollie replied that the queries appeared to be resolving, but not within HDRUK's timeout window. He said he had built a dashboard of min/max/avg cohort query response times and believed many queries were taking over 5 minutes. He also asked whether missing OMOP indexes were still an issue.
4. 3:50 PM yesterday—Ollie widened visibility by CC'ing the SDE team.
5. 8:19 AM today (Fri 24 Apr)—Jakub replied agreeing that increasing the timeout would be prudent, and said he had added three "high-value missing indexes" in DEV, with inclusion in the next refresh.

### Current Shared Position

The thread converges on this interpretation:

- There is a real performance issue, not just a false alert.
- The issue is likely a combination of:
  - HDRUK timeout threshold being too low for some cohort queries, and/or
  - database/indexing inefficiency in the CUH OMOP environment.
- Jakub has started remediation by adding targeted indexes.
- Increasing the timeout is being treated as a sensible mitigation, but not the only fix.

---

## Claim Validation

| Claim | Validation | Confidence | Why |
|---|---|---:|---|
| It would be prudent to increase the timeout, as several queries are likely to exceed five minutes. | Supported | High | Ollie previously said many queries were taking over 5 minutes, and Jakub explicitly agrees in his latest email at 8:19 AM today. |
| We have been gathering statistics to ensure the indexes effectively support the specific query patterns. | Plausible but not independently verified | Medium | This is Jakub's direct statement. I don't see separate evidence of the statistics themselves in the provided context, but it is consistent with the surrounding discussion. |
| Three new "high-value missing indexes" have been added. | Directly supported | High | The email lists the exact `CREATE INDEX` statements. |
| Those indexes should improve performance. | Technically reasonable, not yet proven | Medium | The indexes align with common OMOP query patterns using `*_concept_id` filters and returning `person_id`/visit/date fields, but no before/after metrics are provided yet. |
| There is no guarantee the optimiser will select them every time. | Technically correct | High | That is true in general for SQL Server query optimisation; index presence does not guarantee selection on every execution plan. |
| The indexes have been applied to DEV and will be included in the next refresh. | Directly supported, operationally unverified | High / Medium | High that Jakub said it; medium that the deployment has actually occurred, because we only have the email statement, not environment confirmation. |

---

## Important Nuance / Caveats

### 1. The "5 Minute Timeout" is Still Slightly Soft

Ollie wrote "I think HDRUK set a 5 minute timeout". That means the exact timeout value is likely 5 minutes, but in this thread it isn't evidenced by HDRUK config or documentation directly.

Best wording:

- "There appears to be a 5-minute HDRUK timeout"
rather than
- "HDRUK definitely enforces a 5-minute timeout."

### 2. The Dashboard Evidence Should Be Treated Carefully

Yesterday you were also reviewing logs/dashboards around this issue, and there was some evidence earlier that dashboard calculations needed care. So Ollie's "majority over 5 minutes" point is directionally credible, but it would still be wise to spot-check raw request IDs/logs rather than rely only on the aggregate panel.

### 3. The New Indexes May only Fix part of the Problem

The added indexes cover:

- `measurement.measurement_concept_id`
- `condition_occurrence.condition_concept_id`
- `visit_occurrence.visit_concept_id`

That is helpful, but your earlier bunny log examples also showed queries touching multiple OMOP domains such as:

- `observation`
- `drug_exposure`
- `procedure_occurrence`

So this is a good step, but not necessarily the full indexing set needed for all cohort patterns.

---

## Practical Interpretation

A fair, evidence-based reading is:

> The timeout issue is real. Queries are not consistently failing outright; rather, they are often completing too slowly for the current web/HDRUK timeout budget. Jakub has acknowledged that longer timeouts are sensible and has begun targeted DB optimisation by adding three new indexes in DEV. This should help, but the improvement is not yet empirically validated.

---

## Clean Validated Summary You Could Reuse

Here's a tighter version you can paste internally:

> Summary:
> Ollie raised the issue with Jakub after HDRUK reported cohort discovery timeouts. Initial investigation suggested bunny was receiving/executing requests, but responses were not completing within the current timeout window. Ollie's follow-up indicated that queries appear to resolve, but often take longer than the likely 5-minute HDRUK timeout. He also raised the possibility that missing OMOP indexes were contributing.
>
> In his latest reply at 8:19 AM today, Jakub agreed that increasing the timeout would be prudent and confirmed he has added three new "high-value missing indexes" in DEV, to be included in the next refresh.
>
> Validated points:
> - There is a genuine query latency issue.
> - Increasing the timeout is a reasonable mitigation.
> - Three new indexes have been added in DEV.
> - Those indexes are technically appropriate for the cited query patterns, though their real-world impact is not yet proven.
> 
> Caveat:
> The exact HDRUK timeout value and the "majority over 5 minutes" claim are credible but should still be verified against raw metrics/config rather than treated as fully closed facts.

If you want, I can also turn this into:

1. a reply email to Ollie/Weronika, or
2. a Jira comment / incident note format.
