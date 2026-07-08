---
title: pieces_copilot_message_export_jm
type: note
permalink: llmeon/00-inbox/pieces-copilot-message-export-jm
---

*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Wednesday Jul 8, 2026 - 10:36 AM*
---
## Cannot get secret of a locked object — SpiceDB/zed error

That exact error surfaced **twice today** in your workstream, both around 09:15–09:26 UTC (10:15–10:26 your local time):

- **10:29 AM** — an Obsidian clipboard capture titled "HEAD - 2026-07-07 1224" containing the identical command block you pasted (`kubectl port-forward`, `zed relationship read fitfile/tenant:DcgF9Lb8gRArAIIkbrYaGKvQaaNbRfMX | grep "auth0|633adad9991af2b9ec7446c1"`) with the error `{"level":"error","error":"Cannot get secret of a locked object","time":"2026-07-08T09:15:45Z","message":"terminated with errors"}`.
- **10:28 AM** — a Ghostty terminal session on host `polite-clarinet | hie-sde-v2 (ssh)` running `zed relationship read schema`, logging `9:26AM ERR terminated with errors error="Cannot get secret of a locked object"`.

So this is not a one-off — it hit you on **two separate hosts** (`hie-sde-v2` via SSH, and whatever host produced the Obsidian-captured session) within about 10 minutes of each other, both while running `zed relationship read` against `fitfile` tenants.

### Root cause, per your own prior runbook

Yesterday (Jul 7, ~12:46 PM) you wrote a runbook in Obsidian — **"Runbook: Auditing SpiceDB Permissions via Zed CLI on Headless Jumpboxes"** — that documents a closely related but distinct failure mode:

> "When running on a headless Linux jumpbox, the `zed context set` command will likely fail with: `error="Object does not exist at path "/""`. This happens because the OS lacks a desktop keyring (D-Bus secret service) to store the pre-shared key. **Do not use `zed context set`.** Instead, export the connection details as environment variables."

That runbook's fix was to bypass the keyring entirely by exporting `ZED_ENDPOINT` / `ZED_TOKEN` / `ZED_INSECURE`, which is exactly what your pasted log shows you doing. The `"Cannot get secret of a locked object"` error is a **different symptom of the same underlying keyring/D-Bus-secret-service problem** — rather than "no secret service found" (missing), this is "a secret service exists but the keyring/collection is locked" (e.g., a `gnome-keyring` / `kwallet` collection sitting in a locked state on the jumpbox, likely surfaced by whatever `zed` subcomponent still probes the OS secret store even when `ZED_TOKEN` is exported).

This lines up with a Gemini conversation from yesterday, **[Troubleshooting SpiceDB Zed CLI Secret Store Error](https://portal.azure.com/#@cuhfoundationtrust.onmicrosoft.com/resource/subscriptions/709f3d57-b6d7-48c6-8252-6b1c1174a541/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox/serialConsole)**, where you asked Gemini about the D-Bus secret service failure and got the "no valid secrets service at root path `/`" explanation.

### Cross-checked, but not fully resolved

I searched narrower terms (`"locked object"`, `"Cannot get secret of a locked object"`, `"keyring D-Bus secret service"`) to see if you'd already found a fix for the *locked* variant specifically — that search returned no hits; the only prior context I could ground is the "missing keyring" variant from your own runbook, not a documented fix for "locked." I could not confirm you've resolved this specific locked-object error yet.

### What's likely still open

- You have the `ZED_TOKEN`/`ZED_ENDPOINT`/`ZED_INSECURE` env-var workaround from yesterday's runbook, but that workaround was targeted at the "keyring missing" error, not "keyring locked" — worth checking whether `zed` is still attempting a keyring handshake even with env vars set (possible zed CLI version behavior), or whether the jumpbox's keyring daemon needs unlocking/disabling separately (e.g. `gnome-keyring-daemon --unlock` or ensuring `no-pkcs11` / disabling secret-service lookups).
- This happened on tenant `fitfile/tenant:DcgF9Lb8gRArAIIkbrYaGKvQaaNbRfMX` — worth confirming whether other tenant IDs you audited yesterday (e.g. `CRxdoV6n2KhZDAU9fCqzCXz56PrfYtYN`) hit the same error or only this one.

Want me to dig further into the `hie-sde-v2` Ghostty session for any follow-up troubleshooting steps you may have already taken after the 9:26 AM error?