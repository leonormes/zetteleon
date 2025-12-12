---
aliases: []
confidence: 
created: 2025-10-31T13:52:20Z
epistemic: 
last_reviewed: 
modified: 2025-11-03T09:08:56Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Explain Is Technical Detail How CIDR Addressing Wo
type: 
uid: 
updated: 
---

explain is technical detail how cidr addressing works. Give examples. Also, some technics for planning vnet and subnet address spaces

CIDR (Classless Inter-Domain Routing) addressing is a method of allocating IP addresses and routing IP packets more efficiently than the older classful addressing system. Here's a detailed explanation of how CIDR works, along with examples and techniques for planning VNet and subnet address spaces:

## How CIDR Addressing Works

CIDR uses variable-length subnet masking (VLSM) to allow for more flexible allocation of IP addresses. It combines the network prefix and subnet mask into a single notation.

### CIDR Notation

CIDR notation consists of an IP address followed by a forward slash (/) and a number representing the prefix length. For example:

`192.168.1.0/24`

In this notation:

- 192.168.1.0 is the network address
- /24 indicates that the first 24 bits are used for the network portion

The prefix length can range from 0 to 32 for IPv4 addresses.

### Subnet Mask Calculation

The prefix length determines the subnet mask. To calculate the subnet mask:

1. Start with 32 bits set to 1
2. Set the rightmost (32 - prefix length) bits to 0

For example, with a /24 prefix:

`11111111.11111111.11111111.00000000 = 255.255.255.0`

### Available IP Addresses

The number of available IP addresses in a CIDR block is calculated as 2^(32 - prefix length) - 2.

For a /24 network: 2^(32-24) - 2 = 254 usable addresses

### Examples

1. 10.0.0.0/8
    - Network: 10.0.0.0
    - Subnet mask: 255.0.0.0
    - Available addresses: 10.0.0.1 to 10.255.255.254
    - Total usable addresses: 16,777,214
2. 172.16.0.0/16
    - Network: 172.16.0.0
    - Subnet mask: 255.255.0.0
    - Available addresses: 172.16.0.1 to 172.16.255.254
    - Total usable addresses: 65,534
3. 192.168.1.0/26
    - Network: 192.168.1.0
    - Subnet mask: 255.255.255.192
    - Available addresses: 192.168.1.1 to 192.168.1.62
    - Total usable addresses: 62

## Techniques for Planning VNet and Subnet Address Spaces

When planning Virtual Network (VNet) and subnet address spaces, consider the following techniques:

1. **Start with a large address space**: Begin with a large private IP range for your VNet, such as 10.0.0.0/16 or 172.16.0.0/16, to allow for future growth.
2. **Subnet sizing**: Allocate subnet sizes based on the number of resources you expect to deploy. Common subnet sizes are /24, /25, or /26.
3. **Hierarchical design**: Use a hierarchical addressing scheme. For example:
    - 10.0.0.0/16 for the VNet
    - 10.0.1.0/24, 10.0.2.0/24, etc., for subnets
4. **Reserve address spaces**: Keep some address ranges reserved for future use or expansion.
5. **Avoid overlapping**: Ensure that your VNet address space doesn't overlap with your on-premises network or other VNets you might need to connect to.
6. **Consider peering**: If you plan to use VNet peering, ensure that the address spaces of different VNets don't overlap.
7. **Use network security groups (NSGs)**: Plan your subnets with security in mind, grouping resources with similar security requirements.
8. **Special subnets**: Plan for special subnets like GatewaySubnet for VPN gateways or AzureFirewallSubnet for Azure Firewall.
9. **Documentation**: Maintain clear documentation of your address allocation to avoid conflicts and aid in troubleshooting.
10. **Use CIDR calculators**: Utilize online CIDR calculators to help plan and visualize your address spaces.

By following these techniques and understanding CIDR addressing, you can create an efficient and scalable network architecture for your cloud infrastructure
