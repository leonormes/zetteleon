---
aliases: []
confidence: 
created: 2025-12-09T10:58:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-09T10:59:09Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: raw
tags: [backup, cuh, ffapp-4410, jira, state/thinking]
title: HEAD - FFAPP-4410 - Implement CUH data backup
type: head
uid: 
up: "[[00_Workbench]]"
updated: 
---

## HEAD - FFAPP-4410 - Implement CUH Data Backup

> [!abstract] The Spark (Contextual Wrapper)
> **Why am I writing this right now?**
> **Jira Ticket:** [FFAPP-4410](https://fitfile.atlassian.net/browse/FFAPP-4410)
> **Summary:** Implement CUH data backup
> **Status:** Ready
> **Assignee:** Leon Ormes

### 🧠 My Current Model (The Blind Write)
*Instructions: Write this section BEFORE looking at documentation. How do you think it works? What is your logic? be messy.*

**I think it works like this:**
- The CUH (Cambridge University Hospitals) node is currently running without backups.
- If the node fails, we lose configuration state, specifically "configured Data Sources".
- This state is likely stored in a persistent volume or a local database (Postgres?) running on the node.

**I am assuming that:**
- We need to identify *where* this configuration data lives (PVC? DB?).
- The solution will likely involve **Velero** for cluster resource/PVC backups, or a specific database backup script if it's external.
- "CAB/TT" refers to previous Change Advisory Board or Trouble Ticket records that might already authorize or describe this work.
- I need to communicate the window for this work to the client (CUH) as per the comments.

**The Tension:**
- Is this a full node backup or just the application state?
- Do we have a standard backup pattern for these single-node deployments?
- Need to verify if `velero` is already installed or supported in this environment.

**Next Actions:**
- [ ] Check CAB/TT references.
- [ ] Investigate the CUH node storage architecture.
- [ ] Draft email to CUH regarding implementation schedule.
