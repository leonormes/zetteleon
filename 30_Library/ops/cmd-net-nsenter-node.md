---
type: atomic_command
tool: nsenter
hop_level: local
target_service: host
requires_tunnel: false
tags: #atomic #network #namespaces #linux
---

# Enter Network Namespace (nsenter)

## 🎯 Intent
Directly enter the network namespace of a target container or the host to perform troubleshooting with local tools without installing them in the target environment.

---

## 🌍 Execution Context
Run from:
- [x] Host OS (as root/sudo).
- [x] Privileged netshoot container.

---

## ⚡ Action

### 1. From Host: Enter a Container's Namespace
```bash
# Find the PID of the container
PID=$(docker inspect --format '{{ .State.Pid }}' <container_id_or_name>)

# Enter the namespace
sudo nsenter -t $PID -n <command>
```

### 2. From Privileged Netshoot: Enter Host Namespace
```bash
# Requires: docker run --privileged --pid=host nicolaka/netshoot
nsenter -t 1 -m -u -n -i bash
```

### 3. From Privileged Netshoot: Enter Other Docker Network Namespace
*Requires mounting `/var/run/docker/netns`*
```bash
# Requires: docker run -it --rm -v /var/run/docker/netns:/var/run/docker/netns --privileged=true nicolaka/netshoot
nsenter --net=/var/run/docker/netns/<namespace_id> sh
```

### Placeholders
- `<container_id_or_name>` — Target container.
- `<command>` — Command to run (e.g., `ip addr`, `tcpdump`).
- `<namespace_id>` — The ID found in `/var/run/docker/netns/`.

---

## ✅ Verification
Expected signal:
- Running `ip addr` or `hostname` shows the details of the target namespace, not the source.

---

## 🔗 Related
- [[pb-netshoot-deployment]]
- [[cmd-k8s-run-netshoot]]
