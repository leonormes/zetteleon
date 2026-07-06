---
captured: 2026-04-29T13:28:53+01:00 2026-04-29T13:28:53+01:00
created: 2026-04-29T12:28:56+00:00
modified: 2026-07-04T10:50:46+00:00
permalink: llmeon/30-library/ops/accessing-private-aks-cluster-via-jumpbox-ssh
source: https://claude.ai/chat/891c087e-70b2-4b75-8c59-926c4c7108c1
status: null
tags: [null]
title: Accessing private AKS cluster via jumpbox SSH
type: command
---

I want to access my private aks cluster from my terminal via the jumpbox. I don't want to use the portal but be able to ssh (or equivilant) from my laptop so I can query the k8s api. How best can I do this?

---

## Accessing Private AKS via Jumpbox + Bastion

### The Architecture Decision

You've got two viable patterns here, and I want to be clear about the trade-off before you commit:

| Pattern | What you do | Trade-off |
| --- | --- | --- |
| A. Run `kubectl` on the jumpbox | Bastion SSH → jumpbox → `kubectl` lives there | Simple, but tools, kubeconfig, and shell history all live on the box. Bad DX. |
| B. SOCKS5 proxy through jumpbox → `kubectl` on laptop | Bastion tunnel → SSH SOCKS → `HTTPS_PROXY` → `kubectl` locally | Slightly more setup, but local tooling, IDE integration, normal workflow. ✅ |

You want B. It's the canonical Microsoft-documented pattern for private AKS access.

### Why SOCKS5 (The pRinciple)

A private AKS cluster's API server FQDN (`\<cluster>-\<hash>.\<region>.privatelink.azmk8s.io`) only resolves via a private DNS zone linked to the VNet. Your laptop can't resolve it—and even if you faked DNS with `/etc/hosts`, the API server has no public route.

SOCKS5 solves both problems in one move:

- DNS resolution happens on the SOCKS server (the jumpbox), which sits inside the VNet and _can_ resolve the private FQDN
- TCP traffic is tunnelled through the SSH connection, so the jumpbox terminates the network hop into AKS
- `kubectl` 's underlying Go HTTP client respects `HTTPS_PROXY=socks5://…` natively—no kubeconfig surgery, no `--insecure-skip-tls-verify` hacks, TLS SNI stays correct

The SSH-over-Bastion-tunnel piece is just the secure transport: Bastion gives you a TCP tunnel to port 22 on the jumpbox without exposing it publicly or needing a VPN.

### Prerequisites (Check These oNce)

- Bastion SKU: Native client tunnelling requires Standard SKU (not Basic/Developer). Check with:

```bash
az network bastion show -n bas-ff-uks-gp -g rg-ff-uks-gp-net --query sku
```

If it returns `Basic`, you'll need to upgrade it (one-line change, no downtime).

- SSH key on the jumpbox: You need an SSH credential—either a key pair you've added or a username/password set at VM creation. Confirm with:

```bash
az vm show -g rg-ff-uks-gp-net --name \<jumpbox-vm-name> --query osProfile.linuxConfiguration
```

- AKS RBAC / kubeconfig: You'll still need `az aks get-credentials` to have run at least once, and your AAD identity must have AKS RBAC permissions. The proxy is _network-layer_—it doesn't bypass auth.

### The Steps (Each One is One cOmmand)

You'll have three terminal tabs open. That's the mental model.

#### Tab 1—Open the Bastion Tunnel (Leave rUnning)

```bash
az network bastion tunnel \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id \<jumpbox-vm-resource-id> \
  --resource-port 22 \
  --port 50022
```

This forwards `localhost:50022` → jumpbox:22 through Bastion. Leave it open.

#### Tab 2—Open the SSH SOCKS Proxy (Leave rUnning)

```bash
ssh -D 1080 -N -p 50022 -o IdentityAgent=none -o PreferredAuthentications=password -o PubkeyAuthentication=no azadmin@127.0.0.1
```

- `-D 1080` = dynamic SOCKS5 proxy on local port 1080
- `-N` = no remote command, just the tunnel
- Leave this open too.

#### Tab 3—Use Kubectl Normally

```bash
export HTTPS_PROXY=socks5h://127.0.0.1:1080
export HTTP_PROXY=socks5h://127.0.0.1:1080
export NO_PROXY="login.microsoftonline.com,login.microsoft.com,login.windows.net,management.azure.com,graph.microsoft.com,169.254.169.254,localhost,127.0.0.1"
export no_proxy="$NO_PROXY"
```

That's it. Every `kubectl` call now routes through the jumpbox, resolves the private API FQDN there, and tunnels the HTTPS request back.

### Quality-of-life Polish (Do This once it wOrks)

Wrap the whole thing in a shell function so it's a single command:

```bash
aks-tunnel() {
  az network bastion tunnel \
    --name bas-ff-uks-gp \
    --resource-group rg-ff-uks-gp-net \
    --target-resource-id "$JUMPBOX_ID" \
    --resource-port 22 --port 50022 &
  sleep 3
  ssh -D 1080 -N -p 50022 azureuser@127.0.0.1 &
  export HTTPS_PROXY=socks5://127.0.0.1:1080
}
```

Or, more robust: a `direnv` `.envrc` per cluster that sets `HTTPS_PROXY` and a Makefile target that brings the tunnels up.

---

### 👉 Your Immediate Next Action

Run this one command to get the jumpbox VM's resource ID—you'll need it for step 1:

```bash
az vm list \
  --resource-group rg-ff-uks-gp-net \
  --query "[?contains(name, 'jumpbox') || contains(name, 'JUMPBOX')].{name:name, id:id}" \
  -o table
```

Paste the output back and I'll give you the exact tunnel command with the ID filled in. Then we verify Bastion SKU before you spend any more energy on this.

---

You

Here is the bastion details { "apiVersion": "2025-05-01", "id": "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Network/bastionHosts/bas-ff-uks-gp", "name": "bas-ff-uks-gp", "type": "microsoft.network/bastionhosts", "sku": { "name": "Standard" }, "location": "uksouth", "tags": { "CreatedWith": "Terraform", "Department": "SDE", "Environment": "prod", "ManagedBy": "FITFILE", "Status": "live" }, "properties": { "provisioningState": "Succeeded", "dnsName": "bst-32c271e8-b198-4054-a803-6a07a11cf6ef.bastion.azure.com", "scaleUnits": 2, "enableTunneling": true, "enableIpConnect": true, "publicUri": "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Network/publicIPAddresses/bas-ff-uks-gpPublicIp", "ipConfigurations": \[{ "name": "configuration", "id": "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Network/bastionHosts/bas-ff-uks-gp/bastionHostIpConfigurations/configuration", "etag": "W/\\"420793f3-f451-45d7-9d64-75f3f2aa7f52\\"", "type": "Microsoft.Network/bastionHosts/bastionHostIpConfigurations", "properties": { "provisioningState": "Succeeded", "privateIPAllocationMethod": "Dynamic", "publicIPAddress": { "id": "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Network/publicIPAddresses/bas-ff-uks-gpPublicIp" }, "subnet": { "id": "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Network/virtualNetworks/vnet-ff-uks-gp-1/subnets/AzureBastionSubnet" } } } \] }, "etag": "W/\\"420793f3-f451-45d7-9d64-75f3f2aa7f52\\"" }

---

Claude

## Bastion Verified ✅

Quick read of what you sent:

- SKU: `Standard` ✅ (tunnelling supported)
- `enableTunneling`: `true` ✅ (already enabled—no config change needed)
- `enableIpConnect`: `true` ✅ (bonus—gives you fallback options later)

You're good to go on the Bastion side. We just need the jumpbox VM's resource ID to plug into the tunnel command.

### 👉 Next Action

Run this:

```bash
az vm list \
  --resource-group rg-ff-uks-gp-net \
  --query "[].{name:name, id:id}" \
  -o table
```

The VNet JSON earlier shows a NIC called `FITFILEJUMPBOXNIC` already attached to `snet-ff-uks-gp-jumpbox`, so there should be exactly one VM in that RG (or at most a couple). Paste the output back, and I'll give you the fully-formed tunnel command with the ID dropped in—ready to copy-paste.

While you're at it, also tell me:

1. The admin username on the jumpbox (commonly `azureuser`, but yours may differ—`Fitfile`, `leon`, etc.)
2. Whether you have the SSH private key locally that pairs with whatever was put on the VM at creation time

If you don't know (2), don't worry—we can interrogate it with one more `az` command. One step at a time.

---

You

how do I switch subscriptions

---

Claude

## Switching Azure Subscriptions

### The Mental Model

The Azure CLI keeps a list of subscriptions you have access to (refreshed on `az login`) and marks one as active. Every `az` command implicitly runs against the active one unless you override with `--subscription`.

Your VNet sits in subscription `7bbc8ae5-1710-48ab-ab83-59b52bd0de1a`—that's the one you want active.

### The Commands

1\. See what you've got and what's currently active:

```bash
az account list --output table
```

The `IsDefault` column shows the active one.

2\. Switch to the one with the jumpbox:

```bash
az account set --subscription 7bbc8ae5-1710-48ab-ab83-59b52bd0de1a
```

No output = success (classic Unix philosophy).

3\. Confirm:

```bash
az account show --query "{name:name, id:id}" -o table
```

### Useful to Know

- Names work too: `az account set --subscription "Fitfile Production"` if you prefer readable names over GUIDs.
- Per-command override (no state change): `az vm list --subscription 7bbc8ae5-… -g rg-ff-uks-gp-net -o table`—handy when you're hopping between tenants and don't want to keep flipping the active context.
- If the subscription isn't listed: you likely need `az login` again, or it's in a different tenant—`az login --tenant \<tenant-id>` to pull it in.

### 👉 Immediate Next Action

```bash
az account set --subscription 7bbc8ae5-1710-48ab-ab83-59b52bd0de1a && \
az vm list --resource-group rg-ff-uks-gp-net --query "[].{name:name, id:id}" -o table
```

Two commands chained—switches sub, then lists the jumpbox VM(s). Paste the output back and we'll continue.

---

You

az account set --subscription 7bbc8ae5-1710-48ab-ab83-59b52bd0de1a && \\ az vm list --resource-group rg-ff-uks-gp-net --query "\[\].{name:name, id:id}" -o table Name -------------- FITFILEJumpbox

---

Claude

## Jumpbox Found ✅

One VM, exactly as expected from the NIC reference in the VNet JSON. Let's get the full resource ID and admin username in one shot.

### 👉 Next Action

```bash
az vm show \
  --resource-group rg-ff-uks-gp-net \
  --name FITFILEJumpbox \
  --query "{id:id, adminUser:osProfile.adminUsername, sshKeys:osProfile.linuxConfiguration.ssh.publicKeys[].keyData}" \
  -o json
```

This returns three things we need:

| Field | Why we need it |
| --- | --- |
| `id` | The full resource ID for the Bastion `--target-resource-id` flag |
| `adminUser` | The username for the SSH command (likely `azureuser` but let's confirm) |
| `sshKeys` | The public keys provisioned on the box—so you can match them against your local private keys in `~/.ssh/` |

### What to Look for in the Output

- `id` will be a long `/subscriptions/…/FITFILEJumpbox` string—paste it back.
- `adminUser`—note this verbatim.
- `sshKeys`—this returns the public key(s) that were authorised on the VM at provision time. Compare the start of the key (e.g., `ssh-rsa AAAAB3…` or `ssh-ed25519 AAAAC3…`) against your local keys:

```bash
for f in ~/.ssh/*.pub; do echo "=== $f ==="; cat "$f"; done
```

If one of yours matches, you've got the private key needed to SSH in. If none match, we have a separate small problem to solve (Azure can reset/add keys via `az vm user update`—easy fix).

Paste the `az vm show` output and the local pubkey list back, and I'll give you the fully-formed Bastion tunnel command next.

---

You

az vm show \\ --resource-group rg-ff-uks-gp-net \\ --name FITFILEJumpbox \\ --query "{id:id, adminUser:osProfile.adminUsername, sshKeys:osProfile.linuxConfiguration.ssh.publicKeys\[\].keyData}" \\ -o json { "adminUser": "azadmin", "id": "/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox", "sshKeys": \[\] }

---

Claude

## Three Things Confirmed, One Problem to Solve

### What We Know Now

| Item | Value | Status |
| --- | --- | --- |
| Resource ID | `/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox` | ✅ |
| Admin user | `azadmin` | ✅ |
| SSH public keys provisioned | `[]` (empty) | ⚠️ |

### The Problem (And Why It's Not Really a Problem)

`sshKeys: []` means the VM was created with password authentication, not key-based auth. That's not unusual for a Bastion-fronted jumpbox—Bastion is the security boundary, so the SSH layer behind it is sometimes treated more loosely.

You have three options. Pick based on what you actually know.

#### Option A—You Already Know the Password

Skip to the tunnel step. SSH will prompt for it. Done.

#### Option B—You Don't Know the Password, but want Keys (Recommended)

Inject _your_ public key onto the VM with one command. No reboot, no downtime, runs via the Azure VM agent:

```bash
az vm user update \
  --resource-group rg-ff-uks-gp-net \
  --name FITFILEJumpbox \
  --username azadmin \
  --ssh-key-value "$(cat ~/.ssh/id_ed25519.pub)"
```

> Adjust the path if your key is `id_rsa.pub` or similar. List them with `ls ~/.ssh/*.pub`. If you don't have one, generate it: `ssh-keygen -t ed25519 -C "leon-jumpbox"`.

This adds to `~azadmin/.ssh/authorized_keys`—it doesn't wipe existing access, so it's safe.

#### Option C—Reset the Password

```bash
az vm user update -g rg-ff-uks-gp-net -n FITFILEJumpbox -u azadmin -p '\<NewStrongPassword>'
```

Less hygienic. Avoid unless there's a reason.

### My Recommendation

Option B. Here's why:

- No secrets in shell history (passwords typed at SSH prompts can be logged by terminal recorders, multiplexers, etc.)
- Reproducible—same key works next week, next laptop, next teammate (their key, not yours)
- Auditable—`az vm user update` is logged in Activity Log; password resets are too, but key-based auth makes ongoing access traceable to the keypair
- Matches your existing posture—you already use Vault/VSO for secret discipline; this is consistent

### 👉 Immediate Next Action

Step 1—check what keys you have locally:

```bash
ls -la ~/.ssh/*.pub
```

Paste the output. If you see `id_ed25519.pub` or `id_rsa.pub`, we're ready to inject it. If `~/.ssh/` is empty or doesn't exist, the next step is generating a key—also one command.

---

You

I know the username and password already set. How do I do SOCKS5 option B

---

Claude

## SOCKS5 Tunnel—Username/Password Path

You already have the credentials, so we skip the key-injection step entirely. Here's the full flow.

### Three Tabs, In Order

#### Tab 1—Bastion Tunnel (Leave rUnning)

```bash
az network bastion tunnel \
  --name bas-ff-uks-gp \
  --resource-group rg-ff-uks-gp-net \
  --target-resource-id /subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox \
  --resource-port 22 \
  --port 50022
```

You'll see something like `Opening tunnel on port: 50022` and `Tunnel is ready, connect on port 50022`. Leave this tab open—closing it kills the tunnel.

#### Tab 2—SSH SOCKS Proxy (Leave rUnning)

```bash
ssh -D 1080 -N -p 50022 azadmin@127.0.0.1
```

- First time you connect, SSH will ask you to confirm the host fingerprint (`yes`)
- Then it'll prompt for the password—type it
- After authentication, the terminal will appear to hang—that's correct. `-N` means "no remote command, just hold the tunnel open."

Leave this tab open too.

##### Quick Flag Reference

| Flag | Purpose |
| --- | --- |
| `-D 1080` | Open a SOCKS5 proxy on local port 1080 |
| `-N` | Don't run a remote command (tunnel-only) |
| `-p 50022` | Connect to the local Bastion-forwarded port |

#### Tab 3—Use Kubectl

```bash
export HTTPS_PROXY=socks5://127.0.0.1:1080
export HTTP_PROXY=socks5://127.0.0.1:1080
kubectl get nodes
```

The `HTTPS_PROXY` env var is what `kubectl` 's Go HTTP client picks up. DNS for the private API FQDN gets resolved on the jumpbox side of the SOCKS proxy—which is why this works without any DNS faffing on your laptop.

### Pre-flight Check (Do This once before Tab 1)

Make sure you have a kubeconfig for the cluster. From the same subscription:

```bash
az aks list -o table
```

Then for whichever cluster you're targeting:

```bash
az aks get-credentials \
  --resource-group \<aks-rg> \
  --name \<aks-cluster-name>
```

This writes the kubeconfig context with the private API server FQDN—exactly what you want, because the SOCKS proxy will resolve it inside the VNet.

### Common Gotchas

- `Permission denied` on Tab 2: triple-check the username is `azadmin` and that you're typing the password (it won't echo). If the VM uses `PasswordAuthentication no` in `sshd_config`, you'll need Option B (key injection) after all—let me know if that happens.
- `kubectl` hangs forever: usually means the SOCKS tunnel isn't healthy. Check Tab 2—if SSH disconnected silently, reconnect. Add `-o ServerAliveInterval=30 -o ServerAliveCountMax=3` to the SSH command to keep it alive.
- `Unable to connect to the server: dial tcp: lookup … no such host`: `HTTPS_PROXY` isn't set in the tab where you're running `kubectl`. It's per-shell—you have to export it in Tab 3 specifically.

### 👉 Immediate Next Action

Open Tab 1 and run the `az network bastion tunnel` command above. Wait for the `Tunnel is ready` message, then come back and we'll fire up Tab 2.

If anything errors, paste it here—Bastion tunnel errors are usually a clear permissions or networking message we can fix in one step.

---

You

ssh -D 1080 -N -p 50022 azadmin@127.0.0.1 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ @ WARNING: REMOTE HOST IDENTIFICATION HAS CHANGED! @ @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ IT IS POSSIBLE THAT SOMEONE IS DOING SOMETHING NASTY! Someone could be eavesdropping on you right now (man-in-the-middle attack)! It is also possible that a host key has just been changed. The fingerprint for the ED25519 key sent by the remote host is SHA256:UCGKDJN7GLx3A8s7Gn7NqGD1Ef1mmwY8xm2ivq+lDik. Please contact your system administrator. Add correct host key in /Users/leon.ormes/.ssh/known\_hosts to get rid of this message. Offending ECDSA key in /Users/leon.ormes/.ssh/known\_hosts:43 Host key for \[127.0.0.1\]:50022 has changed and you have requested strict checking. Host key verification failed.

---

Claude

## Expected—Not A Real Security Issue

### What's Actually Happening

SSH is doing its job. Here's the principle:

`127.0.0.1:50022` is just a local port that points somewhere. Today it points to `FITFILEJumpbox` via Bastion. On line 43 of your `known_hosts`, SSH has remembered a _different_ host key for that same `127.0.0.1:50022`—almost certainly from a previous tunnel session to a different VM (could be EOE work, a previous AKS jumpbox, anything).

SSH can't tell whether you've intentionally repointed the tunnel or whether a MITM is happening. It refuses to connect and shouts at you. Correct behaviour.

### The Fix

Remove the stale entry on line 43:

```bash
ssh-keygen -R "[127.0.0.1]:50022"
```

This surgically removes any cached host key for that exact host:port pair. Cleaner than editing `known_hosts` by hand.

Then re-run the SSH command—you'll get the normal first-connection prompt:

```bash
ssh -D 1080 -N -p 50022 azadmin@127.0.0.1
```

You'll see:

```
The authenticity of host '[127.0.0.1]:50022' can't be established.
ED25519 key fingerprint is SHA256:UCGKDJN7GLx3A8s7Gn7NqGD1Ef1mmwY8xm2ivq+lDik.
Are you sure you want to continue connecting (yes/no/[fingerprint])?
```

Type `yes`, then your password.

### Verifying the Fingerprint (Optional but pRoper)

The fingerprint SSH shows you should match what's actually on the jumpbox. You can verify via Bastion's interactive SSH (different code path, no port-forwarding cache) or by running this on the VM once you're in:

```bash
sudo ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

If it matches `SHA256:UCGKDJN7GLx3A8s7Gn7NqGD1Ef1mmwY8xm2ivq+lDik`, you're golden. Given this is your own Bastion → your own VM in your own subscription, the MITM risk surface is essentially zero—but the discipline of checking once is worthwhile.

### Long-Term Fix (Worth Doing oNce)

Add this to `~/.ssh/config` so localhost-tunnel collisions stop happening:

```
Host fitfile-jumpbox
  HostName 127.0.0.1
  Port 50022
  User azadmin
  UserKnownHostsFile ~/.ssh/known_hosts.d/fitfile-jumpbox
  StrictHostKeyChecking accept-new
  DynamicForward 1080
  ServerAliveInterval 30
  ServerAliveCountMax 3
```

Then ensure the directory exists once: `mkdir -p ~/.ssh/known_hosts.d`

After that, `ssh -N fitfile-jumpbox` does everything—separate known\_hosts file means no more collisions with other tunnels on the same port, and `accept-new` means new hosts don't error but changes still do.

### 👉 Immediate Next Action

```bash
ssh-keygen -R "[127.0.0.1]:50022" && ssh -D 1080 -N -p 50022 azadmin@127.0.0.1
```

One line, two commands chained. Removes the stale entry, then opens the SOCKS tunnel. Type `yes` then your password when prompted.

---

You

ssh -D 1080 -N -p 50022 azadmin@127.0.0.1 The authenticity of host '\[127.0.0.1\]:50022 (\[127.0.0.1\]:50022)' can't be established. ED25519 key fingerprint is: SHA256:UCGKDJN7GLx3A8s7Gn7NqGD1Ef1mmwY8xm2ivq+lDik This key is not known by any other names. Are you sure you want to continue connecting (yes/no/\[fingerprint\])? yes Warning: Permanently added '\[127.0.0.1\]:50022' (ED25519) to the list of known hosts. Received disconnect from 127.0.0.1 port 50022:2: Too many authentication failures Disconnected from 127.0.0.1 port 50022 I use 1password to manage ssh keys. I haev this in my ssh/config cat ~/.ssh/config Include /Volumes/DAL/.colima/ssh\_config Include /Users/leon.ormes/.colima/ssh\_config Include /Users/leon.ormes/.config/colima/ssh\_config Host \* IdentityAgent "/Users/leon.ormes/Library/Group Containers/\[2BUA8C4S2C.com\]([http://2BUA8C4S2C.com).1password/t/agent.sock](http://2bua8c4s2c.com\).1password/t/agent.sock) " Host hie-jmp-prod HostName i-09f84bb55556a2c10 User awsadmin IdentityFile ~/.ssh/jumpbox\_awsadmin\_key IdentitiesOnly yes PreferredAuthentications publickey PubkeyAuthentication yes ServerAliveInterval 60 ServerAliveCountMax 3 RequestTTY yes ForwardX11 no ForwardAgent no ProxyCommand sh -c "aws ssm start-session --target %h --region eu-west-2 --profile ${AWS\_PROFILE:-eoe-hie} --document-name AWS-StartSSHSession --parameters 'portNumber=22'" Host hie-jmp-test HostName i-0c1d974fcac60d438 User awsadmin IdentityFile ~/.ssh/jumpbox\_awsadmin\_key IdentitiesOnly yes PreferredAuthentications publickey PubkeyAuthentication yes ServerAliveInterval 60 ServerAliveCountMax 3 RequestTTY yes ForwardX11 no ForwardAgent no ProxyCommand sh -c "aws ssm start-session --target %h --region eu-west-2 --profile ${AWS\_PROFILE:-eoe-hie} --document-name AWS-StartSSHSession --parameters 'portNumber=22'"

---

Claude

## Diagnosed: 1Password Agent is the Culprit

### What's Happening (The pRinciple)

Your top-level `Host *` block tells every SSH connection to use the 1Password agent as its identity source. The 1Password agent then dutifully offers every key it has to the jumpbox, one after another.

OpenSSH servers default to `MaxAuthTries 6`. After 6 failed key attempts, the server disconnects with `Too many authentication failures`—_before SSH ever gets to ask you for a password_.

You never see a password prompt because the connection dies during key offers.

This is a classic 1Password-agent-meets-password-auth conflict. Two ways out: a one-shot flag, or a config block.

### Fix Option 1—One-shot (Quick, Validates the tHeory)

```bash
ssh -D 1080 -N -p 50022 \
  -o IdentityAgent=none \
  -o PreferredAuthentications=password \
  -o PubkeyAuthentication=no \
  azadmin@127.0.0.1
```

What each flag does:

| Flag | Purpose |
| --- | --- |
| `IdentityAgent=none` | Don't use 1Password agent (or any agent) for this connection |
| `PubkeyAuthentication=no` | Don't even try public-key auth |
| `PreferredAuthentications=password` | Go straight to password |

If this works, the diagnosis is confirmed and you can move to Option 2 to make it permanent.

### Fix Option 2—Permanent (Do This once it wOrks)

Add a host block to `~/.ssh/config`. Crucially, place it ABOVE the `Host *` block—SSH applies the _first_ matching value for each option, so order matters.

```
Host fitfile-jumpbox
  HostName 127.0.0.1
  Port 50022
  User azadmin
  IdentityAgent none
  PubkeyAuthentication no
  PreferredAuthentications password
  UserKnownHostsFile ~/.ssh/known_hosts.d/fitfile-jumpbox
  StrictHostKeyChecking accept-new
  DynamicForward 1080
  ServerAliveInterval 30
  ServerAliveCountMax 3
```

Then connect with just:

```bash
mkdir -p ~/.ssh/known_hosts.d   # one-time
ssh -N fitfile-jumpbox
```

The `DynamicForward 1080` baked into the host block means you don't need `-D 1080` on the command line either.

### A Better Fix You Should Genuinely Consider

Now that you can see the friction, injecting your 1Password-managed SSH key onto the jumpbox is the cleaner long-term answer. It would mean:

- No password typing
- No `IdentityAgent=none` workaround fighting your normal posture
- Consistent with how you already access `hie-jmp-prod` / `hie-jmp-test`

If you've got a public key visible in 1Password's SSH agent, you can grab it and inject it onto the VM with one Azure CLI command (the same `az vm user update --ssh-key-value` from earlier). This is what you'd do anyway if a teammate joined the team—keys, not passwords.

But—finish the immediate task first. Get the tunnel working with password auth, prove the SOCKS5 → kubectl path, _then_ graduate to keys when you have the cycles.

### 👉 Immediate Next Action

Run the one-shot version to validate:

```bash
ssh -D 1080 -N -p 50022 \
  -o IdentityAgent=none \
  -o PreferredAuthentications=password \
  -o PubkeyAuthentication=no \
  azadmin@127.0.0.1
```

You should now get a clean password prompt. Enter it. Terminal will then "hang" with no output—that's `-N` doing its job. Open a new tab for `kubectl` and we're at the finish line.

---

You

the kubectl get nodes command failed like this

---

Claude

## Two Distinct Problems Visible—Let's Untangle Them

You're actually past the SSH hurdle. The `Password:` prompt appeared and (presumably) succeeded—the SOCKS tunnel is alive. But two new things have surfaced.

### Problem 1—channel 2: Open Failed: Connect Failed (The SOCKS eRrors)

These are coming from your SSH tunnel. They mean: a SOCKS client asked the jumpbox to open a TCP connection to some destination, and the jumpbox couldn't reach it.

Look at the bottom of your screenshot—the destination it failed on is `login.microsoftonline.com:443`. That's `az` / `kubectl` 's AAD auth call, being forced through your SOCKS proxy and dying inside the VNet.

### Problem 2—az/kubelogin is Going through the Proxy

This is the deeper issue. You set `HTTPS_PROXY=socks5://127.0.0.1:1080` for `kubectl`. But your kubeconfig almost certainly uses `kubelogin` (or `az` exec auth) to fetch an AAD token before talking to the API server. That auth helper _also_ respects `HTTPS_PROXY` and is now tunnelling the AAD token request through the jumpbox—which can't reach `login.microsoftonline.com` because of egress restrictions (Azure Firewall, NSGs, no public route from that subnet, or all of the above).

So the architecture should actually be:

```
AAD token fetch  →  direct internet from your laptop  ✅
kubectl API call →  SOCKS5 → jumpbox → private AKS API  ✅
```

Not:

```
AAD token fetch  →  SOCKS5 → jumpbox → ❌ can't reach login.microsoftonline.com
```

### The Fix—Tell the Proxy to Skip AAD Endpoints

Set `NO_PROXY` so AAD/ARM calls bypass SOCKS:

```bash
export HTTPS_PROXY=socks5://127.0.0.1:1080
export HTTP_PROXY=socks5://127.0.0.1:1080
export NO_PROXY="login.microsoftonline.com,login.microsoft.com,login.windows.net,management.azure.com,graph.microsoft.com,*.azurecr.io"
export no_proxy="$NO_PROXY"   # lowercase too — some libs only check one
kubectl get nodes
```

What this does: any HTTP client (Go's `net/http`, Python's `requests`) checks `NO_PROXY` first. Hostnames matching go direct. So:

- `kubelogin` → AAD = direct ✅
- `kubectl` → private AKS FQDN = via SOCKS ✅

### Get a Clean Token First

Before re-running, refresh your AAD context without the proxy active. Open a fresh tab (no env vars set) and run:

```bash
az account get-access-token --resource https://management.azure.com/ > /dev/null
kubelogin get-token --help >/dev/null 2>&1 && echo "kubelogin present" || echo "kubelogin MISSING"
```

If `kubelogin` is missing, install it: `brew install Azure/kubelogin/kubelogin`. Modern AKS kubeconfigs almost always need it for AAD auth.

### Verifying the SOCKS Path Itself Works

Quick sanity check that the tunnel actually works for _something_:

```bash
curl --socks5-hostname 127.0.0.1:1080 -sI https://www.google.com | head -1
```

`--socks5-hostname` (not `--socks5`) ensures DNS happens on the jumpbox side, mirroring what `kubectl` does. If this returns `HTTP/2 200`, your tunnel is healthy and outbound internet from the jumpbox works. If it hangs or fails, the jumpbox itself has restricted egress and we'll need to think differently (more on this below).

### If The Jumpbox Has No Internet Egress

Possible—it sits in `snet-ff-uks-gp-jumpbox` and may be locked down to "only reach AKS API". In that case:

- The `NO_PROXY` fix above is mandatory (AAD must go direct)
- The SOCKS tunnel only needs to reach the AKS private API IP, not the wider internet—that's fine

### 👉 Immediate Next Action

In your `kubectl` tab (Tab 3), run this complete sequence:

```bash
export HTTPS_PROXY=socks5h://127.0.0.1:1080
export HTTP_PROXY=socks5h://127.0.0.1:1080
export NO_PROXY="login.microsoftonline.com,login.microsoft.com,login.windows.net,management.azure.com,graph.microsoft.com,169.254.169.254,localhost,127.0.0.1"
export no_proxy="$NO_PROXY"
kubectl get nodes
```

Two changes from before:

1. `socks5h://` (the `h` forces remote DNS resolution—same as `--socks5-hostname`; critical for the private AKS FQDN)
2. `NO_PROXY` carves out AAD/ARM so token auth goes direct

Paste the output. If it errors, the error message will now tell us _which_ layer is failing rather than mixing them up.

---

You

curl --socks5-hostname 127.0.0.1:1080 -sI [https://www.google.com](https://www.google.com/) | head -1 HTTP/2 200 /V/D/Z/LLMeon on  main ✘? on ⛵ aks-ff-uks-gp-1 () on ☁ Testing on 🅰 (eu-west-2) at 09:35:27 ❯ export HTTPS\_PROXY=socks5\<h://127.0.0.1:1080> export HTTP\_PROXY=socks5\<h://127.0.0.1:1080> export NO\_PROXY="\[login.microsoftonline.com\]([http://login.microsoftonline.com),\[login.microsoft.com\](http://login.microsoft.com),\[login.windows.net\](http://login.windows.net),\[management.azure.com\](http://management.azure.com),\[graph.microsoft.com\](http://graph.microsoft.com),169.254.169.254,\[localhost\](http://localhost),127.0.0.1](http://login.microsoftonline.com\),[login.microsoft.com]\(http://login.microsoft.com\),[login.windows.net]\(http://login.windows.net\),[management.azure.com]\(http://management.azure.com\),[graph.microsoft.com]\(http://graph.microsoft.com\),169.254.169.254,[localhost]\(http://localhost\),127.0.0.1) " export no\_proxy="$NO\_PROXY" kubectl get nodes NAME STATUS ROLES AGE VERSION aks-system-65569669-vmss00000w Ready \<none> 97m v1.33.2 aks-system-65569669-vmss00000x Ready \<none> 97m v1.33.2

---

Claude

## 🎉 You're In

Two nodes responding, both `Ready`, on the private API of `aks-ff-uks-gp-1`. The full path is now working end-to-end:

```
laptop kubectl
  → SOCKS5 (DNS on jumpbox)
  → Bastion tunnel (TCP)
  → jumpbox in snet-ff-uks-gp-jumpbox
  → private AKS API (privatelink.azmk8s.io)
  ✅
```

And the `curl … google.com → HTTP/2 200` confirms the jumpbox has general internet egress too—useful to know for future debugging.

### What Just Worked (The Principle, Locked iN)

- `socks5h://`—the `h` was the critical fix. Without it, your laptop tries to resolve the private AKS FQDN and fails. With it, DNS happens on the jumpbox, which is inside the VNet linked to the private DNS zone.
- `NO_PROXY` for AAD/ARM—auth tokens fetched direct from your laptop, kube API traffic via SOCKS. Different planes, different paths.
- `IdentityAgent=none` etc.—bypassed 1Password agent so password auth got a chance before `MaxAuthTries` killed the connection.

### Make This Permanent (Recommended, ~5 mIn)

Right now this is fragile across new shells. Three things to do, in priority order.

#### 1\. Persist the SSH Config

Add this above your `Host *` block in `~/.ssh/config`:

```sh
Host fitfile-jumpbox
  HostName 127.0.0.1
  Port 50022
  User azadmin
  IdentityAgent none
  PubkeyAuthentication no
  PreferredAuthentications password
  UserKnownHostsFile ~/.ssh/known_hosts.d/fitfile-jumpbox
  StrictHostKeyChecking accept-new
  DynamicForward 1080
  ServerAliveInterval 30
  ServerAliveCountMax 3
```

Then: `mkdir -p ~/.ssh/known_hosts.d`

#### 2\. A Bring-up Function in Your Shell Rc

Add to `~/.zshrc` (you're clearly on macOS + zsh):

```
# AKS private cluster access via Bastion + jumpbox
aks-ff-up() {
  local jumpbox_id="/subscriptions/7bbc8ae5-1710-48ab-ab83-59b52bd0de1a/resourceGroups/rg-ff-uks-gp-net/providers/Microsoft.Compute/virtualMachines/FITFILEJumpbox"
  echo "→ Opening Bastion tunnel..."
  az network bastion tunnel \
    --name bas-ff-uks-gp \
    --resource-group rg-ff-uks-gp-net \
    --target-resource-id "$jumpbox_id" \
    --resource-port 22 --port 50022 &>/tmp/bastion-tunnel.log &
  echo "  Bastion PID: $!  (log: /tmp/bastion-tunnel.log)"
  sleep 4
  echo "→ Opening SSH SOCKS proxy (will prompt for password)..."
  ssh -N -f fitfile-jumpbox
  echo "→ Tunnels up."
}

aks-ff-env() {
  export HTTPS_PROXY=socks5h://127.0.0.1:1080
  export HTTP_PROXY=socks5h://127.0.0.1:1080
  export NO_PROXY="login.microsoftonline.com,login.microsoft.com,login.windows.net,management.azure.com,graph.microsoft.com,169.254.169.254,localhost,127.0.0.1"
  export no_proxy="$NO_PROXY"
  echo "→ Proxy env set for this shell. kubectl is now routed via SOCKS."
}

aks-ff-down() {
  pkill -f "bastion tunnel.*50022" && echo "→ Bastion tunnel stopped"
  pkill -f "ssh -N -f fitfile-jumpbox" && echo "→ SSH tunnel stopped"
  unset HTTPS_PROXY HTTP_PROXY NO_PROXY no_proxy
  echo "→ Proxy env unset."
}
```

Workflow becomes:

```bash
aks-ff-up        # once per session — types password
aks-ff-env       # in any shell where you want kubectl via SOCKS
kubectl get pods -A
# ... do work ...
aks-ff-down      # when finished
```

The `aks-ff-env` is separate because you only want it in shells where you're using `kubectl` / `helm` / `argocd`—not your general terminal where it would route random `curl` commands through the proxy.

#### 3\. Worth Doing Soon: Kill the Password

You called this out earlier—using passwords here is friction against your existing 1Password-keys posture. Once you've validated the workflow above, inject your 1Password-managed public key:

```bash
# Get your 1Password-served public key
ssh-add -L | grep -v colima   # filter colima keys; grab the one you want

# Inject onto the jumpbox
az vm user update \
  -g rg-ff-uks-gp-net \
  -n FITFILEJumpbox \
  -u azadmin \
  --ssh-key-value "\<paste-the-public-key-line>"
```

Then change the `Host fitfile-jumpbox` block: remove the three `IdentityAgent=none / PubkeyAuthentication=no / PreferredAuthentications=password` lines. SSH will fall back to your normal `Host *` block (1Password agent), find a matching key, and authenticate silently. No more password prompts.

### Things to Sanity-Check Now You're In

While the tunnel's hot, validate a few things you'll care about for the AKS work:

```bash
kubectl get ns                              # what's deployed
kubectl get pods -A | grep -v Running       # any unhealthy
kubectl config current-context              # confirm right cluster
kubectl cluster-info                        # confirms private FQDN in use
```

That last one is satisfying—`cluster-info` will print the `privatelink.azmk8s.io` URL, confirming the private API is what's responding.
