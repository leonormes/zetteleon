---
aliases: []
created: 2025-10-24T14:25:58Z
last_reviewed: ""
modified: 2026-02-01T15:08:32+00:00
status: ""
tags: ["aws", "internet-gateway", "SoftwareEngineering/Networking", "SoftwareEngineering/networking/cloud-networking"]
title: Internet Gateway in AWS Networking
type: ""
updated: 
---

An Internet Gateway (IGW) is a horizontally scaled, redundant, and highly available VPC component that allows communication between your VPC and the internet.

- Function: It serves two primary purposes:
    1. To provide a target in your VPC route tables for internet-routable traffic.
    2. To perform network address translation (NAT) for instances that have public IPv4 addresses.
- Attachment: An IGW must be created and then attached to a specific VPC to enable external connectivity for resources within that VPC.

Without an Internet Gateway, resources in a public subnet cannot directly access or be accessed from the internet.

---

Related: [[VPC Setup for AWS ALB]], Network Address Translation (NAT)
