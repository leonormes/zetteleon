---
aliases: []
confidence:
created: 2025-12-09T10:21:37Z
epistemic:
last_reviewed:
modified: 2025-12-09T10:59:11Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status: active
tags:
  - auth0
  - ffapp-4541
  - jira
  - spicedb
  - state/thinking
title: HEAD - FFAPP-4541 - NNUH Create and configure application users
type: head
uid:
up: "[[00_Workbench]]"
updated:
AoL: Work
---


> [!abstract] The Spark (Contextual Wrapper)
> **Why am I writing this right now?**
> **Jira Ticket:** [FFAPP-4541](https://fitfile.atlassian.net/browse/FFAPP-4541)
> **Summary:** NNUH: Create and configure application users
> **Status:** To Do
> **Assignee:** Leon Ormes

### 🧠 My Current Model (The Blind Write)
*Instructions: Write this section BEFORE looking at documentation. How do you think it works? What is your logic? be messy.*

**I think it works like this:**
- I need to create two new users in Auth0 for NNUH: `mike.shemko@nnuh.nhs.uk` and `ben.goss@nnuh.nhs.uk`.
- I then need to configure their permissions in SpiceDB (our authorization system).
- Both users require the roles: `organisation admin` and `data set manager`.

**I am assuming that:**
- The NNUH tenant/organization already exists in Auth0 and SpiceDB.
- I have the necessary permissions to create users and assign roles in the NNUH environment.
- The role definitions for `organisation admin` and `data set manager` are already established in the schema.
- The email addresses provided are the correct and final ones to be used.

**Technical Details from Ticket:**
- **Emails:** `mike.shemko@nnuh.nhs.uk`, `ben.goss@nnuh.nhs.uk`
- **Required Roles:** `organisation admin`, `data set manager`
- **User Goals:** enable data disclosure, create data schema, authorise data disclosure, upload and manage files.
