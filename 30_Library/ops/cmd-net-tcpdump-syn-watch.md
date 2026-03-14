---
created: 2026-02-19T15:18:30+00:00
hop_level: cluster
modified: 2026-03-14T11:10:11+00:00
tags: [atomic, network, packets]
target_service: network
title: cmd-net-tcpdump-syn-watch
tool: tcpdump
type: atomic_command
---

## Capture Outgoing SYN Retransmissions

### 🎯 Intent

Watch the raw packet flow to prove that SYNs are leaving the pod but no responses (SYN/ACK or RST) are returning. This is the "smoking gun" for ingress filtering.

---

### 🌍 Execution Context

Run from:

- [x] Inside cluster (netshoot pod) - REQUIRES SECOND TERMINAL

---

### ⚡ Action

```bash
export TARGET_IP=<target_ip_address>

tcpdump -nn -i any host $TARGET_IP and tcp port <port>
```

#### Placeholders

- ``—Destination IP
- `<port>`—Target port (e.g., 443)

---

### ✅ Verification

Failure Signature:

- Multiple `Flags [S]` (SYN) leaving with increasing timestamps.
- No `Flags [S.]` (SYN/ACK) or `Flags [R]` (RST) coming back.

---

### 🔗 Related

- [[pb-cross-cluster-connectivity-triage]]
