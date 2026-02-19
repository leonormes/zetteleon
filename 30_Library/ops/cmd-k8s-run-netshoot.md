---
type: atomic_command
tool: kubectl
hop_level: local
target_service: network
requires_tunnel: true
prerequisites:
  - [[cmd-ssh-bastion-tunnel]]
tags: #atomic #kubectl #network #netshoot #debug
---

# Spin Up Netshoot Diagnostic Shell

## 🎯 Intent
Deploy a temporary, ephemeral pod containing a suite of network troubleshooting tools (mtr, nmap, tcpdump, curl, etc.) to diagnose connectivity from within the cluster's network namespace.

---

## 🌍 Execution Context
Run from:
- [x] Local machine (with active tunnel)
- [ ] Bastion host

Active requirements:
- [x] KUBECONFIG context set to target cluster
- [x] SSH tunnel active (if private cluster)

---

## ⚡ Action

```bash
kubectl run tmp-shell-<user_initials> \
  --rm \
  -i \
  --tty \
  --image nicolaka/netshoot \
  --namespace <namespace> \
  -- bash
```

### Placeholders
- `<user_initials>` — To avoid name collisions in multi-user clusters.
- `<namespace>` — The namespace to run the pod in (for testing intra-namespace or service discovery).

---

## ✅ Verification
Inside the pod, run:
```bash
ip addr show eth0
```
Expected signal:
- Pod starts, drops into a bash prompt, and shows a valid cluster IP.

---

## 🧠 Failure Modes
- **ImagePullBackOff:** Cluster cannot reach Docker Hub/Public registries. See [[pb-cross-cluster-connectivity-triage]].
- **Admission Webhook Denied:** PSP or Kyverno/OPA policies may block privileged containers or specific namespaces.

---

## 🔗 Related
- [[pb-cross-cluster-connectivity-triage]]
- [[pb-hie-nnuh-connectivity]]
- [[cmd-net-mtr-tcp]]
- [[cmd-net-nmap-check-filtered]]
- [[cmd-net-get-egress-ip]]
