---
aliases: []
confidence: 
created: 2025-05-12T12:30:53Z
epistemic: 
last_reviewed: 
modified: 2025-10-31T10:41:59Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [topic/technology/networking/dns]
title: DNS is a distributed database
type:
uid: 
updated: 
version:
---

DNS is a simple idea but is made complicated by it being distributed and massive.

When claiming a new domain, we need to fit it in to the global database. Finding an available namespace in that global tree.

## Primary and Slave Nameservers

DNS achieves distribution through primary and slave nameserver roles:

- **Primary Nameserver:**
  - Reads zone data directly from local files
  - Ultimate source of truth for its zones
  - All zone changes must be made here
- **Slave Nameserver:**
  - Gets zone data via transfers from a master (primary or another slave)
  - Provides redundancy and load distribution
  - Appears identical to resolvers (both authoritative)

## Zone Transfers

Slaves synchronize using zone transfers controlled by the zone's SOA record:

1. Slave checks master's SOA serial number
2. Initiates transfer if master's number is higher
3. Updates local zone data

**Critical SOA Fields:**
- Serial number (must increment on changes)
- Refresh/retry intervals
- Expiration timeframe

## DNS as a Distributed Key-Value Store

**Summary:** DNS functions as a distributed database mapping domain names (keys) to resource records (values), with:
- **Keys:** Hierarchical domain names (e.g., example.com)
- **Values:** Structured resource records (A, MX, etc.)
- **Partitioning:** Zones delegate authority for subdomains

**Characteristics:**
- Eventual consistency (through zone transfers)
- High read throughput (caching resolvers)
- Write bottlenecks at zone apexes

**Common Use Cases:**
- Web browsing (A/AAAA records)
- Email routing (MX records)
- CDN optimization (CNAME aliasing)
- Email security (TXT records for SPF/DKIM)
- Service discovery (SRV records)

**Zone File Example:**

```sh
$ORIGIN example.com.
$TTL 86400
@ IN SOA ns1.example.com. admin.example.com. (
    2023102701 ; Serial
    3600       ; Refresh
    1800       ; Retry
    604800     ; Expire
    86400 )    ; Minimum TTL

@    IN A     93.184.216.34
www  IN CNAME @
     IN MX 10 mail.example.com.
```

[[How Computers Identify Each other on a Network]]
