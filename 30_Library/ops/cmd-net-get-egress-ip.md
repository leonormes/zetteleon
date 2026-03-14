---
created: 2026-02-17T08:49:06+00:00
hop_level: cluster
modified: 2026-03-14T11:10:11+00:00
tags: [atomic, egress, network]
target_service: network
title: cmd-net-get-egress-ip
tool: curl
type: atomic_command
---

## Identify Pod Egress IP

### 🎯 Intent

Determine the public IP address that external services see when your pod makes an outbound request. This is critical for allowlisting on destination firewalls.

---

### 🌍 Execution Context

Run from:

- [x] Inside cluster (netshoot pod)
- [x] Local machine

---

### ⚡ Action

```bash
curl -s ifconfig.me
```

---

### ✅ Verification

Expected signal:

- A single public IPv4 address (e.g., `13.42.119.194`).

---

### 🔗 Related

- [[pb-cross-cluster-connectivity-triage]]
