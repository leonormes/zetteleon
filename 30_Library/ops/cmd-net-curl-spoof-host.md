---
type: atomic_command
tool: curl
hop_level: local
target_service: network
tags: #atomic #network #ingress #spoof
---

# Spoof Host Header (Resolve Bypass)

## 🎯 Intent
Test if an application is healthy behind an ingress controller by bypassing public DNS and firewalls. This maps a hostname to a specific internal IP (e.g., Ingress Controller) for the duration of the request.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with VPN/Tunnel)
- [x] Jumpbox

---

## ⚡ Action

```bash
curl -v -k --resolve <hostname>:<port>:<target_ip> https://<hostname>
```

### Placeholders
- `<hostname>` — The public DNS name (e.g., `nnuh-prod-1.fitfile.net`)
- `<port>` — Usually `443`
- `<target_ip>` — The internal IP of the Ingress Controller or Load Balancer

---

## ✅ Verification
Expected signal:
- HTTP 200/302/404 from the actual application server.
- Proves the path from Ingress -> Pod is working.

---

## 🔗 Related
- [[pb-cross-cluster-connectivity-triage]]
