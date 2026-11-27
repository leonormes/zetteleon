---
title: WMSDE - CLI Access
aliases:
- WMSDE access
- West Midlands SDE CLI access
tags:
- wmsde
- azure
- aks
- bastion
- access
- runbook
conformant: true
created: 2026-11-25 16:09:36+00:00
modified: 2026-11-25 16:09:36+00:00
permalink: llmeon/30-library/200-projects/wmsde-cli-access
project_category: deployments
project_name: Deployments
project_status: active
status: seed
type: project
---

Command-line access to the West Midlands SDE (WMSDE) production node, `wmsde-prod-2`: sign-in, Bastion, `kubectl` and the two VMs. Follow it top to bottom the first time, then use it by section.

Last verified 25 Nov 2026. Anything marked **Not verified** has not been run end to end. Sources are at the end.

## 1. What You Are Connecting To

| Item | Value |
|---|---|
| Tenant (WMSDE's own, not FITFILE's) | `1743a07d-8695-4f90-9fa2-0ce2420a0ed5` |
| Subscription | `WM SDE - FITFILE JZ`, `7b7bad5f-1819-44ea-8e9a-8b55c7691dea` |
| Region | UK South |
| Resource group | `rg-ff-uks-wmsde-net` |
| AKS cluster | `aks-ff-uks-wmsde-1`: private API server, Entra and Azure RBAC, local accounts disabled |
| Bastion | `bas-ff-uks-wmsde-1` (Standard, native client tunnelling on) |
| Jumpbox VM | `vm-ff-uks-wmsde-jumpbox`: the FITFILE admin box, which can reach the cluster API and the storage private endpoint |
| ETL VM | `vm-ff-uks-wmsde-etl`: The Hyve's workspace (Entra SSH, RDP) |
| Synthetic data storage | `stffukswmsdesyn01`, private endpoint `10.173.84.100`, public access off |

The cluster API and both VMs have no public address, so every route goes through Bastion.

## 2. Shell Variables

Paste once per terminal. Every command below uses them.

```bash
export WMSDE_TENANT=1743a07d-8695-4f90-9fa2-0ce2420a0ed5
export WMSDE_SUB=7b7bad5f-1819-44ea-8e9a-8b55c7691dea
export WMSDE_RG=rg-ff-uks-wmsde-net
export WMSDE_AKS=aks-ff-uks-wmsde-1
export WMSDE_BASTION=bas-ff-uks-wmsde-1
export WMSDE_JUMPBOX=vm-ff-uks-wmsde-jumpbox
export WMSDE_ETL=vm-ff-uks-wmsde-etl
export WMSDE_API_FQDN=aks-ff-uks-wmsde-1-5xgmhv7q.07b17bcc-840f-4850-bf46-304f21d27ae6.privatelink.uksouth.azmk8s.io
```

## 3. One-off Setup

**Account.** Use your `@safehaven.wmidssecuredataenvironment.nhs.uk` account. A FITFILE login cannot see this subscription.

**Tools.** `kubectl` and the Azure CLI, plus two extensions:

```bash
az extension add --name ssh
az extension add --name bastion
```

`kubelogin` is not needed for the route in section 6.

**Roles.** WMSDE (Jakob) grants these, to Entra groups. Ask for yours if a step below is refused.

| Role | Scope | Needed for |
|---|---|---|
| Reader | `rg-ff-uks-wmsde-net` | Bastion (it checks the VM, its NIC and the Bastion host) |
| Virtual Machine Administrator Login | `rg-ff-uks-wmsde-net` | Entra SSH with sudo (FITFILE engineers) |
| Azure Kubernetes Service RBAC Cluster Admin | the cluster | `kubectl`. Local accounts are off, so there is no admin-kubeconfig fallback |
| Azure Kubernetes Service Cluster User Role | the cluster | `az aks get-credentials`. A standard Azure requirement that the repo README does not list |

## 4. Sign in (Each Session)

```bash
az login --tenant "$WMSDE_TENANT"
az account set --subscription "$WMSDE_SUB"
az account show --query "{name:name, tenant:tenantId}" -o table
```

`az account set` changes the default for every terminal, and your default is normally a FITFILE subscription. The commands below pass `--subscription "$WMSDE_SUB"` anyway.

## 5. Reach the VMs Through Bastion

**ETL VM, Entra sign-in** (used 23 Nov):

```bash
az network bastion ssh --subscription "$WMSDE_SUB" --name "$WMSDE_BASTION" --resource-group "$WMSDE_RG" \
  --target-resource-id "$(az vm show --subscription "$WMSDE_SUB" -g "$WMSDE_RG" -n "$WMSDE_ETL" --query id -o tsv)" \
  --auth-type AAD
```

**Jumpbox, `azadmin` password** (worked 30 Oct):

```bash
az network bastion ssh --subscription "$WMSDE_SUB" --name "$WMSDE_BASTION" --resource-group "$WMSDE_RG" \
  --target-resource-id "$(az vm show --subscription "$WMSDE_SUB" -g "$WMSDE_RG" -n "$WMSDE_JUMPBOX" --query id -o tsv)" \
  --auth-type password --username azadmin -- \
  -o PubkeyAuthentication=no -o PreferredAuthentications=password
```

- The password is the sensitive `jumpbox_admin_password` output of the `wmsde-prod-2` HCP Terraform workspace (`terraform output -raw jumpbox_admin_password`, run in `infrastructure/`). Keep it out of notes, chat and tickets.
- The two `-o` options stop SSH offering every agent key first (`Too many authentication failures`).
- Entra sign-in to the jumpbox with `--auth-type AAD` may also work. **Not verified.**
- If password login is ever switched off (the `jumpbox_ssh_public_key` workspace variable), use `--auth-type ssh-key --username azadmin --ssh-key <private key file>`.

**Run a command without SSH.** Needs only Azure permissions on the VM, no tunnel. It runs as root:

```bash
az vm run-command invoke --subscription "$WMSDE_SUB" -g "$WMSDE_RG" -n "$WMSDE_ETL" \
  --command-id RunShellScript --scripts 'hostname; uptime' --query 'value[0].message' -o tsv
```

**Copy a file to the jumpbox.** Open a tunnel to port 22 and leave it running, then `scp` from a second terminal (from the repo README):

```bash
az network bastion tunnel --subscription "$WMSDE_SUB" --name "$WMSDE_BASTION" --resource-group "$WMSDE_RG" \
  --target-resource-id "$(az vm show --subscription "$WMSDE_SUB" -g "$WMSDE_RG" -n "$WMSDE_JUMPBOX" --query id -o tsv)" \
  --resource-port 22 --port 2222
```

```bash
scp -P 2222 -o PubkeyAuthentication=no -o PreferredAuthentications=password <file> azadmin@127.0.0.1:~
```

## 6. Reach the Cluster from Your Laptop

The API server is private, so `kubectl` goes through an SSH port-forward over Bastion to the jumpbox. This route worked on 30 Oct, while local accounts were still on. They are off now, so the first run needs the cluster roles from section 3. **Not re-tested since local accounts were disabled.**

### 6.1 Build the Kubeconfig (Once)

Token helper. It asks `az` for an AKS token in the WMSDE tenant, whatever your default subscription is:

```bash
mkdir -p ~/.kube/wmsde
cat > ~/.kube/wmsde/token.sh <<'EOF'
#!/bin/sh
exec az account get-access-token --subscription 7b7bad5f-1819-44ea-8e9a-8b55c7691dea \
  --resource 6dae42f8-4368-4678-94ff-3960e28e3630 -o json \
  --query "{apiVersion:'client.authentication.k8s.io/v1',kind:'ExecCredential',status:{token:accessToken}}"
EOF
chmod 700 ~/.kube/wmsde/token.sh
```

The `--resource` value is the fixed Entra application ID of AKS's server app. It is the same in every tenant.

Kubeconfig. It points at the local end of the tunnel and keeps the real API name for TLS:

```bash
export KUBECONFIG=~/.kube/wmsde/kubeconfig
az aks get-credentials --subscription "$WMSDE_SUB" -g "$WMSDE_RG" -n "$WMSDE_AKS" \
  --context wmsde-prod-2 --file "$KUBECONFIG" --overwrite-existing
CL=$(kubectl config view -o jsonpath='{.contexts[0].context.cluster}')
USR=$(kubectl config view -o jsonpath='{.contexts[0].context.user}')
kubectl config set-cluster "$CL" --server=https://127.0.0.1:6443 --tls-server-name="$WMSDE_API_FQDN"
kubectl config set-credentials "$USR" --exec-api-version=client.authentication.k8s.io/v1 \
  --exec-command="$HOME/.kube/wmsde/token.sh" --exec-interactive-mode=Never
chmod 600 "$KUBECONFIG"
```

### 6.2 Open the Tunnel (Each Session)

Run this in a second terminal (with the section 2 variables exported) and leave it open. It asks for the `azadmin` password, then prints nothing:

```bash
az network bastion ssh --subscription "$WMSDE_SUB" --name "$WMSDE_BASTION" --resource-group "$WMSDE_RG" \
  --target-resource-id "$(az vm show --subscription "$WMSDE_SUB" -g "$WMSDE_RG" -n "$WMSDE_JUMPBOX" --query id -o tsv)" \
  --auth-type password --username azadmin -- \
  -o PubkeyAuthentication=no -o PreferredAuthentications=password -o ExitOnForwardFailure=yes \
  -N -L "6443:${WMSDE_API_FQDN}:443"
```

### 6.3 Use It

```bash
export KUBECONFIG=~/.kube/wmsde/kubeconfig
kubectl --context wmsde-prod-2 get nodes
kubectl --context wmsde-prod-2 -n argocd get applications
```

A dedicated `KUBECONFIG` keeps WMSDE out of your default config.

## 7. RDP to the ETL VM (Supporting the Hyve)

The ETL VM runs xrdp on 3389, and the NSG allows 3389 from Bastion only. Open a tunnel, then point an RDP client at `127.0.0.1:33389`:

```bash
az network bastion tunnel --subscription "$WMSDE_SUB" --name "$WMSDE_BASTION" --resource-group "$WMSDE_RG" \
  --target-resource-id "$(az vm show --subscription "$WMSDE_SUB" -g "$WMSDE_RG" -n "$WMSDE_ETL" --query id -o tsv)" \
  --resource-port 3389 --port 33389
```

The Hyve confirmed on 24 Nov that their tunnel and RDP login work. This command is the README's port 22 tunnel with the ports changed, so **not verified as written**.

## 8. Check It Works

- **Subscription:** `az account show --query name -o tsv` returns `WM SDE - FITFILE JZ`.
- **Cluster state:** `az aks show --subscription "$WMSDE_SUB" -g "$WMSDE_RG" -n "$WMSDE_AKS" --query "{power:powerState.code, private:apiServerAccessProfile.enablePrivateCluster, localAccountsDisabled:disableLocalAccounts}" -o table` returns `Running`, `True`, `True` (25 Nov).
- **VMs:** `az vm list --subscription "$WMSDE_SUB" -g "$WMSDE_RG" --query "[].name" -o tsv` lists the jumpbox and the ETL VM.
- **Bastion:** a section 5 command gives you a shell prompt.
- **kubectl:** section 6.3 lists the nodes.

## 9. Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| The WMSDE subscription is missing after `az login` | Signed in with a FITFILE account or without `--tenant` | `az login --tenant "$WMSDE_TENANT"` with your safehaven account |
| Commands act on a FITFILE subscription | Default subscription is not WMSDE | Add `--subscription "$WMSDE_SUB"` |
| `Too many authentication failures` | SSH agent offers every key first | Keep the two `-o` options from section 5 |
| Bastion refuses, or `AuthorizationFailed` | Missing Reader or VM login role | Ask WMSDE for the roles in section 3 |
| `connection refused` on `127.0.0.1:6443` | Tunnel not running, or the port is taken | Restart 6.2. Check with `lsof -nP -iTCP:6443 -sTCP:LISTEN` |
| `x509: certificate is valid for ..., not 127.0.0.1` | `tls-server-name` missing from the kubeconfig | Re-run the `set-cluster` line in 6.1 |
| `Forbidden` or `Unauthorized` from `kubectl` | No AKS RBAC role | Section 3. There is no `--admin` fallback now |

## 10. Where This Differs from the Repo README

The `wmsde-prod-2` README is behind the live environment. Trust this note, then live `az`, over it.

- It says local accounts are on and `kubectl` uses `az aks get-credentials --admin`. Live `disableLocalAccounts` is `true` (25 Nov).
- It describes one VM that is both jumpbox and ETL workspace. Live there are two: `vm-ff-uks-wmsde-jumpbox` (`Standard_D2ads_v6`) and `vm-ff-uks-wmsde-etl` (`Standard_E4ads_v6`).
- It says the Hyve do not use RDP. They do, through a Bastion tunnel (see [FTFL-1249](https://fitfile.atlassian.net/browse/FTFL-1249)).

## 11. Sources and Verification

- **Repo:** `Deployment/Clusters/wmsde/Production/wmsde-prod-2/` (README and `infrastructure/locals.tf`). Related tickets: FTFL-1247 (node build), FTFL-1246 (platform bootstrap), FTFL-1249 (connectivity test), FTFL-1253 (ETL workspace).
- **Checked live, read-only, 25 Nov 2026:** the subscription is in the local `az` account list. Both VMs are provisioned. AKS is running, private, with Azure RBAC on and local accounts disabled. Bastion is Standard with tunnelling on. The private API name in section 2 matches. The `ssh` (2.0.9) and `bastion` (1.4.3) extensions are installed.
- **Taken from earlier sessions, not re-run:** the jumpbox password login and the tunnel and kubeconfig steps (30 Oct), and `az vm run-command` and Entra SSH on the ETL VM (23 Nov).
- **Not verified:** Entra SSH to the jumpbox, the RDP tunnel command as written, `kubectl` with local accounts off, and the Cluster User Role requirement.
