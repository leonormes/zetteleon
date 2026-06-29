---
created: 2026-02-19 15:18:30+00:00
hop_level: cluster
modified: 2026-03-14 11:10:11+00:00
tags:
- atomic
- network
- triage
target_service: network
title: cmd-net-mtr-tcp
tool: mtr
type: atomic_command
permalink: llmeon/30-library/ops/cmd-net-mtr-tcp
---

## TCP Path Trace (MTR)

### 🎯 Intent

Perform a path trace using TCP SYN packets to identify exactly which hop is dropping traffic. This bypasses ICMP filtering common in cloud environments.

---

### 🌍 Execution Context

Run from:

- [x] Inside cluster (netshoot pod)

---

### ⚡ Action

```bash
export TARGET_IP=<target_ip_address>

mtr -n -T -P <port> -r -c 10 $TARGET_IP
```

#### Placeholders

- `<port>`—Target port (e.g., 443)
- ``—Destination IP or hostname

---

### ✅ Verification

Expected signal:

- 0% loss until the destination.
- If it stops at a specific hop with 100% loss (e.g., Hop 11 `???`), that is your drop point.

---

### 🔗 Related

- [[cmd-net-traceroute-tcp]]
- [[pb-cross-cluster-connectivity-triage]]