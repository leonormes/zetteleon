---
tags: [type/protocol, domain/jira, tool/jira]
status: active
related-sot: [[Jira Dependency Management SoT]]
---

## Logic Map
*   **Objective:** Configure Jira to automatically identify and filter for the "Single Next Action" in a dependency chain.
*   **Constraint:** Must work without 3rd party plugins (using Native Automation).
*   **Dependencies:** Project Admin permissions.

## The Algorithm

### 1. Field Configuration
1.  **Create Custom Field:**
    *   **Type:** Select List (Single Choice) or Radio Buttons.
    *   **Name:** `Actionability` (or `Work Status`).
    *   **Options:**
        *   `Ready` (Default)
        *   `Blocked`
        *   `Waiting for Customer`

### 2. Ticket Definition Protocol
When defining work in Jira:
1.  **Granularity:** Create distinct tickets for *every* handoff, including external ones.
    *   *Bad:* Ticket "Deploy App" with a status "Waiting for Client".
    *   *Good:* Ticket A "Prepare Environment" → Ticket B "Client Provides SSL Cert" → Ticket C "Deploy App".
2.  **Linking:**
    *   Use **only** `blocks` / `is blocked by`.
    *   **Direction:** The task that must happen *first* `blocks` the task that happens *next*.
    *   *Check:* If Task A stops Task B from starting, `Task A blocks Task B`.

### 3. Automation Logic (The Engine)
Create these two rules in **Project Settings > Automation**.

#### Rule A: "The Red Light" (Link Created)
*   **Trigger:** Issue linked.
*   **Condition:** Link type equals `is blocked by`.
*   **Condition:** Linked Issue Status Category `!= Done`.
*   **Action:** Edit Issue → Set `Actionability` to `Blocked`.

#### Rule B: "The Green Light" (Blocker Resolved)
*   **Trigger:** Issue transitioned to `Done` (or `Resolved`).
*   **Branch:** For Linked Issues (`blocks` - i.e., the successors).
    *   **Condition:** Linked Issues Match JQL (Check for *other* remaining blockers):
        *   JQL: `issue in linkedIssues("is blocked by") AND statusCategory != Done`
        *   *Check:* Ensure this returns **0** issues (or use "Does not match").
    *   **Action:** Edit Issue → Set `Actionability` to `Ready`.
    *   **Action (Optional):** Add comment "Dependency resolved. Ready for action."

### 4. The View (Next Actions Filter)
Create a saved filter or board query:

```jql
project = "MYPROJECT" 
AND statusCategory != Done 
AND "Actionability" = Ready 
ORDER BY Priority DESC
```

## Error Handling
*   **Circular Dependencies:** If A blocks B and B blocks A, both will stay `Blocked`. Use the "Dependency Map" view to debug.
*   **Manual Override:** If automation fails, manually toggle `Actionability` to `Ready`.
