---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:42Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, namespace, question]
title: linux_namespaces_and_file_system_representation
type:
uid: 
updated: 
version:
---

## Linux Namespaces and File System Representation

I'm exploring Linux namespaces, specifically how the kernel manages the representation of the file system hierarchy when some namespaces are created but a mount namespace is not created.

Scenario:

I've used Linux primitives (e.g., `unshare`, `clone`) to create new:

   Network namespaces

   PID namespaces

   [UTS namespaces](UTS%20namespaces.md)

However, I have not created a new mount namespace. I'm operating within the initial mount namespace.

Question:

In this scenario, how does the kernel track and represent the hierarchical structure of "files" (including regular files, directories, devices, and other file system objects) as they relate to the created network, PID, and [UTS namespaces](UTS%20namespaces.md)? Specifically:

   How does the kernel associate these "files" with the respective namespaces, given that a separate mount namespace isn't present?

   Does the kernel use the initial mount namespace's hierarchy as the basis for all other namespaces in this scenario? If so, how are the different namespace views (network, PID, UTS) reflected within that shared mount namespace structure?

   What are the implications of not having a separate mount namespace for these other namespaces in terms of file system visibility and access?

Motivation:

I'm trying to better understand the underlying mechanisms of containerization and how different namespaces interact, especially when a full container environment with its own mount namespace isn't established. I'm interested in how processes in different namespaces perceive the file system in this limited-namespace scenario.

Expected Output:

A detailed explanation of the kernel's mechanisms, ideally with references to relevant kernel documentation or source code if possible. I'm particularly interested in the data structures and processes involved in managing the file system representation in this context.

## Answer

In the scenario you've described, where network, PID, and [[UTS namespaces]] are created without a corresponding mount namespace, the kernel's management of the file system hierarchy is both interesting and complex. Let's dive into how this works:

### Kernel's File System Representation

When you create new namespaces for network, PID, and UTS without creating a mount namespace, the kernel continues to use the global mount namespace for tracking all files and the overall file system hierarchy[1]. This means that all processes, regardless of their other namespace memberships, share the same view of the file system structure.

#### Shared Mount Namespace

1. Global Mount Structure: The kernel maintains a single, shared data structure for all mounted filesystems, which is visible to all processes across all namespaces[1].
2. No Filesystem Isolation: Without a separate mount namespace, there's no isolation of the filesystem hierarchy. All processes, regardless of their network, PID, or UTS namespace, see the same files and directories[2].
3. Shared /proc and /sys: Processes in different namespaces will share the same `/proc` and `/sys` filesystems, which can lead to information leakage between namespaces[2].

### Namespace-Specific File Representations

While the overall file system hierarchy is shared, the kernel does maintain some namespace-specific file representations:

4. Network Namespace:
   - Network-related files in `/proc`, such as `/proc/net`, are namespace-aware. The kernel presents different content based on the network namespace of the accessing process[6].
   - Example: `/proc/net/tcp` will show different entries for processes in different network namespaces.

5. PID Namespace:
   - The kernel maintains separate process ID mappings for each PID namespace.
   - In `/proc`, process-specific directories (e.g., `/proc/[pid]`) are visible based on the PID namespace of the viewing process[6].
   - Processes in a child PID namespace cannot see processes in the parent namespace through `/proc`.

6. UTS Namespace:
   - Files like `/proc/sys/kernel/hostname` and `/proc/sys/kernel/domainname` reflect the UTS namespace of the accessing process[6].

### Implications and Limitations

7. Limited Isolation: Without a mount namespace, processes can potentially access files they shouldn't, as there's no filesystem-level isolation[2].
8. Shared Root Filesystem: All processes, regardless of their namespace membership, share the same root filesystem and can potentially interfere with each other's files[1].
9. No Custom Mount Points: You cannot create namespace-specific mount points or hide certain directories from specific namespaces without a mount namespace[2].
10. Security Considerations: This setup can lead to potential security risks if untrusted processes are running in these namespaces, as they have access to the global filesystem[2].

### Kernel Mechanisms

11. Inode and Dentry Caches: The kernel uses shared inode and dentry caches across all namespaces when a separate mount namespace isn't created[2].
12. Namespace-Aware Syscalls: Some syscalls (like those related to networking or process management) are namespace-aware and provide different views based on the calling process's namespace membership[6].
13. VFS Layer: The Virtual File System (VFS) layer in the kernel abstracts the underlying filesystems and provides a unified interface, which is shared across all namespaces in this scenario[2].

### Conclusion

In the absence of a mount namespace, the kernel primarily relies on the global mount namespace for file system representation. While this provides a unified view of the filesystem, it limits the isolation between different namespaces. The kernel does provide some namespace-specific views for certain files (especially in `/proc` and `/sys`), but the overall filesystem structure remains shared. This setup is not typically used in full containerization scenarios, where filesystem isolation is usually desired for security and resource management purposes.

For full containerization and proper isolation, creating a separate mount namespace along with other namespaces is generally recommended. This allows for a truly isolated filesystem view, enhancing security and preventing unintended interactions between processes in different namespaces.

Citations:

[1] <https://blog.quarkslab.com/digging-into-linux-namespaces-part-2.html>

[2] <https://aeb.win.tue.nl/linux/lk/lk-8.html>

[3] <https://unix.stackexchange.com/questions/527534/what-sort-of-file-thing-do-namespace-files-point-to>

[4] <https://stackoverflow.com/questions/48776389/unshare-isolate-mount-namespace>

[5] <https://lwn.net/Articles/697278/>

[6] <https://en.wikipedia.org/wiki/Linux_namespaces>

[7] <https://docs.kernel.org/filesystems/overlayfs.html>

[8] <https://blog.quarkslab.com/digging-into-linux-namespaces-part-1.html>

---

Answer from Perplexity: pplx.ai/share

#### Linux Namespaces and File System Representation Without a Mount Namespace

When you create new network, PID, and UTS namespaces without creating a mount namespace, the kernel still operates within the initial (shared) mount namespace. This means that processes within your new namespaces still perceive and interact with the file system as defined by the original mount namespace. However, their views of certain files and directories (especially under `/proc` and `/sys`) may be altered based on namespace-specific information.

---

### 1. Kernel's File System Representation and Namespace Association

The kernel tracks and represents the hierarchical file system structure using VFS (Virtual File System), where each namespace-related object (network, PID, UTS, etc.) does not directly change the file system view unless a new mount namespace is created.

#### How The Kernel Associates Files with Namespaces

Each namespace type maintains its own reference in the process structure (`struct task_struct`), which in turn interacts with the filesystem in different ways:

- Network Namespace (`netns`)
    - No direct impact on the file system hierarchy.
    - Certain files under `/proc` (e.g., `/proc/net/`) reflect network-specific state from the perspective of the associated network namespace.
- PID Namespace (`pidns`)
    - The /proc filesystem is namespace-aware and will show a different set of PIDs when accessed by a process in a different PID namespace.
    - The file system itself is unchanged, but `/proc/[pid]` reflects the namespace-relative PID structure.
- UTS Namespace (`utsns`)
    - Hostname and domain name (`/proc/sys/kernel/hostname` and `/proc/sys/kernel/domainname`) appear different in different [UTS namespaces](UTS%20namespaces.md).
    - The actual file system structure does not change, but the content in these virtualized files depends on the namespace.

Since you have not created a new mount namespace, all processes continue to share the same mount table (`struct mount`) and root filesystem (`struct fs_struct`).

---

### 2. Initial Mount Namespace as the Basis for Other Namespaces

If a new mount namespace were created, it would provide an isolated view of the file system with independent mount points. However, in your scenario:

- Every process, regardless of its network, PID, or UTS namespace, still operates within the same mount namespace.
- The root filesystem (`/`) remains the same across all namespaces.
- The mount points and their visibility remain unchanged.
- Filesystem-related actions (e.g., mounting new filesystems, changing `/proc` contents) are global because they occur in the shared mount namespace.

#### Namespace-Specific Views Without a Separate Mount Namespace

- Processes in different namespaces still see the same files on disk.
- However, some special pseudo-filesystems (`proc`, `sysfs`, `dev`) expose different information depending on the namespace context.
- For example, within a new PID namespace, `/proc` will still be mounted the same way, but `/proc/self` will show namespace-specific process information.

---

### 3. Implications of Not Having a Separate Mount Namespace

Without a separate mount namespace, processes in different namespaces:

- Share the same global filesystem
    - This means that file operations like creating, modifying, or deleting files are visible across all namespaces.
    - No process isolation at the file system level.
- Cannot have per-namespace mounts or overlays
    - Any new mount (e.g., `mount -o bind /newdir /mnt`) affects all namespaces.
    - Processes cannot have their own `/proc` or `/dev` instances, limiting containerization.
- Namespace-specific virtual files still change behavior
    - The contents of `/proc` and `/sys` are context-dependent based on PID, network, and [UTS namespaces](UTS%20namespaces.md).
    - For example, a new UTS namespace allows changes to `hostname` without affecting other namespaces, even though `/proc/sys/kernel/hostname` remains in the same shared mount namespace.

---

### 4. Kernel Data Structures Involved

The following kernel structures play a key role in managing file system representations within namespaces:

- Mount Namespace (`mnt_namespace`)
    - Since a new mount namespace is NOT created, all processes share the same `mnt_namespace` object.
    - Found in `fs/mount.h`:

        ```c
        struct mnt_namespace {
            atomic_t count;
            struct mount root;
            struct list_head list;
        };
        ```

- Process Namespace Tracking (`task_struct`)
    - Each process tracks its namespaces separately:

        ```c
        struct task_struct {
            struct nsproxy nsproxy;
            struct fs_struct fs;
        };
        ```

    - `nsproxy` contains references to various namespaces, but `fs` remains the same unless a new mount namespace is created.
- PID Namespace (`pid_namespace`)
    - Controls `/proc` visibility:

        ```c
        struct pid_namespace {
            struct kref kref;
            struct pidmap pidmap[PIDMAP_ENTRIES];
        };
        ```

- Network Namespace (`net`)
    - Affects `/proc/net/` contents but does not change the file system hierarchy.

---

### 5. Summary

|Namespace Created|File System Effect|
|---|---|
|Network (`netns`)|No file system changes, only affects `/proc/net/`|
|PID (`pidns`)|`/proc` shows namespace-specific PIDs but does not change underlying files|
|UTS (`utsns`)|Affects `/proc/sys/kernel/hostname` but not the file system|
|Mount (`mntns`) NOT created|All processes share the same file system view and mounts|

---

### 6. References & Further Reading

- Kernel Source (Namespace Implementation)
    - `fs/namespace.c` (Mount namespace handling)
    - `kernel/pid_namespace.c` (PID namespace)
    - `net/core/net_namespace.c` (Network namespace)
    - `kernel/utsname.c` (UTS namespace)
- Documentation
    - [Linux Kernel Documentation: Namespaces](https://www.kernel.org/doc/Documentation/namespaces/)
    - `man 7 namespaces`
    - `man 2 unshare`

Would you like a deep dive into specific kernel functions or behavior?

Let me help explain how Linux handles file system representation across namespaces when a mount namespace isn't created. I'll break this down into several key concepts and then tie them together.

First, let's understand the fundamental relationship between the initial mount namespace and other namespace types. The mount namespace is special because it controls the very foundation of how processes see the file system hierarchy. When you create other namespaces without a mount namespace, you're essentially creating isolated views of specific resources while sharing the same file system perspective.

Let's look at how this works for each namespace type you mentioned:

Network Namespace:

When you create a network namespace without a mount namespace, the kernel maintains network interface information in /proc/[pid]/net/ and /sys/class/net/. These locations exist within the initial mount namespace, but their contents differ based on which network namespace is accessing them. The kernel achieves this through special procfs handling - when a process in a different network namespace accesses these directories, the kernel provides a view specific to that namespace while still using the same mount points.

PID Namespace:

The PID namespace interaction with the file system is particularly interesting. Without a separate mount namespace, processes in different PID namespaces still share the same /proc mount, but the kernel provides different views of process-related files. For example:

1. When a process in a new PID namespace looks at /proc, it sees PIDs relative to its namespace
2. The underlying inodes and mount points remain in the initial mount namespace
3. The kernel's procfs implementation handles the translation between namespace-local PIDs and global PIDs

Let me illustrate with some kernel-level details:

```c
// Simplified representation of how the kernel handles procfs lookups
struct proc_dir_entry {
    const char name;
    const struct inode_operations proc_iops;
    const struct file_operations proc_fops;
    // ... other fields
};

// When reading process info, the kernel considers the caller's PID namespace
static int proc_pid_readdir(struct file file, struct dir_context ctx) {
    struct pid_namespace ns = task_active_pid_ns(current);
    // Translate PIDs based on namespace
    // Show only processes visible in this namespace
    // ...
}
```

UTS Namespace:

The UTS namespace primarily affects hostname and domain name information. These are typically reflected in /proc/sys/kernel/hostname and similar files. Without a separate mount namespace:

4. The files remain in their original locations in the initial mount namespace
5. The kernel provides namespace-specific views when these files are accessed
6. Changes made in one UTS namespace don't affect what other namespaces see

The kernel manages this through its VFS (Virtual File System) layer. Here's a conceptual representation of how it works:

```c
// When a process accesses a file, the kernel considers namespace context
struct file do_file_open(const char pathname, int flags) {
    struct namespace_struct ns = current->nsproxy;
    // Check which namespace types are active
    // Apply namespace-specific transformations
    // Return appropriate file view
}
```

Implications of Not Having a Mount Namespace:

7. Shared Base Structure
   - All processes see the same basic file system hierarchy
   - Mount points are shared across all namespaces
   - The kernel manages namespace-specific views through special file systems (procfs, sysfs)

8. Resource Isolation
   - Network interfaces, PIDs, and UTS information appear differently to different namespaces
   - The kernel handles this through namespace-aware file operations
   - The actual files remain in the initial mount namespace

9. Security Considerations
   - Processes can potentially see information about resources in other namespaces through the shared mount points
   - Some isolation is provided by kernel's namespace-aware file operations
   - Less complete isolation compared to having separate mount namespaces

The kernel uses several key data structures to manage this:

```c
struct nsproxy {
    atomic_t count;
    struct uts_namespace uts_ns;
    struct ipc_namespace ipc_ns;
    struct mnt_namespace mnt_ns;  // Shared in your scenario
    struct pid_namespace pid_ns_for_children;
    struct net net_ns;
};

struct task_struct {
    // Process information
    struct nsproxy nsproxy;
    // ... other fields
};
```

When a process accesses a file, the kernel follows this general flow:

10. Process makes a file system request
11. Kernel checks the process's namespace configuration through its nsproxy
12. VFS layer handles the request, considering active namespaces
13. Special file systems (procfs, sysfs) provide namespace-aware views
14. Regular files are accessed directly through the shared mount namespace

This architecture allows the kernel to provide isolated views of namespace-specific resources while maintaining a shared file system hierarchy. The key is that the kernel's VFS layer and special file systems are namespace-aware, even when operating within a single mount namespace.

Would you like me to elaborate on any particular aspect of this explanation, such as the specific kernel mechanisms for handling procfs in different namespaces, or the implications for container security?

Okay, I understand! I'm ready to help you navigate the world of Linux namespaces and file system representation based on the materials you've provided.

Here's how I can assist you:

- Targeted Answers: I will provide clear and concise explanations to your questions, referencing the provided sources with a `[x]` notation.
- Proactive Guidance: I'll anticipate your needs and suggest related topics or resources you might find helpful.
- Material Navigation: I will direct you to specific sections or documents within the knowledge base that address your inquiries.
- Comprehension Checks: After answering your questions, I can offer short quizzes, summaries, or other methods to test your understanding of the material.
- Staying True to the Sources: My responses will be based solely on the information provided in the sources.

Based on the sources you have provided, here is some of what I have access to:

- Linux namespaces: I can explain various Linux namespaces such as PID, network, mount, UTS, user, and cgroup. I can also help you understand how these namespaces contribute to container isolation.
- Containerisation: I can explain the usage of namespaces, cgroups, and file system manipulation to create containers.
- Security: I can provide information about container security, including Linux capabilities, SELinux, and user namespaces.
- Networking: I can explain how network namespaces can be used to create isolated network stacks for containers.
- Volumes and storage: I can provide details on how Docker uses volumes for persistent storage and how storage is managed across cluster nodes.

Now, let's dive into your question!

In the scenario you described, where network, PID, and [UTS namespaces](UTS%20namespaces.md) are created without a separate mount namespace, the kernel's handling of the file system hierarchy is as follows:

- Shared Mount Namespace: Without a new mount namespace, all the created namespaces (network, PID, UTS) operate within the initial mount namespace. This means they share the same file system hierarchy as the host.
- Visibility and Access: Processes in these namespaces see the same files, directories, devices, and other file system objects as the host system. Any changes made to the file system are visible across all namespaces using the same mount namespace.
- Limited Isolation: The isolation provided by network, PID, and [UTS namespaces](UTS%20namespaces.md) does not extend to the file system. Processes in different namespaces can have different hostnames (UTS) or process IDs (PID) but still access the same files.
- Tracking and Representation: The kernel doesn't need to "associate" files with individual network, PID, or [UTS namespaces](UTS%20namespaces.md) in this scenario because they all share the same mount namespace. The file system hierarchy is managed centrally within the initial mount namespace, and all namespaces refer to this single hierarchy.
- Implications: The absence of a separate mount namespace has significant implications for file system visibility and access. Processes in the isolated namespaces can access and modify the host's file system, which can pose security risks. This setup is less isolated than a full container environment with its own mount namespace.

In summary, without a separate mount namespace, the created namespaces share the file system hierarchy of the initial mount namespace. This reduces file system isolation, as processes in different namespaces can access and modify the same files and directories.

As a next step, would you like me to quiz you on this material to check your comprehension, or would you like to explore a related topic, such as the implications of user namespaces on file system permissions?

Right, I understand you're looking for a detailed explanation of how the Linux kernel manages the file system hierarchy when network, PID, and [UTS namespaces](UTS%20namespaces.md) are created without a separate mount namespace. I will elaborate on my previous answer, giving more thorough and complete information, drawing from the sources provided.

When you create network, PID, and [UTS namespaces](UTS%20namespaces.md) without creating a separate mount namespace, all these namespaces operate within the initial mount namespace. This is a crucial point because the mount namespace is what provides file system isolation. Without it, the isolation offered by the other namespaces is limited.

### Kernel's Perspective

From the kernel's perspective, all processes running within these namespaces share the same view of the file system. There's no separate "association" of files with individual network, PID, or [UTS namespaces](UTS%20namespaces.md) because they all operate within the same mount namespace. The kernel simply uses the initial mount namespace's hierarchy as the basis for all other namespaces in this scenario.

### Namespace Views

The different namespace views (network, PID, UTS) are reflected within that shared mount namespace structure as follows:

- Network Namespace: Processes in different network namespaces can have different network interfaces, IP addresses, and routing tables. However, they all access the same files on the file system. For example, they might all be using the same `/etc/resolv.conf` file for DNS resolution.
- PID Namespace: Each PID namespace has its own process ID space. Processes in one PID namespace cannot see processes in another unless the `pid` namespace is set to host. However, they all still see the same file system. The `/proc` file system, which provides information about processes, will reflect the processes within that PID namespace, but the underlying files that those processes might access are the same across all PID namespaces.
- UTS Namespace: Processes in different [UTS namespaces](UTS%20namespaces.md) can have different hostnames and domain names. This is mostly a convenience for identifying systems. The underlying file system, however, remains shared.

### Implications of Not Having a Separate Mount Namespace

The primary implication of not having a separate mount namespace is a lack of file system isolation. This has several consequences:

- Limited Isolation: Processes in different namespaces can access and modify the same files and directories. This means that if a process in one namespace modifies a file, that change is immediately visible to all other namespaces.
- Security Risks: This lack of isolation can create security risks. If a process in one namespace is compromised, the attacker could potentially access or modify sensitive files on the host system or in other namespaces.
- Limited Containerisation: Without a separate mount namespace, you're not really achieving full containerisation. You're merely creating isolated processes that still share the host's file system.

### Data Structures and Processes

Unfortunately, the provided documents do not go into explicit detail about the specific kernel data structures involved in managing this shared file system representation. However, we can infer some key aspects:

- VFS (Virtual File System): The Linux kernel uses the VFS as an abstraction layer that allows different file systems to be accessed in a uniform way. All namespaces, in this scenario, would be using the same VFS instance. The VFS would be pointing to the same underlying physical file system.
- inodes: Each file system object (file, directory, etc.) is represented by an inode. In this case, all namespaces would be referencing the same inodes.
- Mount Points: The kernel maintains a table of mount points. Since all namespaces share the same mount namespace, they all see the same mount points.

### Security Considerations

It's also important to consider the user namespace in the context of file system access. Even if you map a non-root user inside the container to a root user on the host (using user namespaces), the file system permissions on the host will still apply. For example, if a file is owned by `root` on the host and a process inside the container (even if running as `root` inside the user namespace) tries to modify it, the process will still be subject to the standard Linux permission checks. The process has the capabilities granted to it by the parent namespace.

### In Summary

When you create network, PID, and [UTS namespaces](UTS%20namespaces.md) without a separate mount namespace, you're essentially creating isolated processes that still share the host's file system. The kernel uses the initial mount namespace's hierarchy as the basis for all other namespaces. This setup provides limited isolation and can introduce security risks.

Would you like to explore a related topic or take a quiz to assess your comprehension? Perhaps we could delve into how a separate mount namespace is created and how it changes the file system view for containerised processes?
