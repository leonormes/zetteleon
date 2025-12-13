---
aliases: []
confidence: 
created: 2025-01-18T10:15:17Z
epistemic: 
id: k8s network learning project
last_reviewed: 
modified: 2025-12-13T11:39:42Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: k8s network learning project
type:
uid: 
updated: 
version:
---

The networking aspect of Kubernetes, especially in AWS, is fascinating and complex. Let's create a bottom-up learning curriculum for networking, starting from basic Linux networking concepts up to AWS-specific implementations.

## Level 1: Linux Networking Fundamentals

- Network Namespaces & Container Networking Basics
  - Hands-on Project: Create network namespaces using `ip netns` and connect them
  - Practice connecting namespaces with virtual ethernet pairs (veth)
  - Build a simple network bridge to understand container networking
  - Create your own mini-container network to deeply understand what Kubernetes does under the hood

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
        CONTAINERS=$(kubectl get pod $pod -n $ns -o jsonpath='{.spec.containers[*].name}')

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
