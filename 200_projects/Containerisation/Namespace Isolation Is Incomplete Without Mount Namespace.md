---
aliases: []
confidence: 
created: 2025-10-24T15:30:00Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:26Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [container, isolation, linux, namespace, security, type/insight]
title: Namespace Isolation Is Incomplete Without Mount Namespace
type: Insight
uid: 
updated: 
version:
---

**Links:**

- Up: [[MOC - Container Networking Model]]
- Related: [[What is a mount namespace]], [[How namespaces interact without mount namespace]], [[What is a PID namespace]], [[What is a UTS namespace]]

## Summary

Creating network, PID, and UTS namespaces without a mount namespace provides **incomplete isolation**—processes remain vulnerable to file system attacks, can modify host files, and experience confusing behavior where system calls (hostname) and files (/etc/hostname) are decoupled.

## Context / Observation

From real-world scenarios and the original research:

**The Problem**: Developers sometimes assume that creating **any** namespace provides isolation. They create PID or network namespaces for testing but forget mount namespaces, leading to:

- Containers that can read `/etc/shadow`
- Hostname changes that don't match `/etc/hostname`
- `/proc` showing host PIDs instead of container PIDs
- Temporary files leaking between "isolated" processes

**The Insight**: **Mount namespace is the gatekeeper of file system isolation**. Without it, all other namespaces provide **partial, incomplete protection**.

## The Realization

### What Isolation Actually Means

When we say "isolated container," we mean:

| Resource | Namespace Required |
|----------|--------------------|
| Process IDs | PID namespace |
| Network interfaces | Network namespace |
| Hostname | UTS namespace |
| **Files and directories** | **Mount namespace** |
| IPC queues | IPC namespace |
| User/Group IDs | User namespace |

**Critical Point**: If you isolate processes (PID) but not files (mount), you have:

- ✓ Processes cannot see each other
- ✗ Processes can **read each other's files**
- ✗ Processes can **modify shared configuration**
- ✗ No actual security boundary

### The Decoupling Problem

Without mount namespace, **system calls and files diverge**:

```bash
# In UTS namespace without mount namespace:
hostname my-container
hostname
# Output: my-container (syscall uses UTS namespace)

cat /etc/hostname
# Output: host.example.com (file uses shared mount namespace)
```

**Consequence**: Application behavior becomes **unpredictable**:

- Logging uses `gethostname()` → logs show "my-container"
- Config reads `/etc/hostname` → uses "host.example.com"
- Confusion in distributed systems

### The Security Boundary Is at Mount Namespace

From the original note's security example:

**Attack Vector**: Setuid application with hostname-based file paths

```bash
# Attacker creates UTS namespace
unshare --uts /bin/bash
hostname "../../root/.ssh/authorized_keys"

# Runs setuid binary that does:
# FILE=/var/app/$(hostname)/config
# Expands to: /var/app/../../root/.ssh/authorized_keys/config
# Which resolves to: /root/.ssh/authorized_keys

# Attacker writes SSH key to root's authorized_keys!
```

**Root Cause**: No mount namespace means:

1. File system is **shared** with host
2. Setuid binary runs with **host's root privileges**
3. Path traversal affects **host file system**

**Mitigation**: With mount namespace:

- Container has isolated `/var`, `/root`, etc.
- Path traversal limited to container's file system
- Even setuid binaries cannot escape

## Practical Implications

### 1. Debug Containers Need Care

Scenario: "I just want to test network isolation"

```bash
# DANGEROUS:
sudo unshare --net /bin/bash
# Isolated network, but shared file system
# Can still read /etc/passwd, modify /etc/hosts
```

**Better**:

```bash
sudo unshare --net --mount --fork /bin/bash
mount --make-rprivate /
# Now properly isolated
```

### 2. The /proc Mount Problem

Without mount namespace, `/proc` shows **wrong PIDs**:

```bash
# Create PID namespace
unshare --pid --fork /bin/bash

echo $$  # 1 (correct: PID in namespace)
ls /proc/  # 1, 2, 3, ..., 12345, ... (WRONG: host PIDs!)
```

**Why**: `/proc` is mounted in **initial mount namespace**, showing **initial PID namespace**.

**Fix**: Remount `/proc` (requires mount namespace or CAP_SYS_ADMIN):

```bash
unshare --pid --mount --fork --mount-proc /bin/bash
ls /proc/  # 1, 2, 3 (correct: namespace PIDs)
```

### 3. Container Escape Via Shared Filesystem

**Real-world scenario**: Kubernetes node running container without mount namespace.

```bash
# Attacker inside container
cat /etc/shadow  # Reads host shadow file!
echo "attacker::0:0::/root:/bin/bash" >> /etc/passwd
# Adds root user to HOST

exit

# Back on host, attacker logs in:
su attacker
# Now root on HOST
```

**Lesson**: **Never run containers without mount namespace in production**.

## Architectural Patterns

### Pattern 1: Full Isolation (Production)

```bash
# Docker/Kubernetes approach
unshare --pid --net --uts --ipc --mount --user --fork \
  --mount-proc \
  --map-root-user \
  /bin/bash

# All namespaces created
# Complete isolation
```

### Pattern 2: Partial Isolation (Debugging Only)

```bash
# Network testing without file isolation
unshare --net /bin/bash

# Use case: Test network behavior while keeping logs on host
# WARNING: Not secure, debug only
```

### Pattern 3: Host Network (Performance)

```bash
# Kubernetes hostNetwork: true
# Only isolates mount and PID, shares network
docker run --network=host --pid=host myapp

# Use case: High-performance networking (monitoring agents)
# Still has mount isolation for security
```

## Key Takeaways

### For Developers

1. **Always create mount namespace for security**
   - Even if "just testing"
   - Prevents accidental host modification

2. **Remount /proc in PID namespaces**
   - Otherwise /proc shows confusing host PIDs
   - Use `--mount-proc` flag

3. **Check namespace isolation assumptions**
   - `hostname` vs `/etc/hostname` can differ
   - `/tmp` may be shared when you expect isolation

### For Security Engineers

1. **Audit namespace configuration**
   - Check which namespaces are created
   - Mount namespace is **non-negotiable** for security

2. **Test for file system isolation**

   ```bash
   # Inside container:
   touch /tmp/should-not-appear-on-host
   
   # On host:
   ls /tmp/should-not-appear-on-host
   # Should fail if properly isolated
   ```

3. **User namespace adds defense-in-depth**
   - Even with mount namespace, root in container = root on host
   - User namespace remaps UID 0 → UID 100000 on host
   - Limits damage from container escape

### For Kubernetes Operators

1. **Never disable mount namespace**
   - Kubernetes always creates mount namespace
   - Overriding this breaks security model

2. **Use SecurityContext for additional hardening**

   ```yaml
   securityContext:
     runAsNonRoot: true
     readOnlyRootFilesystem: true
     allowPrivilegeEscalation: false
   ```

3. **Monitor for privileged containers**
   - Privileged containers bypass namespace isolation
   - Should require approval and justification

## Quote from Original Research

> "It's important to emphasize that sharing the same file system view across different namespaces increases the attack surface and the potential for privilege escalation. While namespaces provide some isolation, they do not completely eliminate security risks."

**Translation**: Namespace isolation is **additive**—each namespace type adds a layer. **Missing mount namespace removes the most critical layer**.

## Checklist: Is My Container Isolated

- [ ] PID namespace created? (`readlink /proc/$$/ns/pid`)
- [ ] Network namespace created? (`ip addr` shows isolated interfaces)
- [ ] UTS namespace created? (`hostname` is container-specific)
- [ ] **Mount namespace created?** (`findmnt` shows isolated mounts) ← **Critical**
- [ ] `/proc` remounted? (`ls /proc/` shows only container PIDs)
- [ ] User namespace created? (`id` shows remapped UIDs) ← **Bonus security**

**If mount namespace is missing**: You have a **security vulnerability**, not a container.

## Questions / To Explore

- How does Docker ensure all namespaces are created?
- What is the performance cost of mount namespace creation?
- How do you audit running containers for namespace configuration?
- SECURITY - How to detect container escape via shared mount namespace?
- What are Kubernetes PodSecurityStandards for namespace enforcement?
- How does user namespace provide additional isolation beyond mount namespace?
