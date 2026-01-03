---
aliases: ["DNS Architecture", "FQDN", "Hierarchical Naming", "Reverse DNS"]
confidence: "5/5"
created: 2025-03-04T13:42:19Z
epistemic: "theory"
last_reviewed: "2025-12-23"
modified: 2025-12-26T18:18:09+00:00
purpose: "To define the Domain Name System as a hierarchical naming architecture for unique host identification and service discovery."
review_interval: "6 months"
see_also: ["[[SoT - Cloud Networking Core Components]]", "[[SoT - The Data-Centric Theory of Networking]]"]
source_of_truth: []
status: "stable"
tags: ["architecture", "data-centric", "topic/technology/networking/dns", "topic/technology/networking", "topic/technology"]
title: SoT - The Data Architecture of DNS
type: "SoT"
uid: 
updated: 
---

## 1. Definitive Statement

> [!definition] Definition
> **DNS (Domain Name System)** is a distributed hierarchical database designed to assign globally unique, human-readable labels (**Fully Qualified Domain Names**) to network resources. It functions as a layer of indirection that maps service names to physical or virtual addresses.

---

## 2. The Naming Hierarchy & FQDN

DNS operates on a tree structure where each resource is identified by a **Fully Qualified Domain Name (FQDN)**. An FQDN specifies the exact location in the DNS hierarchy, including all domain levels up to the implicit root zone (represented by a final trailing dot).

- **Root Zone:** The top of the tree (e.g., `.`).
- **Top-Level Domain (TLD):** Broad categories (e.g., `.net`, `.com`, `.uk`).
- **Second-Level Domain (SLD):** The registered brand or zone (e.g., `fitfile`).
- **Subdomain / Hostname:** The specific service or machine label (e.g., `relay`).

**Canonical Format:** `[hostname].[domain].[tld].` (e.g., `news.bbc.co.uk.`)

---

## 3. Disambiguating "Hostname"

The term "hostname" is context-dependent and frequently conflated:

1. **OS Identity (Nodename):** The local identity defined in `/etc/hostname` (e.g., `prod-web-34`). Used for local identification within a LAN.
2. **Service Identifier:** The leftmost label of an FQDN (e.g., `www` in `www.example.com`). This represents a *logical service* rather than a physical machine.

Modern architecture achieves **Elasticity** by mapping one logical service name to many ephemeral machine identities.

---

## 4. The Two-Step Communication Protocol

The decoupling of service identity from network location is facilitated by two sequential operations:

1. **DNS Lookup (Location):** The client queries the DNS for an **A/AAAA record**. The system returns the IP address (the "front door").
2. **HTTP Request (Identity):** The client establishes a connection to the IP and sends an HTTP request containing the **Host Header**. This header specifies the intended service (the "office inside the building"), allowing for **Virtual Hosting").

---

## 4. Common Record Types (The Directory)

DNS records map labels to specific information types:

| Type | Name | Mapping | Purpose |
|:--- |:--- |:--- |:--- |
| **A** | Address | Hostname -> IPv4 | Standard resource location. |
| **AAAA**| Quad-A | Hostname -> IPv6 | Modern address location. |
| **CNAME**| Canonical | Hostname -> Hostname | Aliasing one name to another (e.g., `www` to `root`). |
| **MX** | Mail Exchanger | Domain -> Mail Server | Routing email traffic. |
| **PTR** | Pointer | IP -> Hostname | **Reverse DNS (rDNS)**; verifying who an IP belongs to. |

---

## 5. Reverse DNS (rDNS)

While forward DNS maps names to numbers, **PTR records** map numbers back to names.

- **Asymmetry:** The forward and reverse mappings do not have to match (e.g., `relay.fitfile.net` -> `1.2.3.4`, but `1.2.3.4` -> `proxy.isp.net`).
- **Use Case:** Crucial for security verification in email servers and logging.

---

## 6. Summary

DNS is the phonebook of the internet. It makes hostnames actionable by providing the technical mechanism to resolve a conceptual "Name" into a routable "Address."
