---
aliases: []
tags: []
title: January 2026 Budget Review & Migration Report
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
created: 2026-01-01T10:24:11+00:00
modified: 2026-01-01T13:10:04+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
---

# January 2026 Budget Review & Migration Report

**Date:** 2026-01-01
**Status:** Debt Migration Initialized

## 📊 Current Budget Snapshot

- **Ready to Assign:** £263.59
- **Main Groceries:** £800.00
- **Consolidated Debt Funding:** £625.40 (Distributed across 10 individual loan categories)

## 🔄 Migration Status: Debt Consoldiation

The transition to a consolidated "Monthly Debt Obligations" view is in progress.

- **Migration Complete:** All individual loan categories (America, Klarna, Glasses, etc.) have been funded for January.
- **Pending Action:** To fully consolidate into a single line item, you must manually re-pair the Loan Accounts in the YNAB web/mobile app (1-to-1 relationship requirement).
- **Strategy:** Retain individual categories to keep YNAB's automated interest/payoff tracking, but manage them via the **Debt Repayments** group header for a "consolidated" feel.

## 💡 Spendfulness & Strategic Suggestions

Based on a review of statement data (`all_statements.csv`) and vault notes on "Healthy Money":

### 1. Convenience Tracking

**Observation:** Frequent transactions at Co-op, Sainsbury’s Local, and Greggs are currently unfunded in the new categories.
**Recommendation:**
- Allocate **£50–£80** to "Convenience Top-Up" (True Expenses) to cover mid-week necessities.
- Use "Convenience Food" (Just for Fun) specifically for "lazy" meals (e.g., McDonald's, Petrol Station snacks) to distinguish them from intentional family "Dining Out."

### 2. Family & Child Spending

**Observation:** Tension regarding "unilateral spending" on children is noted in vault documentation.
**Recommendation:**
- **The Florida Pot:** Create a specific "Florida Trip" category under "Girl's Money." Even if unfunded, it provides visibility for this major goal and prevents it from leaking into other categories.
- **Strict Categorization:** Ensure all club fees, uniforms, and cheerleading costs are logged here to provide clean data for "Budget Dates."

### 3. Protecting "Value" Spending

- **Dining Out:** Reserve this for high-value family time.
- **Convenience Food:** Use this as the "pressure valve" category when time/energy is low, ensuring it doesn't mask the true cost of your intentional social spending.

## 🗓️ Next Steps

1. **February Budgeting:** Assign the full £625.40 to "Monthly Debt Obligations" first, then distribute to individual loans as needed.
2. **Weekly Review:** Conduct a 15-minute "Budget Date" to review the balance in the "Convenience" categories.

# YNAB Budget Improvement Report

**Date:** 2026-01-01
**Analysis Period:** Sept 2025 - Dec 2025

## Executive Summary

Analysis of Starling bank transactions via `tally` compared against YNAB Plan data reveals several opportunities for budget optimization, primarily around debt consolidation, grocery spending adjustments, and categorization of convenience spending.

---

## 1. Debt & Financial Consolidation

Your current YNAB plan tracks **10 separate debt repayment categories** (e.g., Prom dress, Glasses, Car Tyre).

- **Observation:** This adds significant visual clutter and makes it harder to see the total "debt tax" on your monthly income.
- **Recommendation:** Consolidate these into a single **"Monthly Debt Obligations"** category. Use YNAB **Category Notes** or **Targets** to track individual payoffs.

## 2. Grocery Spending Realignment

- **Observation:** In October, Groceries were overspent by **£153.11** (£1,634.32 actual vs £1,481.21 assigned). Starling data shows high frequency at Co-op and Aldi.
- **Recommendation:** Increase the monthly Grocery target by **£150** to reflect consistent spending patterns. Consider a separate "Convenience Top-up" category for mid-week Co-op trips.

## 3. Convenience vs. Dining

- **Observation:** Tally identified 20+ transactions per month for low-friction food (McDonald's, Coffee Station, Greggs).
- **Recommendation:** Create a **"Convenience Food"** category. Separating this from "Dining Out" provides better psychological feedback on small, frequent spends that drain the budget.

## 4. Subscription Optimization

- **Observation:** Fixed recurring costs for Audible, YouTube, and Google are currently fragmented.
- **Recommendation:** Group all fixed digital services into a single **"Digital Subscriptions"** group with a fixed monthly Spending Target.

## 5. Maintenance Sinking Funds

- **Observation:** High YTD spend on Car Finance/Maintenance (£1,200+). Current YNAB assignments for maintenance were £0 in active months.
- **Recommendation:** Use the "True Expenses" method to build a **Structural Maintenance Fund** for both Car and Home, ensuring buffers are ready before the "big" repairs hit.

## 6. Data Fidelity (Payee Hygiene)

- **Observation:** £11,518 of "Unknown" spending in Tally due to custom YNAB payees (e.g., "👯‍♀️Girl's Money: 🤪 Rae") not matching bank data ("PRIMARK").
- **Recommendation:** Keep the **Payee** as the merchant (e.g., Primark) and use the **Memo** field for the specific child/purpose. This preserves data portability for automated tools.

---

**Next Steps:**
- [ ] Consolidate debt categories.
- [ ] Adjust Grocery target for Jan 2026.
- [ ] Audit digital subscriptions for unused services.
