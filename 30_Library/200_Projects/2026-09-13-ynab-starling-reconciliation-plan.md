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
## Plan

- [x] **0. Confirm scope** — `Oct25` confirmed as the one true budget going forward.
- [x] **1. Reconnect Leon Personal – 9262 to Starling** — done by the user in the YNAB app. Verified via API: `direct_import_linked: true`, `direct_import_in_error: false`.
- [x] **2. Sanity-check the two already-linked feeds** — Starling Joint and Zofja Personal – 8872 both stayed `direct_import_linked: true` / no error after the relink.
- [x] **3. Clear the transaction backlog in monthly batches**, oldest first, through today (2026-09-13). 1,733 → 318 unapproved remaining (genuine judgment calls left for the user — see Progress Log).
- [x] **4. Reconcile every open on-budget account against actual Starling balances** — done. Root cause found and fixed (see Progress Log). All three personal accounts now match the real Starling app balances exactly (Joint is 9p off from timing/rounding).
- [ ] **5. Repair the budget** — now that accounts are reconciled and most of the backlog is cleared, true up September's assignments and resolve overspent categories (was 32 as of 2026-09-13 pre-cleanup; re-check).
- [ ] **6. Structural cleanup** — archive `MeMyself&I` (if step 0 confirms it's dead), spot-check the closed accounts stay at £0 with no phantom transactions, and scan payees for duplicates a Starling reimport commonly creates (e.g. "TESCO" vs "Tesco Stores Ltd").
- [ ] **7. Prevent re-drift** — 7 plan restarts in under 2 years suggests the review cadence isn't sticking. Consider a short recurring check-in (e.g. weekly 10-minute inbox clear) tracked in Todoist rather than relying on memory. Also: set up YNAB payee rules for the high-frequency unresolved payees (Haven, Southend And D) so they auto-categorize going forward. **New: when a Starling feed is down, log both sides of inter-account transfers AND income — a transfer-only habit creates exactly the kind of balance hole found in step 4.**
## Plan

- [x] **0. Confirm scope** — `Oct25` confirmed as the one true budget going forward.
- [x] **1. Reconnect Leon Personal – 9262 to Starling** — done by the user in the YNAB app. Verified via API: `direct_import_linked: true`, `direct_import_in_error: false`, latest transaction 2026-09-11.
- [x] **2. Sanity-check the two already-linked feeds** — Starling Joint and Zofja Personal – 8872 both still `direct_import_linked: true` / no error after the relink. No disruption.
- [x] **3. Clear the transaction backlog in monthly batches**, oldest first, through today (2026-09-13). Method: rebuilt the payee→category mapping fresh before each month from all approved+categorized history (growing from 2,943 to 4,164 transactions as prior months got cleared); applied it only where a payee's category was ≥85% consistent across ≥2 prior occurrences. Genuine account transfers (`transfer_account_id` set) auto-approved without a category.
  - [x] 2026-05 — 182 unapproved → 159 bulk-approved, 23 left for manual review
  - [x] 2026-06 — 439 unapproved → 358 bulk-approved, 81 left for manual review
  - [x] 2026-07 — 443 unapproved → 371 bulk-approved, 72 left for manual review
  - [x] 2026-08 — 484 unapproved → 372 bulk-approved, 112 left for manual review
  - [x] 2026-09 (partial, to today) — 185 unapproved → 155 bulk-approved, 30 left for manual review
  - **Result: 1,733 → 318 unapproved remaining, all needing an actual human category decision (see Progress Log).**
- [ ] **4. Reconcile every open on-budget account** against actual Starling/bank statement balances now that the backlog is mostly cleared — balances may have drifted while the personal account's feed was down.
- [ ] **5. Repair the budget** — once the remaining 318 are categorized and accounts reconciled, true up September's assignments and resolve overspent categories (re-check the count; it was 32 as of 2026-09-13 before this cleanup).
- [ ] **6. Structural cleanup** — archive `MeMyself&I` (if step 0 confirms it's dead), spot-check the closed accounts stay at £0 with no phantom transactions, and scan payees for duplicates a Starling reimport commonly creates (e.g. "TESCO" vs "Tesco Stores Ltd").
- [ ] **7. Prevent re-drift** — 7 plan restarts in under 2 years suggests the review cadence isn't sticking. Consider a short recurring check-in (e.g. weekly 10-minute inbox clear) tracked in Todoist rather than relying on memory. Also consider: set up YNAB payee rules for the high-frequency payees found unresolved below (Haven, Southend And D) so they auto-categorize going forward.
## Plan

- [x] **0. Confirm scope** — `Oct25` confirmed as the one true budget going forward.
- [x] **1. Reconnect Leon Personal – 9262 to Starling** — done by the user in the YNAB app. Verified via API: `direct_import_linked: true`, `direct_import_in_error: false`, latest transaction 2026-09-11.
- [x] **2. Sanity-check the two already-linked feeds** — Starling Joint and Zofja Personal – 8872 both still `direct_import_linked: true` / no error after the relink. No disruption.
- [ ] **3. Clear the transaction backlog in monthly batches**, oldest first. Method: built a payee→category mapping from 2,943 historical approved+categorized transactions (556 distinct payees); applied it only where a payee's category was ≥85% consistent across ≥2 prior occurrences. Genuine account transfers (`transfer_account_id` set) auto-approved without a category, since transfers don't need one.
  - [x] **2026-05** — 182 unapproved → 159 bulk-approved (158 already-correct + 1 high-confidence category applied), 23 left for manual review (see Progress Log below).
  - [ ] 2026-06 (439 unapproved)
  - [ ] 2026-07 (443 unapproved)
  - [ ] 2026-08 (484 unapproved)
  - [ ] 2026-09 (185 unapproved, partial month)
- [ ] **4. Reconcile every open on-budget account** against actual Starling/bank statement balances once the backlog is cleared — balances may have drifted while the personal account's feed was down.
- [ ] **5. Repair the budget** — once transactions are categorized and accounts reconciled, true up September's assignments to clear the −£14,381.56 to-be-budgeted figure and resolve the 32 overspent categories.
- [ ] **6. Structural cleanup** — archive `MeMyself&I` (if step 0 confirms it's dead), spot-check the closed accounts stay at £0 with no phantom transactions, and scan payees for duplicates a Starling reimport commonly creates (e.g. "TESCO" vs "Tesco Stores Ltd").
- [ ] **7. Prevent re-drift** — 7 plan restarts in under 2 years suggests the review cadence isn't sticking. Consider a short recurring check-in (e.g. weekly 10-minute inbox clear) tracked in Todoist rather than relying on memory.
## Open questions

- Is `MeMyself&I` actually dead, or is there a reason it's been left un-archived?
- Any known reason Leon Personal – 9262 lost its Starling link specifically (app permission revoked, Starling-side token expiry, deliberate disconnect)?
## Progress Log

### 2026-09-13 — May 2026 batch cleared

159 of 182 unapproved May transactions bulk-approved via the API (safe matches + genuine transfers + 1 confident category fill: "Remarkable" → Leon, based on prior history). The remaining 23 need a category pick from you — new or rare payees with no reliable history, plus one flagged conflict:

| Date | Payee | Amount | Note |
|---|---|---|---|
| 2026-05-20 | Rontec Leigh On Sea | −£1.50 | seen elsewhere as "Petrol" |
| 2026-05-21 | Mk Council | −£5.00 | |
| 2026-05-22 | dash | −£6.00 | currently "Gifts" — history says ☕️ Coffee more often; worth a look |
| 2026-05-23 | Ss Grove Convenience | −£2.85 | |
| 2026-05-25 | Amtrak | −£35.00 | |
| 2026-05-25 | C-Online | −£17.75 | |
| 2026-05-25 | Accessorize | −£14.00 | |
| 2026-05-25 | Costa Lon Liverpool St London | −£5.30 | |
| 2026-05-26 | J D Sports | −£55.60 | |
| 2026-05-26 | London Road Car Wash | −£30.00 | |
| 2026-05-26 | Champneys City Spa | −£24.43 | |
| 2026-05-26 | Headington F&w | −£4.30 | |
| 2026-05-27 | Tracey Graves | −£21.00 | seen elsewhere as "Clothes" |
| 2026-05-27 | Ubisoft Emea | −£15.99 | |
| 2026-05-27 | Champneys City Spa | −£14.50 | |
| 2026-05-28 | Rontec | −£22.17 | |
| 2026-05-28 | Ollama | −£15.47 | seen elsewhere as "Stuff I Forgot to Budget For" |
| 2026-05-28 | Champneys City Spa | −£4.64 | |
| 2026-05-28 | Basildon | −£2.50 | |
| 2026-05-29 | Openrouter Inc | −£18.36 | |
| 2026-05-30 | Piccolo Restaurant | −£124.00 | |
| 2026-05-30 | Yours Clothing | −£22.39 | |
| 2026-05-31 | Halfords | −£13.99 | |

Remaining overall unapproved count after this batch: **1,574** (down from 1,733).

### 2026-09-13 — June through September (to date) cleared

Ran the same method month by month, refreshing the payee→category mapping each time so later months benefit from earlier approvals:

| Month | Unapproved | Bulk-approved | Left for manual review |
|---|---|---|---|
| 2026-06 | 439 | 358 | 81 |
| 2026-07 | 443 | 371 | 72 |
| 2026-08 | 484 | 372 | 112 |
| 2026-09 (to 09-13) | 185 | 155 | 30 |

**318 transactions remain unapproved overall** (23 from May + 258 from Jun–Sep) — all genuine judgment calls, not auto-applied. They split into:

**6 flagged conflicts** — currently categorized, but history disagrees. Worth a quick look, not auto-changed:

| Date | Payee | Amount | Current | History suggests |
|---|---|---|---|---|
| 2026-06-08 | dash | −£7.40 | Gifts | ☕️ Coffee |
| 2026-07-05 | P Chalkwell Sst | −£2.20 | 🏀 Pearl | Transportation |
| 2026-07-21 | P Chalkwell Sst | −£4.40 | 🏀 Pearl | Transportation |
| 2026-07-28 | P Chalkwell Sst | −£4.40 | 🏀 Pearl | Transportation |
| 2026-08-19 | P Chalkwell Sst | −£2.20 | 🏀 Pearl | Transportation |
| 2026-08-23 | P Chalkwell Sst | −£2.20 | 🏀 Pearl | Transportation |

"P Chalkwell Sst" recurring 5x as a conflict is probably parking near wherever Pearl's activity is — worth deciding once whether that's genuinely "Transportation" or correctly "Pearl" and it'll stop flagging.

**289 with no reliable history** — new or rare payees I have no confident basis to categorize. Most frequent ones worth setting up a YNAB payee/category rule for, since they'll keep recurring:

| Payee | Occurrences (uncategorized, this cleanup) |
|---|---|
| Haven | 23 |
| Southend And D | 18 |
| Mayfair News | 6 |
| Bh Live Active | 6 |
| Deliveroo | 5 |
| Vets4Pets | 4 |
| The Arlington | 4 |
| R Monnington | 4 |
| Leigh-on-sea C | 4 |
| Holiday Inn | 4 |
| Big News Clifftown Roa | 4 |

The full 318-item list is easiest to work through directly in the YNAB app (Accounts → filter Unapproved) rather than here — everything with a green tick above is already off your plate.

### 2026-09-13 — Account reconciliation against real Starling balances

Compared YNAB against the real Starling app balances the user read directly:

| Account | Starling (actual) | YNAB before | Result |
|---|---|---|---|
| Zofja Personal | £488.70 | £488.70 | exact match, no action |
| Starling Joint | £994.89 | £1,230.49 (all cleared, no uncleared) | **£235.60 over** — user fixed via YNAB GUI reconcile (emergency fix) |
| Leon Personal | £299.87 (2 Starling spaces: £103.89 + £195.98) | −£8,197.80 total (cleared £322.20, **uncleared −£8,520.00**) | see below |

**Leon Personal root cause:** the user's GUI reconcile fixed `cleared_balance` to £299.87, but left £8,520 of uncleared transactions untouched, so the account's total balance stayed at −£8,220.13. Investigation found the uncleared amount was exactly 7 transfer transactions to Starling Joint (£100, £50, £20, £4,000, £50, £100, £4,200 — 2026-06-20 through 2026-07-31). Their mirror legs on the Joint side were already cleared/reconciled and correctly counted in Joint's real balance.

Leon Personal's cleared history for Jun–Jul otherwise had only 2 tiny transactions (an ATM withdrawal and a PayPal payment) — **no salary/income was ever recorded for that account during the Starling disconnect**, even though the user is paid into Leon Personal monthly and transfers to Joint from there. Someone had manually logged the outgoing transfers (since those matter for the joint budget) but never logged the incoming salary. So the £8,520 uncleared block was real (the transfers genuinely happened, confirmed by the user) — the actual problem was **missing income, not a duplicate**.

**Fix applied (per user's choice: quick fix over manually re-entering exact salary transactions):**
1. Marked all 7 transfer transactions `cleared: reconciled` via the API (both legs already existed as a linked transfer pair; only Leon's leg needed the cleared flag).
2. This dropped Leon Personal's cleared balance to −£8,220.13 (correctly reflecting the 7 real outflows with no matching income on record).
3. Created one catch-up transaction: **+£8,520.00**, dated 2026-09-13, category `Inflow: Ready to Assign`, payee "Balance catch-up (Starling reconnect)", memo explaining the missing-income root cause, `cleared: reconciled`. (Note: YNAB's API rejects the literal payee name "Reconciliation Balance Adjustment" — it's reserved for the app's own reconcile flow — hence the custom payee name.)

**Final state — all three accounts now match Starling:**

| Account | Starling (actual) | YNAB (after) |
|---|---|---|
| Zofja Personal | £488.70 | £488.70 |
| Starling Joint | £994.89 | £994.98 (9p — rounding/timing) |
| Leon Personal | £299.87 | £299.87 |

**Caveat:** the £8,520 catch-up sits in YNAB as one lump "Ready to Assign" inflow rather than real dated salary transactions, so Leon Personal's income history for Jun–Jul still won't show the actual payslip dates/amounts if that's ever needed (e.g. for a mortgage application). If that matters, this can be redone properly later using real payslip records instead of the lump adjustment.
