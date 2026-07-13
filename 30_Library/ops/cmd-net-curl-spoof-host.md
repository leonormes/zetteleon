---
created: 2026-02-19T15:18:30+00:00
hop_level: local
modified: 2026-07-13T08:45:26+00:00
permalink: llmeon/30-library/ops/cmd-net-curl-spoof-host
tags: [atomic, ingress, network, spoof]
target_service: network
title: cmd-net-curl-spoof-host
tool: curl
---

## Spoof Host Header (Resolve Bypass)

### 🎯 Intent

Test if an application is healthy behind an ingress controller by bypassing public DNS and firewalls. This maps a hostname to a specific internal IP (e.g., Ingress Controller) for the duration of the request.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with VPN/Tunnel)
- [x] Jumpbox

---

### ⚡ Action

```bash
export TARGET_IP=<target_ip_address>

curl -v -k --resolve <hostname>:<port>:$TARGET_IP https://<hostname>
```

#### Placeholders

- `<hostname>`—The public DNS name (e.g., `nnuh-prod-1.fitfile.net`)
- `<port>`—Usually `443`
- ``—The internal IP of the Ingress Controller or Load Balancer

---

### ✅ Verification

Expected signal:

- HTTP 200/302/404 from the actual application server.
- Proves the path from Ingress -> Pod is working.

---

### 🔗 Related

- [[pb-cross-cluster-connectivity-triage]]
