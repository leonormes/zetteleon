---
type: atomic_command
tool: mtr
hop_level: cluster
target_service: network
tags: #atomic #network #triage
---

# TCP Path Trace (MTR)

## 🎯 Intent
Perform a path trace using TCP SYN packets to identify exactly which hop is dropping traffic. This bypasses ICMP filtering common in cloud environments.

---

## 🌍 Execution Context
Run from:
- [x] Inside cluster (netshoot pod)

---

## ⚡ Action

```bash
export TARGET_IP=<target_ip_address>

mtr -n -T -P <port> -r -c 10 $TARGET_IP
```

### Placeholders
- `<port>` — Target port (e.g., 443)
- `` — Destination IP or hostname

---

## ✅ Verification
Expected signal:
- 0% loss until the destination.
- If it stops at a specific hop with 100% loss (e.g., Hop 11 `???`), that is your drop point.

---

## 🔗 Related
- [[cmd-net-traceroute-tcp]]
- [[pb-cross-cluster-connectivity-triage]]
