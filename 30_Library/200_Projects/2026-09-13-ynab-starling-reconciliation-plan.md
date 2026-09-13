---
project_category: finance
project_name: YNAB / Starling Reconciliation
project_status: active
revision: 1
status: draft
tags:
- ynab
- starling
- finance
- budgeting
title: 2026-09-13-ynab-starling-reconciliation-plan
permalink: llmeon/30-library/200-projects/2026-09-13-ynab-starling-reconciliation-plan
---

## Context

Starling bank connections were recently re-enabled after a period of drift. This note captures the current state of the YNAB account (pulled live via the API on 2026-09-13, read-only) and a phased plan to bring it back in line.

**Access used:** YNAB personal access token from 1Password (`op://Private/YNAB PAT/credential`), called directly against `https://api.ynab.com/v1` (note: the API now calls budgets "plans" — `/plans`, `/plans/{plan_id}/accounts`, etc. — a rename since earlier docs). No YNAB MCP/integration tool exists in this environment; all calls were manual `curl` + `op read`, read-only. **Bank-feed linking itself (OAuth handshake with Starling) is not exposed via the API at all — that step has to happen in the YNAB app/website, not here.**

## Findings

### Plan (budget) sprawl
7 plans exist on the account; 5 are archived, evidence of a repeated abandon-and-restart pattern:

| Plan | Status | Last modified |
|---|---|---|
| Oct25 | **active** | 2026-09-13 (today) |
| MeMyself&I | not archived, but orphaned | 2024-08-08 |
| August25 | archived 2025-10-06 | 2025-10-06 |
| This one will work 2025 | archived 2025-08-11 | 2025-10-06 |
| Jan25 | archived 2025-02-12 | 2025-11-21 |
| June 24 | archived 2024-11-23 | 2025-10-07 |
| Nov24 | archived 2024-12-29 | 2024-12-29 |

`Oct25` is the live budget. `MeMyself&I` holds one stray "Personal" checking account (£287.32, never reconciled, untouched since Aug 2024) — looks abandoned rather than in active use.

### Bank-feed (direct import) status in Oct25
Only **2 of 3** personal checking accounts are currently linked to a bank feed:

| Account | Linked? | Last reconciled | Latest txn |
|---|---|---|---|
| Starling Joint | ✅ linked, no error | 2026-02-03 | 2026-09-13 (today) |
| Zofja Personal – 8872 | ✅ linked, no error | 2025-12-21 | 2026-09-12 |
| **Leon Personal – 9262** | ❌ **not linked** | 2025-12-19 | 2026-08-29 (~2 weeks stale) |

→ This is almost certainly the account still needing its Starling connection re-established.

### Transaction backlog
- **1,719** unapproved transactions
- **539** uncategorized transactions
- Oldest unapproved transaction dates back to **2026-05-18** — roughly 4 months of backlog

### Budget health (current month, Sept 2026)
- To-be-budgeted: **−£14,381.56** (deep negative — assigned amounts badly out of sync with actual spend)
- **32 categories** currently overspent
- Age of money: 0

### Other accounts on Oct25
Closed (£0, no action expected): Pearl, Rae, Bessie, MBNA.
Off-budget debt/loan tracking accounts with old or no reconciliation dates: Mortgage, Car Loan, America, Zofja Tax, MBNA Payoff, Leon Klarna, Zofja Klarna, PayPal Credit Card, Leon Glasses, Zofja Glasses, Car Tyre — several have never been reconciled (`last_reconciled_at: null`).

## Plan

- [ ] **0. Confirm scope** — treat `Oct25` as the one true budget going forward. Decide whether `MeMyself&I`'s single account/balance is still needed; if not, archive that plan.
- [ ] **1. Reconnect Leon Personal – 9262 to Starling** — done in the YNAB app/website (Accounts → link account → Starling OAuth); not possible via API. Confirm afterwards that `direct_import_linked` flips to `true` with no `direct_import_in_error`.
- [ ] **2. Sanity-check the two already-linked feeds** — Starling Joint and Zofja Personal – 8872 currently show no errors; re-check after step 1 in case relinking one account disrupts the Starling-side authorisation for the others (has happened with multi-account bank apps before).
- [ ] **3. Clear the transaction backlog in monthly batches**, oldest first (starting 2026-05), rather than one 1,719-row sweep — approve + categorize a month at a time and check in before moving to the next, so a bad categorization pass is easy to spot and undo.
- [ ] **4. Reconcile every open on-budget account** against actual Starling/bank statement balances once the backlog is cleared — balances may have drifted while the personal account's feed was down.
- [ ] **5. Repair the budget** — once transactions are categorized and accounts reconciled, true up September's assignments to clear the −£14,381.56 to-be-budgeted figure and resolve the 32 overspent categories.
- [ ] **6. Structural cleanup** — archive `MeMyself&I` (if step 0 confirms it's dead), spot-check the closed accounts stay at £0 with no phantom transactions, and scan payees for duplicates a Starling reimport commonly creates (e.g. "TESCO" vs "Tesco Stores Ltd").
- [ ] **7. Prevent re-drift** — 7 plan restarts in under 2 years suggests the review cadence isn't sticking. Consider a short recurring check-in (e.g. weekly 10-minute inbox clear) tracked in Todoist rather than relying on memory.

## Open questions

- Is `MeMyself&I` actually dead, or is there a reason it's been left un-archived?
- Any known reason Leon Personal – 9262 lost its Starling link specifically (app permission revoked, Starling-side token expiry, deliberate disconnect)?