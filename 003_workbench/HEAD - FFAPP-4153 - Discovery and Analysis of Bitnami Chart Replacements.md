---
aliases: []
AoL: Work
confidence:
created: 2025-12-09T00:00:00Z
epistemic:
last_reviewed:
modified: 2025-12-10T20:00:14Z
purpose: Planning and analysis for Jira ticket FFAPP-4153 regarding Bitnami chart replacements.
review_interval:
see_also: []
source_of_truth: []
status: someday
tags: [bitnami, ffapp-4153, head, jira, kubernetes, security]
title: HEAD - FFAPP-4153 - Discovery and Analysis of Bitnami Chart Replacements
type: head
uid:
updated:
---

## The Spark

> [!abstract] The Spark (Contextual Wrapper)
**Jira Ticket:** [FFAPP-4153](https://fitfile.atlassian.net/browse/FFAPP-4153)
**Summary:** Discovery and Analysis of Bitnami Chart Replacements
**Status:** Ready
**Priority:** Low
This ticket was triggered by the need to migrate away from or secure our usage of Bitnami charts.

## My Current Model
**User Story:**
"As a Platform Engineer, I want to identify all Bitnami charts currently in use and research suitable, vetted replacements, so that we can create a clear migration plan that meets our security and automation requirements."

**Context from Comments:**
- There is a discussion about whether we can import the `latest` tag as a specific version into our Azure Container Registry (ACR).
- We need to review all dependencies on Bitnami that are *not* currently within our ACR.
- An RFC has been updated with findings: [RFC Transition from Bitnami Helm Charts](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2296381442/RFC+Transition+from+Bitnami+Helm+Charts+to+an+Alternative+Source#7.-Findings%3A-Status-of-Free-Bitnami-Images-(as-of-%5Bdate%5D))

## The Tension
- **Reliability vs. Freshness:** Bitnami `latest` tags are convenient but unstable for production. Importing them as fixed versions in ACR solves stability but requires a process for updates.
- **Scope of Dependency:** We might have hidden dependencies on Bitnami (transitive dependencies in other charts) that are not immediately obvious.
- **Replacement Viability:** "Suitable, vetted replacements" might not exist for everything. We may need to build our own or use vendor-official charts which might lack the consistency of Bitnami.

## The Next Test (Action)
- [ ] **Action:** Read the linked RFC to understand the current "Findings" section.
- [ ] **Action:** Run a script/command to list all currently deployed Helm releases and grep for `bitnami` to establish the ground truth of usage.
