---
type: kb
service: vso
tags: [triage, identity, vault]
---

# KB: VSO Metadata Identifiers

## Mental Model: Tracing the Origin
To find "where a secret comes from in Vault," you must follow the trail:
1. **Secret Metadata**: Check `ownerReferences` to find the CR.
2. **VSO CR Spec**: Check `spec.namespace`, `spec.mount`, and `spec.path`.

## Identifying Owner Kind
| Kind | Use Case |
|---|---|
| `VaultStaticSecret` | For KV-V2 (static) secrets like API tokens. |
| `VaultDynamicSecret` | For lease-based secrets (Azure, AWS, Database). |
| `VaultPKISecret` | For short-lived TLS certificates. |

## External Controllers
- **Reflector**: Look for `reflector.v1.k8s.emberstack.com` annotations.
- **ArgoCD**: Look for `argocd.argoproj.io/tracking-id`.
