---
created: 2026-05-01 02:26:00+00:00
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
title: 2026-05-01-pieces-terraform-backup-module-review
permalink: llmeon/raw/2026-05-01-pieces-terraform-backup-module-review
---

## Pieces LTM Capture—Terraform Backup Module Review

Captured: 2026-04-30T10:34:47Z to 2026-04-30T10:35:50Z

---

### Asset 1 (464355f2-7b36-4546-889d-0d111422acdf)—2026-04-30T10:34:47Z

```
give me a llm prompt for my ide to review the terraform backup module and work out what needs to change. What do we already have, what needs updating and what needs adding in order to automate the backup we implemented via az cli
```

---

### Asset 2 (4fbea6fd-4068-4046-8517-40bfd58d993f)—2026-04-30T10:35:13Z

```
Crafting an LLM Prompt for Terraform Automation

I'm focusing on creating a well-structured LLM prompt for the user to review their Terraform backup module. The prompt will include sections for the goal, input files, and expected output, such as a structured plan and a checklist of changes. I'll reference relevant long-term memories, including existing modules for Azure Backups, specifically FTFL-596 and FTFL-615. The user is looking to understand what exists and what updates are needed for automation via Terraform.
```

---

### Asset 3 (a57f64c3-0ae1-4038-8ca4-963bba70b8bf)—2026-04-30T10:35:15Z

```
Creating a Terraform Prompt for Backup Automation

I'm working on a prompt that summarizes the current backup architecture, detailing elements like private endpoints, storage accounts, and RBAC roles. The objective will be to create an action plan that lists existing components in the Terraform backup module and identifies gaps to automate the existing CLI process. I need to mention constraints like Azure provider versions and idempotency. Finally, the prompt will guide the user to input relevant Terraform module paths or provide a list of files.
```

---

### Asset 4 (588b1723-a6f7-45d7-a381-e7730999559c)—2026-04-30T10:35:17Z

```
Structuring the Terraform Response

I'm focusing on how to present the output in a structured format. I want to include sections like the current state inventory, gaps, proposed changes including new resources, and a migration plan with implementation steps. I'll add Terraform code snippets in pseudo-HCL blocks since technical content allows that formatting. It would also be helpful to map each component to tasks from FTFL-596 and FTFL-615 and include acceptance criteria and tests. Finally, I'll reference long-term memories with appropriate hyperlinks, following the guidelines for citations.
```

---

### Asset 5 (ce33a0b8-d422-4f37-b643-441c25b12a05)—2026-04-30T10:35:29Z

```
Including Placeholders and References

In the prompt, I can add placeholders for links to Jira tickets or Azure documentation, which will be useful for the user. For example, I can include citations like [FTFL-596](https://fitfile.atlassian.net/browse/FTFL-596) and [FTFL-615](https://fitfile.atlassian.net/browse/FTFL-615), as well as links to relevant Azure docs. I should also suggest annotating times using 12-hour formats based on memories. My focus will be on delivering the prompt as a code block—potentially in triple backticks—without producing the final plan results.
```

---

### Asset 6 (044c1ba4-b38b-4716-955c-bb6e86767c66)—2026-04-30T10:35:31Z

```
Drafting the Terraform Prompt

I'm using the provided context to guide the user. I'll reference the memory, including details like 1.26 TB unprotected storage and 9 components such as DNS, vaults, and RBAC. Each item will require naming, type, current state in Terraform, proposed state, delta, and an HCL snippet. I'll instruct generating a "Patch diff" in a "git apply friendly patch" style and remind them not to create unknown resources. The output will be bullet-listed and can include optional examples. I'll incorporate relevant links for FTFL tickets and Azure documentation while keeping everything concise since the user asked for just the prompt.
```

---

### Asset 7 (1293bd24-54eb-4d21-9746-ef947bce9ca6)—2026-04-30T10:35:50Z

```
Message Saved As Workstream Summary
```