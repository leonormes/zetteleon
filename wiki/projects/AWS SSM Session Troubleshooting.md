---
title: AWS SSM Session Troubleshooting
wiki_type: dossier
entity_kind: project
created: 2026-05-01T22:00:00+00:00
modified: 2026-05-01T22:00:00+00:00
tags: [wiki, dossier]
sources:
  - raw/2026-05-01-pieces-aws-ssm-troubleshooting
---

## Summary

Troubleshooting session for AWS Systems Manager (SSM) session login failures. The root cause was identified as missing `s3:GetEncryptionConfiguration` permission on the SSM role's associated IAM policy, preventing session logs from being written to the S3 bucket.

## Key Facts

- SSM session login fails with error indicating the role lacks permission to read S3 bucket encryption settings.
  > "The root cause seems to be that the jumpbox's SSM role doesn't have permission to read the bucket's encryption settings for the logs. This lack of permission prevents the SSM session from starting." — [[raw/2026-05-01-pieces-aws-ssm-troubleshooting]] (Pieces: 129885bd-6e65-48ad-b94c-b4f8965375f1)

- The specific missing permission is `s3:GetEncryptionConfiguration` which is required for SSM to write session logs to the S3 bucket.
  > "the associated role lacks the 's3:GetEncryptionConfiguration' permission, which is necessary" — [[raw/2026-05-01-pieces-aws-ssm-troubleshooting]] (Pieces: b36b382d-7259-45ce-b157-1b37e11c1f29)

- Suggested fix: add `s3:GetEncryptionConfiguration` permission to the IAM role policy attached to the SSM role.
  > "I suggest straight up adding the s3:GetEncryptionConfiguration permission to the role" — [[raw/2026-05-01-pieces-aws-ssm-troubleshooting]] (Pieces: 129885bd-6e65-48ad-b94c-b4f8965375f1)

- AWS CLI commands provided for diagnosing and fixing IAM role permissions:
  - List attached policies: `aws iam list-attached-role-policies --role-name <role-name>`
  - Simulate principal policy to verify permissions: `aws iam simulate-principal-policy`
  > "I'm outlining some commands to check or fix IAM role issues, like listing attached policies or simulating the principal policy to verify permissions for 's3:GetEncryptionConfiguration.'" — [[raw/2026-05-01-pieces-aws-ssm-troubleshooting]] (Pieces: a47a239c-3df0-4169-8a75-ea59e8b10c54)

- Session encryption uses AWS KMS as indicated by the session start message.
  > "This session is encrypted using AWS KMS." — [[raw/2026-05-01-pieces-aws-ssm-troubleshooting]] (Pieces: 43b36746-dbfb-4018-9dd0-c40db9cc0efc)

- SSM sends session logs to an S3 bucket for logging/auditing purposes, which requires the role to have appropriate S3 permissions.
  > "I'm looking at how SSM sends session logs to an S3 bucket, which might be for logging purposes." — [[raw/2026-05-01-pieces-aws-ssm-troubleshooting]] (Pieces: b36b382d-7259-45ce-b157-1b37e11c1f29)

## Timeline

- **2026-05-01 ~13:18 UTC**: SSM session troubleshooting session captured in Pieces LTM (5 assets).
  > Session assets captured between 13:18:10 and 13:19:39 UTC — [[raw/2026-05-01-pieces-aws-ssm-troubleshooting]]

## Connections

- [[wiki/concepts/AWS IAM Permissions]] _(to be created)_
- [[wiki/concepts/SSM Session Manager]] _(to be created)_

## Contradictions

_(none identified)_

## Open Questions

- Which specific S3 bucket is configured for SSM session logs?
- What is the name of the IAM role attached to the jumpbox instance?
- Are there other S3 permissions missing beyond `s3:GetEncryptionConfiguration`?
