---
aliases: [DNS Conditional Forwarder]
confidence:
created: 2025-07-16T17:30:03Z
epistemic:
last_reviewed:
modified: 2025-10-30T15:36:27Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status:
tags: [topic/technology/networking/dns]
title: On-Premises DNS Conditional Forwarder for Hybrid Cloud
type:
uid:
updated:
version:
---

A conditional forwarder is a configuration on a DNS server that forwards queries for specific domain names to another DNS server.

In a hybrid cloud setup, a conditional forwarder is configured on the on-premises DNS server. It is set up to redirect any query for the cloud's [[Private DNS Zones Provide Internal Network Name Resolution|private domain]] (e.g., `*.privatelink.fitfile.net`) to the inbound endpoint IP of the cloud's DNS resolver, such as the Azure DNS Private Resolver Enables Hybrid DNS.

This setup allows on-premises clients to resolve cloud-based resources using their private DNS names, which is a cornerstone of a functional [[Hybrid Cloud DNS Resolution Flow]]. This avoids having to replicate DNS records manually and ensures that the cloud environment remains the source of authority for its own private zones.
