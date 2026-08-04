---
created: 2026-03-30T11:54:49+00:00
modified: 2026-08-04T08:35:23+00:00
permalink: llmeon/30-library/200-projects/nnuh
project_category: deployments
project_name: Deployments
project_status: active
title: NNUH
type: null
---

contacts:

tom.brooks@nnuh.nhs.uk <tom.brooks@nnuh.nhs.uk>

ben.goss@nnuh.nhs.uk <ben.goss@nnuh.nhs.uk>

Here's the full sequence to get from `az login` to a working `kubectl` session against the private AKS API server through Bastion IP Connect/tunneling.

## 1. Authenticate and Set Subscription Context

```bash
az login
az account set --subscription 4ae8fd93-d084-481f-ba6e-370b7d4d8d0d
```

## 2. Make Sure the Bastion CLI Extension is Current

Tunneling to a private AKS management endpoint via `--target-resource-id` needs a recent `bastion` extension.

```bash
az extension add --name bastion --upgrade
```

## 3. Open the Tunnel

Since `enableTunneling: true` and `enableIpConnect: true` are set on `bas-ff-uks-gp`, and the AKS cluster exposes a `management` private link resource, you can target the cluster resource ID directly (no jumpbox VM needed):

```bash
az network bastion tunnel \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id "/subscriptions/4ae8fd93-d084-481f-ba6e-370b7d4d8d0d/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.ContainerService/managedClusters/aks-ff-uks-gp-01" \
  --resource-port 443 \
  --port 6443
```

Leave this running in its own terminal—it forwards `localhost:6443` → the cluster's private API server (443) for as long as the session is open.

## 4. In a Second Terminal, Pull Kubeconfig Credentials

```bash
az aks get-credentials \
  --resource-group rg-ff-uks-gp-net \
  --name aks-ff-uks-gp-01 \
  --overwrite-existing
```

This writes a context using the real `privateFQDN`: `aks-ff-uks-gp-01-nr0s1a5f.725e1bce-a49c-4025-b2d7-4bd997c04024.privatelink.uksouth.azmk8s.io`, which won't resolve/route locally—you need to point it at the tunnel instead.

## 5. Repoint the Kubeconfig Cluster Entry at the Tunnel

Find the cluster name in your kubeconfig (usually matches `aks-ff-uks-gp-01`), then:

```bash
kubectl config set-cluster aks-ff-uks-gp-01 \
  --server=https://127.0.0.1:6443 \
  --tls-server-name=aks-ff-uks-gp-01-nr0s1a5f.725e1bce-a49c-4025-b2d7-4bd997c04024.privatelink.uksouth.azmk8s.io
```

`--tls-server-name` keeps TLS validation working against the cluster's real certificate (issued for the `privateFQDN`) even though you're connecting to `127.0.0.1`, so you avoid `--insecure-skip-tls-verify`.

## 6. Verify

```bash
kubectl get nodes
```

You should see the `system` and `workflows` node pools respond. If you get a TLS name mismatch error instead, confirm the `--tls-server-name` value exactly matches `privateFQDN` from the cluster JSON—a typo there is the most common failure mode with this pattern.

Notes specific to your setup:

- Keep the `az network bastion tunnel` terminal open for the whole session—closing it drops the forwarded port and `kubectl` calls will start timing out.
- `disableLocalAccounts: false` on the cluster means `az aks get-credentials` will fetch local admin/user kubeconfig credentials as normal (no extra `--admin` flag needed unless you specifically want the cluster-admin context—add `--admin` if your local kubeconfig user doesn't have RBAC bindings yet, since `enableRBAC: true`).
- Because this is a private cluster with `enablePrivateClusterPublicFQDN: false`, this Bastion tunnel is the only path in—there's no public fallback endpoint.
