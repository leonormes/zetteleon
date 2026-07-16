---
created: 2026-02-04T09:12:25+00:00
modified: 2026-07-13T08:52:41+00:00
permalink: llmeon/30-library/so-t/protocol-jira-dependency-configuration
related-sot:
- - Jira Dependency Management SoT
tags: [domain/jira, tool/jira, type/protocol]
title: Protocol - Jira Dependency Configuration
type: protocol
conformant: false
non_conformance_reason: "Bulk inferred type. Needs review."
---

## Logic Map

- Objective: Configure Jira to automatically identify and filter for the "Single Next Action" in a dependency chain.
- Constraint: Must work without 3rd party plugins (using Native Automation).
- Dependencies: Project Admin permissions.

## The Algorithm

### 1. Field Configuration

1. Create Custom Field:
    - Type: Select List (Single Choice) or Radio Buttons.
    - Name: `Actionability` (or `Work Status`).
    - Options:
        - `Ready` (Default)
        - `Blocked`
        - `Waiting for Customer`

### 2. Ticket Definition Protocol

When defining work in Jira:

1. Granularity: Create distinct tickets for _every_ handoff, including external ones.
    - _Bad:_ Ticket "Deploy App" with a status "Waiting for Client".
    - _Good:_ Ticket A "Prepare Environment" → Ticket B "Client Provides SSL Cert" → Ticket C "Deploy App".
2. Linking:
    - Use only `blocks` / `is blocked by`.
    - Direction: The task that must happen _first_ `blocks` the task that happens _next_.
    - _Check:_ If Task A stops Task B from starting, `Task A blocks Task B`.

### 3. Automation Logic (The Engine)

Create these two rules in Project Settings > Automation.

#### Rule A: "The Red Light" (Link Created)

- Trigger: Issue linked.
- Condition: Link type equals `is blocked by`.
- Condition: Linked Issue Status Category `!= Done`.
- Action: Edit Issue → Set `Actionability` to `Blocked`.

#### Rule B: "The Green Light" (Blocker Resolved)

- Trigger: Issue transitioned to `Done` (or `Resolved`).
- Branch: For Linked Issues (`blocks` - i.e., the successors).
    - Condition: Linked Issues Match JQL (Check for _other_ remaining blockers):
        - JQL: `issue in linkedIssues("is blocked by") AND statusCategory!= Done`
        - _Check:_ Ensure this returns 0 issues (or use "Does not match").
    - Action: Edit Issue → Set `Actionability` to `Ready`.
    - Action (Optional): Add comment "Dependency resolved. Ready for action."

### 4. The View (Next Actions Filter)

Create a saved filter or board query:

```jql
project = "MYPROJECT" 
AND statusCategory != Done 
AND "Actionability" = Ready 
ORDER BY Priority DESC
```

## Error Handling

- Circular Dependencies: If A blocks B and B blocks A, both will stay `Blocked`. Use the "Dependency Map" view to debug.
- Manual Override: If automation fails, manually toggle `Actionability` to `Ready`.
