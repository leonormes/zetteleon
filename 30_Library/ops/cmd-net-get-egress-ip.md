---
type: atomic_command
tool: curl
hop_level: cluster
target_service: network
tags: #atomic #network #egress
---

# Identify Pod Egress IP

## 🎯 Intent
Determine the public IP address that external services see when your pod makes an outbound request. This is critical for allowlisting on destination firewalls.

---

## 🌍 Execution Context
Run from:
- [x] Inside cluster (netshoot pod)
- [x] Local machine

---

## ⚡ Action

```bash
curl -s ifconfig.me
```

---

## ✅ Verification
Expected signal:
- A single public IPv4 address (e.g., `13.42.119.194`).

---

## 🔗 Related
- [[pb-cross-cluster-connectivity-triage]]
