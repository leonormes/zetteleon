---
aliases: []
confidence: 
created: 2025-02-07T12:57:53Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:42Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers]
title: key linux namespaces
type:
uid: 
updated: 
version:
---

Key Linux Namespaces

- User Namespace: This namespace isolates user and group IDs, allowing a container to have different user permissions than the host system. Each user namespace has its own set of capabilities. A process within a user namespace may have "root" privileges within that namespace but not on the host system. User namespaces are hierarchical, with parent namespaces able to see and access files created by child namespaces, whereas the root user can interact with all namespaces. They are often used in conjunction with other namespaces to enhance isolation.
- Mount Namespace: This namespace isolates mount points, providing each container with its own filesystem. This means a container's root directory is separate from the host's and other containers. It creates a chroot-like environment. By default, systemd shares mount points recursively with new namespaces. However, you can mount specific directories into a new namespace or remount /run to isolate the namespace.
- UTS Namespace: This namespace isolates hostname and Network Information Service (NIS) domain, allowing each container to have its own hostname. The UTS namespace is primarily useful in the context of containers. It's important to note that most communication is done via IP address and port number. This namespace is often used with the mount and user namespaces.
- Network Namespace: This namespace isolates network stacks, including network interfaces, IP addresses, port ranges, and routing tables. Each namespace gets its own loopback interface and virtual ethernet (veth) interfaces for connections between namespaces. A network namespace can have its own broadcast domain, further isolating network traffic. This namespace can be combined with Open vSwitch to isolate communication.
- PID Namespace: This namespace isolates process IDs, giving each container its own process tree. A container within a PID namespace can't see processes in other containers or the host. Each container can have its own PID 1. The PID namespace is useful for isolating processes, allowing for things like pausing a process on one host and resuming it on another, and for running multiple versions of an application with isolated process trees.
- IPC Namespace: This namespace isolates inter-process communication mechanisms, such as shared memory areas, message queues, and semaphores. The main application for IPC is databases.

How these Namespaces are Used Together

These namespaces are not used in isolation. They are used in combination to create secure and isolated container environments. For instance, user namespaces are often used with other namespaces to provide better isolation. Docker containers, for example, use a combination of pid, net, mnt, ipc, uts, and user namespaces.

Capabilities

It's also important to understand *capabilities*. While not a namespace, they work hand-in-hand with namespaces to determine what processes inside a namespace can do. Each namespace has its own set of capabilities, and a namespace cannot have more permissions than its creator.

Containerisation

Namespaces are central to container technology. They allow you to slice up a single OS so that it appears like multiple isolated OSes. They allow you to run multiple web servers on the same OS without port conflicts and run multiple apps without them conflicting over shared files. The combination of these namespaces create a powerful isolation layer.

Tools and Techniques

Several tools and techniques are used for creating and interacting with namespaces:

- `ip netns` command: Used for creating and managing network namespaces.
- `lsns` command: Used to list all available namespaces.
- `nsenter` command: Used to enter a specific namespace.
- `veth` (virtual Ethernet pairs) are used to connect different network namespaces.

eBPF and Tracing

The provided material also introduces BPF, or extended Berkeley Packet Filter. BPF allows you to attach programs to various hooks in the kernel. BPF can also be used to fetch stack traces. It's used in combination with kprobes, which are dynamic trace points that are triggered when a kernel function executes, to get information from the Linux kernel for observability.

Next Steps

To continue your learning, you could consider exploring the following topics:

- Cgroups: These are used in conjunction with namespaces to control the resources (CPU, memory, I/O) that a process can consume.
- CNI (Container Networking Interface): This is how Kubernetes configures container networking.
- Open vSwitch (OVS): This virtual switch can connect multiple namespaces together for more complex network topologies.
- Specific security features: Explore SELinux, AppArmor, and Seccomp which are other ways to enhance container security.

Would you like me to help you with any of these topics specifically? Perhaps you'd like to dive deeper into the user namespace or the network namespace, or even explore how to trace events within these namespaces using BPF tools? I can also create a quiz to test your comprehension of this material if you'd like!
