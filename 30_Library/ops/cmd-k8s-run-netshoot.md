---
created: 2026-02-18T17:19:06+00:00
hop_level: local
modified: 2026-02-19T13:17:45+00:00
prerequisites:
  - [[cmd-ssh-bastion-tunnel]]
requires_tunnel: true
tags: [atomic, debug, kubectl, netshoot, network]
target_service: network
title: cmd-k8s-run-netshoot
tool: kubectl
type: atomic_command
---

## Spin Up Netshoot Diagnostic Shell

### 🎯 Intent

Deploy a temporary, ephemeral pod or container containing a suite of network troubleshooting tools (mtr, nmap, tcpdump, curl, etc.) to diagnose connectivity from within the cluster's network namespace or the host network.

---

### 🌍 Execution Context

Run from:

- [x] Local machine (with active tunnel)
- [ ] Bastion host

Active requirements:

- [x] KUBECONFIG context set to target cluster
- [x] SSH tunnel active (if private cluster)

---

### ⚡ Action

#### 1. Standalone Throwaway Pod (Default)

```bash
kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot -- bash
```

#### 2. Ephemeral Container (Debug Existing Pod)

_Requires Kubernetes 1.23+_

```bash
kubectl debug <pod_name> -it --image=nicolaka/netshoot --namespace <namespace>
```

#### 3. Run on Host Network Namespace

_Use this to troubleshoot the node's network stack directly._

```bash
kubectl run tmp-shell --rm -i --tty --overrides='{"spec": {"hostNetwork": true}}' --image nicolaka/netshoot
```

#### Placeholders

- `<user_initials>`—To avoid name collisions in multi-user clusters.
- `<namespace>`—The namespace to run the pod in.
- `<pod_name>`—Name of the existing pod to debug.

---

### ✅ Verification

Inside the pod, run:

```bash
ip addr show eth0
```

Expected signal:

- Pod starts, drops into a bash prompt, and shows a valid IP address (Pod IP or Host IP depending on mode).

---

### 🧠 Failure Modes

- ImagePullBackOff: Cluster cannot reach Docker Hub/Public registries. See [[pb-cross-cluster-connectivity-triage]].
- Admission Webhook Denied: PSP or Kyverno/OPA policies may block privileged containers, hostNetwork, or specific namespaces.

---

### 🔗 Related

- [[pb-cross-cluster-connectivity-triage]]
- [[pb-hie-nnuh-connectivity]]
- [[cmd-net-mtr-tcp]]
- [[cmd-net-nmap-check-filtered]]
- [[cmd-net-get-egress-ip]]
