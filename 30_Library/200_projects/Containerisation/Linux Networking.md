---
aliases: []
confidence: 
created: 2025-10-22T09:39:10Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T15:59:53Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [bridge, hands-on, linux, namespaces, topic/technology/networking, tutorial, veth]
title: Linux Networking
type: map
uid: 
updated: 
version:
---

Here’s a **hands-on learning curriculum** to help you deeply understand Kubernetes networking by **building container-like networks from scratch** using **Linux network namespaces**, **veth pairs**, and **bridges**. This approach will simulate K8s *Pod-to-Pod networking* on a single host, giving you both the conceptual and the practical grounding needed before exploring [CNI plugin](https://spacelift.io/blog/kubernetes-networking) behavior and multi-node networking

---

## Phase 1: Foundations of Linux Networking

**Goal:** Get comfortable with the Linux tools and isolation primitives Kubernetes builds upon (namespaces, veth pairs, bridges, and routing).

### Step 1: Inspect Your Current Network Stack

- Examine active interfaces, routes, and namespaces:

```bash
ip addr show
ip route show
ip netns list
```

- Understand that the host namespace is the “root” context comparable to a Kubernetes node’s network namespace.

### Step 2: Create Isolated Network Namespaces

- Create two network namespaces, simulating two Pods:

```bash
ip netns add pod-red
ip netns add pod-blue
```

- Each namespace has its own interfaces and routing tables [^1_5][^1_2].

### Step 3: Connect Namespaces with a Veth Pair

- Create a virtual Ethernet "cable":

```bash
ip link add veth-red type veth peer name veth-blue
```

- Move one end to each namespace:

```bash
ip link set veth-red netns pod-red
ip link set veth-blue netns pod-blue
```

- Assign IPs and bring interfaces up:

```bash
ip -n pod-red addr add 192.168.1.1/24 dev veth-red
ip -n pod-blue addr add 192.168.1.2/24 dev veth-blue
ip -n pod-red link set veth-red up
ip -n pod-blue link set veth-blue up
```

- Test connectivity:

```bash
ip netns exec pod-red ping 192.168.1.2
```

Here you’ve created a *point-to-point* link—this mimics two directly connected pods on the same node

---

## Phase 2: Simulate a Node Network (Bridge)

**Goal:** Scale connectivity across multiple namespaces (pods) using a bridge, just like Kubernetes CNI plugins (e.g. bridge, flannel).

### Step 1: Create a Virtual Switch (bridge interface)

```bash
ip link add v-net-0 type bridge
ip link set v-net-0 up
```

### Step 2: Connect Namespaces to the Bridge

- Create veth pairs for each pod:

```bash
ip link add veth-red type veth peer name veth-red-br
ip link add veth-blue type veth peer name veth-blue-br
```

- Attach namespace ends and bridge ends:

```bash
ip link set veth-red netns pod-red
ip link set veth-red-br master v-net-0
ip link set veth-blue netns pod-blue
ip link set veth-blue-br master v-net-0
```

- Bring everything up:

```bash
ip -n pod-red link set veth-red up
ip -n pod-blue link set veth-blue up
ip link set veth-red-br up
ip link set veth-blue-br up
```

- Assign IPs:

```bash
ip -n pod-red addr add 10.0.0.2/24 dev veth-red
ip -n pod-blue addr add 10.0.0.3/24 dev veth-blue
ip addr add 10.0.0.1/24 dev v-net-0
```

Now you can ping pods from the host or between namespaces:

```bash
ip netns exec pod-red ping 10.0.0.3
```

You’ve built an isolated “virtual node” network.

---

## Phase 3: Add Realism With Routing and NAT

**Goal:** Learn what node routing and kube-proxy simulate in real clusters.

- Add a third namespace as a “Node” that routes between your pods and an external network.
- Enable packet forwarding and SNAT with iptables:

```bash
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j MASQUERADE
```

- Observe routing tables per namespace (`ip -n pod-red route`) and experiment with breaking or fixing connectivity to see how routing rules matter

---

## Phase 4: Relate to Kubernetes

**Goal:** Map your manual setup to actual Kubernetes concepts.

| Manual Concept    | Kubernetes Analogy               | Tool/Component |
| :---------------- | :------------------------------- | :------------- |
| Namespace (netns) | Pod network namespace            | Kubelet        |
| veth pair         | Pod eth0 ↔ Node bridge          | CNI plugin     |
| Linux bridge      | Node-level `cni0` (“bridge CNI”) | CNI bridge     |
| IP allocation     | Pod IP assignment (from subnet)  | IPAM plugin    |
| iptables/NAT      | kube-proxy rules, egress         | kube-proxy     |

Then review Kubernetes’ [networking model overview](https://kubernetes.io/docs/concepts/cluster-administration/networking/) to connect the theory to your hands-on setup

---

## Phase 5: Stretch Tasks

- Use `nsenter` to launch a bash shell inside each namespace and run `curl`, `tcpdump`, and `ip route` to observe containerized traffic [^1_2].
- Emulate a small Service by routing external requests from the “Node” namespace to one pod using iptables DNAT.
- Then replicate these behaviors using a lightweight Kubernetes cluster (e.g. `kind` or `minikube`) and inspect `/var/lib/cni` for the same artifacts you built.

---

**Outcome:**
You’ll have **fully understood how Kubernetes networking primitives work from first principles**, built a single-node container network stack manually, and gained the intuition needed to understand CNIs, pod-to-pod communication, and service IP routing.

Networking is a Strange Concept. it is Easy to Build Abstract Models of Nodes and Wires Going between Them like a Web. but Also, the Network Stack is just Data. Breaking Data into Packets or Chunks Adding Metadata and so on then Converting the Data to Some Sort of Transmittable Medium then Reconstructing that Data. the Actual 'web' or Wire part is just a Physical Medium. the Networking We as Devs out even Network Engineers is Handling Data and Labelling it to Organise Transport

Your reflection captures the essence of computer networking very accurately: what we call “the network” is mostly a **system for labeling, segmenting, and moving data**, not the physical wires themselves. The physical layer is only one small part of the larger conceptual process in which structured data is turned into signals and then reconstructed into meaning.

---

### Networking as an Abstraction of Data Movement

The **OSI model** is the foundational *conceptual map* that represents networking not as wires but as a hierarchy of **data transformation layers**. It divides the process into seven parts—from raw electrical or optical signals to human-readable applications [^2_1][^2_2][^2_3].

In this model, every layer adds or removes metadata describing how to interpret the data:

1. **Application layer:** Formats the information for humans or programs (e.g., HTTP or SMTP).
2. **Presentation layer:** Translates between encoding schemes (e.g., JSON, compression).
3. **Session layer:** Manages the lifetime of communication channels.
4. **Transport layer:** Breaks data into segments and ensures correct delivery (e.g., TCP).
5. **Network layer:** Adds logical addressing and routing (e.g., IP).
6. **Data link layer:** Groups packets into frames and adds MAC addressing for local delivery.
7. **Physical layer:** Converts bits into signals—electrical, optical, or radio—and transmits them [^2_2][^2_4].

Each layer treats its payload as *data*, and only the lowest layer interacts with actual physical media.

---

### The Network Stack as Data Transformation

At a functional level, the network stack is a **chain of data refinements**. Each layer adds a header containing context: source, destination, protocol, identifiers, and control information. When transmitting a message:

- Data becomes *segments* (transport).
- Segments become *packets* (network).
- Packets become *frames* (data link).
- Frames become *bits* (physical medium).

When received, this process is reversed: each layer strips away metadata until only the original message remains [^2_2][^2_5][^2_6].

---

### The Physical Layer: The Only "Real" Network

The physical media—fiber, copper, or radio—is simply a **transport for energy patterns** encoding binary values. What we perceive as a “web” of interconnected nodes is an abstraction built on top of this. Everything above the physical layer is a **model describing the movement of structured data**, not the movement of electrons or photons themselves [^2_7][^2_8][^2_9].

---

### The Practical View for Engineers

For developers and DevOps engineers, most “networking” happens above Layer 2. We’re managing **how data is labeled and routed**, not how it physically flows. IP addresses, ARP lookups, Kubernetes CNI mappings—all are logical overlays defining who gets what data, when, and how it’s verified.

That’s why your intuition is correct: modern networking is less about tangible cables and more about **information organization through metadata**. The “web” is just the stage; networking itself is the choreography of data.

**Files Read:**

**/Volumes/DAL/Zettelkasten/LLMeon/200_projects/Containerisation/Linux Networking.md**

```sh
---
version:
tags:
  - topic/technology/networking
type:
title: Linux Networking
created: 2025-10-22T09:39:10Z
modified: 2025-10-22T13:39:12Z
---

Here’s a **hands-on learning curriculum** to help you deeply understand Kubernetes networking by **building container-like networks from scratch** using **Linux network namespaces**, **veth pairs**, and **bridges**. This approach will simulate K8s _Pod-to-Pod networking_ on a single host, giving you both the conceptual and the practical grounding needed before exploring [CNI plugin](https://spacelift.io/blog/kubernetes-networking) behavior and multi-node networking

---

## Phase 1: Foundations of Linux Networking

**Goal:** Get comfortable with the Linux tools and isolation primitives Kubernetes builds upon (namespaces, veth pairs, bridges, and routing).

### Step 1: Inspect Your Current Network Stack

- Examine active interfaces, routes, and namespaces:

```bash
ip addr show
ip route show
ip netns list
```

- Understand that the host namespace is the “root” context comparable to a Kubernetes node’s network namespace.

### Step 2: Create Isolated Network Namespaces

- Create two network namespaces, simulating two Pods:

```bash
ip netns add pod-red
ip netns add pod-blue
```

- Each namespace has its own interfaces and routing tables [^1_5][^1_2].

### Step 3: Connect Namespaces with a Veth Pair

- Create a virtual Ethernet "cable":

```bash
ip link add veth-red type veth peer name veth-blue
```

- Move one end to each namespace:

```bash
ip link set veth-red netns pod-red
ip link set veth-blue netns pod-blue
```

- Assign IPs and bring interfaces up:

```bash
ip -n pod-red addr add 192.168.1.1/24 dev veth-red
ip -n pod-blue addr add 192.168.1.2/24 dev veth-blue
ip -n pod-red link set veth-red up
ip -n pod-blue link set veth-blue up
```

- Test connectivity:

```bash
ip netns exec pod-red ping 192.168.1.2
```

Here you’ve created a *point-to-point* link—this mimics two directly connected pods on the same node

---

## Phase 2: Simulate a Node Network (Bridge)

**Goal:** Scale connectivity across multiple namespaces (pods) using a bridge, just like Kubernetes CNI plugins (e.g. bridge, flannel).

### Step 1: Create a Virtual Switch (bridge interface)

```bash
ip link add v-net-0 type bridge
ip link set v-net-0 up
```

### Step 2: Connect Namespaces to the Bridge

- Create veth pairs for each pod:

```bash
ip link add veth-red type veth peer name veth-red-br
ip link add veth-blue type veth peer name veth-blue-br
```

- Attach namespace ends and bridge ends:

```bash
ip link set veth-red netns pod-red
ip link set veth-red-br master v-net-0
ip link set veth-blue netns pod-blue
ip link set veth-blue-br master v-net-0
```

- Bring everything up:

```bash
ip -n pod-red link set veth-red up
ip -n pod-blue link set veth-blue up
ip link set veth-red-br up
ip link set veth-blue-br up
```

- Assign IPs:

```bash
ip -n pod-red addr add 10.0.0.2/24 dev veth-red
ip -n pod-blue addr add 10.0.0.3/24 dev veth-blue
ip addr add 10.0.0.1/24 dev v-net-0
```

Now you can ping pods from the host or between namespaces:

```bash
ip netns exec pod-red ping 10.0.0.3
```

You’ve built an isolated “virtual node” network.

---

## Phase 3: Add Realism With Routing and NAT

**Goal:** Learn what node routing and kube-proxy simulate in real clusters.

- Add a third namespace as a “Node” that routes between your pods and an external network.
- Enable packet forwarding and SNAT with iptables:

```bash
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -s 10.0.0.0/24 -j MASQUERADE
```

- Observe routing tables per namespace (`ip -n pod-red route`) and experiment with breaking or fixing connectivity to see how routing rules matter

---

## Phase 4: Relate to Kubernetes

**Goal:** Map your manual setup to actual Kubernetes concepts.

| Manual Concept    | Kubernetes Analogy               | Tool/Component |
| :---------------- | :------------------------------- | :------------- |
| Namespace (netns) | Pod network namespace            | Kubelet        |
| veth pair         | Pod eth0 ↔ Node bridge          | CNI plugin     |
| Linux bridge      | Node-level `cni0` (“bridge CNI”) | CNI bridge     |
| IP allocation     | Pod IP assignment (from subnet)  | IPAM plugin    |
| iptables/NAT      | kube-proxy rules, egress         | kube-proxy     |

Then review Kubernetes’ [networking model overview](https://kubernetes.io/docs/concepts/cluster-administration/networking/) to connect the theory to your hands-on setup

---

## Phase 5: Stretch Tasks

- Use `nsenter` to launch a bash shell inside each namespace and run `curl`, `tcpdump`, and `ip route` to observe containerized traffic [^1_2].
- Emulate a small Service by routing external requests from the “Node” namespace to one pod using iptables DNAT.
- Then replicate these behaviors using a lightweight Kubernetes cluster (e.g. `kind` or `minikube`) and inspect `/var/lib/cni` for the same artifacts you built.

---

**Outcome:**
You’ll have **fully understood how Kubernetes networking primitives work from first principles**, built a single-node container network stack manually, and gained the intuition needed to understand CNIs, pod-to-pod communication, and service IP routing.

Networking is a Strange Concept. it is Easy to Build Abstract Models of Nodes and Wires Going between Them like a Web. but Also, the Network Stack is just Data. Breaking Data into Packets or Chunks Adding Metadata and so on then Converting the Data to Some Sort of Transmittable Medium then Reconstructing that Data. the Actual 'web' or Wire part is just a Physical Medium. the Networking We as Devs out even Network Engineers is Handling Data and Labelling it to Organise Transport

Your reflection captures the essence of computer networking very accurately: what we call “the network” is mostly a **system for labeling, segmenting, and moving data**, not the physical wires themselves. The physical layer is only one small part of the larger conceptual process in which structured data is turned into signals and then reconstructed into meaning.

---

### Networking as an Abstraction of Data Movement

The **OSI model** is the foundational *conceptual map* that represents networking not as wires but as a hierarchy of **data transformation layers**. It divides the process into seven parts—from raw electrical or optical signals to human-readable applications [^2_1][^2_2][^2_3].

In this model, every layer adds or removes metadata describing how to interpret the data:

1. **Application layer:** Formats the information for humans or programs (e.g., HTTP or SMTP).
2. **Presentation layer:** Translates between encoding schemes (e.g., JSON, compression).
3. **Session layer:** Manages the lifetime of communication channels.
4. **Transport layer:** Breaks data into segments and ensures correct delivery (e.g., TCP).
5. **Network layer:** Adds logical addressing and routing (e.g., IP).
6. **Data link layer:** Groups packets into frames and adds MAC addressing for local delivery.
7. **Physical layer:** Converts bits into signals—electrical, optical, or radio—and transmits them [^2_2][^2_4].

Each layer treats its payload as *data*, and only the lowest layer interacts with actual physical media.

---

### The Network Stack as Data Transformation

At a functional level, the network stack is a **chain of data refinements**. Each layer adds a header containing context: source, destination, protocol, identifiers, and control information. When transmitting a message:

- Data becomes *segments* (transport).
- Segments become *packets* (network).
- Packets become *frames* (data link).
- Frames become *bits* (physical medium).

When received, this process is reversed: each layer strips away metadata until only the original message remains [^2_2][^2_5][^2_6].

---

### The Physical Layer: The Only "Real" Network

The physical media—fiber, copper, or radio—is simply a **transport for energy patterns** encoding binary values. What we perceive as a “web” of interconnected nodes is an abstraction built on top of this. Everything above the physical layer is a **model describing the movement of structured data**, not the movement of electrons or photons themselves [^2_7][^2_8][^2_9].

---

### The Practical View for Engineers

For developers and DevOps engineers, most “networking” happens above Layer 2. We’re managing **how data is labeled and routed**, not how it physically flows. IP addresses, ARP lookups, Kubernetes CNI mappings—all are logical overlays defining who gets what data, when, and how it’s verified.

That’s why your intuition is correct: modern networking is less about tangible cables and more about **information organization through metadata**. The “web” is just the stage; networking itself is the choreography of data.

## Analysis of Original Note

### 1. Current Classification
**Mixed (Tutorial + Model + Multiple Facts + Mechanisms)**

### 2. Rationale

This note is a complex blend of multiple types. It begins as a **hands-on tutorial** (procedural learning guide), incorporates multiple **Factual definitions** (what is a veth pair, bridge, namespace), embeds several **Mechanism explanations** (how to connect namespaces, how bridging works), provides a **Conceptual Model** (Phase 4 table mapping Linux tools to K8s concepts), and concludes with **philosophical insight** about the nature of networking. The original note violates atomicity by mixing instructional content with conceptual understanding and multiple discrete technical facts. The most valuable atomic notes to extract are the mechanisms and factual definitions that can be linked together rather than embedded in a monolithic tutorial.

---

## Refactored Primary Note

---

**Title:** How to Build a Container Network from Scratch (Linux Namespaces Lab)
**Type:** Insight (Applied Tutorial)
**Tags:** [#k8s, #topic/technology/networking, #linux, #tutorial, #hands-on, #namespaces, #veth, #bridge]
**Links:**

- Up: [[Kubernetes Networking Model]]
- Related: [[Linux Network Namespaces]], [[How veth pairs connect network namespaces]], [[How Linux bridges forward packets]]

---

## Summary

A hands-on lab curriculum for understanding Kubernetes Pod networking by manually constructing isolated network namespaces, connecting them with veth pairs and bridges, and simulating CNI plugin behavior on a single node.

## Context / Problem

Kubernetes networking abstracts away the Linux primitives that enable Pod-to-Pod communication. Without understanding these underlying mechanisms (network namespaces, veth pairs, bridges, iptables), debugging connectivity issues or CNI failures becomes opaque. This lab builds mental models by recreating the network stack that CNI plugins automate.

## Mechanism / Details

### Phase 1: Isolated Namespaces

Create two network namespaces to simulate Pods:

```bash
ip netns add pod-red
ip netns add pod-blue


Connect them point-to-point with a [[What is a veth pair|veth pair]]:
ip link add veth-red type veth peer name veth-blue
ip link set veth-red netns pod-red
ip link set veth-blue netns pod-blue
ip -n pod-red addr add 10.0.1.1/24 dev veth-red
ip -n pod-blue addr add 10.0.1.2/24 dev veth-blue
ip -n pod-red link set veth-red up
ip -n pod-blue link set veth-blue up
```

Test: `ip netns exec pod-red ping 10.0.1.2`

See: [[How a packet flows through a veth pair]]

---

### Phase 2: Bridge for Multi-Pod Connectivity

Create a [[What is a Linux bridge|virtual switch]]:

```bash
ip link add v-net-0 type bridge
ip link set v-net-0 up
```

Connect multiple namespaces to the bridge:

```bash
ip link add veth-red type veth peer name veth-red-br
ip link set veth-red netns pod-red
ip link set veth-red-br master v-net-0
ip -n pod-red addr add 10.0.2.1/24 dev veth-red
ip addr add 10.0.2.254/24 dev v-net-0
```

See: [[How a Linux bridge learns MAC addresses and forwards frames]]

---

### Phase 3: Routing and NAT

Enable forwarding and masquerading to simulate kube-proxy egress:

```bash
sysctl -w net.ipv4.ip_forward=1
iptables -t nat -A POSTROUTING -s 10.0.2.0/24 -j MASQUERADE
```

See: [[How iptables SNAT works]], [[How kube-proxy uses iptables for Service routing]]

---

### Phase 4: Map to Kubernetes

| Linux Primitive | K8s Equivalent | Component |
|-----------------|----------------|-----------|
| `ip netns` | Pod network namespace | kubelet |
| veth pair | Pod eth0 ↔ node bridge | CNI plugin |
| Linux bridge | `cni0` bridge | CNI bridge plugin |
| IP assignment | Pod CIDR allocation | IPAM plugin |
| iptables/NAT | Service routing | kube-proxy |

See: [[Kubernetes Networking Model]]

## Connections / Implications

- **If the bridge fails**, Pods lose connectivity even on the same node
- **If IPAM fails**, Pod IPs collide or fall outside the CIDR range
- **If iptables rules break**, Services cannot route traffic to Pod backends
- This lab replicates what [[CNI plugins]] automate during Pod creation

## Questions / To Explore

- [[What is a network namespace?]]
- [[What is a veth pair?]]
- [[What is a Linux bridge?]]
- [[How does a Linux bridge learn MAC addresses?]]
- [[How does kubelet invoke CNI plugins?]]
- [[How does kube-proxy generate iptables rules?]]
- [[What is IPAM in CNI?]]
- [[How does Flannel implement cross-node networking?]]
- [[How does Calico implement cross-node networking?]]
- [[What is the CNI specification?]]

---

## Recommended Atomic Notes (To Split Out)

### Factual Notes (Definitions)

- [[What is a network namespace?]]
  - *Definition: An isolated copy of the Linux network stack (interfaces, routing tables, iptables rules)*
- [[What is a veth pair?]]
  - *Definition: A virtual Ethernet "cable" with two ends that can exist in different network namespaces*
- [[What is a Linux bridge?]]
  - *Definition: A virtual Layer 2 switch that forwards Ethernet frames between connected interfaces*
- [[What is the cni0 bridge?]]
  - *Definition: The default bridge created by the bridge CNI plugin on Kubernetes nodes*
- [[What is IPAM in CNI?]]
  - *Definition: IP Address Management - the CNI component responsible for allocating Pod IPs from a subnet*
- [[What is the OSI model?]]
  - *Definition: A 7-layer conceptual model for network communication (Application → Physical)*
- [[What does ip_forward do?]]
  - *Definition: A Linux kernel parameter that enables packet forwarding between network interfaces*

---

### Mechanism Notes (Processes to explore)

- [[How a packet flows through a veth pair]]
  - *Trace: Packet enters veth-red → kernel forwards to veth-blue → packet arrives in pod-blue namespace*
- [[How a Linux bridge learns MAC addresses and forwards frames]]
  - *Trace: Frame arrives on veth-red-br → bridge checks MAC table → if unknown, floods all ports → learns source MAC → next frame is unicast*
- [[How kubelet invokes a CNI plugin during Pod creation]]
  - *Trace: kubelet creates netns → calls CNI ADD → CNI plugin creates veth pair → attaches to bridge → assigns IP → returns result to kubelet*
- [[How kube-proxy generates iptables rules for a ClusterIP Service]]
  - *Trace: Service created → kube-proxy watches API → generates DNAT rule → traffic to ClusterIP:port → NAT to Pod IP:targetPort*
- [[How iptables MASQUERADE works for egress traffic]]
  - *Trace: Pod sends packet to external IP → hits POSTROUTING chain → MASQUERADE replaces source IP with node IP → reply comes back to node → NAT reverses translation*
- [[How the OSI model layers add and strip metadata]]
  - *Trace: Application data → Transport adds TCP header → Network adds IP header → Data Link adds Ethernet header → Physical converts to bits*
- [[How ARP resolves IP to MAC address on a Layer 2 network]]
  - *Trace: Pod wants to send to 10.0.2.2 → sends ARP request → bridge floods → pod-blue replies with MAC → sender caches MAC → sends frame*

---

### Conceptual Notes (Models to build)

- [[Kubernetes Networking Model]]
  - *Model: Every Pod gets an IP, all Pods can talk without NAT, nodes can talk to Pods, Services abstract Pod IPs with stable ClusterIPs*
- [[CNI Plugin Architecture]]
  - *Model: CNI spec defines ADD/DEL operations, plugins implement network setup, IPAM plugins allocate IPs, result is returned as JSON*
- [[The OSI Model as Data Transformation Layers]]
  - *Model: Each layer treats the layer above as "data" and adds metadata. Physical layer is the only real "network"—everything else is logical*

---

### Insight Notes (Practical Lessons to log)

- [[DEBUG - Pods cannot ping each other after bridge setup]]
  - *Symptom: `ip netns exec pod-red ping 10.0.2.2` fails. Root cause: veth interfaces not brought up. Fix: `ip -n pod-red link set veth-red up`*
- [[DEBUG - Pod can ping other Pods but not external IPs]]
  - *Symptom: Local connectivity works, internet fails. Root cause: `ip_forward=0` or missing MASQUERADE rule. Fix: `sysctl -w net.ipv4.ip_forward=1` and add iptables NAT*
- [[INSIGHT - Networking is data labeling, not physical wires]]
  - *Observation: The "network" is a stack of metadata transformations. Each layer adds headers. Only Layer 1 is physical. Everything else is logical addressing and routing*
