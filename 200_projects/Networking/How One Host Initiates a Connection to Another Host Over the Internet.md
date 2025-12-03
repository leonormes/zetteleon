---
aliases: []
confidence:
created: 2025-11-26T04:45:04Z
epistemic:
last_reviewed:
modified: 2025-11-26T16:46:07Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [networking/tcp]
title: How One Host Initiates a Connection to Another Host Over the Internet
type:
uid:
updated:
---

## High-Level Overview

When a user or application on one device (the client) wants to connect to another device (the server) over the internet—such as visiting a website—a series of layered, coordinated processes take place. The journey begins with resolving a human-readable domain name (like `www.example.com`) into a machine-readable IP address using the **Domain Name System (DNS)**. Then, a reliable connection is established via the **Transmission Control Protocol (TCP) three-way handshake** before any actual data exchange occurs. Throughout this process, data undergoes **encapsulation** at each networking layer (application, transport, network, and data link), gaining headers that ensure correct routing, delivery, and interpretation by the destination host. Routers, switches, gateways, and other network components work together across these layers to forward packets across complex, interconnected networks—forming the backbone of global internet communication.

This report provides a comprehensive, step-by-step breakdown of the entire connection initiation process, explaining what happens at each stage, how protocols interact across layers, how addressing works (IP, port, MAC), and why each mechanism is essential for reliable end-to-end communication.

---

## Step-by-Step Walkthrough: Connecting to [www.example.com](http://www.example.com/)

We’ll use a concrete example: You open a web browser and type `https://www.example.com`. We will trace the complete lifecycle from that moment until a secure, bidirectional TCP connection is established between your laptop (client) and the remote web server.

Assumptions:

- Your computer has already obtained an IP address (e.g., via DHCP).
- It has internet connectivity through a home router acting as a **default gateway**.
- We're connecting over HTTPS, which uses **TCP port 443**.
- The client’s IP address: `192.168.1.100`
- Default gateway (router): `192.168.1.1`
- DNS resolver: Google Public DNS at `8.8.8.8`
- Target server: `www.example.com` → resolved IP: `93.184.216.34`

---

### Step 1: Application Layer — Initiating the Request and DNS Resolution

#### Action

You type `https://www.example.com` in your browser and press Enter. The browser parses the URL and recognizes:

- **Protocol**: HTTPS (which implies TCP + TLS encryption)
- **Hostname**: `www.example.com`
- **Path**: `/` (default)

Since computers communicate using numerical IP addresses—not domain names—the browser must first determine the **IP address** associated with `www.example.com`. This translation is performed by the **Domain Name System (DNS)**.

#### What Is DNS

**DNS (Domain Name System)** is a hierarchical, distributed directory service that maps domain names to IP addresses. Think of it as the "phonebook of the internet"—users look up a name (`www.example.com`), and DNS returns the corresponding number (its IP address).

#### DNS Resolution Process

The resolution proceeds as follows:

1. **Local Cache Check**
    - The browser first checks its own cache.
    - If not found, it asks the operating system, which may check:
        - Browser cache
        - OS DNS resolver cache
        - Hosts file (e.g., `C:\Windows\System32\drivers\etc\hosts`)
2. **Recursive Query to DNS Resolver**
    - If no cached result exists, the OS sends a **DNS query** to the configured **DNS resolver** (e.g., `8.8.8.8`).
    - This query is sent using **UDP port 53**, unless the response exceeds 512 bytes, in which case **TCP port 53** is used (per RFC 1035 and RFC 6891).
3. **Resolver Performs Recursive Lookup**
    - The resolver acts on your behalf to find the answer:
        - Queries a **root DNS server** → learns about `.com` TLD servers.
        - Queries a **top-level domain (TLD) server** for `.com` → learns about `example.com`'s authoritative name servers.
        - Queries the **authoritative name server** for `example.com` → obtains the A record (IPv4 address) for `www.example.com`.
4. **Response Returned**
    - The authoritative server replies:  
        `www.example.com` → `93.184.216.34`
    - This result is cached at various levels (resolver, OS, browser) for a time defined by the **Time-to-Live (TTL)** value in the DNS record.

> **Example**: Suppose TTL is set to 3600 seconds (1 hour). During this time, future requests skip the full lookup.

#### Encapsulation During DNS Query

At this stage, we generate our first real packet. Let’s walk through **data encapsulation**—the process of adding headers at each layer as data moves down the network stack.

|Layer|Data Construct|Header Added|Purpose|
|---|---|---|---|
|Application|DNS Query|None (raw message format per RFC 1035)|Contains query for `www.example.com`|
|Transport|UDP Segment|Source Port: 54321 (ephemeral)  <br>Destination Port: 53  <br>Length, Checksum|Enables multiplexing; identifies DNS service|
|Network|IP Packet|Source IP: 192.168.1.100  <br>Dest IP: 8.8.8.8  <br>TTL=64  <br>Protocol=17 (UDP)|Logical addressing; used by routers for forwarding|
|Data Link|Ethernet Frame|Src MAC: a1:b2:c3:d4:e5:f6  <br>Dest MAC: XX:XX:XX:XX:XX:XX (gateway’s MAC)  <br>EtherType=0x0800 (IPv4)  <br>FCS trailer|Physical delivery within local network|

Before sending the frame, the client must know the **MAC address** of the next hop (the default gateway, since `8.8.8.8` is not on the local subnet). If unknown, **ARP** is used (see Step 2).

#### Why DNS Is Necessary

- **User Experience**: Users remember names better than numbers.
- **Scalability**: Domain names abstract server locations; IP addresses can change without affecting URLs.
- **Redundancy & Load Balancing**: Multiple IP addresses can map to one domain, enabling failover and geolocation routing.

---

### Step 2: Data Link Layer — Address Resolution Protocol (ARP)

#### Problem

To send the DNS query (and later, the TCP SYN), the client must transmit an Ethernet frame to the **default gateway** (`192.168.1.1`). But Ethernet frames require **destination MAC addresses**, not IP addresses.

The client checks its **ARP cache** (Address Resolution Protocol table) to see if it already knows the MAC address corresponding to `192.168.1.1`.

> Example command to view ARP cache:  
> `arp -a` (on Windows/Linux/macOS)

If not found, **ARP** is triggered.

#### ARP Request and Reply

1. **ARP Request (Broadcast)**
    
    - The client broadcasts a frame: “Who has IP address `192.168.1.1`? Tell `192.168.1.100`”
    - Destination MAC in the Ethernet header is set to `ff:ff:ff:ff:ff:ff` (broadcast).
    - This frame is received by all devices on the local network segment.
2. **Router Responds**
    
    - The default gateway (router) sees the request, matches its own IP, and replies directly:
        - “`192.168.1.1` is at MAC address `aa:bb:cc:dd:ee:ff`”
    - Reply is unicast back to the client.
3. **Client Updates ARP Cache**
    
    - The client stores this mapping (`192.168.1.1` ↔ `aa:bb:cc:dd:ee:ff`) for a few minutes (cache timeout varies by OS).

Now the client can correctly fill in the **destination MAC address** in the Ethernet header for any outgoing packet destined beyond the local network.

#### Why ARP Is Necessary

- **Layer Separation**: IP addresses (Layer 3) don’t carry enough information for physical delivery on a shared medium like Ethernet.
- **MAC Uniqueness**: Each network interface has a globally unique hardware identifier (MAC), allowing precise delivery within a **broadcast domain** (a LAN segment).

---

### Step 3: Transport Layer — TCP Three-Way Handshake

#### Goal

Now that the client knows the server’s IP address (`93.184.216.34`), it must establish a **reliable, bidirectional connection** before sending HTTP data. This is done using **TCP (Transmission Control Protocol)**.

> **TCP vs UDP**: Unlike UDP, TCP is **connection-oriented**. It ensures data arrives in order, retransmits lost segments, and manages flow control.

#### Connection Setup: The Three-Way Handshake

This exchange synchronizes sequence numbers and confirms both parties are ready.

##### 1. SYN (Client → Server)

- The client sends a **SYN (synchronize)** packet:
    - Chooses a random **initial sequence number** (ISN), e.g., `1000`.
    - Sets the **SYN flag** to `1`.
    - Source Port: `54322` (ephemeral port chosen by OS)
    - Destination Port: `443` (HTTPS)
- IP Header:
    - Source IP: `192.168.1.100`
    - Destination IP: `93.184.216.34`
    - TTL: `64`
    - Protocol: `6` (TCP)
- Data Link:
    - Dest MAC: `aa:bb:cc:dd:ee:ff` (gateway)
    - Src MAC: `a1:b2:c3:d4:e5:f6`

This packet says: "I want to start a connection; my starting sequence number is 1000."

##### 2. SYN-ACK (Server → Client)

- The server receives the SYN.
- If accepting, replies with a **SYN-ACK** packet:
    - Sets **SYN=1**, **ACK=1**
    - Acknowledges client’s ISN: `Ack = 1001` (1000 + 1)
    - Sends its own initial sequence number: `Seq = 500`
- This confirms: "Got your request; here’s my starting number."

Note: The packet traverses back through the internet, undergoing similar IP routing and encapsulation.

##### 3. ACK (Client → Server)

- The client sends a final **ACK**:
    - Sets **ACK=1**
    - Acknowledges server’s ISN: `Ack = 501` (500 + 1)
    - No data yet; this completes the handshake.

After this third packet, both hosts have:

- Agreed on initial sequence numbers
- Confirmed round-trip connectivity
- Established connection state (including window sizes, etc.)

> The connection is now **fully established**. Data transfer (e.g., HTTP request) can begin.

#### Detailed TCP Header Fields (SYN Packet Example)

|Field|Value|Explanation|
|---|---|---|
|Source Port|54322|Client-side ephemeral port|
|Destination Port|443|Standard port for HTTPS|
|Sequence Number|1000|Chosen randomly for security and uniqueness|
|Acknowledgment Number|0|Not valid until ACK flag is set|
|Flags|SYN=1|Indicates synchronization|
|Window Size|65535 bytes|Flow control—how much data receiver can accept|
|Checksum|Computed|Ensures segment integrity|
|Options|MSS, SACK, etc.|Optional features (e.g., Maximum Segment Size)|

> The SYN packet typically includes **MSS (Maximum Segment Size)** option: tells the peer the largest payload it can accept in a single TCP segment (usually 1460 bytes on Ethernet).

#### Why the Three-Way Handshake

- Prevents **ambiguity from old/duplicate SYN packets** (e.g., delayed from a previous connection attempt).
- Ensures both sides can **send and receive** data (bidirectional readiness).
- Establishes **synchronized sequence numbers**, enabling reliable recovery from packet loss.

Without it, TCP couldn't guarantee reliability or reassembly order.

---

### Step 4: Network and Data Link Layers — IP Routing and Packet Forwarding

Every packet—whether DNS query, ARP broadcast, or TCP SYN—must be delivered across potentially thousands of miles and hundreds of network links. This is achieved through **IP routing** and **packet forwarding**.

#### IP Addressing and Subnetting

Each host has:

- A **IP address**: a logical, hierarchical identifier (e.g., `192.168.1.100`)
- A **subnet mask**: defines what portion belongs to the network (e.g., `/24` or `255.255.255.0` means first 24 bits identify network)

The client calculates:

- Its network: `192.168.1.0/24`
- Destination network: `93.184.216.34` → belongs to `93.184.216.0/24` → **different network**

So, the packet cannot be sent directly. It must go to the **default gateway** (`192.168.1.1`)—the router responsible for forwarding traffic outside the local network.

#### Role of the Router (Packet Forwarding Process)

Let’s trace the **first TCP SYN packet** as it leaves the client and enters the first router.

1. **Ethernet Frame Arrival**
    
    - The router receives the frame on its local interface (`192.168.1.1`).
    - Validates FCS (Frame Check Sequence) for errors.
    - Strips off Ethernet header (**decapsulation** at Data Link Layer).
2. **Inspect IP Header**
    
    - Sees destination IP: `93.184.216.34`
    - Checks its **routing table** using **longest prefix match**.

    Example routing table entry:

    ```sh
    Destination     Gateway         Genmask         Flags   Iface
    0.0.0.0         203.0.113.1     0.0.0.0         UG      eth1
    192.168.1.0     0.0.0.0         255.255.255.0   U       eth0
    ```

    → No specific route for `93.184.216.0/24`, so uses **default route** (`0.0.0.0/0`) → next hop: `203.0.113.1`

3. **Modify and Re-Encapsulate**
    
    - Decrease **TTL (Time to Live)** by 1: from `64` → `63`
        - Prevents packets from looping forever.
    - Recompute IP header checksum.
    - Determine outgoing interface and next-hop MAC address:
        - Uses **ARP** (if not cached) to learn MAC of `203.0.113.1`
    - Encapsulate IP packet in a new **data link frame** (e.g., Ethernet, PPP, or MPLS depending on link type).
4. **Forward**
    
    - Send frame out via correct interface.

This process repeats at **every router** along the path (called **hops**) until the packet reaches the destination network.

#### BGP, Routing Tables, and Internetworking

Routers use dynamic routing protocols like **BGP (Border Gateway Protocol)**, **OSPF**, or **IS-IS** to learn routes to remote networks. The internet consists of **Autonomous Systems (AS)**, each maintaining routing policies.

> For example, your ISP’s router peers with others via BGP to learn how to reach `93.184.216.0/24` (owned by example.com’s hosting provider).

Each router independently applies **longest prefix match** to determine the next hop.

#### Role of Switches

Unlike routers, **switches** operate at the **data link layer (Layer 2)**. They:

- Receive frames on one port
- Learn **source MAC → port** mappings
- Forward frames only to the port where the **destination MAC** resides (using MAC address table)
- Reduce unnecessary broadcasts (compared to hubs)

> Example: When the client sends the first ARP broadcast, the switch floods it to all ports. After the gateway responds, the switch records `aa:bb:cc:dd:ee:ff` → Port 1.

From then on, frames for `aa:bb:cc:dd:ee:ff` go directly to the gateway’s port.

---

### Step 5: Role of Key Network Devices

|Device|Layer|Function|Example|
|---|---|---|---|
|**Switch**|Data Link (L2)|Forwards frames within a **local area network (LAN)** using **MAC addresses**. Learns port-to-MAC mappings dynamically.|Connects devices in your office/home network|
|**Router**|Network (L3)|Routes packets between **different IP networks** using **IP addresses** and **routing tables**. Performs TTL decrement and fragmentation if needed.|Your home router connecting LAN to the internet|
|**Gateway**|Network/Data Link|A **node that interfaces between networks**. Often a router with both private (LAN) and public (WAN) IP addresses. Serves as the **default gateway** for hosts.|`192.168.1.1` on your laptop’s configuration|

> Note: "Gateway" is a functional term; in most cases, it refers to the local **router interface**.

---

### Step 6: Data Encapsulation and Decapsulation Recap

As data travels **down** the protocol stack on the sender side, each layer adds a **header** (and sometimes a trailer), wrapping the payload from the layer above. This is **encapsulation**.

On the receiver side, each layer removes its header and passes the payload up—this is **decapsulation**.

Let's look at full encapsulation when the client sends the **first TCP SYN packet**.

#### Outbound Packet (Client → Server): Encapsulation

1. **Application Layer**
    
    - **Data**: No headers yet; just the intent to connect (no application data yet, since connection isn't established).
    - *Note*: Actual HTTP request comes **after** TCP handshake.
2. **Transport Layer (TCP)**
    
    - Add **TCP header**:
        - Src Port: `54322`
        - Dst Port: `443`
        - Seq: `1000`
        - SYN=1
        - Window: `65535`
        - Checksum
    - Result: **TCP segment**
3. **Network Layer (IP)**
    
    - Add **IP header**:
        - Src IP: `192.168.1.100`
        - Dst IP: `93.184.216.34`
        - TTL: `64`
        - Protocol: `6` (TCP)
    - Result: **IP packet**
4. **Data Link Layer (Ethernet)**
    
    - Add **Ethernet frame header**:
        - Src MAC: `a1:b2:c3:d4:e5:f6`
        - Dst MAC: `aa:bb:cc:dd:ee:ff` (gateway)
        - EtherType: `0x0800` (IPv4)
    - Add **FCS (Frame Check Sequence)** trailer for error detection
    - Result: **Ethernet frame**

> This frame is transmitted over physical media (e.g., Wi-Fi, Ethernet cable)

#### Inbound Processing (Server Side): Decapsulation

At the destination server:

1. **Data Link Layer**
    
    - Receive frame; verify FCS.
    - Strip Ethernet header/trailer.
    - Pass IP packet to Layer 3.
2. **Network Layer**
    
    - Read destination IP: if matches local interface (or VIP), continue.
    - Check TTL: if >0, proceed.
    - Protocol field = 6 → pass payload to **TCP module**.
3. **Transport Layer**
    
    - TCP subsystem reads destination port (`443`) → delivers to listening web server (e.g., nginx, Apache).
    - Processes SYN flag and sequence number → prepares SYN-ACK response.
4. **Application Layer**
    
    - Web server receives request (only after handshake completes and application data is sent).

> Note: The TCP connection state is now established at both ends.

---

## Summary Flow: Full Connection Initiation from Client to Server

Here is the complete, ordered flow when connecting to `www.example.com`:

1. **User Action**: Type `https://www.example.com` in browser.
2. **DNS Resolution**:
    - Browser checks caches; no result.
    - OS sends **DNS query** (UDP port 53) to resolver (`8.8.8.8`).
    - Resolver performs recursive lookup.
    - Returns IP: `93.184.216.34`.
3. **ARP Resolution**:
    - Client checks ARP cache for gateway (`192.168.1.1`).
    - Sends **ARP broadcast**: “Who has 192.168.1.1?”
    - Gateway replies: “It’s me, MAC=aa:bb:cc:dd:ee:ff”.
4. **TCP Three-Way Handshake**:
    - **SYN**: Client → Server (Seq=1000, SYN=1)
    - **SYN-ACK**: Server → Client (Seq=500, Ack=1001, SYN=1, ACK=1)
    - **ACK**: Client → Server (Ack=501, ACK=1)
5. **Connection Established**:
    - Bidirectional path set up.
    - Client can now send **HTTP request** securely over TLS (for HTTPS).

---

## Encapsulation Overview Table

|Layer|PDU (Protocol Data Unit)|Key Headers Added|Purpose|
|---|---|---|---|
|Application|Message/Data|None|User-level data (e.g., HTTP request)|
|Transport|Segment (TCP) / Datagram (UDP)|Src/Dest Port, Seq/Ack, Flags, Window|End-to-end communication; port multiplexing; reliability (TCP)|
|Network|Packet|Src/Dest IP, TTL, Protocol|Logical addressing; routing across networks|
|Data Link|Frame|Src/Dest MAC, EtherType, FCS|Physical delivery within LAN; error detection|

> **PDU** = Protocol Data Unit: the unit of data at each layer.

---

## Why Each Mechanism Is Necessary

|Mechanism|Purpose|Why It’s Critical|
|---|---|---|
|**DNS**|Translates `www.example.com` → `93.184.216.34`|Enables human-friendly access; abstracts server changes|
|**TCP Handshake**|Establishes bidirectional session|Ensures reliable connection setup; prevents duplicate connections|
|**IP Addressing & Routing**|Routes packets across networks|Makes internetworking possible; scalable addressing|
|**ARP & MAC Addressing**|Maps IP → MAC for local delivery|Required for Ethernet switching within LAN|
|**Routers**|Forward packets between networks|Connect disparate networks; maintain routing tables|
|**Switches**|Forward frames within LAN|Reduce collisions; efficient local delivery|
|**Gateway**|Entry/exit point from local network|Connects private network to public internet|

---

## Final Thoughts: The Power of Layered Architecture

The entire process—from URL entry to connection establishment—relies on the **layered model** of networking (TCP/IP or OSI). Each layer:

- Provides a specific service
- Hides complexity from others (abstraction)
- Communicates only with peer layers on the remote host

This **modular, hierarchical design** allows:

- Independent evolution of protocols (e.g., IPv6 replacing IPv4)
- Interoperability between diverse hardware and software
- Robustness and scalability of the global internet

By understanding each step—not just **what** happens, but **how** and **why**—you build a solid mental model of how networked communication truly works. Every interaction online, from loading a webpage to streaming video, traces this same foundational path.

> Mastery begins here: in the details of DNS, TCP, IP, and ARP—and the elegant dance of encapsulation that binds them all.
