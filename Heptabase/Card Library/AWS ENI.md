# AWS ENI

An **Elastic Network Interface (ENI)** is a critical component in AWS networking. It represents a virtual network interface that can be attached to an Amazon EC2 instance or other AWS resources. ENIs play a vital role in VPC-based networking by providing connectivity and security for resources within your [Virtual Private Cloud (VPC)](https://app.heptabase.com/c16a6d60-49a6-4aec-9d1a-6161cbbe31a8/card/849e6ec4-4ddc-469a-a7c3-619b10530072), particularly for **private Amazon EKS** deployments.

ENIs are an essential component of AWS networking that provides flexibility, security, and scalability in VPCs. In private Amazon EKS clusters, they play a key role in managing pod networking, allowing Kubernetes pods to communicate with other resources within the VPC while adhering to the security controls defined by security groups. They enable efficient and scalable private networking solutions for workloads running in Kubernetes, particularly in private, secure environments.

[The ENI represents the connection point for a resource, like an EC2 instance, into this virtual n.md](The%20ENI%20represents%20the%20connection%20point%20for%20a%20resource,%20like%20an%20EC2%20instance,%20into%20this%20virtual%20n.md)

Now, let’s break it down further:

[What is the ENI connected to!.md](What%20is%20the%20ENI%20connected%20to!.md)

**Isn't the VPC the network between resources?**

The VPC is the overarching network, but it’s subdivided into **subnets**, which are segments of the VPC's IP space. Each ENI exists inside one of these subnets, not directly at the VPC level. The ENI helps your EC2 instance communicate across this network.

1. **Front end of the ENI**:

   - This is the part of the ENI that **logically connects to the subnet**. Once the ENI is attached to a subnet, it gets an IP address from that subnet's IP range. That IP address becomes the **interface’s identity within the subnet**, just like a physical device would get an IP on a local network.

   - The IP address assigned to the ENI becomes **reachable** within the subnet, and potentially across the entire VPC (depending on security groups, route tables, and network ACLs).

2. **Handling traffic to the IP address**:

   - Once the ENI is assigned an IP address, it starts to **handle traffic** directed to that IP address. Essentially, the ENI becomes responsible for receiving and transmitting network traffic to and from that IP.

   - Any **network communication** to this IP (inside the VPC) will be directed through the ENI. The traffic flow goes from other resources/subnets through the VPC networking layer to this ENI, which then routes the traffic to the resource it's attached to (like an EC2 instance).

### Breaking it down:

[ENI gets an IP from the subnet's range.md](ENI%20gets%20an%20IP%20from%20the%20subnet's%20range.md)

[Traffic routing.md](Traffic%20routing.md)

**Reachability**: The **reachability** of the ENI's IP depends on:

**Route Tables**: Define where traffic from the subnet can go. This ensures that traffic destined for the ENI’s IP can be routed correctly.

**Security Groups**: Control what traffic is allowed into and out of the ENI.

**Network ACLs**: At the subnet level, these provide an extra layer of traffic filtering.

### Example:

- Let’s say you have an ENI with an IP `10.0.1.10` in a subnet with a CIDR range of `10.0.1.0/24`. This ENI is attached to an EC2 instance.

- Another EC2 instance in the same VPC (in a different subnet) wants to communicate with `10.0.1.10`.

   - The traffic first flows through the VPC’s routing, following the **route table** rules.

   - Once it reaches the subnet containing `10.0.1.10`, the traffic is directed to the ENI, which receives it.

   - The ENI then hands off this traffic to the attached EC2 instance.

In this way, the ENI **binds** the resource (EC2, Lambda, etc.) to the network, making it reachable via its IP address within the VPC.

[1. Elastic Network Interface (ENI).md](1.%20Elastic%20Network%20Interface%20(ENI).md)

[2. ENI and Subnets.md](2.%20ENI%20and%20Subnets.md)

---

[3. ENI IP Addressing.md](3.%20ENI%20IP%20Addressing.md)

---

[4. Traffic Handling by ENI.md](4.%20Traffic%20Handling%20by%20ENI.md)

---

[5. Security Groups.md](5.%20Security%20Groups.md)

---

[6. Subnet and VPC Relationship.md](6.%20Subnet%20and%20VPC%20Relationship.md)

---

[7. Route Tables.md](7.%20Route%20Tables.md)

---

[Network ACLs.md](Network%20ACLs.md)

---

---