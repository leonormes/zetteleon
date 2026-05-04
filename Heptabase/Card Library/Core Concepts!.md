1. Core Concepts:

   - Linux Namespaces: Understand the different types of namespaces (PID, network, mount, UTS, IPC, user) and how they provide isolation. Learn how to use tools like `ip netns` to create and manage them.

      - *Practical Learning*: Create your own namespaces, and explore their differences. See how they isolate processes and networking. Start with the "Connect Two Network Namespaces" project from the `k8s network learning project.md` and use a structured learning session as described in the same document

   - Control Groups (cgroups): Learn how cgroups limit resource usage (CPU, memory, I/O). Understand their role in managing resource allocation for containers.

      - *Practical Learning*: Implement cgroups to set resource limits on processes you create inside the isolated namespaces that you made in the previous step.

   - Virtual Ethernet (veth) Pairs: Learn how they connect namespaces. Understand how to use `ip link` to create and connect them.

      - *Practical Learning*: Create `veth` pairs, assign one end to one namespace and the other end to another, and then configure them to enable communication.