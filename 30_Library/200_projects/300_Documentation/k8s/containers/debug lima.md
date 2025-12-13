---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, workstation]
title: debug lima
type:
uid: 
updated: 
version:
---

The error `kex_exchange_identification: read: Connection reset by peer` typically indicates a failure in the SSH handshake process. This can occur due to a variety of issues, including the SSH server on the Lima VM not running or refusing the connection. Here's how to debug and fix this:

---

## 1. Verify if the VM is Running

Ensure that the `default` VM is running:

```bash
limactl list
```

- Check the `STATUS` column. If the status is not `Running`, start the VM:

```bash
limactl start default
```

---

## 2. Check SSH Server on the VM

The SSH server inside the Lima VM might not be running or has crashed. You can check this by:

1. Inspecting the Lima VM logs:

```bash
limactl log default
```

    Look for entries related to SSH or port `60022`.
    
2. Restart the Lima VM to ensure a clean state:

```bash
limactl stop default
limactl start default
```

---

## 3. Manually Test SSH on Port 60022

Run an `nc` (Netcat) command to see if the SSH server is listening on port `60022`:

```bash
nc -vz 127.0.0.1 60022
```

- If successful, it will output something like `Connection to 127.0.0.1 60022 port [tcp/] succeeded!`.
- If it fails, the SSH server is not listening, and you'll need to investigate further.

---

## 4. Inspect the VM Configuration

Check the Lima `default` instance's configuration file to ensure proper SSH settings:

```bash
cat ~/.lima/default/lima.yaml
```

- Look for the `sshLocalPort` setting. It should be set to `60022` (or match the port you are connecting to).
- Ensure that `ssh` is listed under `provision` or `provisionControl`.

---

## 5. Recreate SSH Keys

If the SSH keys are corrupted or mismatched, reset them:

1. Delete the old keys:

```bash
rm -rf ~/.lima/_config/user ~/.lima/default/ssh.sock
```

1. Restart the VM to regenerate the keys:

```bash
limactl stop default
limactl start default
```

---

## 6. Recreate the VM (if necessary)

If the above steps fail, the VM might be in a corrupted state. Recreate it:

```bash
limactl delete default
limactl start --name=default
```

Note: Back up any important data before deleting the VM.

---

## 7. Inspect Host Logs

If the issue persists, check the host system logs for more details about the SSH connection failure:

```bash
log show --predicate 'process == "ssh"' --info
```
