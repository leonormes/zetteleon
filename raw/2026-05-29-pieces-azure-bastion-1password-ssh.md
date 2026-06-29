---
title: Azure Bastion SSH — 1Password SSH Agent Fix for AAD Authentication
created: 2026-05-29 19:54:32+00:00
source: pieces-ltm
pieces_ids:
- 9dcbcf77-e097-4506-885a-de3c4bae68b0
tags:
- raw
- pieces
permalink: llmeon/raw/2026-05-29-pieces-azure-bastion-1password-ssh
---

## Asset (Pieces: 9dcbcf77-e097-4506-885a-de3c4bae68b0)

Good context — that changes the fix. `ssh-add -D` won't help you because your keys are managed by **1Password's SSH agent**, not the standard macOS `ssh-agent`. Flushing the standard agent has no effect on what 1Password offers.

Memory confirms you have a `~/.config/1Password/ssh/agent.toml` config file (your 1Password SSH agent configuration). The real fix is there, or bypassing the agent entirely for this AAD connection.

---

## Two options for 1Password users

### Option 1 — Bypass the 1Password agent entirely for this call (quickest)

Since `--auth-type AAD` doesn't use your personal SSH keys at all, you can tell SSH to use no identity agent:

```bash
az network bastion ssh \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id /subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox \
  --auth-type "AAD" \
  -- -o IdentityAgent=none
```

`IdentityAgent=none` tells SSH to ignore the 1Password agent socket entirely for this connection. The AAD certificate injected by `az` still works because it's passed via `-i`, not the agent.

### Option 2 — Limit which keys 1Password offers (permanent fix)

Edit `~/.config/1Password/ssh/agent.toml` to explicitly scope which keys are offered and in what order, reducing the number of attempts before the server disconnects:

```toml
[[ssh-keys]]
vault = "Private"
item = "FITFILEJumpbox"   # only offer the relevant key
```

This prevents 1Password from offering every key in your vault to every server.

---

Option 1 is the right call for AAD-authenticated Bastion connections specifically — your personal keys are irrelevant to that auth flow anyway.