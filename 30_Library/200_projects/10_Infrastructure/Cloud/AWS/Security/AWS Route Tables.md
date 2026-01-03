---
aliases: []
confidence: "null"
created: 2025-02-07T12:57:54Z
epistemic: "null"
ID: "8a9"
last_reviewed: "null"
modified: 2026-01-03T10:19:28+00:00
purpose: "null"
review_interval: "null"
see_also: []
source_of_truth: []
status: "null"
tags: ["topic/technology/networking"]
title: AWS Route Tables
type: "null"
uid: 
updated: 
version: "null"
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
