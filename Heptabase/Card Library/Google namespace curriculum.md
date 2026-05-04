# Google namespace curriculum

Here's a breakdown of the source materials you've provided, which I will use to help you with your learning program:

[BPF Performance Tools.md](BPF%20Performance%20Tools.md)

[Building containers by hand using namespaces.md](Building%20containers%20by%20hand%20using%20namespaces.md)

[Computer Networking A Top-Down Approach.md](Computer%20Networking%20A%20Top-Down%20Approach.md)

[Docker Deep Dive.md](Docker%20Deep%20Dive.md)

[!Kubernetes Networking! This resource is a curated list of materials to help with learning Kubern.md](!Kubernetes%20Networking!%20This%20resource%20is%20a%20curated%20list%20of%20materials%20to%20help%20with%20learning%20Kubern.md)

- "Kubernetes Security and Observability - Brendan Creane.pdf": This book guides you on developing a holistic security and observability strategy for Kubernetes. It covers topics like Kubernetes adoption, security controls, threat defence, observability, log collection, and network policies. It also talks about important security concepts like Pod Security Policies, capabilities, seccomp, AppArmor, and SELinux.

- "The 7 most used Linux [namespaces.md](http://namespaces.md)": This article provides a useful overview of the seven most common Linux namespaces (PID, mount, network, IPC, UTS, user, and cgroup), explains how they provide isolation, and briefly covers how they can be used in the creation of containers.

- "building a container [components.md](http://components.md)": This document focuses on network namespaces, explaining core concepts and providing examples of how to use `ip netns` and virtual ethernet pairs to create isolated networks. It also suggests hands-on learning projects.

- "k8s [curriculum.md](http://curriculum.md)": This document proposes a curriculum for learning about containers, beginning with low-level Linux primitives (namespaces and cgroups), progressing to image creation, and finally to integration projects and Kubernetes. It also includes Kubernetes and Container technology mastery levels, and a practical skills matrix, with a strong focus on hands-on learning. It provides validation methods, resources, and progress tracking for your learning. It also covers visualisation techniques for networks.

- "k8s network learning [project.md](http://project.md)": This document lays out a plan for learning Kubernetes networking, starting with Linux networking basics and progressing to AWS-specific implementations and Calico. It provides hands-on labs for learning each level. It also gives detailed instructions for setting up Calico policies. It proposes a detailed project for setting up and connecting two namespaces.

- "[ldx.md](http://ldx.md)": This article provides a comprehensive guide to LXC and LXD, highlighting their core concepts like namespaces and cgroups, the benefits they offer, and their limitations compared to other containerization technologies.

Now, regarding your specific request to structure a learning program for containers and Linux namespaces, I recommend a curriculum that progresses from the fundamentals to more advanced topics, with hands-on exercises at each stage. Here's a possible structure that takes into account the concepts of practical learning, and overcoming the illusion of explanatory depth:

[Phase 1! Linux Fundamentals.md](Phase%201!%20Linux%20Fundamentals.md)

[Phase 2! Containerisation.md](Phase%202!%20Containerisation.md)

[Phase 3! Container Orchestration with Kubernetes.md](Phase%203!%20Container%20Orchestration%20with%20Kubernetes.md)

## Overcoming the Illusion of Explanatory Depth

- Hands-on Learning: Focus on building and testing rather than just reading.

- "Why" instead of "How": Prioritise understanding the reasons behind design decisions and configurations.

- Visualisation: Use the suggested tools to visualise how the networks are implemented, instead of thinking of them as abstract concepts.

- Troubleshooting: Intentionally break things to learn the root cause of failures.