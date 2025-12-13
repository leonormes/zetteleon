---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
ID: 8a10
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: security_groups
type:
uid: 
updated: 
version:
---

## Security Groups

### Definition

A security group is a stateful firewall that controls the allowed inbound and outbound traffic for an ENI (and thus, for EC2 instances or other resources that the ENI is attached to).

Purpose: It defines what traffic is allowed to reach a resource and what traffic is allowed to leave.

Operates At: The transport and application layers (Layers 4 and 7 of the [[OSI Model]]).

### Components

Inbound Rules: Specify what traffic is allowed to enter the resource.

Outbound Rules: Specify what traffic is allowed to leave the resource.

Port and Protocol: Security groups operate based on IPs, ports, and protocols (e.g., allow TCP traffic on port 80 for HTTP).

Stateful: Security groups automatically allow return traffic, meaning if an outbound connection is initiated, the response is automatically allowed back in.

---

[route table vs NSG](<route table vs NSG>)
