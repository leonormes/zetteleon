---
type: atomic_command
tool: nmap
hop_level: cluster
target_service: network
tags: #atomic #network #security
---

# Check Port Filtered Status (Nmap)

## 🎯 Intent
Determine if a port is being silently dropped by a firewall (`filtered`) or explicitly rejected (`closed`).

---

## 🌍 Execution Context
Run from:
- [x] Inside cluster (netshoot pod)
- [ ] Local machine

---

## ⚡ Action

```bash
nmap -Pn -p <ports> --reason <target_ip>
```

### Placeholders
- `<ports>` — Comma-separated ports (e.g., `80,443`)
- `<target_ip>` — Destination IP

---

## ✅ Verification
- `STATE: open` + `REASON: syn-ack` — Success.
- `STATE: filtered` + `REASON: no-response` — Firewall is dropping packets (silent drop).
- `STATE: closed` + `REASON: conn-refused` — Host reachable, but service not listening.

---

## 🔗 Related
- [[pb-cross-cluster-connectivity-triage]]
