---
created: 2026-02-17T08:59:36+00:00
hop_level: local
modified: 2026-07-04T10:50:44+00:00
permalink: llmeon/30-library/ops/cmd-k8s-get-ingress-map
tags: [atomic, ingress, k8s]
target_service: k8s
title: cmd-k8s-get-ingress-map
tool: kubectl
type: atomic_command
---

## Map Ingress to Backends (JSONPath)

### 🎯 Intent

Quickly audit all Ingress resources across the cluster to see which hostnames map to which backend services and ports.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with context)

---

### ⚡ Action

```bash
kubectl get ingress -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{":
"}{range .spec.rules[*]}{"  "}{.host}{"
"}{range .http.paths[*]}{"    "}{.path}{" -> "}{.backend.service.name}{":"}{.backend.service.port.number}{"
"}{end}{end}{"
"}{end}'
```

---

### ✅ Verification

Expected signal:

- A clear list of namespaces, hosts, and backend service names.

---

### 🔗 Related

- [[sot-az-aks-networking]]
