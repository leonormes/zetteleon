---
aliases: []
confidence: 
created: 2025-10-24T15:29:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:27Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [container, isolation, linux, namespace, security, type/mechanism]
title: How namespaces interact without mount namespace
type: Mechanism
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a mount namespace]], [[What is a PID namespace]], [[What is a UTS namespace]], [[What is a network namespace]], [[What is the Linux VFS (Virtual File System)]]

## Summary

When network, PID, and UTS namespaces are created without a separate mount namespace, processes in different namespaces share the same file system view (initial mount namespace), reducing isolation and creating security risks while simplifying certain debugging scenarios.

## Context / Problem

Full container isolation typically requires **all namespace types**:

- **Mount**: Isolate file system mounts
- **PID**: Isolate process IDs
- **Network**: Isolate network stack
- **UTS**: Isolate hostname
- **IPC**: Isolate inter-process communication
- **User**: Isolate user/group IDs

But what happens when you create **some namespaces without others**? Specifically, **what if you create PID, Network, and UTS namespaces but NO mount namespace?**

This scenario reveals how namespace isolation is **incomplete** and where security boundaries blur.

## Mechanism / Details

### Scenario Setup

```bash
# Create namespaces WITHOUT mount namespace
unshare --pid --net --uts --fork /bin/bash

# What we have:
# ✓ PID namespace: Isolated process IDs
# ✓ Network namespace: Isolated network interfaces
# ✓ UTS namespace: Isolated hostname
# ✗ Mount namespace: SHARED with host (initial mount namespace)

# Inside this "partial container":
hostname my-container
echo $$  # PID 1 (in PID namespace)
ip addr  # No interfaces except lo (network namespace)

# But file system:
ls /etc/passwd  # Host's /etc/passwd!
cat /proc/1/cmdline  # Cannot see (PID namespace isolation)
ls /proc/  # Shows namespace's PIDs only (if /proc remounted)
```

### What's Shared, What's Isolated

| Resource | Isolated? | Why |
|----------|-----------|-----|
| Process IDs | ✓ Yes | PID namespace |
| Network interfaces | ✓ Yes | Network namespace |
| Hostname | ✓ Yes | UTS namespace |
| **File system mounts** | ✗ No | No mount namespace |
| **Files content** | ✗ No | No mount namespace |
| **/etc directory** | ✗ No | Shared mount namespace |
| **/proc entries** | ⚠️ Partial | Depends on remount |

### File System Operations in This Scenario

#### Reading Files

```bash
# Inside partial container:
cat /etc/hosts
# Reads HOST's /etc/hosts

cat /etc/hostname
# Reads HOST's /etc/hostname
# (But hostname command shows namespace's hostname!)
```

**Explanation**:

- `hostname` command uses **sethostname/gethostname syscalls** (UTS namespace affects this)
- `/etc/hostname` is a **file** (mount namespace affects this)
- They are **decoupled** without mount namespace!

#### Writing Files

```bash
# Inside partial container (running as root):
echo "malicious-data" > /etc/hosts
# Modifies HOST's /etc/hosts!

echo "attacker-hostname" > /etc/hostname
# Modifies HOST's /etc/hostname!
# On next boot, host uses this hostname
```

**Security Risk**: Container can modify host files.

#### Creating Files

```bash
# Inside partial container:
touch /tmp/container-file

# Exit container, back on host:
ls /tmp/container-file
# File exists! (shared /tmp)
```

### Kernel Data Structures Interaction

#### Without Mount Namespace

```sh
┌─────────────────────────────────────────┐
│         Kernel Data Structures          │
├─────────────────────────────────────────┤
│ Process A (Host)                        │
│   task_struct                           │
│     ├─ nsproxy                          │
│     │   ├─ uts_ns: &init_uts_ns        │
│     │   ├─ pid_ns: &init_pid_ns        │
│     │   ├─ net_ns: &init_net_ns        │
│     │   └─ mnt_ns: &init_mnt_ns ◄──┐   │
│     │                                │   │
├─────────────────────────────────────┼───┤
│ Process B (Partial Container)        │   │
│   task_struct                        │   │
│     ├─ nsproxy                       │   │
│     │   ├─ uts_ns: &custom_uts      │   │
│     │   ├─ pid_ns: &custom_pid      │   │
│     │   ├─ net_ns: &custom_net      │   │
│     │   └─ mnt_ns: &init_mnt_ns ◄───┘   │
│     │            (SHARED!)                │
└─────────────────────────────────────────┘
```

**Key Insight**: Both processes point to **same `mnt_ns`** (initial mount namespace).

#### File Access Path

```sh
Process B opens /etc/passwd:
1. VFS receives open("/etc/passwd", ...)
2. Checks process's nsproxy->mnt_ns
3. Uses init_mnt_ns->vfsmount tree
4. Resolves path: / → /etc → /etc/passwd
5. Returns inode from HOST's file system
6. Process B reads HOST's /etc/passwd
```

**No isolation at VFS layer** because `vfsmount` tree is shared.

### The /proc Filesystem Problem

`/proc` shows processes **visible in current PID namespace**, but:

```bash
# Inside partial container (without remounting /proc):
ls /proc/
# Shows HOST PIDs! (1, 2, 3, ... 12345, ...)

# But:
ps aux
# Shows only namespace PIDs (1, 2, 3, ...)
```

**Why the discrepancy?**

- `/proc` is mounted in **initial mount namespace**
- Shows PIDs from **initial PID namespace**
- `ps` command filters by **current PID namespace**

**Solution**: Remount `/proc` (requires mount namespace or mount permission):

```bash
unshare --pid --fork --mount-proc /bin/bash
# Now /proc shows correct PIDs
```

### Security Implications

From the original note, this configuration creates **multiple security risks**:

#### 1. File System Access

- Container can read sensitive host files: `/etc/shadow`, `/root/.ssh/id_rsa`
- Container can modify host configuration: `/etc/passwd`, `/etc/hosts`
- Container can create files visible to host: `/tmp/malicious-script`

#### 2. Setuid Vulnerability

From original note:

> "A set-user-ID application could be vulnerable to attacks if an unprivileged user can run the application in a UTS namespace with a specially crafted hostname."

**Attack scenario**:

```bash
# Attacker creates UTS namespace with path traversal hostname
unshare --uts /bin/bash
hostname "../../root/.ssh/authorized_keys"

# Runs setuid application that writes to file based on hostname
/usr/bin/vulnerable-setuid-app
# May overwrite /root/.ssh/authorized_keys with attacker's key!
```

#### 3. Reduced Isolation

- Processes in different namespaces can **interfere** via shared files
- Logs written to `/var/log` are intermingled
- Temporary files in `/tmp` may conflict

## Connections / Implications

### What This Configuration Enables

**Advantages** (limited use cases):

- **Simplified debugging**: Can inspect container files directly from host
- **Reduced overhead**: No mount namespace management
- **Legacy compatibility**: Some old apps incompatible with mount namespaces
- **Resource sharing**: Containers can cooperate via shared `/tmp`

**Example use case**: Testing network isolation while keeping file access:

```bash
# Test app's network behavior in isolated network namespace
# But keep logs accessible on host /var/log
unshare --net --fork myapp
```

### What Breaks or Creates Risks

**Hostname conflicts** (from original note):

- UTS namespace isolates `hostname` command
- But `/etc/hostname` file is shared
- Container writes to `/etc/hostname` affect host on reboot

**Process visibility** (from original note):

- PID namespace hides other namespaces' processes
- But `/proc/<host-pid>` directories still exist (if not remounted)
- Attacker can infer host process structure by enumeration

**Privilege escalation**:

- Container running as root has root privileges on **host file system**
- No user namespace to remap UIDs
- Can overwrite `/etc/sudoers`, `/etc/passwd`, etc.

### How It Maps to Kubernetes

**Kubernetes NEVER uses this configuration**:

- Always creates **mount namespace** for Pods
- Always creates **all namespace types** for full isolation
- Exception: `hostNetwork: true`, `hostPID: true` explicitly shares namespaces

**Why full isolation is critical**:

- Multi-tenant clusters: one Pod cannot access another's files
- Security: unprivileged Pods cannot modify host files
- Stability: Pod crashes don't corrupt host file system

### Real-World Example: Docker Without Mount Namespace

**NOT POSSIBLE in standard Docker**:

```bash
# Docker always creates mount namespace
docker run --rm -it ubuntu /bin/bash
# Full isolation including file system
```

**Manual simulation**:

```bash
# Create partial container manually
sudo unshare --pid --net --uts --fork /bin/bash

# Inside:
hostname my-container
ls /etc/  # Host's /etc/
echo "danger" > /etc/danger  # Affects host!
```

### Comparison Table

| Configuration | PID | Net | UTS | Mount | Isolation Level | Use Case |
|---------------|-----|-----|-----|-------|-----------------|----------|
| **Full container** | ✓ | ✓ | ✓ | ✓ | High | Production |
| **Partial (this scenario)** | ✓ | ✓ | ✓ | ✗ | Low | Debugging, legacy |
| **Host networking** | ✓ | ✗ | ✓ | ✓ | Medium | Network performance |
| **Privileged** | ✗ | ✗ | ✗ | ✗ | None | Host access |

## Questions / To Explore

### Factual Gaps

- What is the IPC namespace and what does it isolate?
- What is the user namespace and how does it remap UIDs?
- What are all Linux namespace types?

### Mechanism Gaps

- How does Docker create a full set of namespaces for containers?
- How does Kubernetes handle hostNetwork and hostPID Pods?
- How do you remount /proc in a new PID namespace?
- How does pivot_root isolate the root filesystem in containers?

### Security Scenarios

- SECURITY - Container escape via shared mount namespace
- SECURITY - Setuid vulnerability with crafted UTS hostname
- DEBUG - Container can modify host files unexpectedly

### Architectural Questions

- Why does Kubernetes always use mount namespaces?
- What is the overhead of creating mount namespaces?
- How do shared subtrees propagate mounts between namespaces?
