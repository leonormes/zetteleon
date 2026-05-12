---
created: 2026-05-11T12:15:28+00:00
modified: 2026-05-12T13:12:00+00:00
title: DNS Audit Results — fitfile.net Analysis
---

Excellent output from Hermes. Here's a tight analysis of the report and the prioritised actions to close FTFL-630.

---

## DNS Audit Results—fitfile.net Analysis

### One Finding That Blocks Everything Else First

Zone ID mismatch in `cloudflare/locals.tf`—this is the highest-priority code fix because it means Terraform has been targeting the wrong zone (`d1122d6b9ed6ccbf6ec81d41cb54605a`) rather than the live one (`7c978fe256ced38d73c4ba3f5b11a46f`). Until this is corrected, any `terraform apply` for deletions or additions will either fail or touch the wrong zone. Fix this before running anything else.

---

### Action Plan by Priority

#### 🔴 Fix First (unblocks All Terraform work)

Update `cloudflare/locals.tf`:

```hcl
locals {
  zone_id = "7c978fe256ced38d73c4ba3f5b11a46f"  # was: d1122d6b9ed6ccbf6ec81d41cb54605a
  ...
}
```

Run `terraform plan` after this to confirm no unintended changes are introduced by the zone switch.

---

#### 🔴 Delete Now (18 records—FTFL-630 Primary deliverable)

Option A—Terraform (preferred, keeps state clean):

Add a `records_to_delete` concept, or simply remove the entries from `locals.tf` if any were accidentally added. For records that were never in Terraform, delete via the Cloudflare API or UI, then verify `terraform plan` shows no orphan imports needed.

Quickest safe path—delete the 18 via Cloudflare API using the record IDs from `dns-audit/drift_results.json`:

```bash
cd ~/projects/dns-audit
source .env
# Example — loop over IDs from drift_results.json where verdict is OLD_PREFIX or DEAD_UNMANAGED
jq -r '.[] | select(.verdict == "OLD_PREFIX" or .verdict == "DEAD_UNMANAGED") | .id' \
  data/drift_results.json | while read id; do
  curl -s -X DELETE \
    "https://api.cloudflare.com/client/v4/zones/7c978fe256ced38d73c4ba3f5b11a46f/dns_records/$id" \
    -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" \
    -H "Content-Type: application/json" | jq '.success'
done
```

Run dry-first—swap the `DELETE` for a `GET` to confirm you're targeting the right IDs before committing.

The 5 `old-*` records are the clearest wins—all pointing to `51.11.2.213` (old production cluster), all modified June 2024, none in Terraform. No investigation needed.

The 13 DEAD_UNMANAGED worth a quick sanity check before deletion:

- `em6282`, `s1._domainkey`, `s2._domainkey` → SendGrid; the `em6282` and domainkey records are dead (`tcp.reachable: false`) but double-check with whoever owns the SendGrid account that it's genuinely decommissioned before deleting
- `mkuh-prd-4` → modified 2026-03-25, dead—likely a decommissioned MKUH cluster node, safe to delete once confirmed with the customer team
- `_62631442aad08d1ebcf38c223e60e420` → AWS ACM validation CNAME, modified 2025-03-13, dead—safe to delete unless an AWS cert renewal is in flight
- The rest (`vpn`, `vpntesting`, `nbtesting`, `echo`, `apples`, `sonarqube`, `mn5-kube`, `_domainconnect`) are all clearly dead and unowned

---

#### 🔴 Critical Security Fixes (add to Terraform)

Add to `cloudflare/records.tf` or a new `cloudflare/email_security.tf`:

```hcl
resource "cloudflare_dns_record" "spf" {
  zone_id = local.zone_id
  name    = "fitfile.net"
  type    = "TXT"
  content = "v=spf1 include:sendgrid.net -all"
  ttl     = 3600
}

resource "cloudflare_dns_record" "dmarc" {
  zone_id = local.zone_id
  name    = "_dmarc.fitfile.net"
  type    = "TXT"
  content = "v=DMARC1; p=quarantine; rua=mailto:dmarc@fitfile.net"
  ttl     = 3600
}
```

Note: starting with `p=quarantine` rather than `p=reject` is safer until you've verified all legitimate mail flows—you can tighten to `reject` once confident. Also confirm `include:sendgrid.net` is still the right SPF include given the SendGrid records are dead.

---

#### 🟡 Investigate (before Importing or Leaving as-is)

The 79 unmanaged records break down into categories that need a team call:

| Category | Count | Action |
|---|---|---|
| ACME challenge TXT records | ~50 | Keep only the newest per hostname; delete older duplicates |
| NHS provider / customer deployment records | ~15 | Verify against active customer onboarding list; import live ones into Terraform |
| Email / verification records (Microsoft 365, Cloudflare DKIM, Probely, SendGrid tracking) | ~6 | Confirm which are still needed; import survivors |
| Stale ACME (2 flagged explicitly) | 2 | Delete—parent A record is gone |

---

### Summary Scorecard for FTFL-630

| Item                                    | Status                                         |
| --------------------------------------- | ---------------------------------------------- |
| 5 `old-*` records deleted               | ◻ Pending                                      |
| 13 dead unmanaged records deleted       | ◻ Pending (SendGrid + MKUH verification first) |
| Zone ID corrected in `locals.tf`        | ◻ Pending                                      |
| SPF record added to Terraform           | ◻ Pending                                      |
| DMARC record added to Terraform         | ◻ Pending                                      |
| Stale ACME TXT records removed          | ◻ Pending                                      |
| 79 unmanaged records reviewed with team | ◻ Scheduled                                    |

The zone ID fix → 18 deletions → SPF/DMARC is a clean run that could close the core ticket in a single focused session. The 79 unmanaged records review is the longer tail but not a blocker for closing FTFL-630.
