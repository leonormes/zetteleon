---
created: 2026-02-19T13:14:43+00:00
hop_level: local
modified: 2026-07-13T08:45:26+00:00
permalink: llmeon/30-library/ops/cmd-net-drill-dns
requires_tunnel: false
tags: [atomic, dns, drill, network]
target_service: network
title: cmd-net-drill-dns
tool: drill
---

## Advanced DNS Query (Drill)

### 🎯 Intent

Gather detailed information from DNS, including full record sets and trace information, to diagnose resolution issues or verify record propagation. `drill` is a modern replacement for `dig`.

---

### 🌍 Execution Context

Run from:

- [x] Inside a netshoot pod or container.
- [x] Local machine (if drill installed).

---

### ⚡ Action

#### 1. Basic Query

```bash
drill <hostname>
```

#### 2. Query Specific Record Type

```bash
drill <record_type> <hostname>
```

#### 3. DNS Trace

```bash
drill -T <hostname>
```

#### 4. Verbose Info (Similar to Dig +trace)

```bash
drill -V 5 <hostname>
```

#### Placeholders

- `<hostname>`—The domain to query (e.g., `google.com` or `my-service.namespace.svc.cluster.local`).
- `<record_type>`—e.g., `A`, `MX`, `TXT`, `SRV`.

---

### ✅ Verification

Expected signal:

- `ANSWER SECTION` containing the expected records.
- Status should be `NOERROR`. `NXDOMAIN` indicates the record does not exist.

---

### 🔗 Related

- [[sot-network-tools-patterns]]
- [[cmd-k8s-run-netshoot]]
