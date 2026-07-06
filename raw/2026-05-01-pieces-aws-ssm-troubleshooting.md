---
created: 2026-05-01T22:02:15+00:00
modified: 2026-07-04T10:50:27+00:00
permalink: llmeon/raw/2026-05-01-pieces-aws-ssm-troubleshooting
pieces_ids: [" 129885bd-6e65-48ad-b94c-b4f8965375f1", " 43b36746-dbfb-4018-9dd0-c40db9cc0efc", " 8bb09341-292b-4eb4-99eb-ff58e973f670", " a47a239c-3df0-4169-8a75-ea59e8b10c54", " b36b382d-7259-45ce-b157-1b37e11c1f29"]
source: pieces-ltm
tags: [pieces, raw]
title: 2026-05-01-pieces-aws-ssm-troubleshooting
---

## AWS SSM Session Troubleshooting—Pieces LTM Capture

Captured: 2026-05-01 22:02 UTC

Session focused on diagnosing SSM session login failures related to S3 bucket encryption permissions.

---

### Asset 1 (Pieces: 43b36746-dbfb-4018-9dd0-c40db9cc0efc)

Captured: 2026-05-01T12:00:01.165858Z

Can you tell what is wrong with this ssm session login aws ssm start-session --target i-0c1d974fcac60d438

Starting session with SessionId: oliver.rushton@fitfile.com-qtg64hh8su5tazsf34ogban7va

This session is encrypted using AWS KMS.

SessionId: oliver.rushton@fitfile.com-qtg64hh8su5tazsf34ogban7va: Couldn't start the session because we are unable to validate encryption on Amazon S3 bucket. Error: AccessDenied: User: arn:aws:sts::135808916559:assumed-role/eoe-test-codisc-jumpbox-ssm-role/i-0c1d974fcac60d438 is not authorized to perform: s3:GetEncryptionConfiguration on resource: "arn:aws:s3:::aws-accelerator-central-logs-381491886943-eu-west-2" because no identity-based policy allows the s3:GetEncryptionConfiguration action

status code: 403, request id: 1KR81ZMFYGCXGF5A, host id: ZshD/1BaNpWYvmz61qPpalIRoHKL2vslEh+RfueF5hC4XAC4ee60AcB9799re/ARfGxZ/XofIoOsmkN67s44sNVgRJcy8xi9

---

### Asset 2 (Pieces: b36b382d-7259-45ce-b157-1b37e11c1f29)

Captured: 2026-05-01T12:00:26.954976Z

Analyzing S3 bucket permissions

I'm looking at how SSM sends session logs to an S3 bucket, which might be for logging purposes. The error indicates that the associated role lacks the "s3:GetEncryptionConfiguration" permission, which is necessary for reading bucket encryption settings, especially if SSE-KMS is involved. To fix this, I need to update the IAM policy for the role to include this permission. I should also verify that the session uses the correct credentials and check for any permission boundaries or missing policies.

---

### Asset 3 (Pieces: a47a239c-3df0-4169-8a75-ea59e8b10c54)

Captured: 2026-05-01T12:00:34.744985Z

Providing AWS commands and recommendations

I'm outlining some commands to check or fix IAM role issues, like listing attached policies or simulating the principal policy to verify permissions for "s3:GetEncryptionConfiguration." If updates are required, I can use "put-user-policy" or "put-role-policy."

The recommended approach is to ensure the jumpbox role has minimal permissions to start an SSM session, including permissions for S3 actions. It's also important to adjust for any region differences if necessary. After any fixes, I should rerun commands to check session functionality and examine CloudTrail logs. If changes can't be made, contacting the IAM admin is a good alternative.

---

### Asset 4 (Pieces: 129885bd-6e65-48ad-b94c-b4f8965375f1)

Captured: 2026-05-01T12:00:41.663911Z

Diagnosing the SSM role issue

The root cause seems to be that the jumpbox's SSM role doesn't have permission to read the bucket's encryption settings for the logs. This lack of permission prevents the SSM session from starting.

I suggest straightforwardly adding the "s3:GetEncryptionConfiguration" permission to the policy for the service principal. To resolve this, I'd recommend the following steps:

- Diagnosis: The error shows insufficient IAM permissions on the S3 bucket's encryption config.
- Action: Update the IAM role policy to include "s3:GetEncryptionConfiguration" for the bucket "arn:aws:s3:::aws-accelerator-central-logs-381491886943-eu-west-2."Diagnosing the S3 permission issue

First, let's confirm the bucket name from the error. To address the issue, I can provide commands like "aws iam put-role-policy" to update the IAM role.

The error indicates that the role needs the "s3:GetEncryptionConfiguration" permission, which is valid for retrieving the bucket's encryption configuration. If the bucket is region-specific, ensure the ARN includes the region suffix.

To test the fix, rerun the start-session command. If that fails, try "aws s3api get-bucket-encryption" to verify. If issues persist, it may be due to policy propagation time, so waiting a few minutes could help.

---

### Asset 5 (Pieces: 8bb09341-292b-4eb4-99eb-ff58e973f670)

Captured: 2026-05-01T13:18:12.806544Z

Organizing validation info

I think I need to create a table to summarize the validation details. There are several components to verify, including Storage Accounts, private endpoints, DNS configurations, and vault settings. I notice some areas, like the vault's immutability feature, show mismatches that need addressing. I'll also need to include notes on privilege levels and resource protection configurations. There's a need to cross-check the existing resources, especially ensuring the protection instance names match appropriately. This should streamline my review process!

---
