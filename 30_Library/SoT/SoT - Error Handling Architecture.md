---
aliases: ["Error Design", "Designing Errors", "The Error Handling Protocol"]
confidence: "High"
created: 2026-01-06
epistemic: "Principle"
last_reviewed: 
modified: 
purpose: "To define Error Handling not as a forwarding mechanism, but as a design discipline centered on communication with two distinct audiences (Humans and Machines)."
review_interval: "1 year"
see_also: 
  - "[[SoT - Rust Type Mechanics]]"
  - "[[SoT - Systems Thinking]]"
  - "[[SoT - Parse, Don't Validate]]"
source_of_truth: []
status: "Active"
tags: ["SoftwareEngineering/Architecture", "error-handling", "observability", "rust"]
title: SoT - Error Handling Architecture
type: "SoT"
uid: 
updated: 
---

# SoT - Error Handling Architecture

> **The Core Thesis:** "Errors are not failure modes to be propagated; they are messages to be designed. If your error type cannot answer 'Should I retry?' you failed the Machine. If your logs cannot answer 'Which user was it?' you failed the Human."

## 1. The Problem: Error Forwarding

We often treat errors like hot potatoes—catch them, wrap them, and throw them up the stack. This preserves the *message* ("JSON error") but loses the *intent* ("Why were we parsing JSON?").

*   **The Log Line at 3 AM:** `Error: expected ',' or '}'`
*   **The Missing Context:** Which user? Which request? Which file?
*   **The Result:** "Error Forwarding" creates systems where the root cause is preserved, but the path to it is lost.

## 2. The Two Audiences

Effective error architecture must satisfy two distinct consumers with opposing needs.

| Audience | Goal | Needs | Architecture Pattern |
|:--- |:--- |:--- |:--- |
| **Machines** | **Recovery** (Retry, Failover) | Flat structure, clear enums, boolean attributes (`is_retryable`). | **Kind-Based Error Types** |
| **Humans** | **Debugging** (Root Cause Analysis) | Rich context, call stacks, business logic path. | **Context Trees** |

## 3. The Architecture Patterns

### A. For Machines: The "Kind" Pattern
Machines hate hierarchy. They do not want to traverse a nested chain of exceptions to find if a database lock occurred. They want a flat, actionable Enum.

*   **Pattern:** `ErrorKind` (Categorized by *Response*, not Origin).
    *   *Bad:* `DatabaseError`, `NetworkError` (Origin).
    *   *Good:* `Transient` (Retry), `Permanent` (Fail), `NotFound` (Ignore), `PermissionDenied` (Escalate).
*   **Result:** The logic becomes `if err.kind() == Transient { retry() }`.

### B. For Humans: The "Context" Tree
Humans need the narrative. We need to know the *logical path* the request took.

*   **Pattern:** **Wrap at the Boundary.**
*   **Rule:** Never propagate an error across a module boundary without adding context.
    *   *Code:* `.or_raise(|| AppError("failed to fetch user {id}"))`
*   **Result:** The error log becomes a story: `Failed to execute Task 123 -> Failed to fetch User 456 -> Connection Refused`.

## 4. Minimum Viable Understanding (MVU)

1.  **Don't Forward, Design:** Treat your `Error` types as part of your public API.
2.  **Separate Concerns:** Use a flat `enum` for logic (Machine) and a nested `context` wrapper for logs (Human).
3.  **The 3 AM Test:** Look at your error log. If it doesn't tell you *who*, *what*, and *why* without opening the code, the error design is broken.

## 5. Related Components
- [[SoT - Rust Type Mechanics]] (Using Enums for Error Kinds).
- [[SoT - Systems Thinking]] (Errors as Feedback Loops).
- [[SoT - Parse, Don't Validate]] (Validation errors are Domain Errors).
