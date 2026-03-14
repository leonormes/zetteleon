---
captured: "2026-03-07T16:54:47+00:00 2026-03-07T16:54:47+00:00"
created: 2026-03-07T16:54:48+00:00
modified: 2026-03-14T11:10:35+00:00
source: "https://claude.ai/chat/2a409c00-6971-4568-824c-841181c4c93a"
status: "processing"
tags: ["input"]
title: HEAD Port forwarding EKS pod through SSM jumpbox
type: "head"
---

## Raw Output / Content

I have a private aws eks cluster. I access it via a jumpbox in the vpc that I can use ssm to reach from my local machine's terminal. The cluster has an application with a webpage that I need to access. Is it possible to portforward the pod via the ssm connection to my local machine so I can use my chome browser to access it?

---

Yes, absolutely. You'll chain two tunnels: SSM Session Manager port-forward from your local machine to the jumpbox, and kubectl port-forward on the jumpbox to the pod. Your browser hits `localhost` → SSM tunnel → jumpbox → kubectl → pod.

There are two main approaches:

---

## Approach 1: SSM Port Forward + Kubectl on the Jumpbox (simplest)

This uses SSM's built-in port forwarding to relay a port from the jumpbox back to your laptop.

### On the Jumpbox (via SSM shell)

Start kubectl port-forward on the jumpbox, binding to `0.0.0.0` so it's reachable from the SSM tunnel:

> If it's a service rather than a pod, use `svc/<service-name>` instead.

### On Your Local Machine

Open an SSM port-forwarding session that maps your local port to the jumpbox's port 8080:

Now open Chrome → `http://localhost:8080`—done.

---

## Approach 2: SSM Remote Port Forward (no Shell Needed on jumpbox)

If `kubectl` is already running on the jumpbox (e.g. via a systemd service or you've backgrounded it), you can use the `AWS-StartPortForwardingSessionToRemoteHost` document to forward directly to `localhost:8080` _on the jumpbox_:

This is handy if you want a single command locally and have `kubectl port-forward` already running on the jumpbox.

---

## Why This Works

SSM Session Manager creates a WebSocket tunnel through the SSM endpoint—no inbound security group rules, no SSH keys, no bastion public IP needed. The `kubectl port-forward` on the jumpbox works because the jumpbox has network access to the EKS API server and pod network (it's in the VPC). The two tunnels compose: local ↔ SSM ↔ jumpbox ↔ k8s pod.

## Gotchas to Watch for

- Security group: The jumpbox's SG doesn't need any inbound rules for SSM, but the EKS cluster security group must allow traffic from the jumpbox on port 443 (API server) and the pod's target port.
- `--address 0.0.0.0`: Without this, `kubectl port-forward` binds to `127.0.0.1` only, which works fine for Approach 2 (since SSM tunnels to `localhost` on the jumpbox) but is needed if anything else on the jumpbox needs to reach it.
- kubeconfig on the jumpbox: Make sure `aws eks update-kubeconfig --name <cluster-name> --region <region>` has been run there, and the jumpbox's IAM role has the right RBAC mapping in the `aws-auth` ConfigMap.

## Your next Micro-step

SSH into the jumpbox now and confirm kubectl works:

Once you can see the target pod, you're one command away from the port-forward.
