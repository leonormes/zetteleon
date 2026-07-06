---
created: 2026-02-21T15:07:26+00:00
modified: 2026-07-04T10:50:40+00:00
permalink: llmeon/30-library/ops/kb-vso-stale-credentials-logic
service: vso
tags: [security, triage, vault]
title: kb_vso_stale_credentials_logic
type: kb
---

## KB: VSO Stale Credentials Logic

### The "Overwrite" Problem

A common failure mode in VSO is where a secret becomes stale (e.g., `401 Unauthorized`) even though the operator logs are green.

#### Root Cause Flow

1. Vault issues dynamic credentials with a finite TTL.
2. The K8s Secret is manually edited or modified by another tool.
3. The Vault lease expires, invalidating the credentials upstream.
4. VSO attempts to sync new credentials, but if `spec.destination.overwrite` is `false` (default in older versions), it silently fails to write to avoid overwriting user changes.

#### Detection

If the Secret `creationTimestamp` is significantly older than the Vault lease renewal time, and credentials are failing, you are in an "overwrite block" state.

#### Solution

1. Patch `overwrite: true`.
2. Delete the Secret to force a clean reconciliation.
