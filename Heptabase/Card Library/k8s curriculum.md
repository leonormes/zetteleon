# k8s curriculum

## Linux Containers: From Scratch to Production

### Learning Path Overview

[Level 1! Container Building Blocks.md](Level%201!%20Container%20Building%20Blocks.md)

[Level 2! Building Basic Containers.md](Level%202!%20Building%20Basic%20Containers.md)

[Level 3! Advanced Container Features.md](Level%203!%20Advanced%20Container%20Features.md)

[Level 4! Integration Projects.md](Level%204!%20Integration%20Projects.md)

### Next Steps

After completing this curriculum:

1. Study container orchestration

2. Learn Docker and Podman

3. Explore Kubernetes concepts

4. Practice container security

I've created a comprehensive curriculum that focuses on building containers from scratch using Linux primitives. The curriculum is structured to provide both theoretical understanding and hands-on practice.

A few key points about this curriculum:

1. It starts with fundamental Linux primitives (namespaces, cgroups) before moving to more complex concepts

2. Each module contains practical exercises you can run on a Linux system

3. The exercises build upon each other, creating a deeper understanding

4. There's a focus on debugging and troubleshooting skills

5. The curriculum includes success criteria so you can track your progress

Would you like to start with the first module on process isolation with namespaces? We can walk through the exercises together, or I can help clarify any concepts that aren't clear.

Also, what kind of Linux environment do you have available for practicing these exercises? This will help me tailor the instructions to your setup.
I'll create a structured progression of Kubernetes mastery levels that builds on the curriculum context provided.

[Level 1! Foundation Builder.md](Level%201!%20Foundation%20Builder.md)

[Validation Methods for Each Level.md](Validation%20Methods%20for%20Each%20Level.md)

[Container Technology Mastery Levels.md](Container%20Technology%20Mastery%20Levels.md)

## Visualizing Container Networks: Inspection Tools and Techniques

### Basic Network Namespace Inspection

#### 1\. List Network Namespaces

```bash
# List all network namespaces
ip netns list

# Show detailed namespace info
ip netns identify <pid>
```

#### 2\. Visualize Network Interfaces

```bash
# Show all interfaces on host
ip link show

# Show interfaces in specific namespace
ip netns exec container_ns ip link show

# Show connections between veth pairs
ethtool -S veth0  # Shows peer_ifindex
```

#### 3\. Real-time Network Monitoring

```bash
# Watch network traffic in real-time (host)
watch -n1 'ip -s link show veth0'

# Watch network traffic in container namespace
ip netns exec container_ns watch -n1 'ip -s link show veth1'
```

### Visual Network Inspection Tools

#### 1\. Network Layout with 'bridge'

```bash
# Install bridge-utils
apt-get install bridge-utils

# Show bridge connections
brctl show

# Show bridge details
brctl showmacs br0  # if using bridge
```

#### 2\. Visual Traffic Analysis with Tcpdump

```bash
# Watch traffic on host interface
tcpdump -i veth0

# Watch traffic in container namespace
ip netns exec container_ns tcpdump -i veth1

# Save traffic for visual analysis
tcpdump -i veth0 -w capture.pcap
# Open with Wireshark for visual analysis
```

#### 3\. Connection Tracking

```bash
# Show active connections
conntrack -L

# Watch connections in real-time
watch -n1 'conntrack -L'
```

### Network State Visualization

#### 1\. Routing Table Inspection

```bash
# Host routing
ip route show

# Container routing
ip netns exec container_ns ip route show

# Watch routing changes
watch -n1 'ip route show'
```

#### 2\. Address Resolution (ARP) Table

```bash
# Host ARP table
ip neigh show

# Container ARP table
ip netns exec container_ns ip neigh show

# Watch ARP changes
watch -n1 'ip neigh show'
```

### Network Testing Tools

#### 1\. Connection Testing

```bash
# Test network connection from host
ping -c 3 172.16.0.2

# Test from container namespace
ip netns exec container_ns ping -c 3 172.16.0.1

# Trace route path
ip netns exec container_ns traceroute 172.16.0.1
```

#### 2\. Port and Service Testing

```bash
# Check listening ports in container
ip netns exec container_ns netstat -tulpn

# Scan ports from host
nc -zv 172.16.0.2 8000

# Monitor open connections
ip netns exec container_ns ss -tan
```

### Advanced Visualization Techniques

#### 1\. Network Graphing

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

#### 2\. Real-time Bandwidth Monitoring

```bash
# Install iftop
apt-get install iftop

# Monitor container interface
ip netns exec container_ns iftop -i veth1

# Monitor host interface
iftop -i veth0
```

### Debugging Common Network Issues

#### 1\. Interface Problems

```bash
# Check interface state
ip link show veth0
ip netns exec container_ns ip link show veth1

# Verify interface is up
ip link set veth0 up
ip netns exec container_ns ip link set veth1 up
```

#### 2\. Routing Issues

```bash
# Check routes on both sides
ip route get 172.16.0.2
ip netns exec container_ns ip route get 172.16.0.1

# Verify routing table
ip route show table all
ip netns exec container_ns ip route show table all
```

#### 3\. DNS Resolution

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

1. After Creating Network Namespace:

```bash
# List namespaces again
ip netns list
# Should show your new container_ns

# Look inside the namespace
ip netns exec container_ns ip link list
# Initially only shows loopback interface
```

1. After Creating veth Pair:

```bash
# On host - show all interfaces
ip link show
# You'll see both veth0 and veth1

# Show connection between interfaces
ethtool -S veth0
# Shows peer_ifindex which links to veth1
```

1. Monitor Traffic in Real-time:

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

1. Network debugging pods:

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

1. CNI plugin tools:

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

- Why are you learning? Your primary motivation is to understand containerisation as a foundation for learning Kubernetes \[your query\]. You also want to overcome the illusion of explanatory depth and understand the underlying technologies \[your query\]. This means we need to focus on *understanding* not just rote memorisation. We will aim to understand the "why" behind everything.

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

- Documentation: You need to keep meticulous notes of everything that you are doing. Use the [README.md](http://README.md) files to explain your thinking, `commands.sh` to track what you did, and a `troubleshooting.md` for problems that you encounter.

This curriculum is designed to help you build a deep and practical understanding of Linux containers and create a solid foundation for learning Kubernetes. It will also help you overcome the illusion of explanatory depth by forcing you to build your knowledge from first principles.

What do you think? Are you ready to start with the first module on process isolation with namespaces? We can walk through the exercises together, or I can help clarify any concepts that aren't clear.

The networking aspect of Kubernetes, especially in AWS, is fascinating and complex. Let's create a bottom-up learning curriculum for networking, starting from basic Linux networking concepts up to AWS-specific implementations.

## Level 1: Linux Networking Fundamentals

- Network Namespaces & Container Networking Basics

   - Hands-on Project: Create network namespaces using `ip netns` and connect them

   - Practice connecting namespaces with virtual ethernet pairs (veth)

   - Build a simple network bridge to understand container networking

   - Create your own mini-container network to deeply understand what Kubernetes does under the hood

\[\[linux networking namespaces\]\]

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

\[\[script output\]\]
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

1. Implement Observability First

- Before adding any restrictions, deploy a CNI that supports network policies (if not already using one):

   - Calico is recommended for AWS EKS

   - It provides good monitoring and policy enforcement

- Enable flow logs and monitoring to understand traffic patterns

- Consider implementing tools like:

   - Cilium for network flow visibility

   - Calico's Flow Logs

   - AWS VPC Flow Logs for external traffic

1. Start with Permissive Logging Policies
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

1. Incremental Implementation Strategy

- Start with one non-critical namespace

- Create a process for rolling out policies:

   1. Monitor normal traffic for 1-2 weeks

   2. Create permissive policies based on observed patterns

   3. Run in audit mode for 1 week

   4. Gradually tighten policies

   5. Move to enforcement mode during a maintenance window

1. Example Implementation Timeline:

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

apiVersion: [projectcalico.org/v3](http://projectcalico.org/v3)
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

apiVersion: [projectcalico.org/v3](http://projectcalico.org/v3)
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

apiVersion: [projectcalico.org/v3](http://projectcalico.org/v3)
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

## 1\. Verify Initial Connectivity

Kubectl -n Policy-test Exec Client -- Wget -q -O- --timeout=5 Nginx-1

## 2\. Apply Default Deny and Verify Isolation

Kubectl Apply -f default-deny.yaml

Kubectl -n Policy-test Exec Client -- Wget -q -O- --timeout=5 Nginx-1 # Should Fail

## 3\. Apply DNS and Web Policies

Kubectl Apply -f allow-dns.yaml

Kubectl Apply -f allow-web.yaml

## 4\. Verify Restored Connectivity

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

1. Verify initial connectivity (this should work as there are no restrictions yet):

```bash
kubectl -n policy-test wait --for=condition=Ready pod/nginx-1 pod/client
kubectl -n policy-test exec client -- wget -q -O- --timeout=5 nginx-1
```

1. Now, let's implement the default deny policy. This is crucial to understand as it's the foundation of zero trust:

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

1. Test connectivity again (this should fail):

```bash
kubectl -n policy-test exec client -- wget -q -O- --timeout=5 nginx-1
```

1. Let's add the DNS policy (necessary for name resolution):

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

1. Finally, add the specific web traffic policy:

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

1. Test connectivity one final time (should work):

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

\[Previous curriculum content would go here\]

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

1. During the Session:

- Take notes on what you learn

- Document any challenges

- Record successful implementations

- Note questions that arise

1. Suggested First Request:
   "Based on this context, please create my first hands-on exercise for understanding network namespaces. Break it down into small steps, but leave some aspects for me to figure out through exploration."

2. After Completing Exercises:

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

1. SSH into the node running your pod:

```bash
# If using EKS, you can use SSM
aws ssm start-session --target <node-id>
# Or traditional SSH if you have direct access
ssh ec2-user@<node-ip>
```

1. Find the pod's network namespace:

```bash
# List all network namespaces on the node
sudo ip netns list

# For containerd, the network namespaces are usually in:
sudo ls -l /var/run/netns/

# For Docker, they're typically in:
sudo ls -l /var/run/docker/netns/
```

1. Find the pod's container ID and network namespace:

```bash
# Get the container ID
sudo crictl pods | grep <pod-name>
sudo crictl ps | grep <pod-id>

# The network namespace will be in:
sudo ls -l /proc/<container-pid>/ns/net
```

1. Examine the network configuration inside the pod's namespace:

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