---
created: 2026-05-12T09:56:03+00:00
I now have comprehensive data from the Cloudflare UI, browser history, and memory. Here is the full report ready to paste into FTFL-630:
modified: 2026-05-12T13:12:02+00:00
title: Cloudflare DNS Deletion Report
---

## Cloudflare DNS Deletion Report—`fitfile.net`

Date: Tuesday 12 May 2026

Performed by: `leon.ormes@fitfile.com`

Account: FITFILE Account (`7c978fe256ced38d73c4ba3f5b11a46f`)

Zone: `fitfile.net`

Ticket: [FTFL-630 — Review Cloudflare records](https://fitfile.atlassian.net/jira/software/c/projects/FTFL/boards/281/backlog?assignee=633ae2b9fedc6169aed8f601)

Source: Cloudflare Dashboard → [DNS | Records | fitfile.net](https://dash.cloudflare.com/7c978fe256ced38d73c4ba3f5b11a46f/fitfile.net/dns/records) + [Audit Log](https://dash.cloudflare.com/7c978fe256ced38d73c4ba3f5b11a46f/audit-log)

---

### Records Deleted

| # | Record Name | Type | Content / Notes | Approx. Time (BST) | Method |
|---|---|---|---|---|---|
| 1 | `old-ac` | A | `51.11.2.213`—Proxied. Verdict: `OLD_PREFIX`. Last modified 2024-02-29. | ~08:46 | Batch delete (group of 5) |
| 2 | `old-app2` | A | `OLD_PREFIX`—part of same batch | ~08:46 | Batch delete |
| 3 | `old-app3` | A | `OLD_PREFIX`—part of same batch | ~08:46 | Batch delete |
| 4 | `old-app` | A | `OLD_PREFIX`—part of same batch | ~08:46 | Batch delete |
| 5 | `old-barts` | A | `OLD_PREFIX`—part of same batch | ~08:46 | Batch delete |
| 6 | `apples.fitfile.net` | CNAME | Stale CNAME record—no active target | ~08:47 | Single delete |
| 7 | `mn5` | (A/CNAME) | `51.132.186.147`—previously visible in full DNS list | ~09:14 | Single delete |
| 8 | `sonar` | (A/CNAME) | Stale/unmanaged record | ~09:14 | Single delete |
| 9 | `vpn` | (A/CNAME) | Stale/unmanaged record | ~09:14 | Single delete |
| 10 | `echo` | (A/CNAME) | Search → 1 record confirmed deleted | ~09:13 | Single delete |
| 11 | `nbtest` | (A/CNAME) | Search → 1 record confirmed deleted | ~09:15 | Single delete |
| 12 | `_6263144…` (CNAME) | CNAME | Dead ACM validation CNAME—DNS unresolvable (confirmed in `probes.json`) | ~09:15–09:18 | Single delete |

---

### Summary Counts

| Category | Count |
|---|---|
| `OLD_PREFIX` A records (batch) | 5 |
| Stale CNAME (`apples.fitfile.net`) | 1 |
| Stale/unmanaged A or CNAME records (`mn5`, `sonar`, `vpn`, `echo`, `nbtest`) | 5 |
| Dead ACM validation CNAME (`_6263144…`) | 1 |
| Total records deleted | 12 |

---

### Context & Rationale

This work was carried out as part of the Cloudflare DNS audit for `fitfile.net`, scoped under FTFL-630—Review Cloudflare records (Sprint 17, 6–13 May). The audit was driven by a Terraform zone ID mismatch (`cloudflare/locals.tf` was targeting an incorrect zone `d1122d6b9ed6ccbf6ec81d41cb54605a` instead of the live zone `7c978fe256ced38d73c4ba3f5b11a46f`), which meant previously unmanaged records had accumulated outside of IaC control.

Records were identified for deletion using the `dns-audit` tool (`central-services/dns-audit/`), which produced `drift_results.json` and `probes.json`. Deletion verdicts were primarily `OLD_PREFIX` (stale `old-*` naming convention) and dead validation CNAMEs confirmed unresolvable via probe.

---

> Note: The Cloudflare audit log (visible at [Audit logs | FITFILE Account](https://dash.cloudflare.com/7c978fe256ced38d73c4ba3f5b11a46f/audit-log)) records these as `Batch DNS Records` and individual `dns_records` delete events, all attributed to `leon.ormes@fitfile.com` via `dash` context.
