---
aliases: []
confidence: 
created: 2025-02-17T11:58:11Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:51Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [ff_deploy, networking]
title: Minimum IP Requirements for a Firewall Subnet
type:
uid: 
updated: 
version: 1
---

## Minimum IP Requirements for a Firewall Subnet

For a basic firewall subnet with a single firewall instance, the minimum number of IP addresses you need is **two**. This is the same as the jumpbox scenario we discussed earlier.

Here's why:

1. **Primary IP for the Firewall:** Your firewall instance requires one private IP address to communicate within the VPC and with other networks (e.g., the internet or on-premises networks) through a NAT Gateway or VPN connection.
2. **Network Address:** Every subnet requires a network address, which is the first address in the subnet range and cannot be assigned to any instance.

## Considerations for Adding More IPs

While two IP addresses are sufficient for a basic firewall subnet, you might need to add more IPs in the following scenarios:

- **High Availability (HA):** If you want to deploy a highly available firewall solution with multiple instances for redundancy and failover, you'll need additional IP addresses for each instance.
- **Management Interfaces:** Some firewalls have separate management interfaces for administrative access. These interfaces might require dedicated IP addresses.
- **Virtual IP Addresses (VIPs):** VIPs are used for load balancing or failover scenarios. If your firewall setup uses VIPs, you'll need additional IP addresses for them.
- **External Services:** If your firewall needs to host external services, such as a web server for management or a VPN endpoint, you might need additional IP addresses for these services.

## Starting Number of IPs

As a starting point, it's reasonable to allocate a subnet with a slightly larger CIDR block than the minimum required. This provides some flexibility for future expansion or changes without wasting too many IP addresses.

A `/31` CIDR block, which accommodates two IP addresses, can be a good starting point for a simple firewall subnet. If you anticipate needing more IP addresses in the future, you can start with a larger CIDR block, such as `/30` (four IP addresses) or `/29` (eight IP addresses).

## Obsidian Markdown

Markdown

```sh
## Firewall Subnet IP Requirements

**Minimum IPs:** 2

**Why:**
* Primary IP for the firewall instance
* Network address for the subnet

**Considerations for More IPs:**
* High availability (HA) with multiple instances
* Management interfaces
* Virtual IP addresses (VIPs)
* External services

**Starting Number:**
* `/31` CIDR block (2 IPs) for basic setups
* `/30` or `/29` for potential expansion
```

Remember, you can always adjust the subnet size later if needed, but it's generally easier to start with a slightly larger subnet than to expand it later.
