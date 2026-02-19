---
type: atomic_command
tool: drill
hop_level: local
target_service: network
requires_tunnel: false
tags: #atomic #network #dns #drill
---

# Advanced DNS Query (drill)

## 🎯 Intent
Gather detailed information from DNS, including full record sets and trace information, to diagnose resolution issues or verify record propagation. `drill` is a modern replacement for `dig`.

---

## 🌍 Execution Context
Run from:
- [x] Inside a netshoot pod or container.
- [x] Local machine (if drill installed).

---

## ⚡ Action

### 1. Basic Query
```bash
drill <hostname>
```

### 2. Query Specific Record Type
```bash
drill <record_type> <hostname>
```

### 3. DNS Trace
```bash
drill -T <hostname>
```

### 4. Verbose Info (similar to dig +trace)
```bash
drill -V 5 <hostname>
```

### Placeholders
- `<hostname>` — The domain to query (e.g., `google.com` or `my-service.namespace.svc.cluster.local`).
- `<record_type>` — e.g., `A`, `MX`, `TXT`, `SRV`.

---

## ✅ Verification
Expected signal:
- `ANSWER SECTION` containing the expected records.
- Status should be `NOERROR`. `NXDOMAIN` indicates the record does not exist.

---

## 🔗 Related
- [[sot-network-tools-patterns]]
- [[cmd-k8s-run-netshoot]]
