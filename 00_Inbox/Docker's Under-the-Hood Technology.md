# **Under the Hood of Docker: Namespaces, Cgroups, and Union File Systems**

Docker has revolutionized software development and deployment by packaging applications and their dependencies into isolated containers. This approach simplifies the development lifecycle and enhances portability across diverse environments. But how does Docker achieve this? This article delves into the core technologies behind Docker: namespaces, cgroups, and union file systems.

## **Namespaces: Isolating Container Worlds**

Imagine a modern skyscraper with numerous offices, each occupied by different companies with their own unique operations and work styles. Namespaces in Docker are like these offices, providing isolated environments for containers to operate without interfering with each other or the host system. They create the illusion that each container has its own dedicated set of system resources, even though they share the underlying kernel. This isolation is crucial for security and stability in containerized environments.

### **Types of Namespaces**

Docker utilizes six primary types of namespaces to achieve this isolation 1:

* **PID Namespace:** Isolates process IDs, giving each container its own process ID space. This means that processes in one container cannot see or interact with processes in other containers or on the host system. The first process in a container is assigned PID 1, just like a traditional operating system 2.  
* **Network Namespace:** Provides each container with its own virtual network stack, including network interfaces, IP addresses, routing tables, and ports 4. This isolation allows containers to have independent network configurations without conflicts.  
* **Mount Namespace:** Isolates the file system, giving each container its own view of the file system hierarchy 3. Changes made to the file system within a container are not visible outside of that container.  
* **UTS Namespace:** Isolates hostname and domain name 4. Each container can have a unique hostname, which is essential for network identification and management.  
* **IPC Namespace:** Isolates inter-process communication (IPC) resources, such as message queues and semaphores 3. This prevents containers from interfering with each other's IPC mechanisms.  
* **User Namespace:** Isolates user and group IDs 1. This allows containers to have their own user and group settings, enhancing security by preventing privilege escalation attacks. For instance, a process running as root inside a container can be mapped to a non-root user on the host system, limiting its privileges 5.

In addition to these six main namespaces, Linux also supports cgroup and time namespaces, which are not typically used by Docker 1.

### **User Namespaces and Security**

Docker provides the \--user option to specify a non-root user for running the main process within a container 5. This enhances security by limiting the container's privileges and reducing the potential impact of vulnerabilities. User namespaces further strengthen security by remapping user IDs and group IDs within the container to different IDs on the host system. This prevents a containerized process running as root from having root privileges on the host 7.

### **Namespaces in Kubernetes**

The concept of namespaces also extends to container orchestration platforms like Kubernetes. In Kubernetes, namespaces provide a way to divide cluster resources among multiple users or teams 8. This allows for logical grouping and isolation of resources within a shared cluster. However, it's important to note that overusing namespaces in Kubernetes can lead to management overhead and potential inefficiencies 9.

### **Advantages and Disadvantages of Namespaces**

Namespaces offer significant advantages in terms of security, resource isolation, and portability. They enhance security by preventing processes in one container from accessing or interfering with those in other containers or on the host system. This isolation also ensures that each container has its own dedicated view of system resources, preventing conflicts and improving performance. Furthermore, namespaces enable containers to be moved between different environments without compatibility issues.

However, configuring and managing namespaces can be complex, especially when dealing with user namespaces and bind mounts. Some Docker features may also be incompatible with user namespaces, requiring careful consideration and configuration.

## **Cgroups: Managing Container Resources**

While namespaces provide isolation, cgroups (control groups) are responsible for managing and limiting the resources that containers can consume. They act as resource controllers, allowing you to set limits on CPU usage, memory allocation, disk I/O, and network bandwidth for each container.

### **Cgroups and Resource Management**

Docker utilizes cgroups to ensure that containers do not overconsume resources and affect the performance of other containers or the host system 5. Here are some of the key cgroup functionalities used by Docker:

* **CPU Management:** Docker can limit the CPU usage of a container by setting CPU quotas and periods. This prevents a single container from monopolizing the CPU and ensures fair resource allocation among containers 11. For example, you can use the \--cpus flag with the docker run command to specify the number of CPUs a container can use 13.  
* **Memory Management:** Cgroups allow Docker to set memory limits for containers, preventing them from exceeding their allocated memory and causing system instability 14. The \--memory flag can be used to set a memory limit for a container 13.  
* **Block I/O Management:** Docker can control the disk I/O bandwidth available to a container, preventing I/O-intensive containers from affecting the performance of other containers or the host system 15.  
* **Network Bandwidth Management:** Cgroups can limit the network bandwidth available to a container, ensuring fair sharing of network resources among containers 12. While Docker doesn't have built-in options for network bandwidth management, third-party tools like docker-tc can be used to achieve this 16.

### **Cgroup Types**

Cgroups provide various controllers for managing different types of resources 17:

* **blkio:** This controller sets limits for block I/O devices, such as disk drives.  
* **cpuset:** This controller allocates specific CPU cores and memory nodes to a cgroup.  
* **memory:** This controller sets limits for memory usage.  
* **cpu:** This controller limits CPU usage.  
* **devices:** This controller controls access to devices.  
* **freezer:** This controller allows suspending and resuming processes within a cgroup.  
* **net\_cls:** This controller allows classifying network traffic generated by processes within a cgroup.  
* **perf\_event:** This controller allows monitoring performance counters for processes within a cgroup.  
* **hugetlb:** This controller manages access to huge pages.

### **Cgroup Drivers**

Docker supports different cgroup drivers, including cgroupfs and systemd 5. The cgroup driver determines how cgroup information is organized and stored on the host system. The location of cgroup information for a container varies depending on the cgroup version and driver used.

### **Monitoring Cgroup Usage**

Docker provides the docker stats command to monitor real-time resource usage statistics for containers 13. This command displays CPU usage, memory usage, network I/O, and block I/O for each running container. You can also inspect cgroup settings directly by accessing the cgroup filesystem 13. This allows for more detailed analysis and troubleshooting of container resource usage.

### **Advantages and Disadvantages of Cgroups**

Cgroups offer fine-grained control over resource allocation, enabling efficient resource utilization and system stability. They prevent resource contention and ensure that applications run smoothly by limiting resource usage. Cgroups also contribute to security by preventing resource exhaustion and denial-of-service attacks like fork bombs 10.

However, configuring cgroups can be complex, especially when dealing with different cgroup versions and drivers. Monitoring cgroup usage can also be challenging, requiring specialized tools and knowledge.

## **Union File Systems: Building Efficient Container Images**

Union file systems (UnionFS) are the foundation of Docker's image management system. They enable the creation of layered file systems, where multiple file systems are stacked on top of each other to create a single unified view. This layering approach allows Docker to create lightweight and efficient images by sharing common files and only storing the differences between images.

### **Layered File Systems**

Docker images are built as a series of read-only layers, each representing a change to the image 19. When you run a container from an image, Docker creates a thin writable layer on top of the image layers, called the container layer. This layer stores any changes made to the container during its lifetime.

### **OverlayFS**

Docker uses a UnionFS variant called overlay2 by default 19. Overlay2 provides improved performance and efficiency compared to earlier UnionFS implementations. It works by using two directories for each layer: a "lowerdir" containing files from the previous layer and an "upperdir" containing changes for the current layer. When a container is run, a "merged" directory provides a unified view of all layers, and a "diff" directory stores container-specific changes.

### **Whiteouts**

Union file systems support the concept of "whiteouts," which allow for the effective deletion of files from lower layers 20. A whiteout is a special file that indicates that a file from a lower layer should be hidden in the merged view.

### **Docker Container Commit**

The docker container commit command allows users to create new image layers manually by saving changes made to a container as a new image 21. This command provides a practical way to understand and utilize the layering capabilities of union file systems.

### **Advantages and Disadvantages of Union File Systems**

Union file systems offer significant advantages for Docker images. Layering allows images to share common files, reducing storage space and improving image build and deployment times. Each layer represents a change to the image, making it easy to track changes and revert to previous versions. Layers can also be reused across multiple images, simplifying image creation and management.

However, accessing files in a layered file system can introduce some performance overhead compared to a traditional file system. Understanding and managing layered file systems can also be complex, especially when dealing with many layers.

## **A Historical Perspective**

The concepts of namespaces and cgroups have a rich history in the Linux kernel. Namespaces were introduced around 2002 to provide process isolation, and cgroups were introduced in 2007 to manage resource allocation 18. These technologies have evolved over time, with significant improvements and additions in recent years. The development of these technologies has been crucial for the rise of containerization and its widespread adoption in modern software development.

## **Conclusion**

Namespaces, cgroups, and union file systems are fundamental to Docker's containerization technology. Namespaces provide isolation, cgroups manage resources, and union file systems enable efficient image management. These technologies work together seamlessly to provide a robust and efficient platform for building, deploying, and running containerized applications.

Understanding these core technologies is essential for developers and system administrators working with Docker. This knowledge allows for better resource utilization, improved security, and efficient image management. By mastering these concepts, you can unlock the full potential of Docker and optimize your containerized applications.

#### **Works cited**

1\. Container security fundamentals part 2: Isolation & namespaces, accessed on January 25, 2025, [https://securitylabs.datadoghq.com/articles/container-security-fundamentals-part-2/](https://securitylabs.datadoghq.com/articles/container-security-fundamentals-part-2/)  
2\. Understanding Process Isolation In Docker: An In-Depth Look at PID Namespaces, accessed on January 25, 2025, [https://dev.to/kalkwst/understanding-process-isolation-in-docker-an-in-depth-look-at-pid-namespaces-2ehh](https://dev.to/kalkwst/understanding-process-isolation-in-docker-an-in-depth-look-at-pid-namespaces-2ehh)  
3\. What is Docker Namespaces? \- GeeksforGeeks, accessed on January 25, 2025, [https://www.geeksforgeeks.org/what-is-docker-namespaces/](https://www.geeksforgeeks.org/what-is-docker-namespaces/)  
4\. How to Use Docker Namespaces to Isolate Containers \- Earthly Blog, accessed on January 25, 2025, [https://earthly.dev/blog/namespaces-and-containers-in-depth/](https://earthly.dev/blog/namespaces-and-containers-in-depth/)  
5\. How to Use Linux Namespaces and cgroups to Control Docker Performance \- Earthly Blog, accessed on January 25, 2025, [https://earthly.dev/blog/namespaces-and-cgroups-docker/](https://earthly.dev/blog/namespaces-and-cgroups-docker/)  
6\. Diving deep: How docker achieves container isolation using the underlying OS \[Part 1\], accessed on January 25, 2025, [https://hewi.blog/diving-deep-how-docker-achieves-container-isolation-using-the-underlying-os-part-1](https://hewi.blog/diving-deep-how-docker-achieves-container-isolation-using-the-underlying-os-part-1)  
7\. Isolate containers with a user namespace \- Docker Docs, accessed on January 25, 2025, [https://docs.docker.com/engine/security/userns-remap/](https://docs.docker.com/engine/security/userns-remap/)  
8\. Namespaces \- Kubernetes, accessed on January 25, 2025, [https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/](https://kubernetes.io/docs/concepts/overview/working-with-objects/namespaces/)  
9\. Kubernetes Namespaces: Security Best Practices \- Wiz, accessed on January 25, 2025, [https://www.wiz.io/academy/kubernetes-namespaces](https://www.wiz.io/academy/kubernetes-namespaces)  
10\. Container security fundamentals part 4: Cgroups | Datadog Security ..., accessed on January 25, 2025, [https://securitylabs.datadoghq.com/articles/container-security-fundamentals-part-4/](https://securitylabs.datadoghq.com/articles/container-security-fundamentals-part-4/)  
11\. Docker — Linux security technologies (cGroups) | by Fsegredo \- Medium, accessed on January 25, 2025, [https://medium.com/@fsegredo2000/docker-linux-security-technologies-cgroups-979002f28c7d](https://medium.com/@fsegredo2000/docker-linux-security-technologies-cgroups-979002f28c7d)  
12\. Understanding Docker Containers: Leveraging Linux Kernel's Namespaces and cgroups, accessed on January 25, 2025, [https://dev.to/mochafreddo/understanding-docker-containers-leveraging-linux-kernels-namespaces-and-cgroups-4fkk](https://dev.to/mochafreddo/understanding-docker-containers-leveraging-linux-kernels-namespaces-and-cgroups-4fkk)  
13\. Managing Docker Resources with Cgroups: A Practical Guide | by Ramkrushna Maheshwar | Medium, accessed on January 25, 2025, [https://medium.com/@maheshwar.ramkrushna/managing-docker-resources-with-cgroups-a-practical-guide-169289c80451](https://medium.com/@maheshwar.ramkrushna/managing-docker-resources-with-cgroups-a-practical-guide-169289c80451)  
14\. Resource constraints \- Docker Docs, accessed on January 25, 2025, [https://docs.docker.com/engine/containers/resource\_constraints/](https://docs.docker.com/engine/containers/resource_constraints/)  
15\. How Docker uses cgroups to set resource limits? \- Shekhar Gulati, accessed on January 25, 2025, [https://shekhargulati.com/2019/01/03/how-docker-uses-cgroups-to-set-resource-limits/](https://shekhargulati.com/2019/01/03/how-docker-uses-cgroups-to-set-resource-limits/)  
16\. shivacherukuri/Docker-Network-Bandwidth \- GitHub, accessed on January 25, 2025, [https://github.com/shivacherukuri/Docker-Network-Bandwidth](https://github.com/shivacherukuri/Docker-Network-Bandwidth)  
17\. Cgroups: Container Resource Limitation \- Henry Du Blog, accessed on January 25, 2025, [https://www.henrydu.com/2021/11/20/cgroups-container-resource-limitation/](https://www.henrydu.com/2021/11/20/cgroups-container-resource-limitation/)  
18\. Cgroups \- Wikipedia, accessed on January 25, 2025, [https://en.wikipedia.org/wiki/Cgroups](https://en.wikipedia.org/wiki/Cgroups)  
19\. Docker Images: A Deep Dive into Container Technology | by Roman Glushach | Medium, accessed on January 25, 2025, [https://romanglushach.medium.com/docker-images-a-deep-dive-into-container-technology-43ea01b4d7e1](https://romanglushach.medium.com/docker-images-a-deep-dive-into-container-technology-43ea01b4d7e1)  
20\. Unioning file systems: Architecture, features, and design choices \- LWN.net, accessed on January 25, 2025, [https://lwn.net/Articles/324291/](https://lwn.net/Articles/324291/)  
21\. Understanding the image layers \- Docker Docs, accessed on January 25, 2025, [https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/](https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/)