---
created: 2026-02-04T09:12:25+00:00
last-synthesis: 2026-02-04
modified: 2026-05-26T11:44:21+00:00
source_of_truth: true
status: evergreen
synthesis-count: 1
tags: [domain/productivity, tool/jira, type/SoT]
title: Jira Dependency Management SoT
trust-level: stable
---

## Minimum Viable Understanding (MVU)

Native Jira (Cloud) cannot natively filter for "Actionable" tasks (i.e., tasks where all predecessors are `Done`) using standard JQL. While it supports `blocks` / `is blocked by` linking, the search engine cannot query the _status_ of linked issues dynamically. To achieve a "Next Action" view, you must either use Jira Automation to update a custom status field or install Marketplace Apps (e.g., ScriptRunner, JQL Search Extensions).

## Working Knowledge

### 1. The Core Limitation

- Native Links: Jira supports `blocks` links, but they are metadata only. They do not prevent transition or change visibility by default.
- JQL Gap: You can find "tickets that have blockers" (`issueLinkType = "is blocked by"`), but you cannot find "tickets where the blocker is _open_" without extensions.

### 2. The Solution Patterns

#### Pattern A: The Automation Workaround (Zero Cost)

- Mechanism: A custom field (`Action Status`) is updated via Automation Rules.
    - When a link is added → Set status to `Blocked`.
    - When a predecessor closes → Check for other open blockers → If none, set status to `Ready`.
- Pros: Works on all plans, no plugin cost.
- Cons: "Eventual consistency" (slight delay), requires rule maintenance.

#### Pattern C: Terminal UI (Lazyjira)

For high-velocity engineers, the Jira Web UI is often a bottleneck. Lazyjira provides a keyboard-driven interface similar to `lazygit`.

- Mechanism: CLI tool that supports JQL search with autocomplete and vim-style navigation.
- Benefit: Reduces latency for status updates, comment drafting, and JQL experimentation. Allows creating branches directly from issues.
- Usage: `lazyjira` command from the terminal.

### 3. Structural Best Practices

- Customer Actions: Model customer dependencies (e.g., "UAT", "Provide Certs") as separate tickets, not just statuses. This allows them to participate in the dependency chain (`Dev Task` → `Customer Task` → `Deploy Task`).
- Link Direction: Always use `A blocks B` (Predecessor blocks Successor).

## Current Understanding

The user requires a specific protocol for the "Automation Workaround" pattern to enable a GTD-like "Next Actions" list for deployment workflows. This process is codified in [[Protocol - Jira Dependency Configuration]].
