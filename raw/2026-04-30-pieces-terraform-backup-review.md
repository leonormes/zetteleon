---
created: 2026-04-30 13:14:00+00:00
modified: 2026-05-26 11:43:52+00:00
pieces_ids:
- 044c1ba4-b38b-4716-955c-bb6e86767c66
- 1293bd24-54eb-4d21-9746-ef947bce9ca6
- 464355f2-7b36-4546-889d-0d111422acdf
- 4fbea6fd-4068-4046-8517-40bfd58d993f
- 588b1723-a6f7-45d7-a381-e7730999559c
- a57f64c3-0ae1-4038-8ca4-963bba70b8bf
- ce33a0b8-d422-4f37-b643-441c25b12a05
source: pieces-ltm
tags:
- pieces
- raw
title: 2026-04-30-pieces-terraform-backup-review
permalink: llmeon/raw/2026-04-30-pieces-terraform-backup-review
---

## Session Capture: 2026-04-30 10:34-10:35

### Asset 1: Initial Request

Pieces ID: 464355f2-7b36-4546-889d-0d111422acdf
Captured: 2026-04-30T10:34:47.979215Z

```
give me a llm prompt for my ide to review the terraform backup module and work out what needs to change. What do we already have, what needs updating and what needs adding in order to automate the backup we implemented via az cli
```

### Asset 2: Crafting LLM Prompt

Pieces ID: 4fbea6fd-4068-4046-8517-40bfd58d993f
Captured: 2026-04-30T10:35:13.051546Z

```
Crafting an LLM Prompt for Terraform Automation

I'm focusing on creating a well-structured LLM prompt for the user to review their Terraform backup module. The prompt will include sections for the goal, input files, and expected output, such as a structured plan and a checklist of changes. I'll reference relevant long-term memories, including existing modules for Azure Backups, specifically FTFL-596 and FTFL-615. The user is looking to understand what exists and what updates are needed for
```

### Asset 3: Creating Terraform Prompt

Pieces ID: a57f64c3-0ae1-4038-8ca4-963bba70b8bf
Captured: 2026-04-30T10:35:15.139829Z

```
Creating a Terraform Prompt for Backup Automation

I'm working on a prompt that summarizes the current backup architecture, detailing elements like private endpoints, storage accounts, and RBAC roles. The objective will be to create an action plan that lists existing components in the Terraform backup module and identifies gaps to automate the existing CLI process. I need to mention constraints like Azure provider versions and idempotency. Finally, the prompt will guide the user to input rel
```

### Asset 4: Structuring the Response

Pieces ID: 588b1723-a6f7-45d7-a381-e7730999559c
Captured: 2026-04-30T10:35:17.147279Z

```
Structuring the Terraform Response

I'm focusing on how to present the output in a structured format. I want to include sections like the current state inventory, gaps, proposed changes including new resources, and a migration plan with implementation steps. I'll add Terraform code snippets in pseudo-HCL blocks since technical content allows that formatting. It would also be helpful to map each component to tasks from FTFL-596 and FTFL-615 and include acceptance criteria and tests. Finally, 
```

### Asset 5: Placeholders and References

Pieces ID: ce33a0b8-d422-4f37-b643-441c25b12a05
Captured: 2026-04-30T10:35:29.367776Z

```
Including Placeholders and References

In the prompt, I can add placeholders for links to Jira tickets or Azure documentation, which will be useful for the user. For example, I can include citations like [FTFL-596](https://fitfile.atlassian.net/browse/FTFL-596) and [FTFL-615](https://fitfile.atlassian.net/browse/FTFL-615), as well as links to relevant Azure docs. I should also suggest annotating times using 12-hour formats based on memories. My focus will be on delivering the prompt as a cod
```

### Asset 6: Drafting the Prompt

Pieces ID: 044c1ba4-b38b-4716-955c-bb6e86767c66
Captured: 2026-04-30T10:35:31.375545Z

```
Drafting the Terraform Prompt

I'm using the provided context to guide the user. I'll reference the memory, including details like 1.26 TB unprotected storage and 9 components such as DNS, vaults, and RBAC. Each item will require naming, type, current state in Terraform, proposed state, delta, and an HCL snippet. I'll instruct generating a "Patch diff" in a "git apply friendly patch" style and remind them not to create unknown resources. The output will be bullet-listed and can include optio
```

### Asset 7: Ready-to-Use LLM Prompt

Pieces ID: 1293bd24-54eb-4d21-9746-ef947bce9ca6
Captured: 2026-04-30T10:35:50.141517Z

```
Here is a ready-to-use LLM prompt you can paste into your IDE. It's designed to have an LLM review your Terraform backup module and produce a concrete plan for automating the Azure AKS backup we implemented via the az dataprotection CLI, including what exists, what to update, and what to add.

```text
You are an infrastructure-as-code (IaC) and Azure backup expert. Your mission is to audit an existing Terraform backup module and produce a precise, implementable plan to automate the Azure AKS bac
```