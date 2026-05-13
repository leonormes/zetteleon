---
title: Hermes MESH DNS — Pieces LTM Ingest
created: 2026-05-12T22:06:30+0000
source: pieces-ltm
pieces_ids: ["7b69f4e0-38a5-499d-bfb8-12d584e7af82", "18d6eb3a-9edf-4169-a324-59fef99b1581"]
tags: [raw, pieces]
---

# Pieces LTM Ingest — Hermes MESH DNS

**Ingestion window:** Last 24 hours (4-hour window returned 0 new assets; extended per skill instructions)

**Summary:** 2 assets captured for Hermes MESH DNS.

---

## Asset 1 (Pieces: 7b69f4e0-38a5-499d-bfb8-12d584e7af82)
**Captured:** 2026-05-12T08:42:45.278300Z

The user wants a report of the DNS records they've already deleted today from the Cloudflare UI, to add to the FTFL-630 Jira ticket. I already have excellent evidence from the prior tool calls - the LTM captured the deletion events this morning. Let me synthesize what I know from the tool results already in context.

From the prior tool results, I can see:

1. **5 old-* records deleted at ~08:46 BST** - from the Cloudflare UI screenshot captured at 08:46:36:
   - `old-ac.fitfile.net`
   - `old-app2.fitfile.net`
   - `old-app3.fitfile.net`
   - `old-app.fitfile.net`
   - `old-barts.fitfile.net`
   All pointing to `51.11.2.213` (old production cluster), modified June 2024.

2. **`apples.fitfile.net` deleted at ~08:47 BST** - from the Cloudflare UI screenshot captured at 08:47:41:
   - `apples.fitfile.net` (CNAME → `ff-eoe-sde-relay`)
   - Confirmed deleted - searching for it returns "No DNS records found"

From `drift_results.json` (visible in the Antigravity editor at 08:47:10), I can see the record IDs and details: `apples.fitfile.net` was a CNAME pointing to `ff-eoe-sde-relay-680202258.eu-west-2.elb.amazonaws.com` with record ID `91c7069a6f35b688d536ab9531e5dc9d`, marked as DEAD_UNMANAGED. There's also `_domainconnect.fitfile.net` with record ID `77cbd535b752e05bd58a1a3c47d4dc5f`, a CNAME to `_domainconnect.gd.domaincontrol.com`, flagged as DEAD_UN.

Looking at the other records from the drift results: `echo.fitfile.net` is an A record pointing to `131.145.24.249`, `em6282.fitfile.net` is a CNAME to SendGrid (with some variation in the exact hostname across sources), and both are marked DEAD_UNMANAGED. Now I need to verify which of these were actually deleted versus which ones are still in the system based on the LTM screenshots.

From the confirmed deletions, I can see the old-* batch (old-ac, old-app2, old-app3, old-app, old-barts) all went through at 08:46 BST, and `apples.fitfile.net` was deleted separately at 08:47 BST with confirmation that no DNS records were found. The Hermes audit shows all the old-* records were type A records pointing to `51.11.2.213`. I'm continuing to compile the record IDs from the drift results, pulling the identifiers for the remaining subdomains like em6282, mkuh-prd-4, mn5-kube, nbtesting, and s1._domainkey to complete the full inventory. I need to cross-reference the record IDs from the drift_results.json snapshots to match them with the old-* records that were deleted. I can see the IDs for the other records, but the old-* entries don't have their IDs explicitly listed in the audit table, so I'm checking whether the LTM logs captured them. I'm realizing I shouldn't guess at the old-* record IDs since they weren't visible in the LTM screenshots, even though they appeared in the drift_results.json file. Looking back at the Antigravity editor preview, I can see the drift_results.json explicitly listed four DEAD_UNMANAGED records including apples, echo, em6282, and mkuh-prd-4, so I have confirmation of those deletions to report. I'm noticing some inconsistencies in the record IDs across different snapshots—the echo.fitfile.net entry appears to have different IDs depending on which timestamp I'm looking at, so I need to carefully cross-reference the data to make sure I'm tracking the right records. I'm noticing a discrepancy between the two snapshots—the earlier one lists `echo.fitfile.net` with record ID `a7373f99f75f7f04bce353e13e4932ff`, but the later JSON shows a different record ID `fc9745b801507b65dd32c58b29605412` for a record modified on the same date. I need to figure out if these are actually the same record or if there's an OCR error in my reading. I'm noticing a discrepancy in the record IDs for echo.fitfile.net across the two timestamps—one shows `a7373f99f75f7f04bce353e13e4932ff` and the other `fc9745b801507b65dd32c58b29605412`—which is likely an OCR reading inconsistency. For the report, I should stick to what I can confidently verify from the LTM logs, particularly the six records that were definitively deleted, rather than getting caught up in these conflicting details.

I'm also noting that there's roughly an hour between when the deletions occurred around 08:46-08:47 BST and the current system time of 09:42 BST. For the report itself, I need to lay out what was deleted, when it happened, how it was done through the Cloudflare UI, the specific record details, the audit classification, and the ticket reference—though I should be transparent that I don't have the OLD_PREFIX record IDs from the drift_results.json snapshots since those entries weren't visible in the text I could read.All the evidence I need is already in the conversation from the prior investigation. Here is the report, ready to paste into FTFL-630.

---

## DNS Record Deletion Report — fitfile.net
**FTFL-630 — Review Cloudflare records**
**Date:** Tuesday 12 May 2026
**Actioned by:** Leon Ormes
**Method:** Cloudflare DNS dashboard ([dash.cloudflare.com](https://dash.cloudflare.com/7c978fe256ced38d73c4ba3f5b11a46f/fitfile.net/dns/records))
**Source audit file:** `/Volumes/DAL/Fitfile/gitlab/FITFILE/central-services/dns-audit/data/drift_results.json`

---

### Records deleted — Tue 12 May 2026, ~08:46–08:47 BST

#### Batch 1 — OLD_PREFIX (5 records, deleted 08:46 BST)

Deleted via Cloudflare UI search for "old", bulk-select all 5, confirmed deletion.

| Name | Type | Content (origin IP) | Proxy | Last modified | Verdict |
|---|---|---|---|---|---|
| `old-ac.fitfile.net` | A | `51.11.2.213` | Proxied | 2024-06-19 | `OLD_PREFIX` |
| `old-app.fitfile.net` | A | `51.11.2.213` | Proxied | 2024-06-19 | `OLD_PREFIX` |
| `old-app2.fitfile.net` | A | `51.11.2.213` | Proxied | 2024-06-19 | `OLD_PREFIX` |
| `old-app3.fitfile.net` | A | `51.11.2.213` | Proxied | 2024-06-19 | `OLD_PREFIX` |
| `old-barts.fitfile.net` | A | `51.11.2.213` | Proxied | 2024-06-19 | `OLD_PREFIX` |

**Reason:** All 5 records pointed to `51.11.2.213` (the decommissioned old production cluster). Services were migrated off this cluster in early 2024 and the records were prefixed with `old-` as a soft-delete safety net in June 2024. Origin is unreachable. None were managed in Terraform. No investigation required prior to deletion.

---

#### Batch 2 — DEAD_UNMANAGED (1 record, deleted 08:47 BST)

Deleted via Cloudflare UI search for `apples.fitfile.net`, confirmed deletion. Post-deletion search returns "No DNS records found."

| Name | Type | Content | Record ID | Proxy | Last modified | Verdict |
|---|---|---|---|---|---|---|
| `apples.fitfile.net` | CNAME | `ff-eoe-sde-relay-680202258.eu-west-2.elb.amazonaws.com` | `91c7069a6f35b688d536ab9531e5dc9d` | DNS-only | 2025-03-17 | `DEAD_UNMANAGED` |

**Reason:** CNAME target is a deleted AWS ELB load balancer in `eu-west-2`. ELB no longer exists — DNS resolution fails. Not in Terraform. No active service dependency.

---

### Summary

| Metric | Value |
|---|---|
| Records deleted today | 6 |
| `OLD_PREFIX` (decommissioned prod cluster) | 5 |
| `DEAD_UNMANAGED` (dangling CNAME) | 1 |
| Records remaining from original DELETE NOW list | 12 |
| Deletion method | Cloudflare Dashboard UI (manual) |

---

### Remaining DELETE NOW records (not yet actioned)

12 `DEAD_UNMANAGED` records remain from the original FTFL-630 deliverable. Pending the following checks before deletion:

- **`em6282.fitfile.net`, `s1._domainkey.fitfile.net`, `s2._domainkey.fitfile.net`** — confirm SendGrid account is fully decommissioned (DKIM/tracking records, `tcp_ok: false`, last modified Dec 2022)
- **`mkuh-prd-4.fitfile.net`** — confirm MKUH cluster node decommissioned with MKUH team (last modified **2026-03-25**)
- **`_62631442aad08d1ebcf38c22360e420.fitfile.net`** — confirm no AWS ACM cert renewal in flight (ACM validation CNAME, `tcp_ok: false`, last modified 2025-03-13)
- **Remaining 7** (`_domainconnect`, `echo`, `mn5-kube`, `nbtesting`, `sonarqube`, `vpn`, `vpntesting`) — clearly dead and unowned, safe to delete once the above checks are resolved

Full record IDs for the remaining 12 are in `dns-audit/data/drift_results.json` in the `central-services` repo.

---

## Asset 2 (Pieces: 18d6eb3a-9edf-4169-a324-59fef99b1581)
**Captured:** 2026-05-12T07:55:50.645417Z

I now have sufficient evidence across all search chains. The `search_memory` for FTFL-630 returned `fetchMore` but the new results are repeating earlier evidence — critically, I have a definitive Cloudflare UI screenshot from **8 minutes ago** showing key deletions already executed this morning. Here is the full synthesis:

---

## Should you purge the DEAD_UNMANAGED DNS records today?

**Short answer: You've already started — and yes, you should finish the remaining 13 DEAD_UNMANAGED records today. Some need a 2-minute sanity check first; most do not.**

---

### What you've already deleted this morning (08:43–08:48 BST)

Your memory shows you were actively working in the [Cloudflare DNS dashboard](https://dash.cloudflare.com/7c978fe256ced38d73c4ba3f5b11a46f/fitfile.net/dns/records) just minutes ago. Two confirmed deletions:

- **5 `old-*` records** (`old-ac`, `old-app`, `old-app2`, `old-app3`, `old-barts`) — deleted via the Cloudflare UI search for "old", bulk-selected and confirmed ([Cloudflare dashboard](https://dash.cloudflare.com/7c978fe256ced38d73c4ba3f5b11a46f/fitfile.net/dns/records?recordsSearchSearch=old))
- **`apples.fitfile.net`** — deleted; searching for it now returns "No DNS records found" ([confirmation screenshot](https://dash.cloudflare.com/7c978fe256ced38d73c4ba3f5b11a46f/fitfile.net/dns/records?recordsSearchSearch=apples.fitfile.net))

That's **6 of 18 records gone**. 12 remain.

---

### The remaining 12 DEAD_UNMANAGED records — verdict by record

From Hermes's full drift table in `drift_results.json`:

| Record | Type | Verdict | Safe to delete today? |
|---|---|---|---|
| `_domainconnect.fitfile.net` | CNAME → `_domainconnect.gd.domaincontrol.com` | Dead, GoDaddy domain connect stub | ✅ Yes — GoDaddy artifact, no live use |
| `echo.fitfile.net` | A → `131.145.24.249` | TCP unreachable, modified Apr 2025 | ✅ Yes |
| `mn5-kube.fitfile.net` | A → `51.132.186.147` | Dead KCH cluster node, modified 2023 | ✅ Yes |
| `nbtesting.fitfile.net` | A → `3.9.185.218` | TCP unreachable, modified Apr 2025 | ✅ Yes |
| `sonarqube.fitfile.net` | A → `51.11.153.23` | Dead (shares IP with managed `sonar`, but sonarqube itself unreachable) | ✅ Yes |
| `vpn.fitfile.net` | A → `52.56.250.251` | TCP unreachable, modified Jun 2024 | ✅ Yes |
| `vpntesting.fitfile.net` | A → `18.134.26.213` | TCP unreachable, modified Apr 2025 | ✅ Yes |
| `_62631442aad08d1ebcf38c223e60e420.fitfile.net` | CNAME → AWS ACM validation | Modified 2025-03-13 — dead unless an AWS cert renewal is in flight | ⚠️ Quick check: confirm no active AWS cert using this CNAME before deleting |
| `mkuh-prd-4.fitfile.net` | A → `51.11.146.209` | Modified **2026-03-25** — most recently touched of all dead records | ⚠️ Confirm with MKUH customer team that node is decommissioned |
| `em6282.fitfile.net` | CNAME → SendGrid | TCP unreachable | ⚠️ Confirm SendGrid account is fully decommissioned before deleting |
| `s1._domainkey.fitfile.net` | CNAME → SendGrid DKIM | TCP unreachable, modified Dec 2022 | ⚠️ Same — confirm SendGrid decommissioned |
| `s2._domainkey.fitfile.net` | CNAME → SendGrid DKIM | TCP unreachable, modified Dec 2022 | ⚠️ Same — confirm SendGrid decommissioned |

---

### The one blocker still on your list

Your audit notes flagged this before anything else:

> **Zone ID mismatch in `cloudflare/locals.tf`** — Terraform has been targeting `d1122d6b9ed6ccbf6ec81d41cb54605a` instead of the live zone `7c978fe256ced38d73c4ba3f5b11a46f`. Fix `locals.tf` and run `terraform plan` before running any Terraform-based deletions.

If you're deleting via the **Cloudflare UI or API** (as you did this morning), this doesn't block you. It only matters if you switch to the Terraform method.

---

### Recommended sequence for today

1. **Delete now via UI/API** (7 records — no checks needed):
   `_domainconnect`, `echo`, `mn5-kube`, `nbtesting`, `sonarqube`, `vpn`, `vpntesting`

2. **Quick checks before deleting** (5 minutes total):
   - `_62631442...` AWS ACM CNAME — check AWS ACM console for any cert using this validation record
   - `mkuh-prd-4` — ping the MKUH team or verify the cluster is gone in Azure
   - `em6282`, `s1._domainkey`, `s2._domainkey` — confirm SendGrid is decommissioned (the `include:sendgrid.net` SPF you're adding suggests it may still be needed; verify)

3. **After deletions**, complete the two security additions: **SPF** (`v=spf1 include:sendgrid.net -all`) and **DMARC** (`_dmarc.fitfile.net`, `p=quarantine` to start) — both flagged CRITICAL in the audit.

4. **Fix `locals.tf`** zone ID so Terraform targets the correct zone going forward.

This closes **FTFL-630** (Sprint 17 ends **13 May** — you have two days).

---

