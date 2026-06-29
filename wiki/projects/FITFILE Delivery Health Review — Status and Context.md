---
title: FITFILE Delivery Health Review — Status and Context
type: report
permalink: llmeon/wiki/projects/fitfile-delivery-health-review-status-and-context
tags:
- fitfile
- delivery
- confluence
- review
---

Working revision of the FITFILE Delivery Health Review Confluence page (page ID 2881290243, https://fitfile.atlassian.net/wiki/x/AwC9qw), incorporating Robin Mofakham's 21 inline review comments and cross-referenced against the underlying FITFILE Value Stream Report (2026-06-20) and the FTFL-512 CI/CD incident investigation.

## Observations

- [status] Draft revision written to wiki/projects/FITFILE Delivery Health Review — Draft Revision (Robin's Comments).md; not yet copied back to Confluence #draft
- [source] Confluence page 2881290243 is the business-facing doc under review; raw data lives in the FITFILE Value Stream Report (2026-06-20) #data-source
- [finding] 0 of 88 merged MRs across `deployment` (59) and `InsightFILE` (29) repos in the 9 May-20 June 2026 window had a human review comment #review-gap
- [finding] InsightFILE's CI pipeline passes only ~52% of the time, dominated by frontend_unit_tests/frontend_lint/verify_ffcloud failures; deployment's CI fails mostly on lint_workflows (86% of its failures) #ci-quality
- [finding] InsightFILE has no real release mechanism (floating latest-release tag only) vs deployment's ~2 semver releases/week — this is the primary shipping bottleneck #release-process
- [finding] Robin's pushback that the backlog is "reasonably sorted" into epics is confirmed by the Value Stream Report (only 2 of 29 epics lack child stories) #confirmed
- [open-question] Robin dislikes the proposed protected-branch-plus-reviewer checkpoint for a small team; no alternative proposed yet #needs-input
- [open-question] Robin's claim that tickets are blocked on "OR" (likely Ollie Rushton) reviewing them isn't supported by aggregate WIP/MR data, but may refer to specific tickets not visible in the aggregates #needs-input
- [incident] FTFL-512: an unreviewed MR (!802) broke ff-test-a staging via an ArgoCD admission-webhook rejection, blocking unrelated deploys for ~8h47m (7h40m of that completely silent, no alert) #incident #grounding

## Relations

- summarizes [[FITFILE Delivery Health Review — Draft Revision (Robin's Comments)]]
- derived_from [[FITFILE Value Stream Report - 2026-06-20]]
- references [[FTFL-512 CI-CD Pipeline Incident Investigation]]
- about_person [[Robin Mofakham]]
