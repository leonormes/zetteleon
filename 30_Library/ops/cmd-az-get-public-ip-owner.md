---
created: 2026-02-19T15:18:30+00:00
hop_level: local
modified: 2026-07-13T08:52:58+00:00
permalink: llmeon/30-library/ops/cmd-az-get-public-ip-owner
tags: [atomic, azure, network]
target_service: azure
title: cmd-az-get-public-ip-owner
tool: az
---

## Identify Azure Public IP Owner

### 🎯 Intent

Verify if a specific Public IP address belongs to your subscription and which resource (Load Balancer, NAT Gateway, etc.) it is attached to.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (authenticated to AZ CLI)

---

### ⚡ Action

```bash
export TARGET_IP=<target_ip_address>

az network public-ip list --query "[?ipAddress=='$TARGET_IP']"
```

#### Placeholders

- ``—The IP address to investigate (e.g., `195.171.151.154`)

---

### ✅ Verification

Expected signal:

- JSON block containing `id`, `resourceGroup`, and `ipConfiguration`.
- If empty, the IP is likely external or in a different subscription.

---

### 🔗 Related

- [[sot-az-aks-networking]]
