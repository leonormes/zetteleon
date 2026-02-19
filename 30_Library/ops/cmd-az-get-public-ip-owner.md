---
type: atomic_command
tool: az
hop_level: local
target_service: azure
tags: #atomic #azure #network
---

# Identify Azure Public IP Owner

## 🎯 Intent
Verify if a specific Public IP address belongs to your subscription and which resource (Load Balancer, NAT Gateway, etc.) it is attached to.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (authenticated to AZ CLI)

---

## ⚡ Action

```bash
az network public-ip list --query "[?ipAddress=='<target_ip>']"
```

### Placeholders
- `<target_ip>` — The IP address to investigate (e.g., `195.171.151.154`)

---

## ✅ Verification
Expected signal:
- JSON block containing `id`, `resourceGroup`, and `ipConfiguration`.
- If empty, the IP is likely external or in a different subscription.

---

## 🔗 Related
- [[sot-az-aks-networking]]
