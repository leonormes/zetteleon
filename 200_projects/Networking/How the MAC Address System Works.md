---
aliases: []
confidence: 
created: 2025-10-25T17:43:33Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T11:06:54Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: How the MAC Address System Works
type:
uid: 
updated: 
version:
---

Okay, let's break down the MAC address system.

**How the MAC Address System Works**

1. Purpose: A Media Access Control (MAC) address is a unique identifier assigned to a Network Interface Controller (NIC).1 The NIC is the hardware component (like an Ethernet port or Wi-Fi chip) that connects a device to a network.2 Its primary function is to provide a unique, hardware-level address for devices communicating on a *local* network segment.3  
2. **Layer:** MAC addresses operate at the Data Link Layer (Layer 2\) of the OSI network model. This layer is responsible for node-to-node data transfer between devices on the same physical network segment (like your home Wi-Fi network).4  
3. Format: A standard MAC address (EUI-48) is a 48-bit number.5 It's usually represented as 12 hexadecimal digits (0-9 and A-F), typically grouped in pairs and separated by colons or hyphens (e.g., 00:1A:2B:3C:4D:5E or 00-1A-2B-3C-4D-5E).6  
4. **Structure:** The 48 bits are divided into two main parts:  
   - Organisationally Unique Identifier (OUI): The first 24 bits (the first 6 hexadecimal digits, e.g., 00:1A:2B).7 This prefix identifies the manufacturer of the NIC.8 The IEEE (Institute of Electrical and Electronics Engineers) assigns these OUIs to manufacturers.9  
   - **Network Interface Controller Specific / Device Identifier:** The last 24 bits (the last 6 hexadecimal digits, e.g., 3C:4D:5E). The manufacturer assigns this part, ensuring it is unique for each device they produce within a specific OUI.  
5. **Function in Networking:** When data is sent on a local network (like an Ethernet LAN or Wi-Fi network), it's put into frames. Each frame contains the source MAC address (of the sending device) and the destination MAC address (of the receiving device on that same local network). Network switches use these MAC addresses to forward the frames only to the correct physical port connected to the destination device, making local communication efficient.10

**Is a MAC Address Globally Unique? How?**

- In Theory: Yes, MAC addresses are *designed* to be globally unique.11 The system of the IEEE assigning unique OUIs to manufacturers, and manufacturers assigning unique serial numbers within their OUI block, creates a potential address space of 248 (over 281 trillion) unique identifiers. This system ensures that, theoretically, no two NICs manufactured anywhere should have the same MAC address.  
- **In Practice:** While the system aims for global uniqueness, MAC addresses only *need* to be unique within the same Layer 2 broadcast domain (e.g., your local LAN or VLAN). It is *possible* (though rare) for duplicate MAC addresses to exist globally due to manufacturing errors, virtual machine configurations, or deliberate changing ("spoofing") of MAC addresses via software.12 However, as long as two devices with the same MAC address are not on the *same* local network simultaneously, it typically doesn't cause a problem because MAC addresses aren't used for routing across the wider internet. If a manufacturer uses up all the addresses in their assigned OUI (over 16.7 million), they must obtain a new OUI from the IEEE.

**When Did the Concept First Develop?**

The concept of the MAC address originated with the **Xerox Network Systems (XNS) Ethernet addressing scheme** developed at Xerox PARC (Palo Alto Research Centre) likely during the 1970s as part of the development of Ethernet. This 48-bit addressing scheme was later adopted for the **IEEE 802 standards**, which include Ethernet (IEEE 802.3) and Wi-Fi (IEEE 802.11).

**Was it Part of the Routable Network Spec from the Beginning?**

No, MAC addresses were not part of the *routable* network specification (like the Internet Protocol, IP) from the beginning.13

- MAC addresses operate at Layer 2 (Data Link Layer) and are intended for addressing on a *local* network segment only.14 They have a "flat" structure and contain no information about network location.15 They are not routable across different networks.  
- **IP addresses** operate at Layer 3 (Network Layer) and were designed for routing packets *between* different networks across the internet. They have a hierarchical structure (network portion and host portion).16

When a data packet travels from a computer on one network to a computer on another network across the internet, the IP addresses (source and destination) generally remain the same for the entire journey. However, the Layer 2 frame containing the packet, including the source and destination MAC addresses, is stripped and rebuilt at each router (hop) along the path. The MAC addresses used are only relevant for the specific local link between two adjacent devices (e.g., computer to router, router to next router).

Here’s a detailed answer to your questions about the MAC address (physical address) system, its uniqueness, origins, and its role in network design:

## **How Does the MAC Address (physical address) System work?**

A MAC (Media Access Control) address is a unique identifier assigned to a network interface card (NIC) by the manufacturer. It operates at the Data Link Layer (Layer 2\) of the OSI model. When devices communicate on a local network (like Ethernet or Wi-Fi), they use MAC addresses to identify the source and destination of frames. The MAC address is embedded in the hardware and is used for local delivery of data within the same network segment. When a device sends a frame, it includes both its own MAC address (source) and the recipient’s MAC address (destination) in the frame header. Switches use these addresses to forward frames to the correct device on the local network.

## **Is A MAC Address Globally Unique? How?**

Yes, MAC addresses are designed to be globally unique. Each MAC address is 48 bits (6 bytes) long and is usually written in hexadecimal (e.g., 00:1A:2B:3C:4D:5E). The first 24 bits (the first three octets) are the Organizationally Unique Identifier (OUI), which is assigned by the IEEE to hardware manufacturers. The manufacturer then assigns the remaining 24 bits uniquely to each NIC they produce. This system ensures that no two devices should have the same MAC address, making them globally unique. However, it is possible to change (spoof) a MAC address in software, and there are also locally administered addresses, but the default, factory-set MAC is intended to be unique worldwide.  
 [More details on MAC address structure and uniqueness](https://www.geeksforgeeks.org/mac-address-in-computer-network/)

## **When Did the Concept First develop?**

The concept of the MAC address originated with the development of Ethernet in the 1970s by Xerox PARC. As Ethernet became standardized (IEEE 802.3), the need for unique hardware addresses for network devices was formalized. The IEEE took over the responsibility for assigning OUIs and managing the global uniqueness of MAC addresses as part of the IEEE 802 standards.

## **Was It part of the Routable Network Spec from the beginning?**

No, MAC addresses were not designed for routable (Layer 3\) networking. They are strictly for local network identification and communication at Layer 2\. The concept of routable addressing (Layer 3\) came with the development of protocols like IP (Internet Protocol), which uses logical addresses (IP addresses) for routing data between different networks. MAC addresses are used for local delivery within a single network segment, while IP addresses are used for end-to-end communication across multiple networks.  
 [More on the distinction between MAC and IP addresses](https://www.geeksforgeeks.org/why-is-the-ip-address-called-a-logical-address-and-the-mac-address-is-called-a-physical-address/)

## **Summary**

- MAC addresses are hardware addresses used for local network communication.  
- They are globally unique by design, managed by the IEEE through the OUI system.  
- The concept dates back to the origins of Ethernet in the 1970s.  
- MAC addresses are not routable and were not intended for use beyond the local network segment; routable addressing is handled by IP addresses at Layer 3\.
