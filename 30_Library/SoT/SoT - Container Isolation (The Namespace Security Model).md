---
aliases: ["Container Isolation Architecture", "Namespace Security Model", "The Mount Namespace Gatekeeper"]
confidence: "5/5"
created: 2025-12-19T00:00:00Z
epistemic: "authoritative"
last_reviewed: "2025-12-19"
modified: 2025-12-30T14:11:35+00:00
purpose: "To define the definitive security model for container isolation, explicitly stating that mount namespaces are the primary gatekeeper for security."
review_interval: "1 year"
see_also: ["[[MOC - Linux Container Primitives]]", "[[SoT - Namespacing in Computing]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "container", "linux", "namespace", "security"]
title: SoT - Container Isolation (The Namespace Security Model)
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> True container isolation is an **additive property** requiring the coordinated application of all six Linux namespaces. However, the **Mount Namespace** acts as the *primary gatekeeper* of security. Without it, a container is merely a process with a confused identity, retaining full read/write access to the host filesystem.

- **The Myth:** "Namespaces provide isolation." (False. *Which* namespaces?)
- **The Reality:** Isolation is a spectrum. Missing the mount namespace breaks the security boundary entirely.

## 2. The Isolation Spectrum

| Namespace | Resource Isolated | Security Impact (If Missing) |
|:--- |:--- |:--- |
| **PID** | Process IDs | Low. Process visibility only. |
| **Network** | Interfaces, Ports | Medium. Can sniff/spoof host traffic. |
| **UTS** | Hostname | Low. Confusion in logs. |
| **IPC** | Message Queues | Low. Inter-process communication leaks. |
| **User** | UID/GID | High. Root in container = Root on host. |
| **Mount** | **Filesystem** | **CRITICAL. Zero isolation.** |

### The "Incomplete Isolation" Failure Mode

Creating Network, PID, and UTS namespaces without a Mount namespace creates a dangerous state of **"Decoupled Identity."**

- **System Calls diverge from Files:**
  - `hostname` syscall returns "container-name" (UTS isolated).
  - `/etc/hostname` file returns "host-name" (Mount shared).
- **Security Collapse:**
  - Apps read `/etc/shadow` from the host.
  - Attackers use setuid binaries on the host to escalate privileges.
  - `/proc` exposes host PIDs, breaking the illusion of the PID namespace.

### The "Incomplete Isolation" Failure Mode: Decoupled Identity

Creating Network, PID, and UTS namespaces without a **Mount Namespace** creates a dangerous state of **Decoupled Identity**:

- **Syscall/File Mismatch:**
  - The `hostname` syscall returns the isolated name (UTS isolated).
  - The `/etc/hostname` file returns the host's name (Mount shared).
- **VFS Leakage:** The kernel uses shared inode and dentry caches. Untrusted processes can access sensitive host files (e.g., `/etc/shadow`) because there is no filesystem-level jail.
- **Root Exposure:** Even with user namespaces, the shared root filesystem allows a process to interfere with global system state if permissions are misconfigured.

## 3. The Security Boundary Architecture

The security boundary is defined by the **Mount Namespace** in conjunction with **Pivot Root**.

### The Mechanism

1. **Clone:** Create process with `CLONE_NEWNS` (Mount Namespace).
2. **Mount:** Set up isolated tmpfs, procfs, sysfs.
3. **Pivot Root:** Switch the root filesystem (`/`) to the container image.
4. **Unmount:** Detach the old root (host filesystem) so it is unreachable.

**Without this sequence, there is no container. There is only a process with a mask.**

## 4. Operational Protocols

### A. The "Never Just Unshare" Rule

Developers often use `unshare --net` for quick debugging. This is dangerous.

- **Rule:** Always use `unshare --mount --net --pid --fork --mount-proc` for any testing that involves untrusted code or network traffic.

### B. The "/proc" Remount Requirement

A common bug is creating a PID namespace but seeing host PIDs in `ps`.

- **Cause:** `/proc` is a filesystem. It reflects the PID namespace *at the time of mount*.
- **Fix:** You must mount a *new* instance of procfs *inside* the new mount namespace.

### C. The User Namespace Defense

Even with a Mount namespace, a container process running as `root` (UID 0) is dangerous if it escapes.

- **Defense:** **User Namespaces** map `UID 0` inside the container to `UID 10000+` on the host. Even if they break out of the chroot/mount jail, they are nobody on the host.

## 5. Minimum Viable Isolation (MVI) Criteria

A process qualifies as a "Container" only if:

1. It has a unique **Mount Namespace**.
2. It has a unique **PID Namespace**.
3. `/proc` is mounted specifically for that PID namespace.
4. The root filesystem is pivoted/chrooted away from the host root.

## 6. Sources and Links

- Synthesized from [[Namespace Isolation Is Incomplete Without Mount Namespace]].
- Related: [[What is a mount namespace]], [[What is a PID namespace]].
