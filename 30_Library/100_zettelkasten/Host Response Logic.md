---
created: 2026-04-14T11:11:37+00:00
created_utc: "2026-04-14T10:35:00Z"
kind: mechanism
modified: 2026-04-19T18:30:42+00:00
source_title: "Networking Is Label Transformation Under Policy"
source_url: "N/A"
status: seed
tags: [host-behaviour, routing, source-tuple, tcp-ip]
title: Host Response Logic
type: atom
upstream: "[[SoT - Linux Networking Primitives]]"
---

## Host Response Logic

A host replies to the specific source IP and port tuple observed on the incoming packet. This behaviour is a fundamental property of the TCP/IP stack and operates independently of the original client's intent or real identity.

### Scope & Conditions

Standard behaviour for any host receiving a network packet; becomes critical in environments involving NAT, proxies, or load balancers.

### Evidence

> "It replies to the source IP and port on the packet that arrived."

### Implications

- If an upstream device performs NAT, the host will reply to the NAT device's IP, not the original client's.
- Incorrect source rewriting by an intermediary guarantees that the host's reply will follow an incorrect path.

### Related

- [[INSIGHT - Networking is data labeling not wires]]—shared mechanism: explains why "the wrong IP" shows up at the destination.
- [[SoT - The Architecture of Packet Encapsulation (TCP-IP)]]—shared mechanism: describes the construction of reply packets using incoming headers.

### See Also

- [[SoT - Linux Networking Primitives]]
