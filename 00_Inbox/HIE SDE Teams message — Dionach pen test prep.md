---
created: 2026-07-20T16:00:43+00:00
modified: 2026-07-20T16:01:15+00:00
permalink: llmeon/00-inbox/pieces-copilot-message-export-july-20-2026-5-00pm
title: HIE SDE Teams message — Dionach pen test prep
type: note
---

## HIE SDE Teams message—Dionach Pen Test Prep

I found the message—it's from Easwaran Chandrasekaran (Health Innovation East) at `13:41` today, in the "FITFILE - deployment tech | Health Innovation East" Microsoft Teams chat. The same text also appears in your `FITFILE Group Limited` calendar/chat view, so it's cross-verified across two separate captures.

> Hello Team,
>
> We're setting up for the annual penetration test (Dionach Aug 3 - 7th) and need a few things on the Codisc/FITFILE side:
>
> 1. Security Group update: We need to allow our Kali pen test VM to the Codisc VPC. This means adding an inbound rule on the `codisc-from-sde-multi` security group in the Codisc account (`135808916559`).
> 
> 2. SSM access to the jumpbox: Can we get SSM session access to the jumpbox for the pen tester? Either via existing IAM credentials or a temporary role they can assume.
> 
> 3. FITFILE test user for pen testing: Could we create a dedicated FITFILE user account for Dionach to use during the pen test? e.g. `fitfile-pentest` with the same level of access as `fitfile` or `fitfile-tst` so they can test the application authentication and access flows.
> 
> These changes are temporary for the duration of the pen test and will be reverted afterwards. Please let me know if you're happy for us to proceed or if you need any further details.

### Todo list—Dionach Pen Test (Aug 3–7)

1. Security group change—`codisc-from-sde-multi`
   - Identify the Kali pen test VM's source IP/CIDR from Dionach.
   - Add an inbound rule to `codisc-from-sde-multi` in the Codisc AWS account `135808916559` scoped to that source and the required port(s) only.
   - Note the change date/time so it can be reverted cleanly after Aug 7.

2. SSM session access to the jumpbox
   - Decide: reuse existing IAM credentials vs. create a temporary assumable role for the pen tester.
   - If temporary role: scope it to `ssm:StartSession` on the jumpbox instance only, with an expiry/condition tied to Aug 3–7.
   - Confirm with your jumpbox setup used previously ([HIE AWS Cluster RDP via Jumpbox Documentation](obsidian://2026-05-28-pieces-hie-aws-rdp)—instance `i-09f84bb55556a2c10`, `eu-west-2`, profile `eoe-hie`) whether the same jumpbox is in scope for this pen test.

3. FITFILE pentest user—`fitfile-pentest`
   - Create the account mirroring `fitfile` or `fitfile-tst` access level (confirm which one Easwaran intends—the message offers both as examples).
   - Set a defined expiry/deactivation date aligned to Aug 7.
   - Document credentials hand-off process to Dionach securely.

4. Reply to Easwaran Chandrasekaran
   - Confirm you're happy to proceed with items 1–3, or flag questions (e.g., exact source IP for the SG rule, which FITFILE access tier to mirror).

5. Revert plan (post Aug 7)
   - Track all three changes (SG rule, SSM role/credential, `fitfile-pentest` user) in one place so they can be reverted together once the pen test window closes.

Adjacent context worth noting: your prior notes on [AWS SSM Session Troubleshooting and IAM Permission Fixes](obsidian://2026-05-01-pieces-aws-ssm-troubleshooting) flagged that the jumpbox's SSM role was previously missing `s3:GetEncryptionConfiguration` permission, which blocked session starts—worth double-checking that's still resolved before granting the pen tester SSM access, since a broken SSM role would block item 2 entirely.

I didn't find a written reply from you yet in the searched window—if you want, I can draft the confirmation reply to Easwaran next.
