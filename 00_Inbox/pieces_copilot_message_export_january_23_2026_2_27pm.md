---
created: 2026-01-23T14:27:28+00:00
modified: 2026-01-23T14:49:08+00:00
---
Here are practical commands to list everything in the spicedb Kubernetes namespace. They cover standard Kubernetes resources plus SpiceDB Vault CRDs you’ve been using (VaultStaticSecret, VaultDynamicSecret, VaultAuth), so you get a full picture.

Quick overview of all standard Kubernetes resources in the namespace:
**Shell Snippet**
```sh
for t in pods deployments statefulsets services secrets serviceaccounts vaultstaticsecret vaultdynamicsecret vaultauth; do kubectl -n spicedb get $t --ignore-not-found; done
kubectl -n spicedb describe <resource-type> <name>
kubectl -n spicedb get all --ignore-not-found
kubectl -n spicedb get all -o wide --ignore-not-found
kubectl -n spicedb get all -o yaml --ignore-not-found
kubectl -n spicedb get all,vaultstaticsecret,vaultdynamicsecret,vaultauth --ignore-not-found
kubectl -n spicedb get pods,deployments,statefulsets,services,secrets -o wide --ignore-not-found
kubectl -n spicedb get secrets configmaps serviceaccounts networkpolicies poddisruptionbudget --ignore-not-found
kubectl -n spicedb get secrets configmaps serviceaccounts networkpolicies poddisruptionbudget -o wide --ignore-not-found
kubectl -n spicedb get vaultstaticsecret vaultdynamicsecret vaultauth --ignore-not-found
kubectl -n spicedb get vaultstaticsecret vaultdynamicsecret vaultauth --ignore-not-found
kubectl -n spicedb get vaultstaticsecret vaultdynamicsecret vaultauth -o wide --ignore-not-found
kubectl -n spicedb logs <pod-name> (for pod-level debugging)
```




**Links:**
- [Azure Platform Deployment Guide](<00_Inbox/Azure Platform Deployment Guide.md>)
