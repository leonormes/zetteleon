---
created: 2026-02-19T15:18:30+00:00
hop_level: cluster
modified: 2026-08-13T10:53:53+00:00
permalink: llmeon/30-library/ops/cmd-net-nmap-check-filtered
tags: [atomic, network, security]
target_service: network
title: cmd-net-nmap-check-filtered
tool: nmap
---

## Check Port Filtered Status (Nmap)

### 🎯 Intent

Determine if a port is being silently dropped by a firewall (`filtered`) or explicitly rejected (`closed`).

---

### 🌍 Execution Context

Run from:

- [x] Inside cluster (netshoot pod)
- [ ] Local machine

---

### ⚡ Action

```bash
export TARGET_IP=<target_ip_address>

nmap -Pn -p <ports> --reason $TARGET_IP
```

#### Placeholders

- `<ports>`—Comma-separated ports (e.g., `80,443`)
- ``—Destination IP

---

### ✅ Verification

- `STATE: open` + `REASON: syn-ack`—Success.
- `STATE: filtered` + `REASON: no-response`—Firewall is dropping packets (silent drop).
- `STATE: closed` + `REASON: conn-refused`—Host reachable, but service not listening.

---

### 🔗 Related

- [[pb-cross-cluster-connectivity-triage]]
