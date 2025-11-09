---
aliases: []
confidence: 
created: 2025-11-03T08:46:09Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T13:48:22Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: We are using the Calico cni. It has its own set o...
type: 
uid: 
updated: 
---

You are correct. When you use Calico as your primary CNI (Container Network Interface) and IPAM (IP Address Management) plugin, you are introducing a new model.

This model is known as an **overlay network**. Your mental model is still correct, but there is now a new "virtual" layer *inside* the node layer.

Let's adjust the hierarchy based on using Calico CNI (in its most common overlay mode):

---

## **The Calico CNI Model (IPIP Overlay)**

### **1 & 2\. VNet and Node Layers**

These remain **exactly the same**.

- **VNet/Subnet:** Managed by Azure (e.g., 10.42.0.0/16).  
- **Node (VM):** Gets its IP from the subnet via Azure DHCP (e.g., 10.42.1.4).

The Azure VNet is the "underlay" network. It knows how to route traffic between your nodes (VMs).

### **3\. The Pod Layer (Calico's Overlay)**

This is where your mental model changes significantly. The Pod IPs are now in a **separate logical network** that "floats" on top of the VNet.

- **Resource:** The Pod.  
- **IP Distribution:** You define a completely separate **Pod CIDR** when you install Calico (e.g., 192.168.0.0/16). This IP range is **not** known to your Azure VNet.  
- **IP Manager:** **Calico IPAM**.  
  - **How it works:** When a new node joins the cluster, Calico's IPAM allocates it a *block* (a small subnet) from the main Pod CIDR (e.g., Node 1 gets 192.168.1.0/24, Node 2 gets 192.168.2.0/24).  
  - When a Pod is scheduled on Node 1, the **Calico CNI plugin** assigns it an IP from that node's block (e.g., 192.168.1.10).

### **The Crucial Missing Piece: How Does It Route?**

The Azure VNet has no idea how to route a packet to 192.168.1.10. This is where the overlay's "magic" happens, typically using **IPIP (IP-in-IP) encapsulation**.

Let's trace a packet from Pod A (on Node 1\) to Pod B (on Node 2):

1. **Original Packet:** Pod A (192.168.1.10) sends a packet to Pod B (192.168.2.20).  
2. **Calico Encapsulation:** The packet leaves the pod and hits the node's (Node 1\) kernel. Calico intercepts this. It sees the destination (192.168.2.20) is on Node 2 (which has the VNet IP 10.42.1.5).  
3. Calico **wraps** the *entire* original packet inside a *new* IP packet.  
   - **Original Packet (Inner):**  
     - Source: 192.168.1.10  
     - Destination: 192.168.2.20  
   - **New Packet (Outer):**  
     - Source: 10.42.1.4 (Node 1's IP)  
     - Destination: 10.42.1.5 (Node 2's IP)  
4. **VNet Transport:** The Azure VNet receives this *outer* packet. It knows how to route 10.42.1.4 to 10.42.1.5. The VNet is completely blind to the "inner" 192.168 packet.  
5. **Calico De-encapsulation:** Node 2 receives the packet. Calico sees it's an IPIP packet, "unwraps" it, and finds the original packet inside. It then routes this original packet to Pod B (192.168.2.20).

Think of it as putting a private letter (the pod packet) into a new, official postal envelope (the node packet) to get it delivered.

---

### **Alternative: Calico with BGP (No Overlay)**

There is a non-overlay (or "underlay") mode. Instead of encapsulating, Calico can use **BGP (Border Gateway Protocol)**.

In this model, the Calico agent on each node peers with the Azure network (using Azure Route Server or User-Defined Routes) and **advertises** its pod routes.

- Node 1 tells the VNet router: "Hey, if you want to reach 192.168.1.0/24, send the traffic to me at 10.42.1.4."  
- Node 2 tells the VNet router: "To reach 192.168.2.0/24, send traffic to me at 10.42.1.5."

Now, the Azure VNet *learns* the pod routes. No encapsulation is needed, which is more performant but more complex to configure.

---

### **Clarification: Calico CNI vs. Calico Network Policy**

This is a common point of confusion, especially in AKS. You can use Calico in two ways:

1. **Calico as CNI (Network \+ Policy):** This is what you've described. Calico manages IPAM and routes packets (using IPIP or BGP). This is the "full" Calico experience.  
2. **Calico as Network Policy *Only***: This is a very common setup on AKS. You would choose **Azure CNI** as your network plugin, and **Calico** as your network *policy* provider.  
   - In *this* model:  
   - **IPAM:** **Azure CNI** handles it. Pods get "real" VNet IPs (e.g., 10.42.1.35) from the node's subnet.  
   - **Routing:** Azure CNI and the VNet handle all routing natively.  
   - **Calico's Job:** Calico does *not* route. It just enforces NetworkPolicy resources (e.g., "Allow pods with label app=backend to talk to app=db on port 5432"). It acts as a distributed firewall.

So, the key question for your model is: are you using Calico *for* networking (IPAM and routing) or just *for* policy enforcement on top of another CNI?

If you are using it for networking, your model now includes a new **overlay** layer managed by Calico, which encapsulates pod traffic inside node-to-node VNet traffic.

## **Updated Summary Table (with Calico Overlay)**

| Resource | IP Address Source | Managed By |
| :---- | :---- | :---- |
| **VNet / Subnet** | You define this CIDR (e.g., 10.42.0.0/16) | **Azure Virtual Network** |
| **Node (VM)** | From the VNet Subnet (e.g., 10.42.1.4) | **Azure DHCP** |
| **Pod (Calico CNI)** | From a separate Pod CIDR (e.g., 192.168.1.10) | **Calico IPAM** |
| **Container** | *Shares the Pod's IP Address* | **Kubernetes (Kubelet)** |
| **Service (ClusterIP)** | From the Service CIDR (e.g., 10.0.10.20) | **Kube-proxy** & **CoreDNS** |
| **Pod-to-Pod Traffic** | Encapsulated in Node IP packets (e.g., IPIP) | **Calico Routing** |
