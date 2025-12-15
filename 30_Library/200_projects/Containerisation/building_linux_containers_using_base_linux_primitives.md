---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:47Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers]
title: building_linux_containers_using_base_linux_primitives
type: instruction
uid: 
updated: 
version: 1
---

## Introduction to Containers

- Containers are isolated systems that share the host kernel without virtualizing hardware or firmware.
- They are user-space constructs, combining Linux kernel features like namespaces and [cgroups](Cgroups.md) for process isolation and resource control.

## Key Linux Primitives for Containers

1. Filesystem Isolation:

    - Uses `chroot` (insecure) or `pivot_root` (preferred) to create isolated root filesystems.
    - Pivot_root securely reassigns the filesystem root, often paired with mount namespaces.
2. Namespaces:

    - Provide isolation for kernel resources:
        - Mount: Separate mount tables for processes.
        - PID: Separate process ID hierarchy.
        - Network: Private network interfaces and routing tables.
        - UTS: Isolate hostname and domain name.
        - User: Map user IDs, ensuring containers see themselves as root without true privileges.
        - Cgroup and Time: Isolate resource control and system time.
    - Sequence and order of namespace creation matter for security and functionality.
3. Cgroups (Control Groups):

    - Limit and prioritize resource usage (CPU, memory, I/O) by processes.
    - Two versions:
        - v1: Separate hierarchies for each resource type.
        - v2: Unified hierarchy simplifying configuration.
    - Used to prevent denial-of-service attacks via resource exhaustion.
4. Security Mechanisms:

    - Seccomp (Secure Computing Mode): Filters system calls to prevent malicious or unsafe operations.
    - Capabilities: Fine-grained privilege management to replace traditional root privileges.
    - Linux Security Modules (LSMs):
        - Examples: AppArmor, SELinux.
        - Enforce mandatory access controls for additional security layers.

## Key Warnings and Best Practices

- Avoid Privileged Containers: Privileged containers are a security risk as they can directly affect the host kernel.
- Complexity of DIY Container Runtimes:
    - Writing a container runtime is challenging due to nuances in namespace ordering, syscall filtering, and compatibility across kernel versions.
- Use Established Tools: Leverage existing libraries and runtimes (e.g., LXC, Docker) to avoid reinventing the wheel and introducing vulnerabilities.

## Demonstrations

- Practical examples of isolating processes using namespaces, limiting resources with cgroups, and enforcing security policies using AppArmor and seccomp.

Would you like a deeper exploration of any particular section, or should I summarize further?

Here’s an overview of the other Linux primitives critical for containers, summarized and elaborated for clarity:

---

## 1. Seccomp (Secure Computing Mode)

- Purpose: Restricts system calls (syscalls) available to containerized processes.
- Mechanism:
    - A syscall allowlist or denylist is defined.
    - Denied syscalls can return predefined error codes (e.g., `EPERM` or `ENOSYS`) to signal a failure gracefully.
- Advanced Features:
    - Uses Classic BPF (cBPF) for syscall filtering.
    - Can filter based on syscall arguments (limited to register-based arguments, not pointers).
    - Recent extensions allow syscall emulation or outsourcing decisions to a monitoring user-space process.
- Use Case: Seccomp is essential for container security, especially in untrusted or privileged environments, to block syscalls that could allow privilege escalation or system compromise.

---

## 2. Capabilities

- Purpose: Break down the all-powerful `root` privilege into discrete capabilities.
- How It Works:
    - Capabilities like `CAP_NET_ADMIN` or `CAP_SYS_ADMIN` are assigned to processes.
    - These capabilities control specific privileged operations (e.g., network setup, filesystem mounting).
- Integration with User Namespaces:
    - Capabilities are scoped to the namespace that owns them.
    - A process in a user namespace might have `CAP_SYS_ADMIN`, but this applies only to resources in that namespace.
- File Capabilities:
    - Allow specific binaries to carry limited privileges.
    - Example: The `ping` command is granted raw socket access (`CAP_NET_RAW`) without requiring full root privileges.
- Use Case: Capabilities prevent containers from needing full root access, limiting the impact of potential exploits.

---

## 3. Linux Security Modules (LSMs)

- Purpose: Provide mandatory access control (MAC) for containers.
- Popular LSMs:
    - AppArmor: Applies profiles to processes, restricting file access and syscalls.
    - SELinux: Enforces detailed access policies based on labels for files, processes, and network resources.
- Container Integration:
    - Containers often inherit the host’s LSM policies, with profiles customized for isolation.
    - Nested containers face challenges due to non-stacking LSM limitations.
    - Work is ongoing to support stacking (e.g., AppArmor on the host, SELinux inside a container).
- Use Case: Adds another security layer, particularly critical for privileged containers or systems with stringent isolation needs.

---

## 4. Cgroups (Control Groups)

- Purpose: Control and limit the resource usage of containerized processes.
- Types of Resources Controlled:
    - CPU: Limit CPU time or allocate specific cores.
    - Memory: Cap memory usage to prevent exhaustion.
    - I/O: Control block device access rates.
    - PIDs: Limit the number of processes within a container.
- Versions:
    - v1: Separate hierarchies for different resources, requiring more management complexity.
    - v2: Unified hierarchy, simplifying resource management and addressing fairness issues between parent and child processes.
- Use Case: Ensures fair resource allocation across containers and prevents denial-of-service attacks caused by resource exhaustion.

---

## 5. Mount and Filesystem Isolation

- Purpose: Isolate the filesystem view of processes.
- Mechanisms:
    - Chroot: Insecure and easy to break out of; not recommended.
    - Pivot_root: Replaces the filesystem root securely, often used with a mount namespace to isolate processes completely.
- Practical Use: Ensures a containerized process sees only its designated filesystem, preventing accidental or malicious access to the host’s filesystem.

---

## 6. PID Namespace

- Purpose: Provide process ID (PID) isolation.
- How It Works:
    - Each container has its own PID 1, independent of the host or other containers.
    - Prevents visibility and interference with processes outside the namespace.
- Use Case: Critical for creating isolated process hierarchies in containers.

---

## 7. UTS Namespace

- Purpose: Isolate system identifiers like hostname and NIS domain name.
- Use Case: Allows each container to have its own hostname, ensuring unique identification and avoiding conflicts with the host.

---

## 8. IPC Namespace

- Purpose: Isolate interprocess communication (IPC) resources, such as shared memory and message queues.
- Use Case: Prevents containers from accessing or interfering with IPC mechanisms used by processes outside the namespace.

---

## 9. Network Namespace

- Purpose: Provide isolated network stacks for containers.
- Features:
    - Private interfaces, routing tables, and firewall rules.
    - Containers can have independent IP addresses and network configurations.
- Use Case: Essential for running network-isolated applications or managing traffic independently for each container.

---

## 10. Time Namespace

- Purpose: Isolate system time within a container.
- Features:
    - Allows setting time offsets relative to the host.
    - Useful for migrating containers between hosts without time inconsistencies.
- Use Case: Particularly relevant for high-availability and distributed systems where time synchronization is critical.

---

These primitives collectively allow fine-grained control over containerized processes, ensuring strong isolation, efficient resource use, and robust security. If you need more detail on any specific primitive, let me know!
