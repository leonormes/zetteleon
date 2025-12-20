---
aliases: []
confidence: 
created: 2025-02-07T12:57:54Z
epistemic: 
ID: 8a9
last_reviewed: 
modified: 2025-12-13T11:39:52Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [networking]
title: aws_route_tables
type: 
uid: 
updated: 
version: 
---

## AWS Route Tables

Definition: A route table controls the routing of network traffic within a VPC. It defines where traffic from a subnet (or specific IP range) is directed.

Purpose: It determines the path traffic takes to reach its destination, either within the VPC, across VPCs, or out to the internet.

Operates At: The network layer (Layer 3 of the [[OSI Model]]).

Components:

Destination: The IP range of the destination (e.g., `0.0.0.0/0` for all IP addresses).

Target: The next hop for the traffic (e.g., an internet gateway, NAT gateway, or a peered VPC).

Example Use: Routes traffic from a subnet to an internet gateway for external access, or between private subnets within a VPC.

Analogy: A route table is like a map for directing traffic. It says, "If traffic is destined for X network, send it via Y gateway."

[route table vs NSG](<route table vs NSG>)
