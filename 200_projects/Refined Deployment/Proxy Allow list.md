---
aliases: []
confidence: 
created: 2025-08-05T08:45:48Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [allowlist, firewall, proxy, security, topic/technology/networking]
title: Proxy Allow list
type:
uid: 
updated: 
version:
---

| **Title**                                                                   | **Purpose**                                                  | **Ports** | **Protocol** |
| --------------------------------------------------------------------------- | ------------------------------------------------------------ | --------- | ------------ |
| releases.hashicorp.com                                                      | HashiCorp releases                                           | 80, 443   | HTTP/HTTPS   |
| registry.terraform.io                                                       | Terraform registry                                           | 80, 443   | HTTP/HTTPS   |
| app.terraform.io                                                            | Terraform services                                           | 80, 443   | HTTP/HTTPS   |
| archivist.terraform.io                                                      | Terraform services                                           | 80, 443   | HTTP/HTTPS   |
| vault-public-vault-8b38a0c2.e3dedc53.z1.hashicorp.cloud                     | HashiCorp Vault                                              | 443, 8200 | HTTPS        |
| fitfile-prod.eu.auth0.com                                                   | Auth0 authentication                                         | 443       | HTTPS        |
| cdn.auth0.com                                                               | Auth0 UI components                                          | 443       | HTTPS        |
| fitfile.com                                                                 | FITFILE main domain                                          | 443       | HTTPS        |
| logs-prod-008.grafana.net                                                   | Grafana logging                                              | 443       | HTTPS        |
| tempo-prod-06-prod-gb-south-0.grafana.net                                   | Grafana Tempo tracing                                        | 443       | HTTPS        |
| gitlab.com                                                                  | Source code repository (also SSH access)                     | 22, 443   | TCP/HTTPS    |
| packages.microsoft.com                                                      | Microsoft package repository                                 | 80, 443   | HTTP/HTTPS   |
| fitfileregistry.azurecr.io                                                  | FITFILE Private ACR                                          | 443       | HTTPS        |
| fitfilepublic.azurecr.io                                                    | FITFILE Public ACR                                           | 443       | HTTPS        |
| \*<https://www.google.com/search?q=.data.mcr.microsoft.com>                 | Microsoft Container Registry CDN                             | 443       | HTTPS        |
| mcr.microsoft.com                                                           | Microsoft Container Registry                                 | 443       | HTTPS        |
| <https://www.google.com/search?q=login.microsoftonline.com>                 | Azure AD authentication                                      | 443       | HTTPS        |
| <https://www.google.com/search?q=management.azure.com>                      | Azure API operations                                         | 443       | HTTPS        |
| \*<https://www.google.com/search?q=.monitoring.azure.com>                   | Azure Monitor metrics                                        | 443       | HTTPS        |
| <https://www.google.com/search?q=uksouth.ingest.monitor.azure.com>          | Prometheus metrics ingestion (region subdomain configurable) | 443       | HTTPS        |
| <https://www.google.com/search?q=uksouth.handler.control.monitor.azure.com> | Cluster data collection (region subdomain configurable)      | 443       | HTTPS        |
| \*<https://www.google.com/search?q=.ods.opinsights.azure.com>               | Azure Monitor / Log Analytics                                | 443       | HTTPS        |
| \*<https://www.google.com/search?q=.opinsights.azure.com>                   | Azure Monitor / Log Analytics                                | 443       | HTTPS        |
| \*<https://www.google.com/search?q=.oms.opinsights.azure.com>               | Azure Monitor / Log Analytics                                | 443       | HTTPS        |
| <https://www.google.com/search?q=dc.services.visualstudio.com>              | Container Agent Telemetry                                    | 443       | HTTPS        |
| acs-mirror.azureedge.net                                                    | Azure CNI / Kubenet                                          | 443       | HTTPS        |
| \*.azureedge.net                                                            | Azure CDN                                                    | 443       | HTTPS        |
| uksmanaged208.blob.core.windows.net                                         | Azure Blob Storage (Vault)                                   | 443       | HTTPS        |
| azurecliprod.blob.core.windows.net                                          | Azure CLI Installation                                       | 443       | HTTPS        |
| data.policy.core.windows.net                                                | Kubernetes policy sync                                       | 443       | HTTPS        |
| store.policy.core.windows.net                                               | Gatekeeper policy artifacts                                  | 443       | HTTPS        |
| azure.archive.ubuntu.com                                                    | Ubuntu package updates (for Jumpbox)                         | 80, 443   | HTTP/HTTPS   |
| \*<https://www.google.com/search?q=.canonical.com>                          | Canonical package services (for Jumpbox)                     | 80, 443   | HTTP/HTTPS   |
| security.ubuntu.com                                                         | Ubuntu security updates (for Jumpbox)                        | 80, 443   | HTTP/HTTPS   |
| changelogs.ubuntu.com                                                       | Ubuntu changelogs (for Jumpbox)                              | 80, 443   | HTTP/HTTPS   |
| <https://www.google.com/search?q=ntp.ubuntu.com>                            | Time sync (for Jumpbox)                                      | 123       | UDP          |
| download.opensuse.org                                                       | OpenSUSE packages (for Jumpbox)                              | 80, 443   | HTTP/HTTPS   |

Hi Leon - would you be able to produce a tracert output from a FitFile server to any URL in the allow list.

Networks want to see the full picture of how traffic is currently routing from the FitFile subscription.

There is a default route on the Azure FW that sends traffic direct to the internet unless that is overridden by configuring a Proxy at source (like you have done for FitFile subscription.). In that case it will go FitFile > Azure FW > On-Prem FW > On-Prem Proxy > Internet

**1. Restarting deployments in all namespaces:**

```bash
kubectl get deployments --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace} {.metadata.name}\n{end}' | while read ns name; do kubectl rollout restart deployment "$name" -n "$ns"; done
```

This command gets all deployments across all namespaces and then iterates through them, restarting each one.

**2. Restarting deployments in specific namespaces:**

If you only need to restart deployments in certain namespaces (e.g., `cuh-prod-1`, `argocd`), you can modify the command:

```bash
for ns in cuh-prod-1 argocd; do kubectl get deployments -n "$ns" -o jsonpath='{range .items[*]}{.metadata.name}\n{end}' | while read name; do kubectl rollout restart deployment "$name" -n "$ns"; done; done

```

**3. Restarting deployments with specific labels:**

If your deployments have a common label signifying they need the updated environment variables (e.g., `app=needs-restart`), use a label selector:

```bash
kubectl get deployments --all-namespaces -l app=needs-restart -o jsonpath='{range .items[*]}{.metadata.namespace} {.metadata.name}\n{end}' | while read ns name; do kubectl rollout restart deployment "$name" -n "$ns"; done
```

**4. Draining nodes (for more comprehensive restarts):**

For scenarios requiring a full node restart (e.g., kernel updates, underlying infrastructure changes), use `kubectl drain` and `kubectl uncordon`:

```bash
kubectl get nodes | while read node; do kubectl drain "$node" --ignore-daemonsets --delete-local-data --force; kubectl uncordon "$node"; done
```

This drains each node, evicting pods gracefully (respecting PodDisruptionBudgets), then uncordons the node to make it schedulable again. This approach is the most disruptive but ensures every pod gets restarted on a fresh node.

**Important Considerations:**

- **Downtime:** Rolling restarts minimize downtime, but some disruption is possible depending on your application and deployment configuration.
- **Resource Limits:** Ensure your cluster has enough resources to handle the rolling restarts. New pods are created before old ones are terminated.
- **PodDisruptionBudgets (PDBs):** If you're using PDBs, the drain process will respect those and may pause if minimum availability requirements aren't met.
- **Testing:** Test these commands in a non-production environment first to understand their impact.

Choose the method that best suits your situation, and always proceed with caution in a production environment. If possible, consider using configmaps or secrets for environment variables as these can be updated without restarting deployments.
