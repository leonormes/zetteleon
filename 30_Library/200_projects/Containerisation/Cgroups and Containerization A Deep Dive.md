---
aliases: []
confidence: 
created: 2025-12-13T19:35:10Z
epistemic: 
last_reviewed: 
modified: 2025-12-14T17:53:38Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Cgroups and Containerization A Deep Dive
type: 
uid: 
updated: 
---

## **Cgroups: A Deep Dive into Containerization**

Cgroups (control groups) are a crucial Linux kernel feature that revolutionized resource management and laid the groundwork for modern containerization technologies like Docker and Kubernetes. This article provides a deep practical understanding of cgroups, exploring their mechanisms, functionalities, and how they enable containerization.

### **What Are Cgroups?**

Cgroups are defined as a Linux kernel feature that provides a mechanism for aggregating sets of processes into hierarchical groups with specialized behavior 1. These groups can then be managed by assigning specific parameters for one or more subsystems. In essence, cgroups act as resource "containers," allowing for fine-grained control over how processes utilize system resources such as CPU, memory, disk I/O, and network bandwidth.

Cgroups achieve this control by:

- **Grouping:** Organizing processes into hierarchical groups, where child groups inherit properties from their parent groups.  
- **Resource Limiting:** Setting limits on the amount of resources a group of processes can consume (e.g., maximum memory usage, CPU time).  
- **Prioritization:** Assigning relative shares of resources among groups, ensuring that critical processes receive adequate resources.  
- **Accounting:** Tracking resource usage by each group, providing valuable insights for performance analysis and capacity planning.  
- **Isolation:** Preventing processes in different groups from interfering with each other's resource usage.

### **How Cgroups Work**

Cgroups are implemented through a pseudo-filesystem called cgroupfs 2. This filesystem provides a hierarchical structure where each directory represents a cgroup, and files within each directory control the group's parameters.

For example, Red Hat Enterprise Linux 7 binds the cgroup hierarchy with the systemd unit tree, allowing system administrators to manage system resources with systemctl commands or by modifying systemd unit files 4.

Here's a breakdown of how to interact with the cgroupfs filesystem:

1. **Hierarchy Creation:** Cgroup hierarchies are created by mounting the cgroupfs filesystem. Each hierarchy is associated with one or more resource controllers (subsystems) that manage specific resources (e.g., CPU, memory).  
2. **Cgroup Creation:** Creating a directory within a hierarchy creates a new cgroup. For example, to create a cgroup named "mygroup," you would use the command mkdir /sys/fs/cgroup/cpu/mygroup.  
3. **Resource Control:** Files within each cgroup directory allow you to set limits and configure resource allocation for the processes in that cgroup. For instance, to limit the CPU usage of processes in "mygroup" to 50%, you would write 50000 100000 to the cpu.max file within that directory.  
4. **Process Association:** Processes are added to a cgroup by writing their process IDs (PIDs) to the cgroup.procs file in the corresponding cgroup directory.  
5. **Inheritance:** When a process forks a child process, the child process inherits the cgroup membership of its parent.  
6. **Cgroup Removal:** To remove a cgroup, you can use the command rmdir, but only if the cgroup is not in use (no child cgroups or processes attached).

Cgroups dynamically share idle resources for CPU and I/O, allowing other cgroups to utilize available bandwidth when not in use by another cgroup 5. However, memory sharing is more restrictive, often involving hard limits that are not exceeded even if there is unused capacity 5.

### **Cgroups And Containerization**

Cgroups are a fundamental building block for containerization technologies like Docker, Kubernetes, and Apptainer. They provide the necessary mechanisms to isolate containers and control their resource usage, ensuring that containers do not interfere with each other or with the host system.

Here's how cgroups enable containerization:

- **Resource Limits:** Cgroups allow container engines to set limits on the amount of CPU, memory, and other resources that a container can consume. This prevents resource exhaustion and ensures that containers run predictably.  
- **Isolation:** Cgroups isolate containers from each other, preventing them from accessing or affecting each other's resources. This ensures that one container's behavior does not impact the stability or performance of other containers.  
- **Security:** Cgroups can be used to restrict a container's access to devices and other system resources, enhancing security and preventing potential exploits.

A key insight is that cgroups help prevent "noisy neighbor" issues in containerized environments, especially in Kubernetes where multiple applications share resources 6. By limiting and isolating resource usage, cgroups ensure that one application's excessive resource consumption does not negatively impact other applications running on the same host.

#### **Docker And Cgroups**

Docker uses cgroups to manage and limit resources for containers. When you start a Docker container, Docker creates a new set of cgroups for the container and assigns the container's processes to those cgroups 7. Docker uses the \--cpus and \--memory flags to set CPU and memory limits for containers, respectively 8. These limits are enforced using cgroups.

In addition to cgroups, Docker leverages Linux namespaces to achieve container isolation 9. Namespaces provide isolation for various system resources, such as process IDs (PIDs), network interfaces, and mount points. By combining namespaces and cgroups, Docker creates an isolated environment for each container with controlled resource usage.

#### **Kubernetes And Cgroups**

Kubernetes also relies heavily on cgroups for resource management. Kubernetes uses cgroups to enforce resource quotas, limit container resource usage, and ensure quality of service (QoS) for pods 10. Kubernetes supports both cgroup v1 and v2, with cgroup v2 being the recommended version for its improved features and performance 11.

#### **Apptainer And Cgroups**

Apptainer, formerly known as Singularity, is another containerization technology that utilizes cgroups for resource management. Apptainer allows you to limit memory and CPU usage, rate limit block I/O and network I/O, and control access to device nodes within containers 12. This can be achieved by running the apptainer command inside an existing cgroup or by using the \--apply-cgroups flag with a TOML file specifying the cgroup configuration.

### **Practical Examples of Using Cgroups**

Here are some practical examples of how to use cgroups to limit resources for specific processes or containers:

**Example 1: Limiting CPU and Memory with cgroupfs 13**

1. Create a new cgroup: mkdir /sys/fs/cgroup/hog\_pen  
2. Limit CPU usage to 50%: echo "50000 100000" \> /sys/fs/cgroup/hog\_pen/cpu.max  
3. Limit memory usage to 100MB: echo "100M" \> /sys/fs/cgroup/hog\_pen/memory.max  
4. Add a process to the cgroup: echo \<process\_id\> \> /sys/fs/cgroup/hog\_pen/cgroup.procs

**Example 2: Setting Memory and CPU Limits 14**

1. Navigate to the cgroup directory: cd /sys/fs/cgroup  
2. Create a child cgroup: mkdir memory/cgroup\_test  
3. Define memory limit: echo "100m" \> memory/cgroup\_test/memory.limit\_in\_bytes  
4. Add a process to the cgroup: echo \<process\_id\> \> memory/cgroup\_test/cgroup.procs

These examples demonstrate how to manually create cgroups and set resource limits using the cgroupfs filesystem. Containerization technologies like Docker and Kubernetes often automate these steps, making it easier to manage resources for containers.

### **Types Of Cgroups**

| Cgroup Type | Function |
| :---- | :---- |
| CPU | Limits and controls CPU usage. |
| Memory | Limits and monitors memory usage. |
| Blkio | Controls and monitors block I/O. |
| Devices | Controls access to devices, including read, write, and mknod operations. The devices cgroup plays a crucial role in system security by restricting access to sensitive devices 15. |
| Freezer | Suspends and resumes processes. |
| Cpuset | Assigns processes to specific CPUs and memory nodes. This is particularly useful in NUMA environments to optimize memory access and performance 16. |
| HugeTLB | Controls access to huge pages. |
| Net\_cls | Classifies network packets. |
| Net\_prio | Prioritizes network traffic. |
| Pids | Limits the number of processes. |
| RDMA | Controls access to RDMA devices. |

### **Limitations And Security Concerns**

While cgroups are a powerful tool, they have some limitations:

- **No strict isolation:** Cgroups provide resource isolation, but they do not offer complete process isolation like virtual machines. Processes in different cgroups can still communicate and potentially affect each other through shared kernel resources.  
- **Complexity:** Managing cgroups can be complex, especially when dealing with multiple hierarchies and controllers.  
- **Security vulnerabilities:** Historically, there have been security vulnerabilities in cgroups that could allow processes to escape their resource constraints or gain unauthorized access to the host system 19.

Furthermore, it's important to be aware of the security risks associated with kernel exploits and misconfigurations in container environments 21. A vulnerability in the host kernel could potentially be exploited to compromise containers or the entire host system. Proper configuration and security hardening are essential to mitigate these risks.

### **Evolution Of Cgroups**

Cgroups have evolved significantly since their introduction. The initial version, cgroups v1, had limitations and inconsistencies that led to the development of cgroups v2 3. Cgroups v2 offers a unified hierarchy, improved resource management, and enhanced security features.

The move to cgroups v2 is driven by the need for improved scalability and a more consistent interface, aligning with the industry trend 22. This transition reflects the increasing demands of modern containerized workloads and the need for more robust and efficient resource management.

Some notable improvements in cgroups v2 include:

- **Unified hierarchy:** A single hierarchy for all controllers, simplifying management and improving performance.  
- **Safer subtree delegation:** Improved security for delegating control of cgroups to containers.  
- **Pressure Stall Information (PSI):** Provides metrics on resource contention, allowing for better resource allocation and performance tuning.  
- **Rootless containers:** Allows running containers without root privileges, enhancing security11.

### **Conclusion**

Cgroups are a powerful resource management feature in the Linux kernel that has enabled the rise of containerization. By providing resource limiting, prioritization, accounting, and isolation capabilities, cgroups allow container engines like Docker and Kubernetes to effectively manage and control resource usage for containers. This ensures that containers run predictably, do not interfere with each other, and are protected from potential security exploits.

The evolution of cgroups, with the introduction of cgroups v2, has brought significant improvements in terms of scalability, consistency, and security. Features like a unified hierarchy, safer subtree delegation, and rootless containers further enhance the capabilities of cgroups and their role in containerization. As cgroups continue to evolve, they will play an even more critical role in shaping the future of cloud-native computing.

#### **Works cited**

1\. Control Group v2 \- The Linux Kernel documentation, accessed on January 24, 2025, [https://docs.kernel.org/admin-guide/cgroup-v2.html](https://docs.kernel.org/admin-guide/cgroup-v2.html)  
2\. cgroups \- Linux control groups \- Ubuntu Manpage, accessed on January 24, 2025, [https://manpages.ubuntu.com/manpages/focal/man7/cgroups.7.html](https://manpages.ubuntu.com/manpages/focal/man7/cgroups.7.html)  
3\. cgroups(7) \- Linux manual page \- man7.org, accessed on January 24, 2025, [https://man7.org/linux/man-pages/man7/cgroups.7.html](https://man7.org/linux/man-pages/man7/cgroups.7.html)  
4\. Chapter 1\. Introduction to Control Groups (Cgroups) | Red Hat ..., accessed on January 24, 2025, [https://docs.redhat.com/en/documentation/red\_hat\_enterprise\_linux/7/html/resource\_management\_guide/chap-introduction\_to\_control\_groups](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/resource_management_guide/chap-introduction_to_control_groups)  
5\. Chapter 1\. Introduction to Control Groups (Cgroups) | Red Hat Product Documentation, accessed on January 24, 2025, [https://docs.redhat.com/en/documentation/red\_hat\_enterprise\_linux/6/html/resource\_management\_guide/ch01](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/6/html/resource_management_guide/ch01)  
6\. securitylabs.datadoghq.com, accessed on January 24, 2025, [https://securitylabs.datadoghq.com/articles/container-security-fundamentals-part-4/\#:\~:text=Docker%20and%20other%20containerization%20tools,resources%20on%20the%20same%20host.](https://securitylabs.datadoghq.com/articles/container-security-fundamentals-part-4/#:~:text=Docker%20and%20other%20containerization%20tools,resources%20on%20the%20same%20host.)  
7\. Understanding How Containers Work Behind the Scenes \- Kubesimplify, accessed on January 24, 2025, [https://blog.kubesimplify.com/understanding-how-containers-work-behind-the-scenes](https://blog.kubesimplify.com/understanding-how-containers-work-behind-the-scenes)  
8\. Managing Docker Resources with Cgroups: A Practical Guide | by Ramkrushna Maheshwar | Medium, accessed on January 24, 2025, [https://medium.com/@maheshwar.ramkrushna/managing-docker-resources-with-cgroups-a-practical-guide-169289c80451](https://medium.com/@maheshwar.ramkrushna/managing-docker-resources-with-cgroups-a-practical-guide-169289c80451)  
9\. Understanding Docker Containers: Leveraging Linux Kernel's Namespaces and cgroups, accessed on January 24, 2025, [https://dev.to/mochafreddo/understanding-docker-containers-leveraging-linux-kernels-namespaces-and-cgroups-4fkk](https://dev.to/mochafreddo/understanding-docker-containers-leveraging-linux-kernels-namespaces-and-cgroups-4fkk)  
10\. cgroups v2 changes in Kubernetes 1.28 and why it impacts your CAS Server availability, accessed on January 24, 2025, [https://communities.sas.com/t5/SAS-Communities-Library/cgroups-v2-changes-in-Kubernetes-1-28-and-why-it-impacts-your/ta-p/944364](https://communities.sas.com/t5/SAS-Communities-Library/cgroups-v2-changes-in-Kubernetes-1-28-and-why-it-impacts-your/ta-p/944364)  
11\. About cgroup v2 | Kubernetes, accessed on January 24, 2025, [https://kubernetes.io/docs/concepts/architecture/cgroups/](https://kubernetes.io/docs/concepts/architecture/cgroups/)  
12\. Limiting Container Resources with Cgroups — Apptainer User Guide 1.0 documentation, accessed on January 24, 2025, [https://apptainer.org/docs/user/1.0/cgroups.html](https://apptainer.org/docs/user/1.0/cgroups.html)  
13\. Controlling Process Resources with Linux Control Groups \- iximiuz Labs, accessed on January 24, 2025, [https://labs.iximiuz.com/tutorials/controlling-process-resources-with-cgroups](https://labs.iximiuz.com/tutorials/controlling-process-resources-with-cgroups)  
14\. Cgroup and Resource limits of containers | by Sankeerthan ..., accessed on January 24, 2025, [https://medium.com/@sankeerthan.kasilingam/cgroups-and-resource-limits-of-containers-33277489bce3](https://medium.com/@sankeerthan.kasilingam/cgroups-and-resource-limits-of-containers-33277489bce3)  
15\. A Linux sysadmin's introduction to cgroups \- Red Hat, accessed on January 24, 2025, [https://www.redhat.com/en/blog/cgroups-part-one](https://www.redhat.com/en/blog/cgroups-part-one)  
16\. An introduction to control groups (cgroups) version 2 \- Michael Kerrisk \- NDC TechTown 2021 \- YouTube, accessed on January 24, 2025, [https://www.youtube.com/watch?v=kcnFQgg9ToY](https://www.youtube.com/watch?v=kcnFQgg9ToY)  
17\. cgroups \- Wikipedia, accessed on January 24, 2025, [https://en.wikipedia.org/wiki/Cgroups](https://en.wikipedia.org/wiki/Cgroups)  
18\. cgroups \- ArchWiki, accessed on January 24, 2025, [https://wiki.archlinux.org/title/Cgroups](https://wiki.archlinux.org/title/Cgroups)  
19\. New Linux Kernel Vulnerability: Escaping Containers by Abusing Cgroups \- Aqua Security, accessed on January 24, 2025, [https://www.aquasec.com/blog/new-linux-kernel-vulnerability-escaping-containers-by-abusing-cgroups/](https://www.aquasec.com/blog/new-linux-kernel-vulnerability-escaping-containers-by-abusing-cgroups/)  
20\. New Linux Vulnerability CVE-2022-0492 Affecting Cgroups: Can Containers Escape?, accessed on January 24, 2025, [https://unit42.paloaltonetworks.com/cve-2022-0492-cgroups/](https://unit42.paloaltonetworks.com/cve-2022-0492-cgroups/)  
21\. What are Linux Containers? A Security Review \- Wiz, accessed on January 24, 2025, [https://www.wiz.io/academy/linux-containers-a-security-review](https://www.wiz.io/academy/linux-containers-a-security-review)  
22\. Kubernetes 1.31: Moving cgroup v1 Support into Maintenance Mode, accessed on January 24, 2025, [https://kubernetes.io/blog/2024/08/14/kubernetes-1-31-moving-cgroup-v1-support-maintenance-mode/](https://kubernetes.io/blog/2024/08/14/kubernetes-1-31-moving-cgroup-v1-support-maintenance-mode/)  
23\. Linux cgroups v2 Brings Rootless Containers, Superior Memory Management, accessed on January 24, 2025, [https://thenewstack.io/linux-cgroups-v2-brings-rootless-containers-superior-memory-management/](https://thenewstack.io/linux-cgroups-v2-brings-rootless-containers-superior-memory-management/)
