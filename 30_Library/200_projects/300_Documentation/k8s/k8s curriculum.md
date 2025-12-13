---
aliases: []
confidence: 
created: 2025-02-07T12:57:52Z
epistemic: 
id: container-curriculum
last_reviewed: 
modified: 2025-12-13T11:39:42Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [containers, k8s]
title: k8s curriculum
type: curriculum
uid: 
updated: 
version: 
---

## Linux Containers: From Scratch to Production

### Learning Path Overview

This curriculum focuses on building containers from scratch using Linux primitives, helping you understand the fundamental building blocks before moving to tools like Docker.

### Level 1: Container Building Blocks

#### Module 1: Process Isolation with Namespaces

Theory:

- Understanding Linux namespaces (pid, net, mnt, uts, ipc, user)
- Process isolation principles
- Resource containment basics

Practical Exercises:

1. Create an isolated process:

```bash
# Create a new UTS namespace
unshare --uts /bin/bash
# Verify isolation by changing hostname
hostname container1
# Verify change doesn't affect host
```

2. Explore PID namespace:

```bash
# Create new PID namespace
unshare --pid --fork /bin/bash
# List processes and observe isolation
ps aux
```

#### Module 2: Resource Control with Cgroups

Theory:

- Understanding cgroup hierarchy
- Resource limiting mechanisms
- CPU, memory, and I/O control

Practical Exercises:

1. Create and manage cgroups:

```bash
# Create a new cgroup
sudo mkdir /sys/fs/cgroup/memory/mycontainer
# Set memory limit (100MB)
echo 100000000 > /sys/fs/cgroup/memory/mycontainer/memory.limit_in_bytes
# Run process in cgroup
echo $$ > /sys/fs/cgroup/memory/mycontainer/cgroup.procs
```

2. Monitor resource usage:

```bash
# Watch memory usage
cat /sys/fs/cgroup/memory/mycontainer/memory.usage_in_bytes
```

### Level 2: Building Basic Containers

#### Module 1: File System Isolation

Theory:

- Root filesystem concepts
- Mount namespaces
- Overlay filesystems

Practical Exercises:

1. Create container root filesystem:

```bash
# Create minimal root filesystem
mkdir container-root
cd container-root
mkdir bin lib proc sys
# Copy basic binaries
cp /bin/bash bin/
# Copy required libraries
ldd /bin/bash | grep -o '/lib.\.[0-9]' | xargs -I {} cp {} lib/
```

2. Mount proc filesystem:

```bash
# Mount proc in container
mount -t proc none container-root/proc
```

#### Module 2: Network Isolation

Theory:

- Network namespaces
- Virtual interfaces
- Container networking models

Practical Exercises:

1. Create network namespace:

```bash
# Create namespace
ip netns add container1
# Create veth pair
ip link add veth0 type veth peer name veth1
# Move one end to namespace
ip link set veth1 netns container1
```

2. Configure networking:

```bash
# Configure IP addresses
ip addr add 172.16.0.1/24 dev veth0
ip netns exec container1 ip addr add 172.16.0.2/24 dev veth1
# Enable interfaces
ip link set veth0 up
ip netns exec container1 ip link set veth1 up
```

### Level 3: Advanced Container Features

#### Module 1: Security and Capabilities

Theory:

- Linux capabilities
- Seccomp profiles
- AppArmor/SELinux basics

Practical Exercises:

1. Drop capabilities:

```bash
# Start container with limited capabilities
unshare --pid --net --mount-proc cap_drop=all /bin/bash
# Test network operations
ping 8.8.8.8  # Should fail
```

2. Create seccomp profile:

```bash
# Create basic seccomp profile
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {"names": ["read", "write"], "action": "SCMP_ACT_ALLOW"}
  ]
}
```

#### Module 2: Container Image Creation

Theory:

- Layer architecture
- Image manifests
- Distribution formats

Practical Projects:

1. Create layered filesystem:

```bash
# Create base layer
mkdir base-layer
# Add application layer
mkdir app-layer
# Create overlay mount
mount -t overlay overlay -o lowerdir=app-layer:base-layer /merged
```

### Level 4: Integration Projects

1. Basic Container Runtime:

- Combine namespace isolation
- Implement cgroup controls
- Add basic networking

2. Container Image Builder:

- Create OCI-compatible images
- Implement layer management
- Add metadata handling

### Success Criteria

For each level, you should be able to:

1. Explain the purpose of each isolation mechanism
2. Create containers using command-line tools
3. Debug common container issues
4. Understand security implications

### Troubleshooting Guide

Common issues and solutions:

1. Permission denied:

   - Check capability requirements
   - Verify user permissions
   - Check SELinux/AppArmor contexts

2. Network connectivity:

   - Verify namespace configuration
   - Check routing tables
   - Validate interface status

3. Resource limits:
   - Verify cgroup settings
   - Check resource availability
   - Monitor usage patterns

### Additional Resources

1. Linux Kernel Documentation:

   - Namespaces
   - Cgroups
   - Capabilities

2. OCI Specifications:

   - Runtime Specification
   - Image Specification
   - Distribution Specification

3. Related Tools:
   - runc
   - containerd
   - buildah

### Next Steps

After completing this curriculum:

1. Study container orchestration
2. Learn Docker and Podman
3. Explore Kubernetes concepts
4. Practice container security

## Kubernetes Mastery Levels

### Level 1: Foundation Builder

Focus: Basic Kubernetes concepts and simple deployments

Skills:

- Create and manage basic Pods, Deployments, and Services
- Use kubectl for basic operations
- Understand basic Kubernetes architecture
- Navigate the cluster using kubectl commands
- Create simple YAML manifests

Success Indicators:

- Can deploy a basic application with proper labels
- Understands pod lifecycle
- Can troubleshoot simple pod issues
- Knows how to scale deployments
- Can create ClusterIP and NodePort services

Practice Projects:

1. Deploy a stateless web application
2. Create a multi-pod application with services
3. Implement basic health checks
4. Practice rolling updates

### Level 2: Service Architect

Focus: Application management and service networking

Skills:

- Design effective service architectures
- Implement Ingress controllers
- Configure persistent storage
- Manage ConfigMaps and Secrets
- Understand pod-to-pod communication

Success Indicators:

- Can design proper label schemas
- Implements effective service discovery
- Manages application configurations properly
- Understands network policies
- Can troubleshoot service connectivity issues

Practice Projects:

1. Deploy a database with persistent storage
2. Implement an Ingress controller
3. Create a complete microservices application
4. Configure mutual TLS between services

### Level 3: Platform Engineer

Focus: Cluster operations and advanced workloads

Skills:

- Manage node pools and cluster scaling
- Implement resource quotas and limits
- Configure cluster autoscaling
- Understand StatefulSets and DaemonSets
- Master custom resource definitions (CRDs)

Success Indicators:

- Can design for high availability
- Implements proper resource management
- Understands cluster networking deeply
- Can troubleshoot node issues
- Manages complex stateful applications

Practice Projects:

1. Deploy a distributed database cluster
2. Implement custom controllers
3. Create cluster monitoring solution
4. Design disaster recovery procedures

### Level 4: Security Specialist

Focus: Security and compliance

Skills:

- Implement RBAC effectively
- Configure network policies
- Manage pod security policies
- Implement security contexts
- Understand service accounts and authentication

Success Indicators:

- Creates least-privilege RBAC policies
- Implements effective network isolation
- Understands security best practices
- Can audit cluster security
- Manages secrets effectively

Practice Projects:

1. Implement zero-trust networking
2. Create custom admission controllers
3. Set up vulnerability scanning
4. Design security monitoring

### Level 5: System Architect

Focus: Multi-cluster and cloud-native architecture

Skills:

- Design multi-cluster solutions
- Implement service mesh architectures
- Manage cluster federation
- Understand GitOps principles
- Master cloud-native patterns

Success Indicators:

- Designs scalable architectures
- Implements effective multi-cluster strategies
- Understands cloud-native best practices
- Can troubleshoot complex distributed systems
- Manages large-scale deployments

Practice Projects:

1. Implement multi-cluster service mesh
2. Create GitOps pipelines
3. Design global load balancing
4. Build custom cloud-native solutions

### Level 6: Enterprise Architect

Focus: Enterprise-scale operations and optimization

Skills:

- Design for multi-tenancy
- Implement cost optimization
- Manage compliance at scale
- Design for disaster recovery
- Understand cloud provider integrations

Success Indicators:

- Creates effective multi-tenant solutions
- Implements cost-effective architectures
- Manages enterprise compliance
- Designs reliable backup strategies
- Understands cloud-specific optimizations

Practice Projects:

1. Design multi-tenant platform
2. Implement cost allocation system
3. Create compliance automation
4. Build enterprise monitoring solution

### Validation Methods for Each Level

#### Technical Assessment

- Practical implementation tasks
- Troubleshooting scenarios
- Architecture design reviews
- Security audits
- Performance optimization challenges

#### Documentation Skills

- Architecture documentation
- Runbooks creation
- Disaster recovery plans
- Security policies
- Standard operating procedures

#### Operational Knowledge

- Incident response handling
- Performance troubleshooting
- Security incident management
- Capacity planning
- Cost optimization

### Learning Resources

#### Official Documentation

- Kubernetes documentation
- Cloud provider guides
- CNCF project documentation
- Security best practices
- Architecture patterns

#### Hands-on Practice

- Local development clusters
- Cloud provider sandboxes
- CI/CD pipelines
- Security testing environments
- Performance testing environments

#### Community Engagement

- Kubernetes community meetings
- Special Interest Groups (SIGs)
- Local meetups
- Online forums
- Open source contributions

### Progress Tracking

#### For Each Level

1. Complete all practice projects
2. Pass technical assessments
3. Create required documentation
4. Demonstrate operational knowledge
5. Contribute to community projects

#### Advancement Criteria

- Consistent successful implementation
- Effective problem-solving
- Clear communication of concepts
- Meaningful contributions to teams
- Demonstrated leadership in area

I've created a comprehensive mastery framework that spans from beginner to enterprise architect level. Each level includes:

1. Clear focus areas
2. Required skills
3. Success indicators
4. Practical projects
5. Validation methods

This framework aligns with industry roles and responsibilities while maintaining a clear progression path. You can use it to:

1. Assess your current level
2. Plan your learning journey
3. Track your progress
4. Identify skill gaps
5. Focus your practice efforts

Would you like to assess your current level or focus on a specific area? I can help you create a targeted learning plan based on where you are and where you want to go.

I'll create a mastery framework specifically for container skills, starting from basic Linux primitives through to advanced containerization practices.

## Container Technology Mastery Levels

### Level 1: Container Fundamentals

Focus: Understanding container primitives and basic isolation

Skills:

- Work with Linux namespaces (pid, net, mnt, user)
- Understand and configure cgroups
- Create basic chroot environments
- Use basic networking tools
- Understand process isolation

Success Indicators:

- Can create isolated processes using namespaces
- Successfully limits resources using cgroups
- Understands container filesystem basics
- Can troubleshoot basic isolation issues
- Creates basic network spaces

Practice Projects:

1. Build a basic container using namespaces
2. Create resource-limited environments with cgroups
3. Set up isolated network spaces
4. Create isolated filesystem environments

### Level 2: Container Implementation

Focus: Building and running containers

Skills:

- Write Dockerfiles efficiently
- Understand layer optimization
- Implement multi-stage builds
- Handle container security
- Manage container networking

Success Indicators:

- Creates efficient container images
- Implements proper layer caching
- Understands build context
- Manages container volumes effectively
- Configures container networking properly

Practice Projects:

1. Create optimized multi-stage builds
2. Implement proper security scanning
3. Set up container networks
4. Build custom base images

### Level 3: Container Operations

Focus: Running containers in production

Skills:

- Implement container orchestration
- Manage container lifecycle
- Handle logging and monitoring
- Configure container security
- Implement CI/CD for containers

Success Indicators:

- Manages container deployments effectively
- Implements proper monitoring
- Handles container logging
- Understands security best practices
- Creates efficient CI/CD pipelines

Practice Projects:

1. Set up container orchestration
2. Implement monitoring solution
3. Create automated build pipelines
4. Design security policies

### Level 4: Advanced Networking

Focus: Complex container networking

Skills:

- Implement overlay networks
- Configure service discovery
- Manage container DNS
- Handle network security
- Implement load balancing

Success Indicators:

- Creates effective network architectures
- Implements service discovery solutions
- Manages container DNS effectively
- Configures network security
- Understands network troubleshooting

Practice Projects:

1. Build overlay network
2. Implement service mesh
3. Create custom CNI plugin
4. Design network security policy

### Level 5: Platform Engineering

Focus: Building container platforms

Skills:

- Design container platforms
- Implement multi-tenancy
- Manage container registries
- Handle platform security
- Implement automation

Success Indicators:

- Creates scalable platforms
- Manages multi-tenant environments
- Implements registry security
- Automates platform operations
- Understands platform architecture

Practice Projects:

1. Build private container registry
2. Create automated platform
3. Implement multi-tenant isolation
4. Design platform security

### Practical Skills Matrix

#### Basic Container Operations

- Container creation
- Image building
- Basic networking
- Volume management
- Resource limits

#### Advanced Container Management

- Custom network creation
- Security implementation
- Performance optimization
- Debugging and troubleshooting
- Registry management

#### Container Platform Development

- Platform automation
- Multi-tenancy
- Security frameworks
- Monitoring solutions
- CI/CD integration

### Validation Methods

#### Technical Assessment

1. Implementation Projects:

   - Build containers from scratch
   - Create optimized images
   - Set up networking
   - Implement security

2. Troubleshooting Scenarios:
   - Network issues
   - Performance problems
   - Security incidents
   - Build failures

#### Documentation Skills

1. Required Documentation:

   - Architecture diagrams
   - Network layouts
   - Security policies
   - Operational procedures

2. Knowledge Sharing:
   - Technical writing
   - Architecture reviews
   - Peer training
   - Process documentation

### Learning Resources

#### Hands-on Labs

1. Local Environment:

   - Linux VM setup
   - Container runtime installation
   - Network configuration
   - Storage setup

2. Cloud Practice:
   - Cloud container services
   - Registry services
   - Networking services
   - Security services

#### Technical Documentation

1. Official Resources:

   - OCI specifications
   - Runtime documentation
   - Security guidelines
   - Best practices

2. Community Resources:
   - Blog posts
   - Conference talks
   - Discussion forums
   - Open source projects

### Progress Tracking

#### For Each Level

1. Complete required projects
2. Pass technical assessments
3. Create documentation
4. Demonstrate troubleshooting
5. Contribute to community

#### Advancement Requirements

1. Technical Proficiency:

   - Successfully complete projects
   - Pass technical assessments
   - Demonstrate debugging skills

2. Operational Knowledge:

   - Handle production issues
   - Manage deployments
   - Implement security

3. Architecture Understanding:
   - Design solutions
   - Review architectures
   - Optimize implementations

### Next Steps After Mastery

1. Container orchestration (Kubernetes)
2. Cloud-native architectures
3. Platform engineering
4. DevOps practices
5. Site Reliability Engineering

I've created a comprehensive mastery framework that covers everything from basic container primitives to advanced platform engineering. The framework is designed to:

1. Build skills incrementally from fundamentals
2. Focus on practical, hands-on experience
3. Include real-world validation methods
4. Cover both technical and operational aspects
5. Provide clear progression paths

Each level builds on the previous one, ensuring a solid foundation before moving to more complex topics. Would you like to:

1. Assess your current level?
2. Start with fundamentals exercises?
3. Focus on a specific skill area?
4. Get started with practical projects?

Let me know what interests you most, and I can help you create a focused learning plan.

I'll help you create a visual understanding of container networking by showing you commands and tools to inspect and visualize the network state. Here's how you can "see" what's happening:

## Visualizing Container Networks: Inspection Tools and Techniques

### Basic Network Namespace Inspection

#### 1. List Network Namespaces

```bash
# List all network namespaces
ip netns list

# Show detailed namespace info
ip netns identify <pid>
```

#### 2. Visualize Network Interfaces

```bash
# Show all interfaces on host
ip link show

# Show interfaces in specific namespace
ip netns exec container_ns ip link show

# Show connections between veth pairs
ethtool -S veth0  # Shows peer_ifindex
```

#### 3. Real-time Network Monitoring

```bash
# Watch network traffic in real-time (host)
watch -n1 'ip -s link show veth0'

# Watch network traffic in container namespace
ip netns exec container_ns watch -n1 'ip -s link show veth1'
```

### Visual Network Inspection Tools

#### 1. Network Layout with 'bridge'

```bash
# Install bridge-utils
apt-get install bridge-utils

# Show bridge connections
brctl show

# Show bridge details
brctl showmacs br0  # if using bridge
```

#### 2. Visual Traffic Analysis with Tcpdump

```bash
# Watch traffic on host interface
tcpdump -i veth0

# Watch traffic in container namespace
ip netns exec container_ns tcpdump -i veth1

# Save traffic for visual analysis
tcpdump -i veth0 -w capture.pcap
# Open with Wireshark for visual analysis
```

#### 3. Connection Tracking

```bash
# Show active connections
conntrack -L

# Watch connections in real-time
watch -n1 'conntrack -L'
```

### Network State Visualization

#### 1. Routing Table Inspection

```bash
# Host routing
ip route show

# Container routing
ip netns exec container_ns ip route show

# Watch routing changes
watch -n1 'ip route show'
```

#### 2. Address Resolution (ARP) Table

```bash
# Host ARP table
ip neigh show

# Container ARP table
ip netns exec container_ns ip neigh show

# Watch ARP changes
watch -n1 'ip neigh show'
```

### Network Testing Tools

#### 1. Connection Testing

```bash
# Test network connection from host
ping -c 3 172.16.0.2

# Test from container namespace
ip netns exec container_ns ping -c 3 172.16.0.1

# Trace route path
ip netns exec container_ns traceroute 172.16.0.1
```

#### 2. Port and Service Testing

```bash
# Check listening ports in container
ip netns exec container_ns netstat -tulpn

# Scan ports from host
nc -zv 172.16.0.2 8000

# Monitor open connections
ip netns exec container_ns ss -tan
```

### Advanced Visualization Techniques

#### 1. Network Graphing

```bash
# Install graphviz
apt-get install graphviz

# Create network graph (example script)
#!/bin/bash
echo "digraph network {" > net.dot
echo "  rankdir=LR;" >> net.dot
ip link | grep -E '^[0-9]+' | while read line; do
    dev=$(echo $line | awk -F: '{print $2}')
    echo "  \"$dev\";" >> net.dot
done
echo "}" >> net.dot
dot -Tpng net.dot > network.png
```

#### 2. Real-time Bandwidth Monitoring

```bash
# Install iftop
apt-get install iftop

# Monitor container interface
ip netns exec container_ns iftop -i veth1

# Monitor host interface
iftop -i veth0
```

### Debugging Common Network Issues

#### 1. Interface Problems

```bash
# Check interface state
ip link show veth0
ip netns exec container_ns ip link show veth1

# Verify interface is up
ip link set veth0 up
ip netns exec container_ns ip link set veth1 up
```

#### 2. Routing Issues

```bash
# Check routes on both sides
ip route get 172.16.0.2
ip netns exec container_ns ip route get 172.16.0.1

# Verify routing table
ip route show table all
ip netns exec container_ns ip route show table all
```

#### 3. DNS Resolution

```bash
# Test DNS resolution
ip netns exec container_ns dig google.com

# Check DNS configuration
ip netns exec container_ns cat /etc/resolv.conf
```

### Network Monitoring Best Practices

1. Regular State Checks:

   - Monitor interface status
   - Check routing tables
   - Verify ARP tables
   - Monitor active connections

2. Traffic Analysis:

   - Use tcpdump for packet inspection
   - Monitor bandwidth usage
   - Track connection states
   - Analyze traffic patterns

3. Performance Monitoring:

   - Track interface statistics
   - Monitor error counters
   - Check dropped packets
   - Measure latency

4. Documentation:
   - Map network topology
   - Document interface connections
   - Track routing changes
   - Log debugging steps

Let me give you some specific examples of how to use these tools in your container project:

1. Before Creating Network Namespace:

```bash
# Check current network namespaces
ip netns list
# Should show none or existing namespaces
```

2. After Creating Network Namespace:

```bash
# List namespaces again
ip netns list
# Should show your new container_ns

# Look inside the namespace
ip netns exec container_ns ip link list
# Initially only shows loopback interface
```

3. After Creating veth Pair:

```bash
# On host - show all interfaces
ip link show
# You'll see both veth0 and veth1

# Show connection between interfaces
ethtool -S veth0
# Shows peer_ifindex which links to veth1
```

4. Monitor Traffic in Real-time:

```bash
# Open two terminals

# Terminal 1 - Watch container interface
ip netns exec container_ns watch -n1 'ip -s link show veth1'

# Terminal 2 - Generate some traffic
ping 172.16.0.2
```

Would you like to try these visualization techniques with your container setup? We can start with any step, and I can help you understand what you're seeing.

These tools will help make the "invisible" network connections more visible and understandable. Let me know which aspect you'd like to explore first!

Not all of these commands will work directly in a Kubernetes pod, since pods have more restricted capabilities than raw Linux containers. Let me explain what you can and cannot do, and provide alternative ways to inspect networking in Kubernetes:

Commands that WILL work in most K8s pods:

```bash
ip addr show             # Show IP addresses
ip route show            # Show routing table
netstat -tulpn          # Show listening ports
ss -tan                 # Show connections
ping                    # If ping is installed
traceroute              # If traceroute is installed
cat /etc/resolv.conf    # Check DNS config
```

Commands that WON'T work in standard K8s pods:

```bash
ip netns                # No access to namespaces
ip link set             # No interface modification
tcpdump                 # Requires privileges
brctl                   # No bridge control
iptables               # No firewall access
```

Instead, for Kubernetes networking inspection, you should use:

1. kubectl commands from your workstation:

```bash
# Get pod networking info
kubectl describe pod <pod-name>

# Get service info
kubectl describe service <service-name>

# Check pod connectivity
kubectl exec <pod-name> -- ping <ip-address>

# View pod logs
kubectl logs <pod-name>
```

2. Network debugging pods:

```bash
# Deploy a network debugging pod
kubectl run netshoot --rm -i --tty \
    --image nicolaka/netshoot \
    -- /bin/bash

# Or use a privileged debugging pod
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: network-debug
spec:
  hostNetwork: true
  containers:
  - name: network-debug
    image: nicolaka/netshoot
    securityContext:
      privileged: true
EOF
```

3. CNI plugin tools:

```bash
# For Calico
calicoctl get workloadendpoint
calicoctl get ippool

# For Cilium
cilium endpoint list
cilium service list
```

Would you like me to show you how to set up a debugging pod to inspect your Kubernetes networking? Or would you prefer to learn about specific kubectl commands for network troubleshooting?

Based on the material you've provided, we have a wealth of knowledge at our fingertips. This includes deep dives into:

- Linux Namespaces: How they provide isolation for containers. We have articles explaining user, mount, UTS, PID and net namespaces as well as the general concept.
- Containerization Fundamentals: Practical guides to building containers by hand using namespaces, including details on file system isolation, and network isolation, and how to combine these for powerful isolation.
- Container Runtimes: Information on Docker, Podman, and related technologies like CRI-O and containerd.
- Networking: How BPF can extend our visibility into systems and applications, and how it plays a key role in the rise of distributed cloud computing. There is also guidance on the components that make up a Docker network, and how you can set them up for yourself.
- Kubernetes: How containers are used by Kubernetes, and how it has become the dominant container orchestrator.
- Ultralearning Principles: A guide to accelerating learning by focusing on metalearning, directness, drilling, retrieval, feedback, retention, intuition, and experimentation.
- Security: We have information on the security implications of containers, including how to use user namespaces, SELinux, and Linux capabilities.
- Troubleshooting: Guidance on identifying common problems and how to work through them.
- Practical Implementation: Details for setting up network namespaces by hand and the kind of command line instructions you might use, so that you can understand what is happening under the hood.

Here's a practical curriculum drawing from all of this, structured using the *Ultralearning* principles, to guide you:

Overall Goal: To build a deep, intuitive understanding of Linux containers, starting from the most basic concepts, and progressing to the point where you understand how Kubernetes uses these concepts.

Phase 1: Metalearning (Mapping Your Learning)

- Why are you learning? Your primary motivation is to understand containerisation as a foundation for learning Kubernetes [your query]. You also want to overcome the illusion of explanatory depth and understand the underlying technologies [your query]. This means we need to focus on *understanding* not just rote memorisation. We will aim to understand the "why" behind everything.
- What are you learning? We are going to break down the technology into three main pillars: Linux Namespaces, Cgroups and Networking primitives. These are our main concepts to master.
- How will you learn? We'll combine theory with hands-on exercises, practical projects, and documentation. We will actively try and apply what we learn, and practice our troubleshooting skills. We will also use the Feynman technique, by teaching concepts back to me and yourself.

Phase 2: Building a Container from Scratch: Hands-On

Principle 2: Focus: Sharpen Your Knife

- Eliminate distractions. Set aside dedicated time for learning.
- Break down large tasks into small, manageable steps.

Principle 3: Directness: Go Straight Ahead

- Learn by doing, not just reading. You need to build a container by hand.
  - Module 1: Process Isolation with Namespaces
    - Theory: Start with the core idea of namespaces. Understand what namespaces are, and the different types (PID, network, mount, UTS, user). The most important thing is to understand *why* they are necessary.
    - Practical Exercise 1: Create a basic isolated process with `unshare`. Observe how a new process id is created when you use unshare. What happens when you run `lsns` both inside and outside the namespace?.
    - Practical Exercise 2: Create a user namespace and map a range of users. Explore what happens if you map the entire range, and try becoming the apache user.
    - Practical Exercise 3: Experiment with UTS namespace. Create a new namespace and try changing the hostname.
    - Documentation: For each exercise, you should write a `README.md` explaining what you're building, why each step is necessary, what you learned, and what failed and why. You should also maintain a `commands.sh` with all the commands you used.
  - Module 2: Resource Control with Cgroups
    - Theory: Learn about cgroups and how they allow you to limit resources like CPU and memory. *Why* is this an important component in containerisation?
    - Practical Exercise 1: Create and manage cgroups. Limit the CPU and memory available to a process in a namespace. How would you manage I/O?
    - Practical Exercise 2: Monitor the resource usage of your cgroup. How would you do this in a production system?
  - Module 3: File System Isolation
    - Theory: Explore the concepts of a root filesystem, mount namespaces, and overlay filesystems. What problem are these features solving?
    - Practical Exercise 1: Create a minimal container root filesystem. What do you need to include? How would you add the proc filesystem?
    - Practical Exercise 2: Use the mount namespace to create a chroot-like environment.
  - Module 4: Network Isolation
    - Theory: Understand network namespaces, virtual interfaces (veth pairs), and container networking models. Why do you need a virtual ethernet pair to connect namespaces?
    - Practical Exercise 1: Create two network namespaces and connect them using veth pairs. Can you ping between them?.
    - Practical Exercise 2: Use a bridge to connect multiple namespaces.

Principle 4: Drill: Attack Your Weakest Point

- Identify areas where you struggle and focus your practice there.
- Don't move on to the next module until you deeply understand the current one.
- Use prerequisite chaining - if you encounter a problem, go back and learn the foundational element that you are missing.

Phase 3: Advanced Containerization and Networking

Principle 5: Retrieval: Test to Learn

- Regularly test your understanding through self-generated challenges.
- Use active recall - try to remember information without looking at notes.
- Try closed-book exercises - where you build the whole system without instructions or notes.
  - Module 5: Security and Capabilities
    - Theory: Delve into Linux capabilities, seccomp profiles, and SELinux/AppArmor basics. *Why* is it important to understand the power of root?.
    - Practical Exercise 1: Drop capabilities from a containerised process. Why do you need these capabilities?
    - Practical Exercise 2: Create a seccomp profile. How does this improve security?
  - Module 6: Container Image Creation
    - Theory: Learn about container image layer architecture, image manifests, and distribution formats.
    - Practical Exercise 1: Create a layered filesystem.
    - Practical Exercise 2: Create an OCI compatible image.
  - Module 7: Network Namespaces in Kubernetes
    - Theory: Study how network namespaces are used by Kubernetes and how CNI plugins are used.
    - Practical Exercise: Inspect network namespaces in Kubernetes using tools like `kubectl` and `nsenter`.
    - Practical Exercise: Implement Kubernetes network policies to see how isolation works in a cluster.

Principle 6: Feedback: Don’t Dodge the Punches

- Actively seek feedback on your progress by asking questions of me, and also try to teach these concepts to others.
- Use that feedback to correct your understanding.

Phase 4: Integration Projects & Kubernetes

Principle 7: Retention: Don’t Fill a Leaky Bucket

- Use spaced repetition to review previously learned concepts.
- Turn factual knowledge into procedures. Practice what you've learned.
  - Project 1: Basic Container Runtime
    - Combine all previous modules to create a simple container runtime.
  - Project 2: Container Image Builder
    - Build OCI-compatible images with layer management.
  - Project 3: Kubernetes Networking
    - Deep dive into Kubernetes networking concepts. Study the Kubernetes networking model.
    - Learn about CNI plugins and how they are used.
    - Understand how pods get IP addresses.
  - Project 4: Calico Network Policies
    - Implement Calico policies. Build a default deny policy.

Principle 8: Intuition: Dig Deep Before Building Up

- Ensure a deep understanding of the concepts before moving forward.
- Use the Feynman Technique to ensure you understand what you are learning.

Principle 9: Experimentation: Explore Outside Your Comfort Zone

- Try different tools, methods and approaches.

Phase 5: Long-Term Learning

- Explore other container technologies like Docker and Podman.
- Study container orchestration technologies like Kubernetes.
- Investigate BPF and it's role in observing containers.

Practical Considerations

- Environment: You'll need a Linux environment (virtual machine or physical machine) to perform these exercises. Let me know what you have available, and I can tailor my instructions.
- Troubleshooting: You need to develop your troubleshooting skills. Each exercise should be an opportunity to learn from mistakes.
- Documentation: You need to keep meticulous notes of everything that you are doing. Use the README.md files to explain your thinking, `commands.sh` to track what you did, and a `troubleshooting.md` for problems that you encounter.

This curriculum is designed to help you build a deep and practical understanding of Linux containers and create a solid foundation for learning Kubernetes. It will also help you overcome the illusion of explanatory depth by forcing you to build your knowledge from first principles.

What do you think? Are you ready to start with the first module on process isolation with namespaces? We can walk through the exercises together, or I can help clarify any concepts that aren't clear.

The networking aspect of Kubernetes, especially in AWS, is fascinating and complex. Let's create a bottom-up learning curriculum for networking, starting from basic Linux networking concepts up to AWS-specific implementations.

## Level 1: Linux Networking Fundamentals

- Network Namespaces & Container Networking Basics
  - Hands-on Project: Create network namespaces using `ip netns` and connect them
  - Practice connecting namespaces with virtual ethernet pairs (veth)
  - Build a simple network bridge to understand container networking
  - Create your own mini-container network to deeply understand what Kubernetes does under the hood

[[linux networking namespaces]]

## Level 2: Container Networking Interface (CNI)

- Understanding CNI Specification
  - Project: Write a basic CNI plugin in a language of your choice
  - Experiment with different CNI plugins (Calico, Flannel, Weave)
  - Deep dive into how pods get IP addresses
  - Understand the role of kubelet in networking

## Level 3: Kubernetes Networking Model

- Pod-to-Pod Communication
  - Set up a multi-node cluster locally using tools like kind or minikube
  - Trace packet flows between pods on same/different nodes
  - Configure network policies to control traffic flow
  - Deep dive into kube-proxy and service implementation

## Level 4: AWS-specific Networking

- VPC and Subnet Design for EKS
  - Project: Design and implement a production-grade VPC for EKS
  - Understand AWS CNI implementation differences
  - Work with security groups and NACLs in EKS context
  - Implementation of AWS Load Balancers with Services

Let's start with a concrete first project for Level 1 to get your hands dirty with network namespaces:

```sh
#!/bin/bash

# This script creates and connects two network namespaces

# to demonstrate basic container networking concepts

# Create two network namespaces

sudo ip netns add ns1
sudo ip netns add ns2

# Create a virtual ethernet pair

sudo ip link add veth1 type veth peer name veth2

# Connect each end of the pair to a namespace

sudo ip link set veth1 netns ns1
sudo ip link set veth2 netns ns2

# Configure IP addresses

sudo ip netns exec ns1 ip addr add 10.0.0.1/24 dev veth1
sudo ip netns exec ns2 ip addr add 10.0.0.2/24 dev veth2

# Bring up the interfaces

sudo ip netns exec ns1 ip link set veth1 up
sudo ip netns exec ns2 ip link set veth2 up
sudo ip netns exec ns1 ip link set lo up
sudo ip netns exec ns2 ip link set lo up

# Test connectivity

echo "Testing ping from ns1 to ns2:"
sudo ip netns exec ns1 ping -c 3 10.0.0.2

# Show network interfaces in each namespace

echo -e "\nInterfaces in ns1:"
sudo ip netns exec ns1 ip addr show

echo -e "\nInterfaces in ns2:"
sudo ip netns exec ns2 ip addr show

# Cleanup function

cleanup() {
echo "Cleaning up network namespaces..."
sudo ip netns delete ns1
sudo ip netns delete ns2
}

# Register cleanup function to run on script exit

sudo trap cleanup EXIT
```

[[script output]]

This script creates a foundational setup that mimics how container networking works. After running this, try these exercises:

1. Modify the script to add a third namespace
2. Create a bridge network and connect all namespaces to it
3. Implement basic network policies using iptables within the namespaces
4. Monitor traffic between namespaces using tcpdump

Understanding this level helps you grasp how Kubernetes networking works under the hood. For example, when Kubernetes creates a pod, it essentially:

1. Creates a network namespace
2. Sets up interfaces within that namespace
3. Configures routing and NAT rules
4. Implements network policies

Would you like to dive deeper into any of these concepts? We could explore how to add a bridge network next, or move on to implementing a basic CNI plugin to understand how Kubernetes automates this process.

I'd also be curious to hear about any specific networking challenges you've encountered in your AWS EKS environment that we could incorporate into the learning plan.

This is a common scenario - moving from an open cluster to zero trust requires careful planning and incremental implementation. Let's create a systematic approach to implementing network policies:

1. First Step: Traffic Analysis & Mapping

- Before implementing any restrictions, we need to understand existing communication patterns:

```sh
#!/bin/bash

# This script helps analyze pod-to-pod communication patterns

# Get all namespaces excluding kube-system

NAMESPACES=$(kubectl get namespaces --no-headers -o custom-columns=":metadata.name" | grep -v "kube-system")

echo "Analyzing pod communication patterns..."

for ns in $NAMESPACES; do
echo "Namespace: $ns"

    # Get all pods in namespace
    PODS=$(kubectl get pods -n $ns --no-headers -o custom-columns=":metadata.name")

    for pod in $PODS; do
        echo "  Pod: $pod"

        # Get container names in pod
        CONTAINERS=$(kubectl get pod $pod -n $ns -o jsonpath='{.spec.containers[].name}')

        for container in $CONTAINERS; do
            echo "    Container: $container"

            # Capture network connections for 60 seconds
            echo "    Active connections:"
            kubectl exec -n $ns $pod -c $container -- timeout 60 netstat -tnp 2>/dev/null | \
                grep ESTABLISHED | \
                awk '{print $5}' | \
                sort | uniq -c | \
                sort -nr
        done
    done

done
```

2. Implement Observability First

- Before adding any restrictions, deploy a CNI that supports network policies (if not already using one):
  - Calico is recommended for AWS EKS
  - It provides good monitoring and policy enforcement
- Enable flow logs and monitoring to understand traffic patterns
- Consider implementing tools like:
  - Cilium for network flow visibility
  - Calico's Flow Logs
  - AWS VPC Flow Logs for external traffic

3. Start with Permissive Logging Policies
   Create "audit-only" network policies first that don't block traffic but log violations:

```yaml
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
name: default-deny-audit
namespace: your-namespace
spec:
podSelector: {}
policyTypes:

- Ingress
- Egress
  ingress:
- from:
  - namespaceSelector:
    matchLabels:
    kubernetes.io/metadata.name: kube-system
    egress:
- to:
  - namespaceSelector:
    matchLabels:
    kubernetes.io/metadata.name: kube-system
    ports:
  - port: 53
    protocol: UDP
  - port: 53
    protocol: TCP
- to:
  - namespaceSelector: {}
    podSelector: {}

---

# Example allowance policy for specific service

apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
name: allow-frontend-to-backend
namespace: your-namespace
spec:
podSelector:
matchLabels:
app: backend
policyTypes:

- Ingress
  ingress:
- from:
  - podSelector:
    matchLabels:
    app: frontend
    ports:
  - protocol: TCP
    port: 8080
```

4. Incremental Implementation Strategy

- Start with one non-critical namespace
- Create a process for rolling out policies:
  1. Monitor normal traffic for 1-2 weeks
  2. Create permissive policies based on observed patterns
  3. Run in audit mode for 1 week
  4. Gradually tighten policies
  5. Move to enforcement mode during a maintenance window
5. Example Implementation Timeline:

Week 1-2: Monitor traffic patterns

Week 3: Deploy audit policies in one namespace

Week 4: Analyze audit logs and refine policies

Week 5: Enable enforcement in test namespace

Week 6-8: Gradually roll out to other namespaces

Would you like me to help you create:

1. A specific monitoring plan for your cluster to identify communication patterns?
2. Or shall we draft some initial audit-mode network policies for a specific namespace?

The key is to avoid breaking applications while gradually moving towards zero trust. We can start with a single service or namespace that you're most familiar with.

I'll expand our networking curriculum to include a deep focus on Calico. Here's a structured learning path specifically for mastering Calico in the context of our zero-trust journey:

Level 1: Calico Architecture & Basics

- Core Components Understanding
  - Felix (node agent)
  - BIRD (BGP client)
  - CNI plugin
  - etcd or Kubernetes datastore
- Hands-on Project: Set up a local cluster with Calico using kind or minikube
- Practice task: Monitor Felix and BIRD processes, understand their logs

Level 2: Calico Policy Implementation

- Basic Policy Grammar
  - Understand label-based selectors
  - Policy ordering and precedence
  - Rule types and actions
- Practice Exercise: Create policies that:
  1. Deny all traffic (default deny)
  2. Allow DNS
  3. Allow monitoring tools
  4. Create app-specific rules

Level 3: Advanced Calico Features

- BGP Configuration
  - Understand BGP peering
  - Route reflectors
  - External BGP peers
- IPAM Management
  - IP Pool configuration
  - Block affinity
- Enterprise Features
  - Wireguard encryption
  - Flow logs
  - Compliance reporting

Let's start with a concrete first project to understand Calico policies:

## Lab 1: Understanding Calico Policy Basics

## Step 1: Create Test Namespaces and Applications

apiVersion: v1

kind: Namespace

metadata:

name: policy-test

---

## Create Test Pods

apiVersion: v1

kind: Pod

metadata:

name: nginx-1

namespace: policy-test

labels:

app: web

spec:

containers:

- name: nginx
  image: nginx:1.14.2
  ports:
  - containerPort: 80

---

apiVersion: v1

kind: Pod

metadata:

name: client

namespace: policy-test

labels:

app: client

spec:

containers:

- name: alpine
  image: alpine
  command:

---

## Step 2: Default Deny Policy

apiVersion: projectcalico.org/v3

kind: NetworkPolicy

metadata:

name: default-deny

namespace: policy-test

spec:

selector: all()

types:

- Ingress
- Egress

---

## Step 3: Allow DNS Policy

apiVersion: projectcalico.org/v3

kind: NetworkPolicy

metadata:

name: allow-dns

namespace: policy-test

spec:

selector: all()

types:

- Egress
  egress:
- action: Allow
  protocol: UDP
  destination:
  selector: k8s-app == "kube-dns"
  ports:
  - 53

---

## Step 4: Allow Specific Web Traffic

apiVersion: projectcalico.org/v3

kind: NetworkPolicy

metadata:

name: allow-web

namespace: policy-test

spec:

selector: app == 'web'

types:

- Ingress
  ingress:
- action: Allow
  protocol: TCP
  destination:
  ports:
  - 80
    source:
    selector: app == 'client'

## Validation Steps (run These commands)

## 1. Verify Initial Connectivity

Kubectl -n Policy-test Exec Client -- Wget -q -O- --timeout=5 Nginx-1

## 2. Apply Default Deny and Verify Isolation

Kubectl Apply -f default-deny.yaml

Kubectl -n Policy-test Exec Client -- Wget -q -O- --timeout=5 Nginx-1 # Should Fail

## 3. Apply DNS and Web Policies

Kubectl Apply -f allow-dns.yaml

Kubectl Apply -f allow-web.yaml

## 4. Verify Restored Connectivity

Kubectl -n Policy-test Exec Client -- Wget -q -O- --timeout=5 Nginx-1 # Should Succeed

Level 4: Advanced Implementation & Troubleshooting

- Policy Troubleshooting
  - Using calicoctl to debug policies
  - Understanding policy logs
  - Packet tracing
- Integration with AWS EKS
  - VPC CNI integration
  - Security group policy
  - Multi-cluster networking

Practice Project: Zero Trust Implementation

1. Create an isolated dev environment
2. Map application dependencies
3. Implement and test staged policies:
   - Global default-deny
   - Allow system-level communication
   - Application-specific policies
4. Monitor and refine using:
   - Calico flow logs
   - Policy audit logs
   - Compliance reports

Would you like to:

1. Start with the basic policy lab above to understand fundamentals?
2. Jump into mapping your application's communication patterns?
3. Focus on a specific advanced Calico feature?

Each level builds on the previous one, and we can adjust the pace based on your comfort level with each concept. The key is to practice each component hands-on in a safe environment before implementing in production.

Let's work through the Calico policy lab step by step. First, we'll set up a test environment and then gradually implement and understand each policy component.

1. First, let's create our test namespace and applications:

```bash
# Create the namespace
kubectl create namespace policy-test

# Deploy test pods
kubectl apply -f - <<EOF
apiVersion: v1
kind: Pod
metadata:
  name: nginx-1
  namespace: policy-test
  labels:
    app: web
spec:
  containers:
  - name: nginx
    image: nginx:1.14.2
    ports:
    - containerPort: 80
---
apiVersion: v1
kind: Pod
metadata:
  name: client
  namespace: policy-test
  labels:
    app: client
spec:
  containers:
  - name: alpine
    image: alpine
    command:
EOF
```

2. Verify initial connectivity (this should work as there are no restrictions yet):

```bash
kubectl -n policy-test wait --for=condition=Ready pod/nginx-1 pod/client
kubectl -n policy-test exec client -- wget -q -O- --timeout=5 nginx-1
```

3. Now, let's implement the default deny policy. This is crucial to understand as it's the foundation of zero trust:

```bash
kubectl apply -f - <<EOF
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: default-deny
  namespace: policy-test
spec:
  selector: all()
  types:
  - Ingress
  - Egress
EOF
```

4. Test connectivity again (this should fail):

```bash
kubectl -n policy-test exec client -- wget -q -O- --timeout=5 nginx-1
```

5. Let's add the DNS policy (necessary for name resolution):

```bash
kubectl apply -f - <<EOF
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: allow-dns
  namespace: policy-test
spec:
  selector: all()
  types:
  - Egress
  egress:
  - action: Allow
    protocol: UDP
    destination:
      selector: k8s-app == "kube-dns"
      ports:
      - 53
EOF
```

6. Finally, add the specific web traffic policy:

```bash
kubectl apply -f - <<EOF
apiVersion: projectcalico.org/v3
kind: NetworkPolicy
metadata:
  name: allow-web
  namespace: policy-test
spec:
  selector: app == 'web'
  types:
  - Ingress
  ingress:
  - action: Allow
    protocol: TCP
    destination:
      ports:
      - 80
    source:
      selector: app == 'client'
EOF
```

7. Test connectivity one final time (should work):

```bash
kubectl -n policy-test exec client -- wget -q -O- --timeout=5 nginx-1
```

Key Learning Points:

1. Notice how the default-deny policy immediately blocks all traffic
2. Observe that DNS access is crucial for pod-to-pod communication by name
3. See how specific policies can allow targeted communication paths

Let's validate your understanding:

- Can you explain why we needed the DNS policy?
- What would happen if we removed the selector from the allow-web policy?
- How would you modify the allow-web policy to permit traffic only during business hours?

Would you like to:

1. Explore policy troubleshooting by intentionally breaking something?
2. Add more complex policies (like egress restrictions)?
3. Learn how to monitor policy effectiveness using Calico's observability features?

You're right - let's slow down and master the fundamentals. Here's your focused learning plan for understanding network namespaces:

First Project: "Connect Two Network Namespaces"

Target: Understand how container networking works at the Linux level by creating and connecting two network namespaces.

Step 1: Setup and Exploration

- Create two network namespaces using `ip netns`
- Inspect what happens in `/var/run/netns/`
- TASK FOR YOU: Figure out how to list all network namespaces on your system

Step 2: Understanding Isolation

- Look inside each namespace to see its network interfaces
- Try to ping between namespaces (this will fail - understand why)
- TASK FOR YOU: Find a way to see all network interfaces within a specific namespace

Step 3: Creating Connections

- Create a virtual ethernet pair (veth)
- Connect each end to a different namespace
- TASK FOR YOU: Determine what happens to these virtual interfaces in the root namespace

Step 4: Configuration and Testing

- Assign IP addresses to interfaces in each namespace
- Enable the interfaces
- Test connectivity
- TASK FOR YOU: Figure out how to capture traffic between the namespaces

Self-Study Questions to Answer:

1. Why can't the namespaces communicate immediately after creation?
2. What's the relationship between veth pairs and how they enable communication?
3. How is this similar to how containers communicate?

Once you've completed this and understood each component, we'll move on to creating a more complex setup with three namespaces and a bridge - but let's master this first.

Would you like me to provide the exact commands for any of these steps, or would you prefer to research and discover them yourself first?

I'll help create your first structured learning session, starting with Level 1 of Network Namespaces. Here's how to frame your first interaction with Claude:

## Learning Session Context

I am following a structured curriculum to master Kubernetes networking, starting from Linux fundamentals and progressing to zero trust implementation in AWS EKS. Here's my current status:

### Current Progress

- Level: 1 - Linux Networking Fundamentals
- Topic: Network Namespaces Basics
- Previous Understanding: Basic Linux commands, basic networking concepts (IP addresses, interfaces)
- Current Challenge: Understanding network namespace isolation and implementation

### Today's Learning Goals

1. Create and interact with network namespaces
2. Understand namespace isolation principles
3. Practice examining network configurations within namespaces

### Curriculum Context

[Previous curriculum content would go here]

### Questions for This Session

1. How do network namespaces relate to the isolation I see in Kubernetes pods?
2. What specific tools and commands should I master for working with network namespaces?
3. How can I verify that network isolation is working as expected?

### Practical Exercise Needed

I need a hands-on exercise that will help me:

- Create network namespaces
- Inspect their properties
- Understand their isolation
- Learn common troubleshooting approaches

### Real-World Application

I work with AWS EKS, and I want to understand how these fundamentals connect to:

- Pod networking in EKS
- Network isolation in Kubernetes
- Container networking principles

### Learning Style Preferences

- Hands-on exercises preferred
- Need to understand the "why" behind each concept
- Like to see real-world applications
- Prefer iterative learning with practical validation

### Session Format Request

1. Start with a small, focused exercise
2. Include exploration tasks that I need to figure out
3. Provide clear verification steps to confirm understanding
4. Connect concepts to higher-level Kubernetes networking

Please help me begin this learning journey with a focused, hands-on approach to understanding network namespaces.

Here's how to use this framework:

1. Start Your Session:

- Copy this entire context into a new conversation with Claude
- Add the full curriculum we created earlier
- Ask Claude to create your first learning exercise

2. During the Session:

- Take notes on what you learn
- Document any challenges
- Record successful implementations
- Note questions that arise

3. Suggested First Request:
   "Based on this context, please create my first hands-on exercise for understanding network namespaces. Break it down into small steps, but leave some aspects for me to figure out through exploration."

4. After Completing Exercises:

- Update the context with what you've learned
- Note any areas that need more practice
- Ask for the next logical step
- Connect concepts to your AWS EKS environment

Would you like me to show you how to start this first conversation with Claude, or would you prefer to try crafting the initial prompt yourself based on this framework?

Remember: The key is to maintain context between sessions while progressively building your knowledge. Each session should have clear objectives and connect back to your ultimate goal of implementing zero trust in your EKS environment.

Let's explore how to examine network namespaces in a running Kubernetes cluster. We'll use various tools to peek under the hood of pod networking.

1. First, let's find a pod to examine:

```bash
# List pods across all namespaces
kubectl get pods -A

# Choose a running pod and note its node
kubectl get pod <pod-name> -n <namespace> -o wide
```

2. SSH into the node running your pod:

```bash
# If using EKS, you can use SSM
aws ssm start-session --target <node-id>
# Or traditional SSH if you have direct access
ssh ec2-user@<node-ip>
```

3. Find the pod's network namespace:

```bash
# List all network namespaces on the node
sudo ip netns list

# For containerd, the network namespaces are usually in:
sudo ls -l /var/run/netns/

# For Docker, they're typically in:
sudo ls -l /var/run/docker/netns/
```

4. Find the pod's container ID and network namespace:

```bash
# Get the container ID
sudo crictl pods | grep <pod-name>
sudo crictl ps | grep <pod-id>

# The network namespace will be in:
sudo ls -l /proc/<container-pid>/ns/net
```

5. Examine the network configuration inside the pod's namespace:

```bash
# Link the namespace temporarily for easy access
sudo ln -f /proc/<container-pid>/ns/net /var/run/netns/pod1

# Now you can inspect it
sudo ip netns exec pod1 ip addr
sudo ip netns exec pod1 ip route
sudo ip netns exec pod1 iptables -L

# Watch traffic
sudo ip netns exec pod1 tcpdump
```

Let's try a practical example. Would you like to:

1. Examine a specific pod in your cluster to see its network setup?
2. Create a test pod and inspect its networking configuration?
3. Set up traffic monitoring between two communicating pods?

This hands-on inspection will help you understand:

- How Kubernetes creates isolated network namespaces for pods
- How CNI plugins configure networking
- How pod-to-pod communication works at the Linux level

Each of these topics connects back to our learning path about network isolation and zero trust implementation.

Here’s a structured, hands-on curriculum to learn Linux containers from scratch, with a focus on CLI commands and practical exercises. The curriculum progresses from foundational concepts to advanced containerization, ensuring deep understanding through active practice.

---

## Curriculum: Building Linux Containers from Scratch

Goal: Learn container internals, build a container manually, and transition to Docker CLI.

Prerequisites: Basic Linux CLI familiarity (commands like `chroot`, `mount`, `ip`).

---

## Phase 1: Foundations of Containers
### 1.1 What Are Containers
- Objective: Understand containers vs. VMs, isolation, and use cases.
- Exercise:
  - Run `docker run hello-world` and observe the output.
  - Compare `ps aux` inside a container vs. the host.

### 1.2 Linux Kernel Basics
- Key Concepts: Namespaces (pid, net, mnt, uts, ipc, user) and cgroups.
- Lab:
  - Use `lsns` to list namespaces on your system.
  - Inspect cgroups: `cat /proc/$$/cgroup`.

---

## Phase 2: Building a Container Manually
### 2.1 Filesystem Isolation
- Objective: Create a minimal root filesystem.
- Lab:

  ```bash
  # Create a directory for the container
  mkdir ~/my_container && cd ~/my_container  
  # Use debootstrap to create a minimal filesystem (Debian/Ubuntu)
  sudo debootstrap focal ./rootfs http://archive.ubuntu.com/ubuntu/  
  ```

- Challenge: Replace `debootstrap` with `docker export` to extract a base image.

### 2.2 Process Isolation with Namespaces
- Lab: Use `unshare` to create isolated namespaces:

  ```bash
  sudo unshare --pid --uts --ipc --mount --net --fork /bin/bash  
  # Mount procfs inside the namespace
  mount -t proc proc /proc  
  # Verify isolation: `ps aux`, `hostname`, `ip addr`
  ```

- Key Command: `unshare` creates namespaces; `nsenter` joins them.

### 2.3 Resource Limits with Cgroups
- Lab: Limit CPU and memory for a process:

  ```bash
  # Create a cgroup
  sudo cgcreate -g cpu,memory:/my_container  
  # Set limits (e.g., 50% CPU, 512MB RAM)
  echo 50000 > /sys/fs/cgroup/cpu/my_container/cpu.cfs_quota_us  
  echo 536870912 > /sys/fs/cgroup/memory/my_container/memory.limit_in_bytes  
  # Add a process to the cgroup
  echo $$ > /sys/fs/cgroup/cpu/my_container/tasks  
  ```

### 2.4 Network Isolation
- Lab: Create a virtual Ethernet pair for the container:

  ```bash
  ip link add veth0 type veth peer name veth1  
  ip link set veth1 netns <container-pid>  # Use `lsns` to find PID
  # Assign IP addresses and set up NAT
  ```

---

## Phase 3: Automating with CLI Tools
### 3.1 Scripting a Basic Container
- Lab: Write a Bash script to automate Phase 2 steps:

  ```bash
  #!/bin/bash
  unshare --pid --uts --ipc --mount --net --fork \
    chroot ~/my_container/rootfs /bin/bash
  ```

- Challenge: Add cgroup limits to the script.

### 3.2 Using `systemd-nspawn`
- Lab: Launch a container with `systemd-nspawn`:

  ```bash
  sudo systemd-nspawn -D ~/my_container/rootfs --boot  
  ```

- Compare: How this differs from manual namespace setup.

---

## Phase 4: Transition to Docker (CLI Focus)
### 4.1 Docker Internals
- Key Concepts: Images, layers, Docker daemon, and `containerd`.
- Exercise:
  - Build an image from scratch:

    ```bash
    echo "FROM scratch" > Dockerfile  
    docker build -t my_image .  
    ```

### 4.2 Docker CLI Deep Dive
- Lab:
  - Run a container with resource limits:

    ```bash
    docker run -it --cpus="0.5" --memory="512m" ubuntu /bin/bash  
    ```

  - Inspect namespaces: `docker inspect --format '{{.State.Pid}}' <container_id>`
  - Use `docker exec` to run commands in a running container.

### 4.3 Building a Docker Image Manually
- Lab:
  - Extract a Docker image’s filesystem:

    ```bash
    docker export $(docker create alpine) > alpine.tar  
    tar -xf alpine.tar -C ~/my_container/rootfs  
    ```

  - Run it using your manual script from Phase 3.

---

## Phase 5: Advanced Topics
### 5.1 Security Hardening
- Lab:
  - Run a container as a non-root user:

    ```bash
    docker run -u 1000 alpine  
    ```

  - Use SELinux/AppArmor:

    ```bash
    docker run --security-opt apparmor=my_profile ...
    ```

### 5.2 Container Networking
- Lab:
  - Create a bridge network:

    ```bash
    docker network create my_network  
    docker run --network=my_network ...
    ```

  - Use `iptables` to inspect Docker’s NAT rules.

### 5.3 Debugging Containers
- Lab:
  - Use `docker logs`, `docker stats`, and `docker events` for monitoring.
  - Debug a broken container using `docker exec -it <container_id> sh`.

---

## Final Project

Build a Containerized Application:

1. Write a Python/Go app that listens on a port.
2. Create a Dockerfile to package it.
3. Run it with resource limits and custom networking.
4. Use `docker-compose` to add a Redis database.

---

## Resources For Active Learning
1. Books: Linux Containers and Virtualization by Shashank Mohan Jain.
2. Interactive Labs: [Katacoda](https://katacoda.com/courses/containers) or [Play with Docker](https://labs.play-with-docker.com/).
3. Repositories:
   - [LinuxKit](https://github.com/linuxkit/linuxkit) (Build minimal container OS).
   - [Buildah](https://github.com/containers/buildah) (Build containers without Docker).

---

## Troubleshooting Tips
- Use `strace` to trace system calls in your manual container.
- Inspect `dmesg` logs for kernel-level container errors.
- Run `docker system prune` to clean up orphaned containers/images.

By following this curriculum, you’ll gain a deep understanding of containers, from low-level kernel mechanics to Docker’s abstractions. The hands-on labs ensure you internalize each concept through practice.

To transition from passive to active learning and structure a challenging curriculum (especially for complex topics like Kubernetes), here’s a step-by-step framework inspired by active learning principles and tailored for developers:

---

## 1. Adopt Active Learning Strategies

Active learning prioritizes engagement, reflection, and application over passive consumption. For Kubernetes or similar technical topics:

- Problem-Based Learning: Tackle real-world Kubernetes challenges (e.g., deploying a microservice, configuring persistent storage) instead of memorizing theory .
- Think-Pair-Share: Collaborate with peers to solve Kubernetes cluster issues, then share solutions in forums like Kubernetes Slack or GitHub communities .
- Simulations and Labs: Use hands-on labs (e.g., [CKAD exam simulators](https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/) or [Kubernetes Playground](https://killercoda.com/)) to practice deployments, scaling, and troubleshooting .
- Flipped Classroom: Study Kubernetes documentation first, then apply concepts in projects like setting up a cluster with Ansible or deploying a CI/CD pipeline .

---

## 2. Structure a Challenging Curriculum

For Kubernetes, break the topic into core components and design milestones with active learning in mind:

### Phase 1: Foundations
- Core Concepts: Learn pods, deployments, services via interactive tutorials (e.g., [Boot.dev’s Kubernetes course](https://www.boot.dev/courses/learn-kubernetes)) .
- Hands-On Practice: Deploy a simple app using `kubectl` and YAML manifests. Use GitHub repositories like [iKubernetes/learning-k8s](https://github.com/iKubernetes/learning-k8s) for guided projects .
- Active Recall: Quiz yourself on Kubernetes architecture using flashcards or platforms like [CKAD Prep](https://github.com/bmuschko/ckad-prep) .

### Phase 2: Advanced Topics
- Multi-Container Pods: Build sidecar or init container patterns using case studies from [Microsoft’s Kubernetes Learning Path](https://github.com/microsoft/kubernetes-learning-path) .
- Networking and Security: Experiment with NetworkPolicies and Ingress controllers. Use tools like MetalLB or OpenELB .
- Stateful Workloads: Deploy stateful applications (e.g., databases) with PersistentVolumes and StorageClasses .

### Phase 3: Mastery and Certification
- CKAD/CKA Prep: Enroll in structured courses like [Coursera’s CKAD specialization](https://www.coursera.org/specializations/certified-kubernetes-application-developer-ckad-course) with labs and exam simulations .
- Contribute to Open Source: Fix bugs or add features to Kubernetes-related projects on GitHub (e.g., Helm charts, operators) .

---

## 3. Implement Active Learning Techniques
- Uncertainty Sampling: Focus on areas where your knowledge is weakest. For example, if you struggle with Kubernetes RBAC, prioritize labs on role-based access control .
- Reflection: After each project, write a post-mortem analysis. What went wrong? How did you fix it? Share these reflections on a blog or GitHub README .
- Gamification: Compete in Kubernetes hackathons or set personal goals (e.g., “Deploy a fault-tolerant cluster in 2 hours”) .

---

## 4. Leverage Community and Feedback
- Peer Teaching: Explain Kubernetes concepts to others via meetups or YouTube tutorials. Teaching forces you to solidify your understanding .
- Join Learning Circles: Participate in study groups like [Kubernetes Community Days](https://kubernetescommunitydays.org/) or Discord channels for collaborative problem-solving .
- Seek Feedback: Use platforms like [KodeKloud](https://kodekloud.com/) for graded Kubernetes exercises and peer reviews .

---

## 5. Track Progress and Iterate
- Milestones: Set SMART goals (e.g., “Master Helm chart templating by March”). Track progress using tools like Notion or GitHub Projects .
- Assessments: Regularly test yourself with CKAD practice exams or scenario-based labs .
- Iterate: If a method isn’t working (e.g., passive video tutorials), switch to active alternatives like coding challenges or contributing to open-source .

---

## Example: Ultra-Learning Curriculum for Kubernetes

| Week | Topic | Active Learning Activity | Resources |
|------|-------|--------------------------|-----------|
| 1–2 | Core Concepts | Deploy a static website using pods and services. Debug failures using `kubectl logs` . | [Boot.dev](https://www.boot.dev/courses/learn-kubernetes)  |
| 3–4 | Networking | Set up Ingress with Nginx and troubleshoot network policies. Use Katacoda labs for simulations . | [Kubernetes.io Docs](https://kubernetes.io/docs/concepts/services-networking/)  |
| 5–6 | State Management | Deploy PostgreSQL with PersistentVolumes. Test failover scenarios . | [iKubernetes/learning-k8s](https://github.com/iKubernetes/learning-k8s)  |
| 7–8 | Security | Configure RBAC and audit cluster security. Use tools like kube-bench . | [CKAD Prep Course](https://github.com/bmuschko/ckad-prep)  |
| 9–10 | Certification Prep | Solve timed CKAD exam simulations. Review mistakes with peers . | [Linux Foundation CKAD](https://training.linuxfoundation.org/certification/certified-kubernetes-application-developer-ckad/)  |

---

## Key Takeaways
1. Shift from passive to active: Replace tutorials with hands-on projects and problem-solving .
2. Structure with milestones: Break Kubernetes into manageable components and track progress .
3. Engage the community: Learn collaboratively and teach others to reinforce knowledge .
4. Iterate and adapt: Continuously refine your methods based on feedback and gaps .

By integrating these strategies, you’ll not only master Kubernetes but also develop a lifelong framework for tackling complex topics efficiently.

Here's a breakdown of the source materials you've provided, which I will use to help you with your learning program:

- "BPF Performance Tools - Brendan Gregg.pdf": This book delves deep into performance analysis using BPF (Berkeley Packet Filter) and covers topics like CPU, memory, file systems, disk I/O, networking, security, and even containers and hypervisors. It includes a focus on both traditional and BPF-based analysis tools, and offers one-liners and practical exercises.
- "Building a Linux container by hand using namespaces.md", "Building a container by hand using namespaces The UTS namespace.md", "Building containers by hand using namespaces The net namespace 1.md", and "Building containers by hand using namespaces The net namespace.md": These articles provide practical, hands-on guides to creating containers using various Linux namespaces, including user, mount, UTS, and network namespaces. They include clear examples, command-line instructions, and discussions of the security implications.
- "Computer Networking\_ A Top-Down Approach, - James F. Kurose.pdf": This textbook provides a comprehensive overview of computer networking concepts, protocols, and technologies. It takes a top-down approach, starting from the application layer and working down to the link layer. It includes summaries, homework problems, and references for further learning. It also discusses topics like network management and security.
- "Docker Deep Dive\_ 2023 Edition - Nigel Poulton.pdf": This book is dedicated to teaching you about Docker, covering the big picture concepts like the history of containers, the Docker Engine and the OCI, and diving into the technical details of images, containers, networking, security, and orchestration with Docker Swarm and Compose. The book also includes hands-on examples and labs, and covers topics for enterprise environments. It also prepares you for the Docker Certified Associate exam.
- "Kubernetes Networking.md": This resource is a curated list of materials to help with learning Kubernetes networking, including guides, documentation, visualisations, and projects. It encourages active learning, project-based learning, and the Feynman technique to enhance understanding.
- "Kubernetes Security and Observability - Brendan Creane.pdf": This book guides you on developing a holistic security and observability strategy for Kubernetes. It covers topics like Kubernetes adoption, security controls, threat defence, observability, log collection, and network policies. It also talks about important security concepts like Pod Security Policies, capabilities, seccomp, AppArmor, and SELinux.
- "The 7 most used Linux namespaces.md": This article provides a useful overview of the seven most common Linux namespaces (PID, mount, network, IPC, UTS, user, and cgroup), explains how they provide isolation, and briefly covers how they can be used in the creation of containers.
- "building a container components.md": This document focuses on network namespaces, explaining core concepts and providing examples of how to use `ip netns` and virtual ethernet pairs to create isolated networks. It also suggests hands-on learning projects.
- "k8s curriculum.md": This document proposes a curriculum for learning about containers, beginning with low-level Linux primitives (namespaces and cgroups), progressing to image creation, and finally to integration projects and Kubernetes. It also includes Kubernetes and Container technology mastery levels, and a practical skills matrix, with a strong focus on hands-on learning. It provides validation methods, resources, and progress tracking for your learning. It also covers visualisation techniques for networks.
- "k8s network learning project.md": This document lays out a plan for learning Kubernetes networking, starting with Linux networking basics and progressing to AWS-specific implementations and Calico. It provides hands-on labs for learning each level. It also gives detailed instructions for setting up Calico policies. It proposes a detailed project for setting up and connecting two namespaces.
- "ldx.md": This article provides a comprehensive guide to LXC and LXD, highlighting their core concepts like namespaces and cgroups, the benefits they offer, and their limitations compared to other containerization technologies.

Now, regarding your specific request to structure a learning program for containers and Linux namespaces, I recommend a curriculum that progresses from the fundamentals to more advanced topics, with hands-on exercises at each stage. Here's a possible structure that takes into account the concepts of practical learning, and overcoming the illusion of explanatory depth:

## Phase 1: Linux Fundamentals

1. Core Concepts:
   - Linux Namespaces: Understand the different types of namespaces (PID, network, mount, UTS, IPC, user) and how they provide isolation. Learn how to use tools like `ip netns` to create and manage them.
     - *Practical Learning*: Create your own namespaces, and explore their differences. See how they isolate processes and networking. Start with the "Connect Two Network Namespaces" project from the `k8s network learning project.md` and use a structured learning session as described in the same document
   - Control Groups (cgroups): Learn how cgroups limit resource usage (CPU, memory, I/O). Understand their role in managing resource allocation for containers.
     - *Practical Learning*: Implement cgroups to set resource limits on processes you create inside the isolated namespaces that you made in the previous step.
   - Virtual Ethernet (veth) Pairs: Learn how they connect namespaces. Understand how to use `ip link` to create and connect them.
     - *Practical Learning*: Create `veth` pairs, assign one end to one namespace and the other end to another, and then configure them to enable communication.
2. Hands-on Projects:
   - Create a basic container from scratch: Combine namespaces and cgroups to create an isolated process environment.
     - *Practical Learning*: Build a simple container using the skills that you have developed in the previous practical learning sections. The goal is to truly understand the foundational mechanisms that enable container technology.
   - Set up isolated network environments: Connect namespaces using veth pairs and configure IP addresses. Implement a network bridge to understand container networking.
     - *Practical Learning*: Build a more complex network by connecting multiple namespaces to a bridge. Learn how to isolate network traffic. Implement basic network policies using `iptables` within the namespaces.
   - Start from first principles: Create all the required configuration step by step in such a way that you could explain each step as you are doing it.

## Phase 2: Containerisation

1. Container Images:
   - Layered Architecture: Understand how container images are composed of read-only layers. Learn how to create layered filesystems.
     - *Practical Learning*: Investigate a Docker image. Look at its layers using the `docker image inspect` command. See how the layers have been put together.
   - Dockerfiles: Learn how to use Dockerfiles to define the steps for building a container image.
     - *Practical Learning*: Create a Dockerfile for a basic web app. Use multi-stage builds.
   - Image Registries: Learn about the role of registries and how they are used for storing and sharing container images.
     - *Practical Learning*: Use Docker Hub or other registries to push and pull images.
2. Container Runtimes:
   - Docker Engine: Understand the architecture of the Docker Engine, including the daemon, containerd, and runc.
     - *Practical Learning*: Explore these components using the `docker` CLI or by looking at the underlying process structure on your machine.
   - Other runtimes: Learn about OCI-compliant runtimes like containerd and runc, and explore LXC and LXD.
     - *Practical Learning*: Compare the performance of multiple container runtimes.
3. Container Networking:
   - Docker Networking: Learn about Docker's networking model, including bridge and overlay networks.
     - *Practical Learning*: Create a custom network bridge and connect multiple containers using Docker's network features. Explore the network configuration of a running Docker container. Use `docker network inspect` to view your networks. Use tools like `tcpdump` to see how traffic flows in the network.
   - Container Network Interface (CNI): Understand the CNI specification and how it allows container runtimes to work with different networking solutions.
     - *Practical Learning:* Look at the different CNI plugins like Calico, Flannel, and Weave.
4. Security:
   - Linux Capabilities: Understand how Linux capabilities control access to privileged operations.
     - *Practical Learning*: Drop capabilities from a running container.
   - Seccomp: Learn how seccomp profiles can restrict the system calls available to a container.
     - *Practical Learning*: Create and implement a seccomp profile for a container.
   - AppArmor and SELinux: Understand MAC systems and their use in container security.
     - *Practical Learning*: Investigate the security policies for a running container that is using SELinux.

## Phase 3: Container Orchestration with Kubernetes

1. Kubernetes Networking:
   - Pod-to-Pod Communication: Learn how pods communicate with each other, including on the same and different nodes. Understand the role of `kube-proxy` and services.
     - *Practical Learning*: Examine the networking configuration of a pod in a Kubernetes cluster. Trace packet flows between pods.
   - Network Policies: Configure network policies to control traffic flow within the cluster.
     - *Practical Learning*: Implement Kubernetes network policies to restrict traffic between namespaces and pods.
   - Calico Policies: Explore Calico, an open-source project that simplifies, scales, and secures container and Kubernetes networks.
     - *Practical Learning*: Set up a cluster with Calico and follow the Calico policy lab.
2. Kubernetes Security:
   - Pod Security Policies: Understand how PSPs can control the capabilities and security settings of pods.
   - Observability: Learn how to monitor and secure a Kubernetes cluster. Understand how to collect logs and set up alerts.
     - *Practical Learning*: Explore the observability features of your Kubernetes implementation, using metrics, logs, and traces.

## Overcoming the Illusion of Explanatory Depth

- Hands-on Learning: Focus on building and testing rather than just reading.
- "Why" instead of "How": Prioritise understanding the reasons behind design decisions and configurations.
- Visualisation: Use the suggested tools to visualise how the networks are implemented, instead of thinking of them as abstract concepts.
- Troubleshooting: Intentionally break things to learn the root cause of failures.

## Comprehensive Curriculum for Mastering Linux Containers from First Principles

To overcome the Illusion of Explanatory Depth (IoED) and deeply understand Linux containers, this curriculum combines foundational theory with hands-on practice using Linux primitives (namespaces, cgroups, filesystem isolation, etc.). Below is a structured learning path with resources and exercises to ensure active engagement and concrete understanding.

---

### Phase 1: Core Linux Primitives

Objective: Grasp the building blocks of containers at the kernel level.

1. Namespaces:

   - [[PID Namespace]]: Isolate process trees.
     *Exercise*: Use `unshare -p` to create a new PID namespace and observe isolated processes .
   - Mount Namespace: Isolate filesystem views.
     *Exercise*: Combine `unshare -m` with `chroot` to create a filesystem jail .
   - Network Namespace: Isolate network interfaces.
     *Exercise*: Create a virtual Ethernet pair with `ip netns` .
   - UTS Namespace: Isolate hostname and domain name .

2. Control Groups (cgroups):

   - Memory Limits: Restrict memory usage via `/sys/fs/cgroup/memory`.
     *Exercise*: Limit a process to 100MB and trigger an OOM kill .
   - CPU Quotas: Use `cpu.max` to allocate CPU shares.
     *Exercise*: Cap a CPU-intensive process to 10% utilization .

3. Filesystem Isolation:
   - chroot: Create a minimal root filesystem using Alpine rootfs .
   - OverlayFS: Layer read-only and writable filesystems for container images .

---

### Phase 2: Building a Container from Scratch

Objective: Assemble primitives into a functional container runtime.

1. Step-by-Step Implementation:

   - Create a PID namespace with `unshare --pid --fork`.
   - Mount a custom root filesystem with `chroot` or `pivot_root` .
   - Apply cgroups to limit CPU/memory .
   - Use `nsenter` to debug namespaces .

2. Security Hardening:

   - Linux Capabilities: Drop unnecessary privileges (e.g., `CAP_NET_BIND_SERVICE` for binding low ports) .
   - Seccomp: Filter syscalls to reduce attack surface.

3. Toolchain Integration:
   - Use `buildah` to create OCI-compliant images from scratch .
   - Experiment with `runc` to execute containers .

---

### Phase 3: Advanced Topics

Objective: Explore real-world container ecosystems and optimizations.

1. Container Networking:
   - Bridge networks with `veth` pairs and `iptables` .
2. Storage Layers:
   - Manage volumes with `overlay2` and `tmpfs` .
3. Orchestration Basics:
   - Deploy multi-container apps using `docker-compose` or `podman-play-kube` .

---

## Superb Resources to Eliminate IoED

1. Hands-On Labs:

   - Linux Container Primitives Jupyter Notebooks [GitHub](https://github.com/aws-samples/linux-container-primitives-presentation-notebooks): Interactive tutorials for cgroups and namespaces .
   - Containers from Scratch [Blog](https://www.cnblogs.com/lfri/p/15820394.html): Step-by-step guide to building containers without Docker .

2. Structured Courses:

   - LFS253: Containers Fundamentals [Linux Foundation](https://training.linuxfoundation.org/training/containers-fundamentals/): Covers Docker, Podman, and OCI specifications .

3. Deep Dives:

   - Control Groups Internals [Schutzwerk Blog](https://www.schutzwerk.com/en/blog/linux-container-cgroups-01-intro/): Explains cgroups v1/v2 and kernel mechanics .
   - Building a Docker Clone in Go [Michal Pitr’s Blog](https://michalpitr.substack.com/p/linux-container-from-scratch): Code-driven approach to container internals .

4. Books:
   - *Linux Kernel Development* by Robert Love: Covers namespaces and cgroups in depth.
   - *Container Security* by Liz Rice: Focuses on hardening containerized environments.

---

## Active Learning Strategies to Combat IoED

1. Feynman Technique: After each module, explain concepts in simple terms (e.g., "How does a PID namespace work?") .
2. Iterative Prompting: Use ChatGPT to validate your understanding (e.g., "Why does `unshare` require `--fork`?").
3. Break & Fix: Intentionally misconfigure cgroups/namespaces and debug the failures .

---

By following this curriculum, you'll transition from surface-level familiarity to mechanistic understanding, ensuring you can design, debug, and optimize containers without relying on abstractions like Docker.

Based on your latest query, you want me to review the "Container Security\_ Fundamental Technology" document by Liz Rice and update your container curriculum with ideas and practical examples from it. This book is a deep dive into the fundamental technologies that underpin container security. It covers topics ranging from basic Linux mechanisms to container isolation and network security. I will extract relevant concepts and examples from this book and suggest how to integrate them into your existing curriculum.

Here's how I can help you update your curriculum, drawing directly from Liz Rice's book:

1. Foundational Linux Concepts:

- System Calls, Permissions, and Capabilities: The book stresses that containers run as Linux processes and use system calls, permissions, and privileges just like regular processes. Your curriculum should cover these foundational Linux mechanisms.
- Practical Example: Include an exercise where you demonstrate how to use `strace` to observe the system calls made by a containerized application. Then explore how to control the capabilities granted to a container, for example, dropping the `CAP_NET_RAW` capability to prevent raw socket access.
- Namespaces: The book explains that containers use Linux namespaces to isolate various aspects of the system such as process IDs, network interfaces, and mount points. Your curriculum should explore namespaces thoroughly.
- Practical Example: Guide learners to manually create and use namespaces using the `unshare` command. This could be followed by manually creating a container using `chroot` and namespaces, showing how a container is created from first principles.
- cgroups: The book explains that control groups (cgroups) are used to manage resources like CPU, memory, and I/O for containers. Your curriculum should include these concepts.
- Practical Example: Have students create cgroups and limit the resources available to a specific container, and observe the impact on the running application.

2. Container Isolation and Security:

- Container vs. Virtual Machines: The book contrasts container isolation with virtual machine isolation. Your curriculum should differentiate between the two, particularly focusing on their security implications.
- Practical Example: Run a vulnerable application in both a container and a virtual machine. Analyse the different levels of isolation that each provides and the impact on potential security breaches.
- Image Security: Rice's book highlights that container images can contain vulnerabilities. It also discusses supply chain attacks and misconfigured containers. Your curriculum should emphasize image scanning, secure image building practices, and how to avoid misconfigurations.
- Practical Example: Incorporate a vulnerability scanning step into the image build pipeline, using tools like Trivy. Explore how to build minimal images with the least amount of software to reduce the attack surface.
- Runtime Security: The book explores ways to harden containers beyond basic isolation using Linux security measures. It also examines ways container isolation can be compromised due to misconfigurations. Your curriculum should include runtime protection mechanisms such as AppArmor, SELinux, and seccomp.
- Practical Example: Implement a seccomp profile that restricts the system calls available to a containerized application. Demonstrate the use of AppArmor or SELinux to enforce mandatory access control policies on containerized applications.

3. Container Networking and Communication:

- Container Networking: The book details how containers communicate, including network security features of service meshes. Your curriculum should include detailed explanations of container networking.
- Practical Example: Set up a basic container network and then use tools like `tcpdump` or `wireshark` to observe the network traffic between containers. Also demonstrate how to use Kubernetes network policies to control traffic to and from container workloads.
- Secure Communication: The book highlights the importance of keys and certificates for secure communication between containers.
- Practical Example: Include a project where students use TLS certificates to secure the communication channel between two containers. Then discuss the best way to securely pass secrets to containers, avoiding the common pitfall of storing secrets in container images.

4. Vulnerability Management and Scanning:

- Image Scanning: The book discusses software vulnerabilities in images, emphasizing the importance of regular image scanning. Your curriculum should stress the need to integrate image scanning into CI/CD pipelines.
- Practical Example: Use a tool such as Clair or Trivy to scan a container image for vulnerabilities and demonstrate how to interpret the results. Have students practice patching vulnerable packages and rebuilding images.
- OWASP Top 10: The book references the OWASP Top 10 security risks and relates them to container-specific mitigations.
- Practical Example: Map the OWASP top 10 to specific container security practices, like using image scanning, reducing the attack surface, and implementing network policies.

5. Practical Curriculum Updates:

- Hands-on Labs: Create hands-on labs for each of these concepts, focusing on practical tasks and building real-world experience.
- This will align with the curriculum that you have outlined in `k8s curriculum.md`
- Integration Projects: Create integration projects that combine these concepts. For example, have learners build a containerized microservice application, apply security measures at different levels, and deploy the application to a Kubernetes cluster.
- This aligns with your existing curriculum ideas.
- Immutability: Emphasize the importance of immutable containers and how to enforce immutability to enhance security.
- Practical Example: Configure a container to run with a read-only file system and mount a temporary writable file system for application needs.
- Supply Chain Security: Incorporate concepts such as using trusted base images, verifying image signatures, and using private registries to secure the software supply chain.
- Practical Example: Walk through the process of signing a container image using Docker Content Trust, or a similar method, and then verify the image before deployment.

By integrating these ideas and practical examples from Liz Rice's book, your container curriculum will be more comprehensive, hands-on, and focused on real-world security considerations.

As a next step, I suggest that we dive into Chapter 2 of the book which covers Linux system calls, permissions, and capabilities and how they come into play for containers. Would you like me to provide a summary of Chapter 2 and related practical exercises that could be incorporated into your curriculum? Or perhaps you'd like to explore a different aspect of the book? I can also quiz you on this information if you'd like.

Certainly! Based on the citations provided and your goal to learn about Linux containers with a focus on practical exercises, I can help you create a structured Phase 1 curriculum. This curriculum will cover the foundational concepts and provide practical exercises to reinforce your learning.

### Phase 1 Curriculum: Introduction to Linux Containers

#### Week 1: Understanding Containers

Objective: Gain a basic understanding of what containers are, their types (application vs. system containers), and why they are important in modern deployment strategies.

Topics Covered:

- What are Containers?
- Application Containers vs. System Containers
- Benefits of Using Containers (e.g., reducing attack surface, limiting blast radius, segregation of duties)

Resources:

- Citation 1: Read the section about application and system containers.
- Online Tutorials:
  - [Docker's What are Containers?](https://www.docker.com/resources/what-is-a-container/)
  - [Kubernetes Overview](https://kubernetes.io/docs/concepts/overview/what-is-kubernetes/)

Practical Exercises:

1. Install Docker on Your Machine:
   - Follow the instructions from [Docker's Official Installation Guide](https://docs.docker.com/get-docker/).
2. Run a Simple Container:

   - Run a basic container using an official image (e.g., `nginx` or `alpine`):

     ```bash
     docker run -d --name my-nginx nginx
     ```

   - Verify it’s running:

     ```bash
     docker ps
     ```

#### Week 2: Linux Kernel Features and Container Isolation

Objective: Learn about the core Linux kernel features that enable containerization (control groups, namespaces, and chroot).

Topics Covered:

- Control Groups (cgroups)
- Namespaces
- Changing the Root Directory (chroot)

Resources:

- Citation 2: Read the section on how containers use Linux kernel features.
- Online Tutorials:
  - [Understanding Docker: Part 1](https://blog.alexellis.io/understanding-docker-part-1/)
  - [Linux Namespaces and Control Groups for Beginners](https://www.baeldung.com/linux/namespaces-cgroups)

Practical Exercises:

1. Explore Namespaces:

   - Create a new namespace using `unshare`:

     ```bash
     sudo unshare --mount --uts --ipc --net --pid --fork bash
     ```

   - Verify the isolation by checking network interfaces, hostname, and process IDs inside vs. outside the namespace.

2. Experiment with cgroups:

   - Use `cgroups` to limit resource usage of a container:

```bash
sudo cgcreate -g memory:/mygroup
echo 100M > /sys/fs/cgroup/memory/mygroup/memory.limit_in_bytes
sudo cgexec -g memory:/mygroup docker run --rm nginx
```

#### Week 3: Container Security Principles

Objective: Understand the security principles behind containers, including reducing attack surfaces and limiting blast radius.

Topics Covered:

- Threat Models and Attack Vectors for Containers
- Securing Containers Using Linux Kernel Mechanisms

Resources:

- Citation 3: Read about how different security mechanisms work in containers.
- Online Tutorials:
  - [Container Security: Best Practices](https://www.snyk.io/learn/container-security/)
  - [Securing Docker Containers](https://docs.docker.com/engine/security/)

Practical Exercises:

1. Run a Secure Container:

   - Create a Dockerfile with minimal necessary permissions and capabilities:

```dockerfile
FROM alpine:latest
RUN adduser -S myuser
USER myuser
CMD ["sh"]
```

- Build and run the container:

  ```bash
  docker build -t secure-container .
  docker run --rm -it secure-container
  ```

2. Use Docker Security Features:

   - Enable user namespace for isolation:

     ```bash
     docker run --userns=host -d --name my-secure-nginx nginx
     ```

   - Verify the security settings:

     ```bash
     docker inspect my-secure-nginx | grep UsernsMode
     ```

#### Week 4: Building and Managing Container Images

Objective: Learn how to build container images securely, manage image registries, and scan for vulnerabilities.

Topics Covered:

- Building Secure Container Images
- Image Registries (e.g., Docker Hub)
- Vulnerability Scanning

Resources:

- Online Tutorials:
  - [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
  - [Scanning Container Images with Trivy](https://aquasecurity.github.io/trivy/v0.18.2/getting-started/cli/)
- Tools:
  - [Trivy](https://github.com/aquasecurity/trivy) for vulnerability scanning.
  - [Docker Hub](https://hub.docker.com/) for image management.

Practical Exercises:

1. Build a Secure Container Image:

   - Write a Dockerfile that includes minimal packages and uses security best practices (e.g., using `USER` directive).

```dockerfile
FROM alpine:latest
RUN apk add --no-cache nginx
COPY index.html /usr/share/nginx/html/index.html
USER nginx
CMD ["nginx", "-g", "daemon off;"]
```

- Build the image:

  ```bash
  docker build -t my-secure-image .
  ```

2. Push Image to Docker Hub:

   - Create an account on [Docker Hub](https://hub.docker.com/).
   - Push your built image:

```bash
docker tag my-secure-image username/my-secure-image:latest
docker push username/my-secure-image:latest
```

3. Scan the Image for Vulnerabilities:
   - Use Trivy to scan the Docker image:

```bash
trivy image username/my-secure-image:latest
```

## Linux Containers: From Scratch to Production

### Learning Path Overview

This curriculum focuses on building containers from scratch using Linux primitives, helping you understand the fundamental building blocks before moving to tools like Docker.

### Level 1: Container Building Blocks

#### Module 1: Process Isolation with Namespaces

Theory:

- Understanding Linux namespaces (pid, net, mnt, uts, ipc, user)
- Process isolation principles
- Resource containment basics

Practical Exercises:

1. Create an isolated process:

```sh
# Create a new UTS namespace
unshare --uts /bin/bash
# Verify isolation by changing hostname
hostname container1
# Verify change doesn't affect host
```

2. Explore PID namespace:

```sh
# Create new PID namespace
unshare --pid --fork /bin/bash
# List processes and observe isolation
ps aux
```

#### Module 2: Resource Control with Cgroups

Theory:

- Understanding cgroup hierarchy
- Resource limiting mechanisms
- CPU, memory, and I/O control

Practical Exercises:

1. Create and manage cgroups:

```bash
# Create a new cgroup
sudo mkdir /sys/fs/cgroup/memory/mycontainer
# Set memory limit (100MB)
echo 100000000 > /sys/fs/cgroup/memory/mycontainer/memory.limit_in_bytes
# Run process in cgroup
echo $$ > /sys/fs/cgroup/memory/mycontainer/cgroup.procs
```

2. Monitor resource usage:

```bash
# Watch memory usage
cat /sys/fs/cgroup/memory/mycontainer/memory.usage_in_bytes
```

### Level 2: Building Basic Containers

#### Module 1: File System Isolation

Theory:

- Root filesystem concepts
- Mount namespaces
- Overlay filesystems

Practical Exercises:

1. Create container root filesystem:

```bash
# Create minimal root filesystem
mkdir container-root
cd container-root
mkdir bin lib proc sys
# Copy basic binaries
cp /bin/bash bin/
# Copy required libraries
ldd /bin/bash | grep -o '/lib.\.[0-9]' | xargs -I {} cp {} lib/
```

2. Mount proc filesystem:

```bash
# Mount proc in container
mount -t proc none container-root/proc
```

#### Module 2: Network Isolation

Theory:

- Network namespaces
- Virtual interfaces
- Container networking models

Practical Exercises:

1. Create network namespace:

```bash
# Create namespace
ip netns add container1
# Create veth pair
ip link add veth0 type veth peer name veth1
# Move one end to namespace
ip link set veth1 netns container1
```

2. Configure networking:

```bash
# Configure IP addresses
ip addr add 172.16.0.1/24 dev veth0
ip netns exec container1 ip addr add 172.16.0.2/24 dev veth1
# Enable interfaces
ip link set veth0 up
ip netns exec container1 ip link set veth1 up
```

### Level 3: Advanced Container Features

#### Module 1: Security and Capabilities

Theory:

- Linux capabilities
- Seccomp profiles
- AppArmor/SELinux basics

Practical Exercises:

1. Drop capabilities:

```bash
# Start container with limited capabilities
unshare --pid --net --mount-proc cap_drop=all /bin/bash
# Test network operations
ping 8.8.8.8  # Should fail
```

2. Create seccomp profile:

```bash
# Create basic seccomp profile
{
  "defaultAction": "SCMP_ACT_ERRNO",
  "architectures": ["SCMP_ARCH_X86_64"],
  "syscalls": [
    {"names": ["read", "write"], "action": "SCMP_ACT_ALLOW"}
  ]
}
```

#### Module 2: Container Image Creation

Theory:

- Layer architecture
- Image manifests
- Distribution formats

Practical Projects:

1. Create layered filesystem:

```bash
# Create base layer
mkdir base-layer
# Add application layer
mkdir app-layer
# Create overlay mount
mount -t overlay overlay -o lowerdir=app-layer:base-layer /merged
```

### Level 4: Integration Projects

1. Basic Container Runtime:

- Combine namespace isolation
- Implement cgroup controls
- Add basic networking

2. Container Image Builder:

- Create OCI-compatible images
- Implement layer management
- Add metadata handling

### Success Criteria

For each level, you should be able to:

1. Explain the purpose of each isolation mechanism
2. Create containers using command-line tools
3. Debug common container issues
4. Understand security implications

### Troubleshooting Guide

Common issues and solutions:

1. Permission denied:

   - Check capability requirements
   - Verify user permissions
   - Check SELinux/AppArmor contexts

2. Network connectivity:

   - Verify namespace configuration
   - Check routing tables
   - Validate interface status

3. Resource limits:
   - Verify cgroup settings
   - Check resource availability
   - Monitor usage patterns

### Additional Resources

1. Linux Kernel Documentation:

   - Namespaces
   - Cgroups
   - Capabilities

2. OCI Specifications:

   - Runtime Specification
   - Image Specification
   - Distribution Specification

3. Related Tools:
   - runc
   - containerd
   - buildah

### Next Steps

After completing this curriculum:

1. Study container orchestration
2. Learn Docker and Podman
3. Explore Kubernetes concepts
4. Practice container security
