---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
ID: 8a11
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: key_differences_between_route_tables_and_nsg
type:
uid: 
updated: 
version:
---

## Key Differences between Route Tables and NSG

1. Purpose:
   - Route Tables: Focus on where traffic should go based on the destination IP.
   - Security Groups: Focus on what traffic is allowed to reach or leave a resource based on IP addresses, protocols, and ports.

2. Layer:
   - Route Tables: Operate at the network layer (routing level).
   - Security Groups: Operate at the transport/application layer (firewall level).

3. Scope:
   - Route Tables: Apply to a subnet or a specific route within the VPC. They affect traffic flows between subnets or external networks.
   - Security Groups: Apply to individual ENIs or instances. They control traffic to and from specific resources like EC2 instances.

4. Direction of Action:
   - Route Tables: Determine the next hop for traffic (e.g., sending it to the internet or between subnets).
   - Security Groups: Block or allow traffic at the resource level, based on rules for ports, protocols, and IP addresses.

5. State:
   - Route Tables: Are stateless. They do not track connection state. If traffic flows out, the reverse traffic is not automatically allowed back.
   - Security Groups: Are stateful. They automatically allow return traffic for established connections.

---

[route table vs NSG](<route table vs NSG>)
