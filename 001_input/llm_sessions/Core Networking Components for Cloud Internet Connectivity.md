---
aliases: []
confidence: 
created: 2025-11-27T12:57:14Z
epistemic: 
last_reviewed: 
modified: 2025-11-27T13:03:18Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Core Networking Components for Cloud Internet Connectivity
type: 
uid: 
updated: 
---

Core Networking Components for Cloud Internet Connectivity

This report outlines the essential networking components required to establish connectivity between a private virtual network and the public internet in major cloud platforms, specifically Amazon Web Services (AWS) and Microsoft Azure. The focus is strictly on core networking infrastructure, excluding security layers such as firewalls and security groups, to address the fundamental mechanisms of traffic routing and network address translation.

Gateway Devices for Internet Connectivity

Gateway devices are the primary infrastructure components that facilitate the connection between a private cloud network and the public internet, acting as the portal for all outgoing and incoming traffic.

Internet Gateway

An Internet Gateway (IGW) is a critical, highly available, and scalable network component that serves as the bridge enabling communication between a cloud virtual network (such as a VPC or VNet) and the internet[1]. Its primary function is twofold: it provides a routing target for outbound internet traffic defined by a default route (0.0.0.0/0), and it performs Network Address Translation (NAT) for IPv4 traffic originating from private instances.

When an instance within a private network needs to send a packet to the internet, the gateway translates the instance's private source IP address to a public IPv4 address (or an Elastic IP in AWS). This translation allows the instance to initiate an outbound session while remaining logically private within the Virtual Private Cloud. For inbound traffic, the gateway performs the reverse translation, directing internet traffic back to the correct internal resource, but only in response to an established outbound session.

In the context of AWS, an Internet Gateway is a mandatory explicit component that must be created, attached to a Virtual Private Cloud (VPC), and configured in a route table to enable internet connectivity[1]. For Azure, while the functionality of an Internet Gateway exists, it is provided implicitly by the Azure network backbone. Azure automatically provides outbound internet connectivity as a default service for all Virtual Network (VNet) resources, without requiring the user to provision a separate gateway component[3]. Resources in Azure receive default outbound access via dynamic SNAT to an Azure-managed public IP, which is functionally equivalent to the NAT performed by an AWS Internet Gateway but is abstracted from the user.

- **Function:** Provides connectivity between a virtual network and the public internet; serves as a routing target for 0.0.0.0/0; performs IPv4 NAT for public subnets.
- **Cloud Equivalents:**
-   **AWS:** Internet Gateway (IGW)
-   **Azure:** Implicit internet connectivity provided by the Azure backbone (no explicit gateway deployment is required)

NAT Gateway

A NAT Gateway is a dedicated, managed service that enables instances in a private subnet (which are not assigned public IP addresses) to securely initiate outbound connections to the internet while being protected from unsolicited inbound traffic from the internet[4]. It achieves this through Source Network Address Translation (SNAT), where all outbound traffic from private instances is translated to use the public IP address assigned to the NAT Gateway itself.

This component is essential for workloads that require internet access for updates or external API calls but must not be directly addressable from the public internet for security reasons. Upon receiving a response from the internet, the NAT Gateway uses its NAT tables to reverse the translation and forward the data back to the originating private instance.

Unlike an Internet Gateway, which provides internet access directly to resources with public IPs, a NAT Gateway is specifically designed to provide outbound-only internet access from private subnets. A resource using a NAT Gateway for internet access does so via its default gateway, with the route to 0.0.0.0/0 in its subnet's route table pointing to the NAT Gateway ID, not the Internet Gateway.

The NAT Gateway exists as a first-class, fully managed service in both AWS and Azure, offering high resiliency, scalability, and ease of management compared to legacy solutions like NAT instances[6][4].

- **Function:** Enables outbound-only internet access for private instances in a subnet; performs source NAT (SNAT) using a dedicated public IP address to hide the private IP addresses of internal resources.
- **Cloud Equivalents:**
-   **AWS:** NAT Gateway
-   **Azure:** NAT Gateway

Essential Supporting Networking Components

While gateways provide the core connectivity, additional networking components are mandatory to configure and control how traffic flows between the private network and the internet.

Route Table

A Route Table is a fundamental virtual component that contains a set of rules, or routing rules, dictating how network traffic is directed from subnets within a virtual network[7][20]. It is the traffic director of the network, determining the "next hop" for packets based on their destination IP address.

For internet connectivity, a critical entry in the Route Table is the default route (`0.0.0.0/0` for IPv4 or `::/0` for IPv6). The destination of this route specifies whether the traffic should be sent directly to the internet (via an Internet Gateway) or to a NAT Gateway for translation first. A subnet is classified as "public" if its associated route table has a `0.0.0.0/0` route pointing to an Internet Gateway, and "private" if it either has no such route or if the route points to a NAT Gateway instead.

In AWS, every VPC is associated with a main route table by default, which is automatically updated when an Internet Gateway or NAT Gateway is created. In Azure, a system route table is automatically created for each subnet with a default `0.0.0.0/0` route pointing to 'Internet,' enabling outbound connectivity. Users can create User-Defined Route (UDR) tables to override this behavior for specific subnets[3][15].

- **Function:** Contains routing rules that define the next hop for network traffic based on the destination IP address; a route to `0.0.0.0/0` pointing to a gateway is required for internet access.
- **Cloud Equivalents:**
-   **AWS:** Route Table
-   **Azure:** Route Table (System routes or User-Defined Route Table)

Public IP Address

A Public IP Address is a globally routable IPv4 or IPv6 address assigned from a pool managed by the cloud provider. It is the addressable endpoint on the internet that resources within the private network use to communicate with external services[21].

For internet connectivity to function, at least one public IP is required. In AWS, an Internet Gateway itself does not have a public IP; instead, it relies on the public IPv4 address or Elastic IP Address (EIP) that is attached directly to an EC2 instance in a public subnet[1]. The Internet Gateway performs NAT between the instance's private IP and its public IP. In contrast, for a NAT Gateway, a dedicated public IP address (Elastic IP in AWS, Public IP Address in Azure) must be explicitly allocated and assigned to the NAT Gateway resource. This public IP is then used for SNAT for all outbound traffic from the private subnet[4].

Therefore, while the Internet Gateway uses an instance's or load balancer's public IP, a NAT Gateway cannot function without a dedicated public IP assigned to it. As cloud architectures evolve towards using explicit outbound methods, the Public IP Address is a critical prerequisite for the NAT Gateway to provide internet connectivity.

- **Function:** Provides a globally reachable IP address on the internet; serves as the source address for outbound traffic when translated by an Internet Gateway or NAT Gateway.
- **Cloud Equivalents:**
-   **AWS:** Elastic IP Address (for NAT Gateway or static association)
-   **Azure:** Public IP Address
Here’s the networking answer, using AWS/Azure terms but sticking to the *pure networking* bits (no security rules, IAM, etc.).

## 1. The CIDR /24 Piece

When you create a VPC (AWS) or VNet (Azure) you assign it a CIDR block, e.g.:

- `10.0.0.0/24`

You can think of that as a *set* of IP addresses.  
Those IPs are then:

- Split into **subnets** (still sets of IPs)
- Assigned to resources (VMs/instances, load balancers, gateways, etc.)

This is described in the AWS VPC docs: a VPC has a CIDR, then you add subnets and gateways to it, and associate route tables that say where traffic for various IP ranges goes [“how Amazon VPC works”](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html).

---

## 2. Inside-only vs. Talking to the Public Internet

Ignoring security and just looking at routing/devices:

You have a **private network** (VPC/VNet + subnets).  
For it to talk to the **public internet**, you need:

1. **A gateway that connects the private network to the internet**
2. **Routing** that sends “non-local” traffic to that gateway
3. **Public addressing / NAT** so private IPs can be translated to a public IP

Cloud providers implement these as virtual devices, but conceptually they map to traditional network boxes.

---

## 3. AWS: what Devices Are Involved

From a plain networking perspective (no SGs/NACLs):

### a) Public Subnets (instances Directly on the internet)

To have instances/resources that can both send traffic to and receive traffic from the public internet, you need:

1. **Internet Gateway (IGW)**
    
    - A virtual gateway **attached to the VPC**.
    - It’s the “edge router” between your VPC and the public internet.
    - [AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/how-it-works.html#vpc-access-internet) describe it as allowing instances with public IPs to communicate with the internet.
2. **Route table entry** for the subnet:
    
    - Destination: `0.0.0.0/0` (all IPv4 outside the VPC)
    - Target: the **Internet Gateway**
3. **Public IPs** on the instances (or via an Elastic IP on an attached device):
    
    - The IGW handles the mapping so externally you see the public IP.

Conceptual device list (public subnet):

- Private network: **VPC**
- Internal network segments: **Subnets**
- Gateway to internet: **Internet Gateway**
- Routing: **Route table** with `0.0.0.0/0 → IGW`

### b) Private Subnets (no Direct Inbound, but Outbound to internet)

For instances that **don’t** have public IPs but still want outbound internet (e.g. for updates):

1. **NAT device** in a *public* subnet  
    In AWS this is usually:
    
    - **NAT Gateway** (managed service), or
    - A **NAT instance** (EC2 running NAT)
2. **Route table** for the *private* subnet:
    
    - Destination: `0.0.0.0/0`
    - Target: the **NAT Gateway/instance** ENI
3. That NAT device itself needs to:
    
    - Be in a **public subnet**
    - Have a route `0.0.0.0/0 → IGW`
    - Have a **public IP** or Elastic IP

Conceptual device list (private subnet with outbound internet):

- Gateway to internet: **Internet Gateway**
- Translator between private subnet and IGW: **NAT Gateway / NAT instance**
- Routing:
    - Private subnet: `0.0.0.0/0 → NAT`
    - Public subnet hosting NAT: `0.0.0.0/0 → IGW`

AWS explicitly distinguishes these subnet types this way in the subnet docs: public subnet = route to IGW, private subnet = route via a NAT device, isolated = no routes outside VPC [AWS subnet types](https://docs.aws.amazon.com/vpc/latest/userguide/configure-subnets.html#subnet-types).

---

## 4. Azure: Roughly Equivalent Concepts

Azure names are slightly different, but conceptually the same:

- **VNet** = AWS **VPC**
- **Subnet** = same idea
- **Public IP address resource** = thing you bind to a NIC / Load Balancer / NAT gateway so it has a public presence
- **Internet connectivity**:
    - By default, outbound internet is available from a subnet unless you override routes, but to control/evolve it you typically involve:
        - **Azure NAT Gateway** (for outbound internet from private IPs)
        - **Azure Load Balancer / Public IP** for inbound public-facing services

Microsoft’s comparison article notes that both AWS VPC and Azure VNet are built on private RFC1918 ranges and have gateways for internet and hybrid connectivity [Microsoft dev blog](https://devblogs.microsoft.com/premier-developer/differentiating-between-azure-virtual-network-vnet-and-aws-virtual-private-cloud-vpc/).

Conceptually in Azure, your “devices” for internet access are:

- **Default system routing** (gives outbound internet unless overridden)
- Optional **Azure NAT Gateway** (outbound-only from private IPs)
- Optional **public IP + Load Balancer / VM NIC** (for inbound public traffic)

---

## 5. Answering Your Core Question Directly

> Not including security, just pure networking, what device(s) are needed for a private network if it wants to communicate via public internet?

Thinking in generic-network terms (then mapping to cloud):

1. **A router/gateway connecting your private network to the internet**
    
    - Cloud mapping:
        - AWS: **Internet Gateway**
        - Azure: default internet edge + optional NAT Gateway / LB + Public IP
2. **A NAT function** if your internal addresses are private RFC1918 and you don’t want your hosts to have public IPs
    
    - Cloud mapping:
        - AWS: **NAT Gateway** or NAT instance
        - Azure: **Azure NAT Gateway** or resource with a **Public IP** doing SNAT
3. **Routing configuration** so that:
    
    - Traffic destined for the internet (`0.0.0.0/0`) is forwarded to either:
        - The **Internet Gateway** (for public subnets / public IP hosts), or
        - The **NAT device**, which in turn forwards to the internet gateway

So minimal “pure networking” stack for an AWS-style private network talking to the internet:

- VPC with CIDR (your set of IPs)
- At least one subnet
- **Internet Gateway** attached to the VPC
- Optional **NAT Gateway** in a public subnet (if your workloads are “private” but need outbound)
- Route tables sending `0.0.0.0/0` to IGW (public) or to NAT (private)

If you like, I can sketch a super minimal AWS and Azure example:

- “I have `10.0.0.0/24` as my CIDR, show exact subnets, route tables, and which ‘devices’ are needed so that one VM can be public and one is private-with-outbound-only.”
Let’s specialise the earlier explanation to: **“I have a k8s/AKS cluster in a subnet in Azure – what’s needed for ingress and egress to/from the public internet, ignoring security?”**

I’ll focus on Azure-managed AKS, but the same ideas apply to a DIY k8s cluster in a VNet.

---

### 1. Context: AKS in a Subnet

You have:

- A **VNet** with CIDR, e.g. `10.0.0.0/16`
- A **subnet** where your AKS node pool lives, e.g. `10.0.1.0/24`
- Potentially another subnet just for pods (Azure CNI + pod subnet), but conceptually it’s still all inside the same private network

From here, you care about:

- **Ingress**: HTTP(S) from the internet → k8s services/pods
- **Egress**: pods/nodes → internet (for pulling images, calling APIs, etc.)

We ignore NSGs, WAF, etc. – just routing and “what devices exist”.

---

### 2. Egress from the AKS Subnet (cluster → internet)

AKS has the concept of **outboundType**, which controls **how cluster egress reaches the internet**:  
`loadBalancer` (default), `managedNATGateway`, `userAssignedNATGateway`, `userDefinedRouting`, etc. [Microsoft docs](https://learn.microsoft.com/en-us/azure/aks/egress-outboundtype).

Conceptually, you always have:

- **Private addresses** on nodes/pods in the subnet
- Some **NAT/border device** (LB or NAT Gateway or NVA) with a **public IP** that does SNAT and forwards to the internet
- **Routes** that send `0.0.0.0/0` traffic from the subnet to that device

#### 2.1 Outbound Type: `loadBalancer` (default)

Devices / components:

1. **Standard Public Load Balancer**
    
    - Created automatically by AKS
    - Has at least one **public IP**
    - Used for **egress NAT** by default
2. **Route / wiring**
    
    - AKS wires the node scale set NICs into the LB’s backend pool
    - Egress from nodes/pods goes through the LB outbound rules → translated to the LB’s public IP [AKS egress docs](https://learn.microsoft.com/en-us/azure/aks/egress-outboundtype) and [AKS egress deep dive](https://argonsys.com/microsoft-cloud/library/aks-egress-traffic-demystified/).

Conceptual picture:

- Private network: VNet + subnet
- Egress device: **Azure Load Balancer (public)** with public IP
- Route: effectively `0.0.0.0/0 → LB` (SNAT at LB, then out to internet)

#### 2.2 Outbound Type: `managedNATGateway` or `userAssignedNATGateway`

Devices / components:

1. **Azure NAT Gateway**
    
    - Azure-managed NAT on the AKS subnet (`managedNATGateway`), or
    - User-created NAT Gateway attached to the subnet (`userAssignedNATGateway`)
    - Has **one or more public IPs / IP prefixes** for SNAT
    - Handles large numbers of outbound flows [NAT Gateway with AKS](https://learn.microsoft.com/en-us/azure/aks/nat-gateway)
2. **Subnets and routes**
    
    - NAT Gateway is **bound to the subnet**
    - When bound, **all outbound internet traffic** from that subnet is NATed via those public IPs [NAT Gateway overview](https://learn.microsoft.com/en-us/azure/aks/nat-gateway) and [AKS outboundType docs](https://learn.microsoft.com/en-us/azure/aks/egress-outboundtype).

Conceptual picture:

- Private network: VNet + AKS subnet
- Egress device: **Azure NAT Gateway** on the subnet
- Route: `0.0.0.0/0 → internet`, but enforced via NAT Gateway on that subnet

#### 2.3 Outbound Type: `userDefinedRouting` (UDR) – Advanced

Here your “egress device” is **whatever your route table points to**, e.g. an Azure Firewall, NVA, proxy, or even a standard LB doing NAT. In this mode:

- AKS does **not** configure egress for you
- You:
    - Attach a **route table** to the AKS subnet
    - Add a route `0.0.0.0/0 → VirtualAppliance <NVA IP>` (e.g. Azure Firewall)
    - That appliance then does the NAT to a public IP [UDR for AKS egress](https://learn.microsoft.com/en-us/azure/aks/egress-udr)

Conceptual picture:

- Private network: VNet + subnet
- Egress device: **NVA / firewall / proxy** with public IP
- Route: `0.0.0.0/0 → NVA IP` (then NVA → internet)

---

### 3. Ingress to the AKS Subnet (internet → cluster)

Ignoring security, there are two main ingress patterns:

1. **Service of type `LoadBalancer` (public LB)**
2. **App Gateway (L7) with Ingress Controller**

#### 3.1 Service Type `LoadBalancer`

When you do:

```yaml
kind: Service
apiVersion: v1
metadata:
  name: my-service
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 8080
  selector:
    app: my-app
```

AKS (cloud provider) will:

1. **Create or reuse a Standard Public Load Balancer**
2. Create a **public IP** resource and associate it to a **frontend** on that LB
3. Create a **rule**: front-end port 80 → backend pool (node/pod IPs via kube-proxy / NodePort)

So, inbound path:

- Internet → **Public IP (LB frontend)** → LB rule → node/pod

That LB is also typically the same one used for egress in `loadBalancer` outboundType (but can be different from the NAT Gateway used when outboundType is `managedNATGateway`) [AKS egress types + LB behaviour](https://learn.microsoft.com/en-us/azure/aks/egress-outboundtype) and [AKS egress demystified](https://argonsys.com/microsoft-cloud/library/aks-egress-traffic-demystified/).

Devices for ingress here:

- **Public IP**
- **Standard Load Balancer**
- **Node ports / k8s service plumbing**

#### 3.2 Application Gateway + Ingress Controller (AGIC)

Alternative pattern (more L7-aware):

- You deploy **Azure Application Gateway** in a dedicated subnet.
- You run **AGIC** (Application Gateway Ingress Controller) in the cluster, or enable it as an AKS add‑on.
- App Gateway has a **public IP** and L7 listeners/routing rules.
- AGIC reads k8s `Ingress` objects and programs App Gateway accordingly [AKS + NAT Gateway + App Gateway example](https://learn.microsoft.com/en-us/samples/azure-samples/aks-nat-agic/aks-nat-agic/).

So inbound path:

- Internet → **Public IP on App Gateway** → HTTP(S) listener/rules → backend pools → nodes/pods

Devices for ingress here:

- **App Gateway**
- **Public IP** attached to it
- **AGIC** watching k8s Ingress resources

You can combine this with **NAT Gateway** for egress from the AKS subnets (App Gateway uses its own public IP; node/pod outbound uses NAT Gateway) [AKS + NAT Gateway + App Gateway sample](https://learn.microsoft.com/en-us/samples/azure-samples/aks-nat-agic/aks-nat-agic/).

---

### 4. Putting it Together: Minimal Mental Model

> “I have a k8s cluster in an Azure subnet. What’s needed for ingress and egress to the public internet (minus security)?”

Think in terms of **per direction**:

#### Egress (cluster → internet)

At least one of:

- **Standard Public Load Balancer** with outbound rules and public IP(s) (`outboundType=loadBalancer`), or
- **Azure NAT Gateway** attached to the cluster subnet (`outboundType=managedNATGateway` or `userAssignedNATGateway`), or
- **NVA / firewall** reached via **UDR** (`0.0.0.0/0 → VirtualAppliance`)

Plus:

- The subnet is configured so non-VNet destinations route to that device.

#### Ingress (internet → cluster)

At least one of:

- **Service type `LoadBalancer`**:
    - Creates/uses a **Public IP + Standard LB**
    - LB frontends → nodes/pods
- **Application Gateway + AGIC**:
    - Public IP on App Gateway → AG L7 rules → pods

---

If you tell me which exact AKS flavour you’re thinking of (kubenet vs Azure CNI; do you want NAT Gateway or just the default LB; do you prefer App Gateway or plain LB for ingress), I can draw a concrete ASCII diagram and list the exact Azure resources you’d expect to see in the resource group and node RG.
