---
aliases: []
confidence: 
created: 2025-11-25T13:52:47Z
epistemic: 
last_reviewed: 
modified: 2025-11-25T13:53:01Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Use SSH Tunnel Method
type: 
uid: 
updated: 
---

The `--disable-gateway` flag isn't available in your Azure CLI version. Let's use the **SSH tunnel method** instead, which is more reliable for password authentication:

## Use SSH Tunnel Method

```bash
# Start the Bastion tunnel (runs in background)
az network bastion tunnel \
  --name $BASTION_NAME \
  --resource-group $RESOURCE_GROUP \
  --target-resource-id $VM_ID \
  --resource-port 22 \
  --port 2222 &

# Wait a few seconds for tunnel to establish
sleep 5

# Connect via SSH with password authentication forced
ssh -o PreferredAuthentications=password \
    -o PubkeyAuthentication=no \
    -o NumberOfPasswordPrompts=1 \
    azadmin@localhost -p 2222
```

## Alternative: Clear SSH Keys First

If you prefer the direct method, clear your SSH agent keys first:

```bash
# Clear all SSH keys from agent
ssh-add -D

# Retry the direct bastion SSH command
az network bastion ssh \
  --name $BASTION_NAME \
  --resource-group $RESOURCE_GROUP \
  --target-resource-id $VM_ID \
  --auth-type password \
  --username azadmin
```

## Clean Up Tunnel When Done

After you finish your SSH session:

```bash
# Find the tunnel process
jobs

# Kill the background job (use job number, e.g., %1)
kill %1

# Or find and kill by process name
pkill -f "bastion tunnel"
```

The tunnel method creates a local port (2222) that forwards to the VM through Azure Bastion, giving you full control over SSH authentication options. This bypasses the authentication method conflicts that occur with the direct `az network bastion ssh` command.
