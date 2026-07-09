---
created: 2026-07-09T10:08:42+00:00
modified: 2026-07-09T11:34:44+00:00
title: pieces_copilot_message_export_july_9_2026_11_08am
---

_Shared Message from Pieces (<https://pieces.app>) by Leon Ormes (leonormes@gmail.com) on Thursday Jul 9, 2026 - 11:08 AM_
---

## Investigation Plan: Eoe-sde-codisc IAM Unused Access Analyzer Review (135808916559)

### What Your LTM Confirms

The email itself is now in your memory—a Spark Desktop message titled "IAM Unused Access Review: eoe-sde-codisc Account", forwarded via Susannah at 09:38 on 9 Jul with an "IAM User Review" flag from Keiran Raine to Adebambo Ayileka, and a note from Susannah: "Please could you give this your earliest attention. We need to respond to this today, please." This is the same email content you pasted into your query.

Beyond the email, your workstream shows substantial recent hands-on work in this exact AWS account, but on a different workstream than the two flagged users:

- HIE DNS migration—extensive Terraform/CLI activity on 19 Jun in Ghostty (`excellent-platypus | Gather AWS infrastructure state for HIE DNS migration`), using `AWS_PROFILE=eoe-hie` against account `135808916559`, working from `/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/Clusters/eoe/Test/hie-test-34/providers.tf`. This confirms `hie-test-34` / `hie-prod-35` are the Terraform Cloud workspace names for this account, and that Terraform Cloud manages at least some of this account's infra—a strong candidate source for where `tf-deployment`'s permissions are actually consumed.
- EBS CSI Driver IAM policy migration—a coordinated effort with Keiran Raine (Health Innovation East) across 19 Jun and 22 Jun, detaching `AmazonEBSCSIDriverPolicy` and attaching `AmazonEBSCSIDriverEKSClusterScopedPolicy` on role `eoe-sde-codisc-AmazonEKS_EBS_CSI_DriverRole`. This shows the SDE/HIE team actively right-sizing IAM policies in this account already—directly relevant precedent for the least-privilege ask on `tf-deployment`.
- Keiran Raine's message from that thread is telling for context on ownership: "we on the SDE team manage many of the permissions for these accounts through LZA, confirmation of what is and isn't needed is the key item of work."—i.e., permissions in `eoe-sde-codisc` are governed by AWS Landing Zone Accelerator (LZA), which matters for how you'd actually action a policy scope-down (LZA-managed baselines vs. account-local IAM edits).
- Console evidence confirms account access: a Chrome session on 25 Jun hit `https://eu-west-2.console.aws.amazon.com/eks/home?region=eu-west-2` with "Recently visited: eoe-sde-codisc (135808916559)" under role `DiscoveryEngineeringAccess/leon.ormes@fitfile.com`.

None of this touches the two specific IAM users named in the Analyzer email—`eoe-sde-codisc-s3-access-user` or `tf-deployment`—by name, in any search pass (users, ARNs, terraform state, or S3 access searches all returned zero direct hits).

### What's Missing (Gaps to close before yOu cAn rEspond to Keiran/Adebambo)

User 1—`eoe-sde-codisc-s3-access-user`

- No record of what this user is _for_. No Terraform resource, no chat thread, no console screenshot references this ARN or username at all.
- Unknown: who created it, which pipeline/script/service account consumes its S3 access, and whether it's a legacy artifact from a completed migration.

User 2—`tf-deployment`

- No Terraform state file, `.tf` source, or IAM policy document for this specific IAM user has surfaced—only the _workspace names_ (`hie-test-34`, `hie-prod-35`) and the fact that Terraform Cloud drives this account's deployments.
- No confirmation of whether `tf-deployment`'s credentials are the ones actually used by the `hie-test-34`/`hie-prod-35` TFC workspaces, or by a separate CI/CD pipeline.
- No breakdown in memory of why CloudWatch Logs, EC2 Auto Scaling, or KMS permissions were ever granted—i.e., no historical PR/commit showing those services being provisioned via this user's policy.

### Concrete next Steps

1. Confirm `tf-deployment` ↔ Terraform Cloud linkage. Check the TFC workspace settings for `hie-test-34` and `hie-prod-35` (and any prod workspace for `eoe-sde-codisc` proper, not just the HIE test/prod naming) for the AWS credentials/role each workspace assumes. If `tf-deployment`'s access key is the one configured there, that confirms it's live and in-scope for a least-privilege pass rather than a candidate for removal.
2. Search the Terraform source repo directly (`/Volumes/DAL/Fitfile/gitlab/FITFILE/Deployment/…` per your local checkout) for `tf-deployment` in `.tf`/`.tfvars`/IAM policy JSON files, and for the specific unused actions flagged (CloudWatch Logs, EC2 Auto Scaling, KMS) to see which resource blocks originally required them—this tells you whether those were needed once (e.g., during initial cluster bring-up) and are now dead weight.
3. Ask Keiran Raine / the SDE team directly whether the account's permissions being "managed through LZA" (per their own message) means `tf-deployment`'s policy is templated centrally—if so, a scope-down may need to go through an LZA baseline change rather than a direct IAM edit, which changes your response timeline to Adebambo.
4. For `eoe-sde-codisc-s3-access-user`, check CloudTrail (not in LTM—needs AWS console access) for the last actual API call under that user, and cross-reference against known S3-consuming pipelines (e.g., the `fitfile-s3-prd` / DQ report upload flow referenced in the 14 May chat with Oliver Rushton, which uses a _different_ user assuming `arn:aws:iam::339713007003:role/dlz-prd-writer-codisc`—worth ruling out as unrelated, but check it isn't a legacy sibling).
5. Draft the reply to Susannah/Keiran/Adebambo only after steps 1-4 close the ownership gap—the email flagged "We need to respond to this today," so if the TFC/LZA checks can't complete in time, consider an interim reply acknowledging receipt and committing to a dated follow-up with the least-privilege findings, rather than guessing at scope-down actions without confirmed usage data.

Want me to draft that interim acknowledgment email to Susannah/Keiran now, or wait until you've pulled the TFC workspace credentials and repo grep results?
