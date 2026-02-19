---
type: atomic_command
tool: kubectl
hop_level: local
target_service: k8s
tags: #atomic #k8s #ingress
---

# Map Ingress to Backends (JSONPath)

## 🎯 Intent
Quickly audit all Ingress resources across the cluster to see which hostnames map to which backend services and ports.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with context)

---

## ⚡ Action

```bash
kubectl get ingress -A -o jsonpath='{range .items[*]}{.metadata.namespace}/{.metadata.name}{":
"}{range .spec.rules[*]}{"  "}{.host}{"
"}{range .http.paths[*]}{"    "}{.path}{" -> "}{.backend.service.name}{":"}{.backend.service.port.number}{"
"}{end}{end}{"
"}{end}'
```

---

## ✅ Verification
Expected signal:
- A clear list of namespaces, hosts, and backend service names.

---

## 🔗 Related
- [[sot-az-aks-networking]]
