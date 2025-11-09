---
aliases: []
confidence: 
created: 2025-10-24T15:27:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [container, isolation, linux, namespace, pid, type/fact]
title: What is a PID namespace
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a mount namespace]], [[What is a network namespace]], [[What is a UTS namespace]]

## Summary

A PID namespace isolates process ID numbers, allowing each namespace to have its own independent set of PIDs starting from 1, enabling containers to have their own init process and preventing visibility of host or other container processes.

## Context / Problem

On a traditional Linux system, all processes share a single PID space:

- Only one process can have PID 1 (init/systemd)
- All processes can see each other via `/proc/<pid>`
- `kill` can signal any process (if permissions allow)
- Process tree is globally visible

Containers need isolation so:

- Each container has its own PID 1 (container init)
- Container processes cannot see host processes
- Security: unprivileged container cannot kill host processes
- Monitoring: container sees only its own processes

## Mechanism / Details

### What Is It

A PID namespace provides:

- **Isolated PID numbering**: PIDs are scoped to the namespace
- **Independent init process**: First process in namespace is PID 1
- **Nested hierarchy**: PID namespaces can be nested (parent sees child PIDs)
- **Process visibility**: Processes in one namespace cannot see other namespaces

### Creating a PID Namespace

```bash
# Create new PID namespace
unshare --fork --pid /bin/bash

# Check PID in new namespace
echo $$
# Output: 1 (PID 1 in this namespace)

# But from host:
ps aux | grep bash
# Shows actual PID: 12345
```

**Key Point**: A process has **two PIDs**:

1. PID in its own namespace (e.g., 1)
2. PID in parent namespace (e.g., 12345)

### PID Namespace Hierarchy

```sh
Host (PID namespace 0)
  ├─ PID 1: systemd
  ├─ PID 1000: containerd
  │
  └─ Container A (PID namespace 1, child of 0)
      ├─ PID 1: /bin/sh (appears as PID 2000 on host)
      ├─ PID 2: nginx (appears as PID 2001 on host)
      │
      └─ Container B (PID namespace 2, child of 1)
          ├─ PID 1: /bin/bash (appears as PID 3000 on host)
          └─ PID 2: python (appears as PID 3001 on host)
```

**Visibility Rules**:

- **Host** sees ALL PIDs (2000, 2001, 3000, 3001, etc.)
- **Container A** sees only its own PIDs (1, 2) + child Container B's PIDs
- **Container B** sees only its own PIDs (1, 2)
- **Children cannot see parent** PIDs

### /proc Filesystem and PID Namespaces

The `/proc` filesystem shows processes visible in the current PID namespace:

```bash
# On host
ls /proc/
# Shows: 1 2 3 ... 12345 ... (all PIDs)

# In container (PID namespace)
ls /proc/
# Shows: 1 2 3 ... (only container PIDs)
```

**Requirement**: `/proc` must be **mounted in the container's mount namespace** to see correct PIDs:

```bash
unshare --fork --pid --mount-proc /bin/bash
# --mount-proc remounts /proc for the new PID namespace
```

Without remounting `/proc`, container sees **host PIDs** (confusing!).

### PID 1 Responsibilities

PID 1 in any PID namespace has special responsibilities:

1. **Reap zombie processes**: Orphaned children are reparented to PID 1
2. **Signal handling**: Must handle SIGTERM, SIGCHLD
3. **Init shutdown**: Cleanly terminate all processes in namespace

**Example**: Docker containers use `tini` or `dumb-init` as PID 1 to handle these duties.

## Connections / Implications

### What This Enables

- **Process isolation**: Container cannot see or signal host processes
- **Security**: Prevents container from discovering host process structure
- **Clean shutdown**: PID 1 can cleanly terminate all container processes
- **Nested containers**: Containers can run their own containers (Docker-in-Docker)

### What Breaks If This Fails

- **No process isolation**: Container sees all host processes
- **PID conflicts**: Cannot run multiple containers with same application (PID 1 conflict)
- **Security breach**: Container can kill host processes or inspect `/proc/<host-pid>`
- **Zombie accumulation**: Without proper PID 1, zombies accumulate

### Scenario: PID Namespace Without Mount Namespace

From the original note, if you create **PID namespace WITHOUT mount namespace**:

- Processes have isolated PIDs
- But `/proc` is **not remounted**
- Container sees `/proc` from host namespace (shows host PIDs!)
- **Confusion**: `ps aux` shows host processes, but container cannot signal them

**Implication**: Always combine PID namespace with mount namespace to remount `/proc`.

### How It Maps to Kubernetes

**Kubernetes always uses PID namespaces for Pods:**

1. kubelet creates PID namespace for Pod
2. Pause container becomes PID 1 in Pod's PID namespace
3. Other containers join the PID namespace
4. All containers in Pod see each other's processes

**Example**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: multi-container
spec:
  containers:
  - name: app
    image: nginx
  - name: sidecar
    image: busybox
    command: ["/bin/sh", "-c", "sleep 3600"]
```

**Inside Pod**:

```bash
# From 'app' container:
ps aux
# PID 1: /pause (pause container)
# PID 7: nginx
# PID 15: /bin/sh (sidecar)

# Containers share PID namespace!
```

**Kubernetes PID Namespace Sharing**:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: share-pid
spec:
  shareProcessNamespace: true  # Default in Kubernetes
  containers:
  - name: app
    image: nginx
```

With `shareProcessNamespace: false`, each container gets its own PID namespace (rare).

### Real-World Inspection

```bash
# List PID namespaces
ls -l /proc/*/ns/pid

# Compare two processes' PID namespaces
readlink /proc/1000/ns/pid
readlink /proc/2000/ns/pid
# Same inode = same namespace

# View process tree in a namespace
nsenter --pid=/proc/2000/ns/pid ps aux

# Check which namespace current shell is in
readlink /proc/$$/ns/pid
```

### Process Lifecycle in PID Namespace

```bash
# Create PID namespace with proper /proc mount
unshare --fork --pid --mount-proc /bin/bash

# Inside namespace:
echo $$  # 1
ps aux   # Shows only processes in this namespace

# Start background process
sleep 1000 &
# PID: 2

# Exit PID 1 → all processes in namespace are killed
exit
```

**Critical**: Killing PID 1 terminates the entire namespace.

## Questions / To Explore

- [[How does Docker implement PID namespaces?]]
- [[What happens when PID 1 in a container dies?]]
- [[How do zombie processes get reaped in containers?]]
- [[What is the pause container in Kubernetes and why is it PID 1?]]
- [[DEBUG - Container sees host processes in ps output]]
- [[How does systemd handle PID namespaces in containerized environments?]]
- [[What is the difference between --pid=host and default PID namespace?]]
