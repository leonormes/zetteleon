---
aliases: []
confidence: 
created: 2025-10-24T15:26:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [container, isolation, linux, mount, namespace, type/fact]
title: What is a mount namespace
type: Factual
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a network namespace]], [[What is the Linux VFS (Virtual File System)]], [[What is a PID namespace]], [[What is a UTS namespace]]

## Summary

A mount namespace isolates the list of mount points visible to processes, allowing each namespace to have its own independent view of the file system hierarchy without affecting other namespaces—critical for container file system isolation.

## Context / Problem

Containers need isolated file systems so that:

- One container cannot read another container's `/etc/passwd`
- Mounting a filesystem in one container doesn't affect others
- Each container can have its own `/tmp`, `/proc`, `/sys`
- Security: unprivileged container cannot modify host files

Without mount namespaces, all processes share the same mount points, breaking isolation.

## Mechanism / Details

### What Is It

A mount namespace provides:

- **Isolated mount point list**: Each namespace sees different mounted file systems
- **Independent mount operations**: `mount`/`umount` only affects the current namespace
- **Inherited on creation**: New mount namespace starts as copy of parent
- **Copy-on-write semantics**: Changes after creation are isolated

### Creating a Mount Namespace

```bash
# Create new mount namespace (requires unshare or clone)
unshare --mount /bin/bash

# Now in new mount namespace
mount -t tmpfs tmpfs /tmp

# This mount is ONLY visible in this namespace
# Parent namespace still sees original /tmp
```

### Mount Namespace Inheritance

```sh
Parent Process (PID 1000)
  ├─ Mount Namespace A
  │   ├─ / (rootfs)
  │   ├─ /proc
  │   ├─ /sys
  │   └─ /home
  │
  ├─ Child Process (PID 2000, same namespace)
  │   └─ Sees same mounts as parent
  │
  └─ Child Process (PID 3000, NEW namespace)
      └─ Mount Namespace B (copy of A at creation)
          ├─ / (rootfs)
          ├─ /proc
          ├─ /sys
          └─ /home
          └─ /mnt/data (new mount, isolated)
```

**Key Point**: Child's namespace is a **copy** at creation time, then diverges.

### Mount Propagation Types

Mounts can be configured to propagate changes between namespaces:

| Type | Description | Use Case |
|------|-------------|----------|
| **private** | No propagation (default) | Full isolation |
| **shared** | Propagate both ways | Coordinated mounts |
| **slave** | Receive propagation, don't send | Read-only coordination |
| **unbindable** | Cannot be bind-mounted | Security restriction |

**Example**:

```bash
# Make /mnt shared (propagates to child namespaces)
mount --make-shared /mnt

# Create child namespace
unshare --mount --propagation unchanged /bin/bash

# Mount in parent propagates to child
# (if child was created with shared propagation)
```

### Relationship to VFS

Mount namespaces use the VFS `vfsmount` structure:

- Each namespace has its own `vfsmount` tree
- Kernel uses `nsproxy->mnt_ns` to track process's mount namespace
- File operations use the process's `vfsmount` to resolve paths

```sh
Process A (mount namespace 1)
  └─ vfsmount tree:
      / → /dev/sda1
      /home → /dev/sdb1
      /tmp → tmpfs

Process B (mount namespace 2)
  └─ vfsmount tree:
      / → /dev/sda1
      /home → /dev/sdb1
      /tmp → /dev/sdc1  (different!)
```

## Connections / Implications

### What This Enables

- **Container file system isolation**: Each container has its own `/etc`, `/var`, `/tmp`
- **Volume mounting**: Kubernetes mounts volumes into Pod's mount namespace
- **Security**: Container cannot see or modify host file systems
- **Layered file systems**: OverlayFS combines multiple layers in isolated namespace

### What Breaks If This Fails

- **No file system isolation**: Containers share all mount points
- **Security breach**: Container can mount host file systems and read sensitive data
- **Resource conflicts**: Multiple containers compete for same `/tmp` space
- **Container startup fails**: Cannot create isolated `/proc` or `/sys`

### Scenario: No Mount Namespace (From Original Note)

If you create **network, PID, and UTS namespaces WITHOUT mount namespace**:

- Processes in different namespaces **share file system view**
- All operate in the **initial (root) mount namespace**
- Changes by one process visible to all processes
- **Reduced isolation**: Security risk increases
- **Hostname conflicts**: UTS namespace hostname resolved via shared `/etc/hostname`

**Implications**:

- Less overhead (no mount namespace management)
- Useful for debugging (easier to inspect files)
- **Not recommended for production containers**

### How It Maps to Kubernetes

**Kubernetes always uses mount namespaces for Pods:**

1. kubelet creates mount namespace for Pod
2. Mounts volumes into Pod's namespace:
   - EmptyDir → tmpfs mounted at `/path`
   - HostPath → bind mount from host
   - PVC → mount from storage backend
3. Container sees only its namespace's mounts

**Example Pod:**

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: example
spec:
  volumes:
  - name: data
    emptyDir: {}
  containers:
  - name: app
    volumeMounts:
    - name: data
      mountPath: /mnt/data
```

**Behind the scenes:**

```bash
# kubelet (simplified):
unshare --mount /bin/bash  # Create mount namespace
mount -t tmpfs tmpfs /var/lib/kubelet/pods/<pod-id>/volumes/kubernetes.io~empty-dir/data
bind-mount <that-path> /mnt/data  # Inside container's mount namespace
```

### Real-World Inspection

```bash
# List mount namespaces
ls -l /proc/*/ns/mnt

# Compare two processes' mount namespaces
ls -l /proc/1000/ns/mnt
ls -l /proc/2000/ns/mnt
# Same inode = same namespace

# View mounts in a namespace
nsenter --mount=/proc/2000/ns/mnt mount | grep tmpfs

# Check which namespace a process is in
readlink /proc/$$/ns/mnt
```

## Questions / To Explore

- [[How does Docker create mount namespaces for containers?]]
- [[What is the difference between bind mount and mount --rbind?]]
- [[How does OverlayFS work with mount namespaces?]]
- [[How does Kubernetes implement EmptyDir volumes?]]
- [[DEBUG - Container can see host file systems (mount namespace not isolated)]]
- [[What are shared subtrees and how do they work?]]
- [[How does pivot_root differ from chroot in containers?]]
