---
created: 2026-02-19T13:14:28+00:00
incident_type: diagnostic_deployment
modified: 2026-07-13T08:45:30+00:00
permalink: llmeon/30-library/ops/pb-netshoot-deployment
tags: [docker, k8s, netshoot, network, playbook]
target_service: network
title: pb-netshoot-deployment
---

## Playbook: Deploying Netshoot Diagnostic Environment

### 🧭 Trigger Condition

- Need to troubleshoot network connectivity, performance, or DNS within a containerized environment (Docker or Kubernetes).
- Existing containers lack diagnostic tools (curl, tcpdump, mtr, etc.).

---

### 🌍 Execution Context

- Docker: Local engine or remote host.
- Kubernetes: Target cluster via `kubectl`.

---

### 🧱 Execution Flow

#### Option 1: Docker (Single Container)

_Troubleshoot a standalone container or the host._

1. Attach to a container's network namespace:

   ```bash
   docker run -it --rm --net container:<container_name> nicolaka/netshoot
   ```

2. Run on the host's network namespace:

   ```bash
   docker run -it --rm --net host nicolaka/netshoot
   ```

---

#### Option 2: Docker Compose

_Inject netshoot into a multi-container stack._

1. Add to `docker-compose.yml`:

   ```yaml
   services:
     debug-network:
       image: nicolaka/netshoot
       network_mode: "service:<target_service_name>"
       command: ["tail", "-f", "/dev/null"]
   ```

---

#### Option 3: Kubernetes (Standard)

_See detailed commands in [[cmd-k8s-run-netshoot]]._

1. Throwaway Pod: `kubectl run tmp-shell --rm -i --tty --image nicolaka/netshoot`
2. Ephemeral Container: `kubectl debug <pod_name> -it --image=nicolaka/netshoot`

---

#### Option 4: Kubernetes (Sidecar)

_Deploy netshoot alongside your application for persistent debugging._

1. Add container to your Deployment manifest:

   ```yaml
   spec:
     containers:
     - name: my-app
       image: my-app:latest
     - name: netshoot
       image: nicolaka/netshoot
       command: ["/bin/bash"]
       args: ["-c", "while true; do sleep 60; done"]
   ```

2. Execute into the sidecar:

   ```bash
   kubectl exec -it <pod_name> -c netshoot -- bash
   ```

---

### 🛠️ Common Diagnostic Commands (Inside Netshoot)

| Goal | Command |
| --- | --- |
| Performance | `iperf3 -s` (Server) / `iperf3 -c $TARGET_IP` (Client) |
| Packet Trace | `tcpdump -i any port <port> -Xvv` |
| Port Scan | `nmap -p <ports> $TARGET_IP` |
| DNS Info | `drill -V 5 <hostname>` |
| Bandwidth | `iftop -i eth0` |
| Socket Info | `ss -tulpn` |

---

### 🧠 End State

Success =

- Diagnostic environment established.
- Required tools accessible within the target network namespace.

---

### 🔗 Related

- [[cmd-k8s-run-netshoot]]
- [[sot-network-tools-patterns]]
- [[cmd-net-mtr-tcp]]
- [[cmd-net-nmap-check-filtered]]
