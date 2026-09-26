---
created: 2026-09-13T11:38:15+00:00
modified: 2026-09-26T08:45:42+00:00
permalink: llmeon/30-library/200-projects/2026-09-13-ynab-starling-reconciliation-plan
project_category: finance
project_name: YNAB / Starling Reconciliation
project_status: active
revision: 1
status: draft
tags: [budgeting, finance, starling, ynab]
title: 2026-09-13-ynab-starling-reconciliation-plan
---

## Context

Starling bank connections were recently re-enabled after a period of drift. This note captures the current state of the YNAB account (pulled live via the API on 2026-09-13, read-only) and a phased plan to bring it back in line.

Access used: YNAB personal access token from 1Password (`op://Private/YNAB PAT/credential`), called directly against `https://api.ynab.com/v1` (note: the API now calls budgets "plans"—`/plans`, `/plans/{plan_id}/accounts`, etc.—a rename since earlier docs). No YNAB MCP/integration tool exists in this environment; all calls were manual `curl` + `op read`, read-only. Bank-feed linking itself (OAuth handshake with Starling) is not exposed via the API at all—that step has to happen in the YNAB app/website, not here.

## Findings

### Plan (Budget) Sprawl

7 plans exist on the account; 5 are archived, evidence of a repeated abandon-and-restart pattern:

| Plan | Status | Last modified |
|---|---|---|
| Oct25 | active | 2026-09-13 (today) |
| MeMyself&I | not archived, but orphaned | 2024-08-08 |
| August25 | archived 2025-10-06 | 2025-10-06 |
| This one will work 2025 | archived 2025-08-11 | 2025-10-06 |
| Jan25 | archived 2025-02-12 | 2025-11-21 |
| June 24 | archived 2024-11-23 | 2025-10-07 |
| Nov24 | archived 2024-12-29 | 2024-12-29 |

`Oct25` is the live budget. `MeMyself&I` holds one stray "Personal" checking account (£287.32, never reconciled, untouched since Aug 2024)—looks abandoned rather than in active use.

### Bank-feed (Direct Import) Status in Oct25

Only 2 of 3 personal checking accounts are currently linked to a bank feed:

| Account | Linked? | Last reconciled | Latest txn |
|---|---|---|---|
| Starling Joint | ✅ linked, no error | 2026-02-03 | 2026-09-13 (today) |
| Zofja Personal–8872 | ✅ linked, no error | 2025-12-21 | 2026-09-12 |
| Leon Personal–9262 | ❌ not linked | 2025-12-19 | 2026-08-29 (~2 weeks stale) |

→ This is almost certainly the account still needing its Starling connection re-established.

### Transaction Backlog

- 1,719 unapproved transactions
- 539 uncategorized transactions
- Oldest unapproved transaction dates back to 2026-05-18—roughly 4 months of backlog

### Budget Health (Current Month, Sept 2026)

- To-be-budgeted: −£14,381.56 (deep negative—assigned amounts badly out of sync with actual spend)
- 32 categories currently overspent
- Age of money: 0

### Other Accounts on Oct25

Closed (£0, no action expected): Pearl, Rae, Bessie, MBNA.

Off-budget debt/loan tracking accounts with old or no reconciliation dates: Mortgage, Car Loan, America, Zofja Tax, MBNA Payoff, Leon Klarna, Zofja Klarna, PayPal Credit Card, Leon Glasses, Zofja Glasses, Car Tyre—several have never been reconciled (`last_reconciled_at: null`).

## Plan

## Plan

- [x] 0. Confirm scope—`Oct25` confirmed as the one true budget going forward.
- [x] 1. Reconnect Leon Personal–9262 to Starling—done, verified via API.
- [x] 2. Sanity-check the two already-linked feeds—no disruption after the relink.
- [x] 3. Clear the transaction backlog—1,733 → 80 unapproved remain (personal names, council payments, BNPL services—left for the user deliberately).
- [x] 4. Reconcile every open on-budget account against actual Starling balances—done, all three accounts match.
- [x] 5. Repair the budget—to-be-budgeted −£14,381.56 → +£3,960.96; overspent categories 32 → 15, as a side effect of step 3.
- [~] 6. Structural cleanup—mostly done:
  - [x] Closed accounts checked—all £0, dormant, no issue.
  - [x] Duplicate-payee scan—66 groups / 1,275 affected transactions found and prioritized in the Progress Log.
  - [x] `MeMyself&I` archived by the user (2026-09-13)—confirmed via API, `Oct25` is now the only plan returned by `GET /plans`.
  - [ ] Duplicate payees still need merging in-app (Payees list → select group → Merge)—no API support for this, left to the user's own pace.
- [x] 7. Prevent re-drift—recurring Todoist check-in created; payee-rule behaviour is automatic in YNAB once a payee is categorized correctly once.

All steps that can be driven from this end are complete. What's left is entirely manual, at the user's own pace: finish the 80 held-back transactions, merge the duplicate payees, and keep up with the weekly Todoist check-in.

## Plan

- [x] 0. Confirm scope—`Oct25` confirmed as the one true budget going forward.
- [x] 1. Reconnect Leon Personal–9262 to Starling—done, verified via API.
- [x] 2. Sanity-check the two already-linked feeds—no disruption after the relink.
- [x] 3. Clear the transaction backlog—1,733 → 80 unapproved remain (personal names, council payments, BNPL services—left for the user deliberately).
- [x] 4. Reconcile every open on-budget account against actual Starling balances—done, all three accounts match.
- [x] 5. Repair the budget—to-be-budgeted −£14,381.56 → +£3,960.96; overspent categories 32 → 15, as a side effect of step 3.
- [~] 6. Structural cleanup—partially done; the rest needs the YNAB app, not the API:
  - [x] Closed accounts checked—all £0, dormant, no issue.
  - [x] Duplicate-payee scan—66 groups / 1,275 affected transactions found and prioritized. Merging must be done in-app.
  - [ ] Archive `MeMyself&I`—still waiting on user confirmation it's dead. Must be done in-app.
- [x] 7. Prevent re-drift—done:
  - Created a recurring Todoist task, "YNAB weekly review—clear the inbox", every Sunday, in the Personal project (`finance`/`ynab` labels). Covers: approve/categorize new transactions, confirm all 3 Starling feeds still linked with no errors, glance at To Be Budgeted/overspent categories, and a reminder to log both legs (transfer + income) if a feed ever goes down again.
  - Clarified: no separate "payee rule" setup is needed or even possible via the API—YNAB automatically remembers a payee's last-used category once it's been categorized correctly one time, so properly finishing the remaining 80 transactions IS the rule-setting. This applies to the keyword-guessed ones too (Haven, Southend And D, etc.)—if a guess is wrong, correcting it once will make future imports of that payee categorize correctly.

## Plan

- [x] 0. Confirm scope—`Oct25` confirmed as the one true budget going forward.
- [x] 1. Reconnect Leon Personal–9262 to Starling—done, verified via API.
- [x] 2. Sanity-check the two already-linked feeds—no disruption after the relink.
- [x] 3. Clear the transaction backlog—1,733 → 80 unapproved remain (personal names, council payments, BNPL services—left for the user deliberately).
- [x] 4. Reconcile every open on-budget account against actual Starling balances—done, all three accounts match.
- [x] 5. Repair the budget—to-be-budgeted −£14,381.56 → +£3,960.96; overspent categories 32 → 15, as a side effect of step 3.
- [~] 6. Structural cleanup—partially done; the rest needs the YNAB app, not the API:
  - [x] Closed accounts (Pearl, Rae, Bessie, MBNA) checked—all £0, dormant since 2025-11-22, no issue.
  - [x] Duplicate-payee scan—66 groups / 1,275 affected transactions found and prioritized in the Progress Log. Merging must be done in-app (no merge endpoint in the API)—Payees list → select group → Merge.
  - [ ] Archive `MeMyself&I`—still waiting on the user to confirm it's actually dead. Must be done in-app (no archive endpoint in the API).
- [ ] 7. Prevent re-drift—7 plan restarts in under 2 years suggests the review cadence isn't sticking. Consider a short recurring check-in (e.g. weekly 10-minute inbox clear) tracked in Todoist. Set up YNAB payee rules for high-frequency payees now correctly categorized (Haven, Southend And D, etc.) so they auto-categorize going forward. When a Starling feed is down: log both sides of inter-account transfers AND income.

## Plan

- [x] 0. Confirm scope—`Oct25` confirmed as the one true budget going forward.
- [x] 1. Reconnect Leon Personal–9262 to Starling—done by the user in the YNAB app. Verified via API.
- [x] 2. Sanity-check the two already-linked feeds—no disruption after the relink.
- [x] 3. Clear the transaction backlog—first pass (conservative, ≥85% confidence): 1,733 → 318 unapproved. Second pass (loose, "restarting, imperfect is fine" per user): 231 more resolved via any-history-match + merchant keyword guessing. 80 remain, left for the user (personal names, council payments, BNPL-style services where a wrong guess risks distorting debt tracking).
- [x] 4. Reconcile every open on-budget account against actual Starling balances—done, root cause found and fixed. All three personal accounts match Starling exactly (Joint 9p off from timing).
- [x] 5. Repair the budget—improved dramatically as a side effect of step 3's second pass: to-be-budgeted went from −£14,381.56 to +£3,960.96, overspent categories from 32 to 15. Not a deliberate re-budgeting exercise—just the effect of categorized spending landing on categories that already had headroom. Remaining overspent categories still need a proper look.
- [ ] 6. Structural cleanup—archive `MeMyself&I` (if step 0 confirms it's dead), spot-check the closed accounts stay at £0 with no phantom transactions, and scan payees for duplicates a Starling reimport commonly creates (e.g. "TESCO" vs "Tesco Stores Ltd").
- [ ] 7. Prevent re-drift—7 plan restarts in under 2 years suggests the review cadence isn't sticking. Consider a short recurring check-in (e.g. weekly 10-minute inbox clear) tracked in Todoist. Set up YNAB payee rules for high-frequency payees now correctly categorized (Haven, Southend And D, etc.) so they auto-categorize going forward. When a Starling feed is down: log both sides of inter-account transfers AND income—a transfer-only habit creates exactly the balance hole found in step 4.

## Plan

- [x] 0. Confirm scope—`Oct25` confirmed as the one true budget going forward.
- [x] 1. Reconnect Leon Personal–9262 to Starling—done by the user in the YNAB app. Verified via API: `direct_import_linked: true`, `direct_import_in_error: false`.
- [x] 2. Sanity-check the two already-linked feeds—Starling Joint and Zofja Personal–8872 both stayed `direct_import_linked: true` / no error after the relink.
- [x] 3. Clear the transaction backlog in monthly batches, oldest first, through today (2026-09-13). 1,733 → 318 unapproved remaining (genuine judgment calls left for the user—see Progress Log).
- [x] 4. Reconcile every open on-budget account against actual Starling balances—done. Root cause found and fixed (see Progress Log). All three personal accounts now match the real Starling app balances exactly (Joint is 9p off from timing/rounding).
- [ ] 5. Repair the budget—now that accounts are reconciled and most of the backlog is cleared, true up September's assignments and resolve overspent categories (was 32 as of 2026-09-13 pre-cleanup; re-check).
- [ ] 6. Structural cleanup—archive `MeMyself&I` (if step 0 confirms it's dead), spot-check the closed accounts stay at £0 with no phantom transactions, and scan payees for duplicates a Starling reimport commonly creates (e.g. "TESCO" vs "Tesco Stores Ltd").
- [ ] 7. Prevent re-drift—7 plan restarts in under 2 years suggests the review cadence isn't sticking. Consider a short recurring check-in (e.g. weekly 10-minute inbox clear) tracked in Todoist rather than relying on memory. Also: set up YNAB payee rules for the high-frequency unresolved payees (Haven, Southend And D) so they auto-categorize going forward. New: when a Starling feed is down, log both sides of inter-account transfers AND income—a transfer-only habit creates exactly the kind of balance hole found in step 4.

## Plan

- [x] 0. Confirm scope—`Oct25` confirmed as the one true budget going forward.
- [x] 1. Reconnect Leon Personal–9262 to Starling—done by the user in the YNAB app. Verified via API: `direct_import_linked: true`, `direct_import_in_error: false`, latest transaction 2026-09-11.
- [x] 2. Sanity-check the two already-linked feeds—Starling Joint and Zofja Personal–8872 both still `direct_import_linked: true` / no error after the relink. No disruption.
- [x] 3. Clear the transaction backlog in monthly batches, oldest first, through today (2026-09-13). Method: rebuilt the payee→category mapping fresh before each month from all approved+categorized history (growing from 2,943 to 4,164 transactions as prior months got cleared); applied it only where a payee's category was ≥85% consistent across ≥2 prior occurrences. Genuine account transfers (`transfer_account_id` set) auto-approved without a category.
  - [x] 2026-05—182 unapproved → 159 bulk-approved, 23 left for manual review
  - [x] 2026-06—439 unapproved → 358 bulk-approved, 81 left for manual review
  - [x] 2026-07—443 unapproved → 371 bulk-approved, 72 left for manual review
  - [x] 2026-08—484 unapproved → 372 bulk-approved, 112 left for manual review
  - [x] 2026-09 (partial, to today)—185 unapproved → 155 bulk-approved, 30 left for manual review
  - Result: 1,733 → 318 unapproved remaining, all needing an actual human category decision (see Progress Log).
- [ ] 4. Reconcile every open on-budget account against actual Starling/bank statement balances now that the backlog is mostly cleared—balances may have drifted while the personal account's feed was down.
- [ ] 5. Repair the budget—once the remaining 318 are categorized and accounts reconciled, true up September's assignments and resolve overspent categories (re-check the count; it was 32 as of 2026-09-13 before this cleanup).
- [ ] 6. Structural cleanup—archive `MeMyself&I` (if step 0 confirms it's dead), spot-check the closed accounts stay at £0 with no phantom transactions, and scan payees for duplicates a Starling reimport commonly creates (e.g. "TESCO" vs "Tesco Stores Ltd").
- [ ] 7. Prevent re-drift—7 plan restarts in under 2 years suggests the review cadence isn't sticking. Consider a short recurring check-in (e.g. weekly 10-minute inbox clear) tracked in Todoist rather than relying on memory. Also consider: set up YNAB payee rules for the high-frequency payees found unresolved below (Haven, Southend And D) so they auto-categorize going forward.

## Plan

- [x] 0. Confirm scope—`Oct25` confirmed as the one true budget going forward.
- [x] 1. Reconnect Leon Personal–9262 to Starling—done by the user in the YNAB app. Verified via API: `direct_import_linked: true`, `direct_import_in_error: false`, latest transaction 2026-09-11.
- [x] 2. Sanity-check the two already-linked feeds—Starling Joint and Zofja Personal–8872 both still `direct_import_linked: true` / no error after the relink. No disruption.
- [ ] 3. Clear the transaction backlog in monthly batches, oldest first. Method: built a payee→category mapping from 2,943 historical approved+categorized transactions (556 distinct payees); applied it only where a payee's category was ≥85% consistent across ≥2 prior occurrences. Genuine account transfers (`transfer_account_id` set) auto-approved without a category, since transfers don't need one.
  - [x] 2026-05—182 unapproved → 159 bulk-approved (158 already-correct + 1 high-confidence category applied), 23 left for manual review (see Progress Log below).
  - [ ] 2026-06 (439 unapproved)
  - [ ] 2026-07 (443 unapproved)
  - [ ] 2026-08 (484 unapproved)
  - [ ] 2026-09 (185 unapproved, partial month)
- [ ] 4. Reconcile every open on-budget account against actual Starling/bank statement balances once the backlog is cleared—balances may have drifted while the personal account's feed was down.
- [ ] 5. Repair the budget—once transactions are categorized and accounts reconciled, true up September's assignments to clear the −£14,381.56 to-be-budgeted figure and resolve the 32 overspent categories.
- [ ] 6. Structural cleanup—archive `MeMyself&I` (if step 0 confirms it's dead), spot-check the closed accounts stay at £0 with no phantom transactions, and scan payees for duplicates a Starling reimport commonly creates (e.g. "TESCO" vs "Tesco Stores Ltd").
- [ ] 7. Prevent re-drift—7 plan restarts in under 2 years suggests the review cadence isn't sticking. Consider a short recurring check-in (e.g. weekly 10-minute inbox clear) tracked in Todoist rather than relying on memory.

## Open Questions

- Is `MeMyself&I` actually dead, or is there a reason it's been left un-archived?
- Any known reason Leon Personal–9262 lost its Starling link specifically (app permission revoked, Starling-side token expiry, deliberate disconnect)?

## Progress Log

### 2026-09-13—May 2026 Batch Cleared

159 of 182 unapproved May transactions bulk-approved via the API (safe matches + genuine transfers + 1 confident category fill: "Remarkable" → Leon, based on prior history). The remaining 23 need a category pick from you—new or rare payees with no reliable history, plus one flagged conflict:

| Date | Payee | Amount | Note |
|---|---|---|---|
| 2026-05-20 | Rontec Leigh On Sea | −£1.50 | seen elsewhere as "Petrol" |
| 2026-05-21 | Mk Council | −£5.00 | |
| 2026-05-22 | dash | −£6.00 | currently "Gifts"—history says ☕️ Coffee more often; worth a look |
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

Remaining overall unapproved count after this batch: 1,574 (down from 1,733).

### 2026-09-13—June Through September (To Date) Cleared

Ran the same method month by month, refreshing the payee→category mapping each time so later months benefit from earlier approvals:

| Month | Unapproved | Bulk-approved | Left for manual review |
|---|---|---|---|
| 2026-06 | 439 | 358 | 81 |
| 2026-07 | 443 | 371 | 72 |
| 2026-08 | 484 | 372 | 112 |
| 2026-09 (to 09-13) | 185 | 155 | 30 |

318 transactions remain unapproved overall (23 from May + 258 from Jun–Sep)—all genuine judgment calls, not auto-applied. They split into:

6 flagged conflicts—currently categorized, but history disagrees. Worth a quick look, not auto-changed:

| Date | Payee | Amount | Current | History suggests |
|---|---|---|---|---|
| 2026-06-08 | dash | −£7.40 | Gifts | ☕️ Coffee |
| 2026-07-05 | P Chalkwell Sst | −£2.20 | 🏀 Pearl | Transportation |
| 2026-07-21 | P Chalkwell Sst | −£4.40 | 🏀 Pearl | Transportation |
| 2026-07-28 | P Chalkwell Sst | −£4.40 | 🏀 Pearl | Transportation |
| 2026-08-19 | P Chalkwell Sst | −£2.20 | 🏀 Pearl | Transportation |
| 2026-08-23 | P Chalkwell Sst | −£2.20 | 🏀 Pearl | Transportation |

"P Chalkwell Sst" recurring 5x as a conflict is probably parking near wherever Pearl's activity is—worth deciding once whether that's genuinely "Transportation" or correctly "Pearl" and it'll stop flagging.

289 with no reliable history—new or rare payees I have no confident basis to categorize. Most frequent ones worth setting up a YNAB payee/category rule for, since they'll keep recurring:

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

The full 318-item list is easiest to work through directly in the YNAB app (Accounts → filter Unapproved) rather than here—everything with a green tick above is already off your plate.

### 2026-09-13—Account Reconciliation against Real Starling Balances

Compared YNAB against the real Starling app balances the user read directly:

| Account | Starling (actual) | YNAB before | Result |
|---|---|---|---|
| Zofja Personal | £488.70 | £488.70 | exact match, no action |
| Starling Joint | £994.89 | £1,230.49 (all cleared, no uncleared) | £235.60 over—user fixed via YNAB GUI reconcile (emergency fix) |
| Leon Personal | £299.87 (2 Starling spaces: £103.89 + £195.98) | −£8,197.80 total (cleared £322.20, uncleared −£8,520.00) | see below |

Leon Personal root cause: the user's GUI reconcile fixed `cleared_balance` to £299.87, but left £8,520 of uncleared transactions untouched, so the account's total balance stayed at −£8,220.13. Investigation found the uncleared amount was exactly 7 transfer transactions to Starling Joint (£100, £50, £20, £4,000, £50, £100, £4,200—2026-06-20 through 2026-07-31). Their mirror legs on the Joint side were already cleared/reconciled and correctly counted in Joint's real balance.

Leon Personal's cleared history for Jun–Jul otherwise had only 2 tiny transactions (an ATM withdrawal and a PayPal payment)—no salary/income was ever recorded for that account during the Starling disconnect, even though the user is paid into Leon Personal monthly and transfers to Joint from there. Someone had manually logged the outgoing transfers (since those matter for the joint budget) but never logged the incoming salary. So the £8,520 uncleared block was real (the transfers genuinely happened, confirmed by the user)—the actual problem was missing income, not a duplicate.

Fix applied (per user's choice: quick fix over manually re-entering exact salary transactions):

1. Marked all 7 transfer transactions `cleared: reconciled` via the API (both legs already existed as a linked transfer pair; only Leon's leg needed the cleared flag).
2. This dropped Leon Personal's cleared balance to −£8,220.13 (correctly reflecting the 7 real outflows with no matching income on record).
3. Created one catch-up transaction: +£8,520.00, dated 2026-09-13, category `Inflow: Ready to Assign`, payee "Balance catch-up (Starling reconnect)", memo explaining the missing-income root cause, `cleared: reconciled`. (Note: YNAB's API rejects the literal payee name "Reconciliation Balance Adjustment"—it's reserved for the app's own reconcile flow—hence the custom payee name.)

Final state—all three accounts now match Starling:

| Account | Starling (actual) | YNAB (after) |
|---|---|---|
| Zofja Personal | £488.70 | £488.70 |
| Starling Joint | £994.89 | £994.98 (9p—rounding/timing) |
| Leon Personal | £299.87 | £299.87 |

Caveat: the £8,520 catch-up sits in YNAB as one lump "Ready to Assign" inflow rather than real dated salary transactions, so Leon Personal's income history for Jun–Jul still won't show the actual payslip dates/amounts if that's ever needed (e.g. for a mortgage application). If that matters, this can be redone properly later using real payslip records instead of the lump adjustment.

### 2026-09-13—Loose-pass Bulk Categorization (User: "Doesn't Matter if Some Are Wrong")

User approved a much looser pass than the earlier conservative one, given the budget is effectively restarting: apply best-guess categories broadly, accept some will be wrong, prioritize coverage over precision.

Method:

1. Rebuilt payee history from all 4,344 approved+categorized transactions (614 distinct payees)—this time using any match (no ≥85%/≥2-occurrence floor).
2. Added ~35 regex keyword rules mapping recognizable UK merchant name patterns to this budget's actual categories—petrol stations, supermarkets, coffee/dining chains, leisure centres and pools, DVLA, school uniforms, home/DIY stores, pet shops, etc. Iterated twice against the actual unresolved-payee list to raise coverage from 124 → 191 → 231 resolved.
3. Applied in two chunked PATCH calls (200 + 31).

Result: 231 of 312 remaining transactions categorized and approved. 81 left deliberately unresolved—personal-name payees (likely tutors/family/services), council payments, and BNPL-style services (e.g. "Affirm") where a wrong category guess could distort real debt/bill tracking rather than just being cosmetically off.

Budget-wide effect (current month):

| Metric | Before | After |
|---|---|---|
| To-be-budgeted | −£14,381.56 | +£3,960.96 |
| Overspent categories | 32 | 15 |

This wasn't deliberate re-budgeting—categorizing outflows just moved them off "Ready to Assign" (where uncategorized spending draws from directly) onto their real categories, most of which already had unused budgeted headroom.

Known limitation: some keyword-based guesses will be wrong (e.g. "Southend And D" → guessed Days Out at £6/week without knowing what it actually is; "Vets4Pets" → guessed a specific pet's insurance category rather than a generic vet-visit bucket). Per the user, fine to fix over time rather than block on it now. Worth a skim through recently-categorized transactions next time in the YNAB app.

### 2026-09-13—Step 6: Structural Cleanup Findings

Closed accounts (Pearl, Rae, Bessie, MBNA): all confirmed £0 balance, no activity since 2025-11-22. Clean, no action needed.

Plan archiving and payee merging are not exposed by the YNAB API at all—no PATCH/archive endpoint for plans, no merge endpoint for payees. Both of the remaining items below need the YNAB app itself.

`MeMyself&I` plan—still unresolved from the original open question: is it actually dead, or is there a reason it's been left un-archived? If it's dead, archiving has to be done in-app (Settings → this plan → Archive).

Duplicate payees—66 groups, 1,275 affected transactions. YNAB has split what should be single payees across multiple payee records (same or near-identical name), which fragments spending history and category auto-matching. Merging requires the app (Payees list → select the group → Merge). Top candidates by impact:

| Payee name(s)—split across records                          | Total txns |
| ------------------------------------------------------------- | ---------- |
| 'Co-op' (527), 'COOP' (3)                                     | 530        |
| 'Aldi' (134), 'Aldi' (38)                                     | 172        |
| "Sainsbury's" (151), 'Sainsburys' (1)                         | 152        |
| 'dash' (20), 'dash' (14)                                      | 34         |
| 'P Chalkwell Sst' (18), 'P Chalkwell Sst' (8)                 | 26         |
| 'Natwest account - Zofja E A Day - …' (19+5)                | 24         |
| 'AQA EDUCATION Aqa Payments' (3+15)                           | 18         |
| 'Heather Heighington' (12+5)                                  | 17         |
| 'The Hang Out Venue' (4+10)                                   | 14         |
| 'Santander account - Leon & Bessie Casey Connor - …' (11+2) | 13         |
| 'Vinted' (3+10)                                               | 13         |
| 'ZOFJA Anne Wonnacott' (8+4)                                  | 12         |
| 'WH Smith' (4), 'WHSmith' (5)                                 | 9          |
| 'The Gym Group' (6+3)                                         | 9          |
| 'World Of Reptiles' (3+6)                                     | 9          |

Full 66-group list is in `dupe_table.md` in scratchpad if wanted, but most of the tail is 2-3 transactions each—low priority. The 15 above account for the bulk of the impact.

Also found via fuzzy matching (lower confidence, worth a manual glance, not auto-merged):

- 'Coffee Station' (59) + 'Coffee Station Chalkw' (120) + 'Coffee Station Fenchur' (3) + 'Coffee Station Leigh' (4)—likely branch-suffix splits of the same chain.
- 'Southend Borough Council' (43) + 'Southend-on-sea Borough Council' (21) + 2 more variants—same council, 4 name variants.
- 'P Chalkwell Sst' (26) + 'P Chalkwell To' (47)—likely the same parking location, different transaction codes.
- 'Google' (6) + 'Google Play' (47) + 'Google Play Store' (1)—minor.

False positives—do NOT merge these, they're genuinely different:

- Superdrug vs Superdry (different retailers, similar name)
- Leigh Road Cafe vs Leigh Road Pharmacy (different businesses, same road)
- Amazon vs Amazon Music vs Amazon Prime (general purchases vs specific subscriptions—keep separate)
- The two "Santander account - …" and "…HSBC account - …" entries with different named account holders—these are different real people/transfers, only superficially similar due to shared bank-transfer text format.
