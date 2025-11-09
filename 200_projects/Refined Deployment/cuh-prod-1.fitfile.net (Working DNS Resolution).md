---
aliases: []
confidence:
created: 2025-09-09T16:00:43Z
epistemic:
last_reviewed:
modified: 2025-11-03T13:48:17Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [topic/technology/networking/dns]
title: cuh-prod-1.fitfile.net (Working DNS Resolution)
type:
uid:
updated:
version:
---

## Analysis of DNS Query Results

### 1. **For `cuh-prod-1.fitfile.net`** (Working DNS Resolution)

```bash
dig _acme-challenge.cuh-prod-1.fitfile.net TXT
# Returns: "GJGWOWtmEUMPGsF6TFLFxadHu1q22UKGP3ly-ppudQA"
```

- ✅ DNS resolution works correctly
- ✅ The ACME challenge TXT record exists
- ✅ Managed by Cloudflare (SOA: aragorn.ns.cloudflare.com)
- ❌ But cert-manager can't reach external DNS servers (timeout to 173.245.59.67:53)

### 2. **For `cuh-poc-1.privatelink.fitfile.net`** (DNS Structure Issue)

```bash
dig _acme-challenge.cuh-poc-1.privatelink.fitfile.net TXT
# Returns: NXDOMAIN with SOA azureprivatedns.net
```

- ❌ Returns NXDOMAIN (domain doesn't exist)
- ❌ SOA indicates it's managed by Azure Private DNS, NOT Cloudflare
- ❌ Azure Private DNS zones cannot be modified by external DNS providers

## Root Causes

### Issue 1: Network Connectivity for `cuh-prod-1.fitfile.net`

Your internal DNS server (10.2.0.10) can resolve the domain, but cert-manager cannot reach external DNS servers to perform the propagation check. The timeout to Cloudflare's DNS server (173.245.59.67:53) suggests:

- Firewall blocking outbound port 53
- Missing proxy configuration for DNS traffic
- Network policy restrictions

### Issue 2: DNS Delegation for `privatelink.fitfile.net`

The `privatelink.fitfile.net` subdomain is managed by Azure Private DNS (`azureprivatedns.net`), not Cloudflare. This means:

- Cloudflare cannot create DNS records under this subdomain
- Cert-manager cannot use DNS-01 challenges for this domain
- This is an Azure-enforced restriction

## Solutions

### For `cuh-prod-1.fitfile.net` - Fix Network Connectivity

1. **Configure cert-manager to use your internal DNS server:**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cert-manager
  namespace: cert-manager
data:
  # Use your internal DNS server instead of external ones
  dns01-recursive-nameservers: "10.2.0.10:53"
  dns01-recursive-nameservers-only: "true"
```

2. **Allow DNS traffic through the proxy (if needed):**

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: cert-manager
  namespace: cert-manager
spec:
  template:
    spec:
      containers:
        - name: cert-manager-controller
          env:
            - name: HTTP_PROXY
              value: "http://10.252.142.180:8080"
            - name: HTTPS_PROXY
              value: "http://10.252.142.180:8080"
            - name: NO_PROXY
              value: "10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,.svc,.cluster.local,10.2.0.10"
```

3. **Check if external DNS queries work through the proxy:**

```bash
kubectl exec -n cert-manager deployment/cert-manager -- sh -c 'HTTP_PROXY=http://10.252.142.180:8080 curl -v http://173.245.59.67:53'
```

### For `cuh-poc-1.privatelink.fitfile.net` - Change Approach

Since this domain is managed by Azure Private DNS, you have these options:

1. **Use HTTP-01 Challenge Instead:**

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: fitfile-cuh-poc-1
  namespace: cuh-prod-1
spec:
  secretName: fitfile-cuh-poc-1-tls
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  commonName: cuh-poc-1.privatelink.fitfile.net
  dnsNames:
    - cuh-poc-1.privatelink.fitfile.net
  # Force HTTP-01 challenge
  acme:
    config:
      - http01:
          ingress:
            class: nginx
        domains:
          - cuh-poc-1.privatelink.fitfile.net
```

2. **Use a Different Domain:**
   Instead of `privatelink.fitfile.net`, use a domain managed by Cloudflare:

- `cuh-poc-1.internal.fitfile.net`
- `cuh-poc-1.fitfile.net`

3. **Use Self-Signed Certificates for Private Domains:**

```yaml
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: fitfile-cuh-poc-1-selfsigned
  namespace: cuh-prod-1
spec:
  secretName: fitfile-cuh-poc-1-tls
  issuerRef:
    name: selfsigned-issuer
    kind: ClusterIssuer
  commonName: cuh-poc-1.privatelink.fitfile.net
  dnsNames:
    - cuh-poc-1.privatelink.fitfile.net
```

## Immediate Actions

1. **For the working domain (`cuh-prod-1.fitfile.net`):**
   - Apply the ConfigMap to use internal DNS
   - Restart cert-manager deployment

2. **For the privatelink domain:**
   - Switch to HTTP-01 challenge or use a different domain

3. **Debug connectivity:**

```bash
# Test if cert-manager can reach internal DNS
kubectl exec -n cert-manager deployment/cert-manager -- nslookup _acme-challenge.cuh-prod-1.fitfile.net 10.2.0.10

# Check cert-manager logs
kubectl logs -n cert-manager deployment/cert-manager -f
```

The key insight here is that you're dealing with two separate issues: network connectivity for external DNS checks and Azure's control over privatelink domains. Each requires a different solution approach.

Looking at the new error, cert-manager is still trying to reach external DNS servers directly - this time `172.64.33.67:53` (another Cloudflare DNS server). The issue persists because cert-manager hasn't been configured to use your internal DNS server yet.

### Quick Check First

Let's verify if the ConfigMap exists and if cert-manager was restarted:

```bash
# Check if the ConfigMap exists
kubectl get configmap cert-manager -n cert-manager

# If it doesn't exist, you need to create it
```

### Complete Implementation Steps

**1. Create the ConfigMap (if not already done):**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cert-manager
  namespace: cert-manager
data:
  # Use your internal DNS server at 10.2.0.10
  dns01-recursive-nameservers: "10.2.0.10:53"
  dns01-recursive-nameservers-only: "true"
```

**2. Apply it:**

```bash
kubectl apply -f cert-manager-dns-config.yaml
```

**3. Update cert-manager deployment to use the ConfigMap:**

The cert-manager Helm chart should automatically pick up a ConfigMap named `cert-manager`. However, you might need to add an environment variable to ensure it's loaded:

```bash
kubectl edit deployment cert-manager -n cert-manager
```

Look for the `cert-manager-controller` container and add these environment variables if they're not present:

```yaml
env:
  - name: DNS01_RECURSIVE_NAMESERVERS
    value: "10.2.0.10:53"
  - name: DNS01_RECURSIVE_NAMESERVERS_ONLY
    value: "true"
```

**4. Force a restart:**

```bash
kubectl rollout restart deployment/cert-manager -n cert-manager
```

### Alternative: Direct Helm Values Update

If you're using Helm, you can update the values directly:

```yaml
# cert-manager-values.yaml
extraArgs:
  - --dns01-recursive-nameservers=10.2.0.10:53
  - --dns01-recursive-nameservers-only=true
```

Then upgrade the Helm release:

```bash
helm upgrade cert-manager jetstack/cert-manager -n cert-manager -f cert-manager-values.yaml
```

### Verify It's Working

After the restart, monitor the logs:

```bash
kubectl logs -n cert-manager deployment/cert-manager -f | grep -E "(dns|DNS|propagation)"
```

You should see cert-manager attempting to use `10.2.0.10:53` instead of external IPs like `172.64.33.67:53`.

### Why This Is Happening

The error shows cert-manager is trying to verify that the DNS-01 challenge TXT record has propagated by querying authoritative nameservers directly. In your restricted network:

- ❌ Direct connections to `172.64.33.67:53` (Cloudflare) are blocked
- ✅ Your internal DNS at `10.2.0.10` can resolve external domains through approved paths

The internal DNS solution makes cert-manager work within your network's security boundaries rather than trying to bypass them.

The error indicates that the cert-manager CRDs (Custom Resource Definitions) are not installed in your cluster. This means cert-manager itself might not be installed or properly configured.

Here are the commands to check and diagnose this:

## Check if Cert-manager is Installed

```bash
# Check if cert-manager namespace exists
kubectl get namespace cert-manager

# Check if cert-manager pods are running
kubectl get pods -n cert-manager

# Check if cert-manager deployments exist
kubectl get deployments -n cert-manager

# List all CRDs to see if cert-manager CRDs are installed
kubectl get crd | grep cert-manager
```

## If Cert-manager is not Installed

Based on your long-term memories about the [Vault PKI setup](file:///Users/username/path/to/README_PKI.md) and [Private CA configuration](https://fitfile.atlassian.net/wiki/spaces/FITFILE/pages/2263416835/Private+CA+via+HCP+Vault), it appears cert-manager should be installed for your TLS certificate automation to work.

If cert-manager is not installed, you'll need to install it first:

```bash
# Install cert-manager using kubectl
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.3/cert-manager.yaml

# Wait for cert-manager to be ready
kubectl wait --for=condition=Available --timeout=300s deployment/cert-manager -n cert-manager
kubectl wait --for=condition=Available --timeout=300s deployment/cert-manager-webhook -n cert-manager
kubectl wait --for=condition=Available --timeout=300s deployment/cert-manager-cainjector -n cert-manager
```

## Alternative: Check Vault Certificate Management

Since you're using Vault for PKI, check if you're managing certificates directly through Vault instead of cert-manager:

```bash
# Check VaultDynamicSecret resources (which can create TLS certificates)
kubectl get vaultdynamicsecret --all-namespaces

# Check for any TLS secrets created by Vault
kubectl get secrets --all-namespaces -o json | jq '.items[] | select(.type=="kubernetes.io/tls") | {namespace: .metadata.namespace, name: .metadata.name}'

# Check the specific secret that was mentioned in your Terraform plan
kubectl get secret fitfile-tls-cert --all-namespaces
```

## Check Your Current Certificate Setup

Based on your Terraform plan and the memories from 21 days ago (2025-08-19), it looks like you might be using VaultDynamicSecret resources to create TLS certificates instead of cert-manager. The removed resource was creating a certificate for `cuh-prod-1.fitfile.net`:

```bash
# Check if there are any other VaultDynamicSecret resources for TLS
kubectl get vaultdynamicsecret --all-namespaces -o wide

# Check ingress resources to see what certificates they're using
kubectl get ingress --all-namespaces -o jsonpath='{range .items[*]}{.metadata.namespace}{"\t"}{.metadata.name}{"\t"}{.spec.tls[*].secretName}{"\n"}{end}'
```

Based on your memories from 12-13 days ago (2025-08-27), it seems you were working on setting up certificates with the secret name `hie-prod-34-tls-cert`. You might want to check if this setup is still in place:

```bash
# Check for the previously mentioned certificate
kubectl get secret hie-prod-34-tls-cert --all-namespaces
```

The error suggests that your cluster doesn't have cert-manager installed, which means you're likely managing certificates directly through Vault Operator using VaultDynamicSecret resources rather than cert-manager's Certificate resources.

Based on your Terraform plan, I can see you're making changes to Vault-related resources in your cluster. Here are the kubectl commands to verify everything worked correctly after applying these changes:

## Check the Destroyed Resources (confirm They're gone)

```bash
# Verify the VaultDynamicSecret in ingress-nginx namespace was removed
kubectl get vaultdynamicsecret tls-certificate -n ingress-nginx

# Verify the VaultAuth in ingress-nginx namespace was removed
kubectl get vaultauth default -n ingress-nginx

# Verify the secret in ingress-nginx namespace was removed
kubectl get secret fitfile-tls-cert -n ingress-nginx
```

These commands should return "not found" errors if the deletions were successful.

## Check the Created Resources

```bash
# Verify the new VaultAuth was created in cert-manager namespace
kubectl get vaultauth default -n cert-manager -o yaml

# Check the secret for the AppRole credentials
kubectl get secret role-secrets -n cert-manager

# Describe the secret (without showing sensitive data)
kubectl describe secret role-secrets -n cert-manager
kubectl get vaultauth,vaultdynamicsecret,vaultstaticsecret --all-namespaces
NAMESPACE      NAME                                      AGE
argo           vaultauth.secrets.hashicorp.com/default   71d
argocd         vaultauth.secrets.hashicorp.com/default   71d
cert-manager   vaultauth.secrets.hashicorp.com/default   44m
cuh-prod-1     vaultauth.secrets.hashicorp.com/default   71d
hutch          vaultauth.secrets.hashicorp.com/default   71d
monitoring     vaultauth.secrets.hashicorp.com/default   71d
spicedb        vaultauth.secrets.hashicorp.com/default   71d
thehyve        vaultauth.secrets.hashicorp.com/default   71d

NAMESPACE   NAME                                                          AGE
argocd      vaultdynamicsecret.secrets.hashicorp.com/argocd-pull          71d
argocd      vaultdynamicsecret.secrets.hashicorp.com/fitfile-image-pull   71d

NAMESPACE    NAME                                                                          AGE
argo         vaultstaticsecret.secrets.hashicorp.com/argo-postgres-config                  70d
argocd       vaultstaticsecret.secrets.hashicorp.com/argocd-repo-fitfile-deployment-repo   71d
argocd       vaultstaticsecret.secrets.hashicorp.com/argocd-secret                         71d
cuh-prod-1   vaultstaticsecret.secrets.hashicorp.com/ffcloud                               70d
cuh-prod-1   vaultstaticsecret.secrets.hashicorp.com/fitconnect                            70d
cuh-prod-1   vaultstaticsecret.secrets.hashicorp.com/fitfile-rsa-private-key               70d
cuh-prod-1   vaultstaticsecret.secrets.hashicorp.com/frontend                              70d
cuh-prod-1   vaultstaticsecret.secrets.hashicorp.com/minio                                 70d
cuh-prod-1   vaultstaticsecret.secrets.hashicorp.com/mongodb                               41d
cuh-prod-1   vaultstaticsecret.secrets.hashicorp.com/postgresql                            71d
cuh-prod-1   vaultstaticsecret.secrets.hashicorp.com/ude-secret                            70d
cuh-prod-1   vaultstaticsecret.secrets.hashicorp.com/workflows-secrets                     70d
monitoring   vaultstaticsecret.secrets.hashicorp.com/monitoring                            71d
spicedb      vaultstaticsecret.secrets.hashicorp.com/spicedb                               70d
azadmin@FITFILEJumpbox:~/ff-platform/cuh-platform$ kubectl get vaultdynamicsecret tls-certificate -n ingress-nginx
Error from server (NotFound): vaultdynamicsecrets.secrets.hashicorp.com "tls-certificate" not found
azadmin@FITFILEJumpbox:~/ff-platform/cuh-platform$ kubectl get vaultauth default -n ingress-nginx
Error from server (NotFound): vaultauths.secrets.hashicorp.com "default" not found
azadmin@FITFILEJumpbox:~/ff-platform/cuh-platform$ kubectl get secret fitfile-tls-cert -n ingress-nginx
Error from server (NotFound): secrets "fitfile-tls-cert" not found
azadmin@FITFILEJumpbox:~/ff-platform/cuh-platform$
```

## Verify Vault Operator Integration

```bash
# Check if the Vault operator is processing the new resources
kubectl logs -n vault-secrets-operator deployment/vault-secrets-operator --tail=50

# List all VaultAuth resources across namespaces
kubectl get vaultauth --all-namespaces

# Check the status of the VaultAuth resource
kubectl describe vaultauth default -n cert-manager
```

## Monitor Cert-manager (if It's Using These Vault resources)

```bash
# Check cert-manager logs for any authentication issues
kubectl logs -n cert-manager deployment/cert-manager --tail=50
azadmin@FITFILEJumpbox:~/ff-platform/cuh-platform$ kubectl get vaultauth default -n cert-manager -o yaml
apiVersion: secrets.hashicorp.com/v1beta1
kind: VaultAuth
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"secrets.hashicorp.com/v1beta1","kind":"VaultAuth","metadata":{"annotations":{},"labels":{"managedBy":"terraform"},"name":"default","namespace":"cert-manager"},"spec":{"appRole":{"roleId":"751468b0-552d-9a7e-801c-909662df17bb","secretRef":"role-secrets"},"method":"appRole","mount":"approle","namespace":"admin/deployments/cuh-prod-1"}}
  creationTimestamp: "2025-09-09T13:23:12Z"
  finalizers:
  - vaultauth.secrets.hashicorp.com/finalizer
  generation: 1
  labels:
    managedBy: terraform
  name: default
  namespace: cert-manager
  resourceVersion: "43027445"
  uid: 8e604ef8-899b-408f-b73b-bdf9d5eb8271
spec:
  appRole:
    roleId: 751468b0-552d-9a7e-801c-909662df17bb
    secretRef: role-secrets
  method: appRole
  mount: approle
  namespace: admin/deployments/cuh-prod-1
status:
  specHash: b28c206e030e619d3f77617ae21cf3ab8fc779852fae536c770caa68653ff7dc
  valid: true
# List certificates in the cert-manager namespace
kubectl get certificates -n cert-manager

# Check if cert-manager can communicate with Vault
kubectl describe clusterissuer hcp-vault-issuer
```

## Summary View

```bash
# Get a quick overview of all Vault-related custom resources
kubectl get vaultauth,vaultdynamicsecret,vaultstaticsecret --all-namespaces
```

Based on your Terraform plan, it appears you're moving TLS certificate management from the ingress-nginx namespace to cert-manager namespace, which aligns with the PKI setup documented in your long-term memories. The new configuration uses the `cloudflare` AppRole (with roleId `751468b0-552d-9a7e-801c-909662df17bb`) for authentication to Vault.

After running these commands, you should see:

- No Vault resources in the `ingress-nginx` namespace
- A new `VaultAuth` resource in the `cert-manager` namespace
- A `role-secrets` secret in the `cert-manager` namespace containing the AppRole credentials

## Solution 1: Configure Cert-manager to Use Internal DNS Servers

### The Problem

Cert-manager is trying to reach Cloudflare's external DNS server (`173.245.59.67`) directly on port 53 to verify DNS-01 challenges. However, your Kubernetes cluster is in a restricted network environment that blocks direct outbound connections to external DNS servers, causing the timeout error.

### Why This Solution Works

Your cluster already has an internal DNS server at `10.2.0.10` (as shown in your NO_PROXY settings). This internal DNS server can resolve external domains by forwarding queries through your corporate network's allowed channels. By telling cert-manager to use this internal DNS server instead of trying to reach external ones directly, you work within your network's security constraints.

### Step-by-Step Implementation

**Step 1: Create the ConfigMap**

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: cert-manager
  namespace: cert-manager
data:
  # Tell cert-manager to use your internal DNS server
  dns01-recursive-nameservers: "10.2.0.10:53"
  # Only use the DNS servers we specify (don't try external ones)
  dns01-recursive-nameservers-only: "true"
```

Save this as `cert-manager-dns-config.yaml` and apply it:

```bash
kubectl apply -f cert-manager-dns-config.yaml
```

**Step 2: Restart cert-manager to pick up the new configuration**

```bash
kubectl rollout restart deployment/cert-manager -n cert-manager
```

**Step 3: Verify the configuration is applied**

```bash
# Check the ConfigMap was created
kubectl get configmap cert-manager -n cert-manager -o yaml

# Watch the cert-manager pod restart
kubectl get pods -n cert-manager -w
```

### What This Does

1. **`dns01-recursive-nameservers: "10.2.0.10:53"`** - This tells cert-manager: "When you need to look up DNS records for DNS-01 challenges, use this internal DNS server instead of trying to reach external DNS servers directly."
2. **`dns01-recursive-nameservers-only: "true"`** - This tells cert-manager: "ONLY use the DNS servers I've specified. Don't fall back to trying external DNS servers."

### How DNS-01 Challenge Works After This Change

1. Let's Encrypt asks cert-manager to prove ownership of `cuh-prod-1.fitfile.net`
2. Cert-manager creates a TXT record `_acme-challenge.cuh-prod-1.fitfile.net` in your DNS provider (Cloudflare)
3. Cert-manager needs to verify this record exists before telling Let's Encrypt to check
4. **Instead of**: Trying to query `173.245.59.67:53` directly (which times out)
5. **Now**: Queries your internal DNS server at `10.2.0.10:53`, which can reach the internet through proper corporate channels
6. Your internal DNS server returns the TXT record value
7. Cert-manager confirms to Let's Encrypt that the challenge is ready
8. Certificate is issued successfully

### Why Use Internal DNS

From your pod description, I can see your environment uses:

- HTTP proxy: `10.252.142.180:8080` for web traffic
- Internal DNS: `10.2.0.10` for DNS resolution

Your corporate network likely:

- Blocks direct outbound connections on port 53 (DNS)
- Allows the internal DNS server to make external queries through approved paths
- This is a common security practice in enterprise environments

This solution aligns with your existing network architecture rather than trying to bypass it.
