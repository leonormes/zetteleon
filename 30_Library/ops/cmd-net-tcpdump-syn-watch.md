---
type: atomic_command
tool: tcpdump
hop_level: cluster
target_service: network
tags: #atomic #network #packets
---

# Capture Outgoing SYN Retransmissions

## 🎯 Intent
Watch the raw packet flow to prove that SYNs are leaving the pod but no responses (SYN/ACK or RST) are returning. This is the "smoking gun" for ingress filtering.

---

## 🌍 Execution Context
Run from:
- [x] Inside cluster (netshoot pod) - REQUIRES SECOND TERMINAL

---

## ⚡ Action

```bash
export TARGET_IP=<target_ip_address>

tcpdump -nn -i any host $TARGET_IP and tcp port <port>
```

### Placeholders
- `` — Destination IP
- `<port>` — Target port (e.g., 443)

---

## ✅ Verification
Failure Signature:
- Multiple `Flags [S]` (SYN) leaving with increasing timestamps.
- No `Flags [S.]` (SYN/ACK) or `Flags [R]` (RST) coming back.

---

## 🔗 Related
- [[pb-cross-cluster-connectivity-triage]]
