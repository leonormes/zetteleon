---
aliases: []
confidence: 
created: 2025-10-28T11:10:32Z
epistemic: 
last_reviewed: 
modified: 2025-10-31T09:09:16Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [networking]
title: Network Defense   Module 5 Firewall Technologies, Module 6 Zone-Based Policy Firewalls
type:
uid: 
updated: 
version:
---

## <https://youtube.com/watch?v=tDKgZNXcF7A>\&si=VmRFFpB06MCOtHTI

Here is a detailed breakdown of the content from the video "Network Defense Module 5 Firewall Technologies, Module 6 Zone-Based Policy Firewalls," focused on firewall types, their roles in network security, and the practical CLI configuration steps for Zone-Based Policy Firewalls (ZPF) on Cisco devices[^1_1].

### Firewall Technologies Overview

Firewalls are security systems (hardware/software) that enforce access control policies between networks, commonly sitting at the boundary between internal (trusted) and external (untrusted) network segments[^1_1]. Their purpose is to regulate the flow of traffic, block malicious data, and prevent exposure of sensitive resources.

#### Types of Firewalls

- **Packet Filtering Firewall**: Operates mostly at layer 3 (network) and layer 4 (transport), using simple rules to permit or deny traffic based on IP addresses and port numbers; they’re stateless, commonly implemented via access control lists (ACLs)[^1_1].
- **Stateful Firewall**: Tracks active connections and state information, permitting only traffic that matches a known, established connection (typically TCP)[^1_1]. More versatile and common in enterprise deployments, these can defend against spoofing and many denial-of-service attacks.
- **Application Gateway (Proxy) Firewall**: Functions up to layer 7 (application), mediating connections via a proxy. It inspects traffic for specific applications such as HTTP, DNS, email, etc., blocking unknown or unwanted content and hiding internal addresses from external servers[^1_1].
- **Next Generation Firewall (NGFW)**: Embeds advanced features such as intrusion detection, application awareness, and AI-driven threat prediction. These firewalls combine the basic filtering capabilities of other types with dynamic, adaptive security features[^1_1].

### Firewall Placement in Network Design

- Edge firewalls are positioned between the ISP and the internal network; may include separate LAN, WAN, and DMZ interfaces[^1_1].
- Traffic management involves strict rules for directionality: private (internal) to public (external) is inspected and permitted if established; traffic from public to private is typically blocked unless explicitly allowed.

### Zone-Based Policy Firewall (ZPF)

ZPF enhances flexibility by grouping interfaces and devices into zones and then applying security policies between these zones. This model eases management, documentation, and scalability compared to classic per-interface ACL models[^1_1]:

- **Zones** are logical groupings (private LAN, public WAN, DMZ, etc.). Policies set for a zone affect all members collectively.
- **Zone Pairs**: Policies are created between source and destination zones (e.g., private to public), defining what sessions and protocols can traverse.

#### ZPF Operation \& Configuration Steps

To configure a Zone-Based Policy Firewall in Cisco IOS CLI:

1. **Create Zones**

```shell
zone security private
zone security public
```

2. **Identify Traffic with Class Maps**

```shell
class-map type inspect match-any HTTP-TRAFFIC
  match protocol http
  match protocol https
  match protocol dns
```

3. **Define Actions with Policy Maps**

```shell
policy-map type inspect PRIVATE-TO-PUBLIC
  class type inspect HTTP-TRAFFIC
    inspect
```

4. **Define Zone Pairs and Attach Policy**

```shell
zone-pair security PRIVATE-TO-PUBLIC source private destination public
  service-policy type inspect PRIVATE-TO-PUBLIC
```

5. **Assign Zones to Interfaces**

```shell
interface GigabitEthernet0/0
  zone-member security private
interface Serial0/0
  zone-member security public
```

6. **Verification**

```shell
show run | begin class-map
```

Policies default to blocking all traffic unless explicitly allowed by a configured service-policy for a zone pair. Each interface can belong to only one zone; changing zone membership may temporarily interrupt service until fully configured[^1_1].

#### CLI Example: Permit HTTP Traffic from LAN to WAN

```shell
zone security private
zone security public

class-map type inspect match-any HTTP-TRAFFIC
  match protocol http
  match protocol https

policy-map type inspect PRIVATE-TO-PUBLIC
  class type inspect HTTP-TRAFFIC
    inspect

zone-pair security PRIVATE-TO-PUBLIC source private destination public
  service-policy type inspect PRIVATE-TO-PUBLIC

interface GigabitEthernet0/0
  zone-member security private

interface Serial0/0
  zone-member security public
```

This configuration permits HTTP/HTTPS traffic initiated internally to flow to the internet and return, while blocking unsolicited inbound connections[^1_1].

### Key Concepts and Best Practices

- Deny all traffic by default; permit only necessary services.
- Group interfaces/devices logically into zones (DMZ, private LAN, guest, etc.).
- Regularly monitor firewall logs and apply change management to configuration.
- Layered security is preferred: multiple firewall types and segmentation for defense-in-depth.
- Firewalls do not protect against all threats (internal rogue devices, improper backups, non-technical attacks)[^1_1].

### Summary Table: Firewall Types

| Firewall Type | OSI Layers | Main Features | Primary Use | Example Config Command |
| :-- | :-- | :-- | :-- | :-- |
| Packet Filtering | 3,4 | Permit/Deny by IP/Port | Perimeter filtering | access-list (classic model)[^1_1] |
| Stateful | 3,4,5 | Tracks connection state | Session management | ip inspect (classic)[^1_1] |
| Application Gateway | 3,4,5,7 | Deep packet/app inspection (proxy) | Application filtering | match protocol (ZPF)[^1_1] |
| NGFW | 3-7, AI | Intrusion prevention, adaptive | Advanced threats | Vendor-specific commands[^1_1] |

***

The video gives comprehensive insight into firewall types, pros/cons, network placement, zone pair logic, practical CLI steps for ZPF, and best practices for secure network architecture[^1_1].

<div align="center">⁂</div>

[^1_1]: <https://www.youtube.com/watch?v=tDKgZNXcF7A>\&si=VmRFFpB06MCOtHTI
