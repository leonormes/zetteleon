---
aliases: [Hybrid DNS]
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
title: Hybrid Cloud DNS Resolution Flow
type:
uid:
updated:
version:
---

In a hybrid cloud environment that connects a remote private network (like an AWS-based SDE) to a cloud VNet (like Azure) via an on-premises network (CUH), DNS resolution for private endpoints follows a specific path:

1. Initiation: A remote application (SDE) makes a DNS query for a private cloud resource, like `app.privatelink.fitfile.net`.
2. Forward to On-Premises: The remote site's DNS is configured to forward the query to the main on-premises DNS server (CUH).
3. Conditional Forwarding to Cloud: The [[On-Premises DNS Conditional Forwarder for Hybrid Cloud|on-premises DNS server]] has a rule to forward any query for the `privatelink.fitfile.net` domain to the Azure DNS Private Resolver Enables Hybrid DNS|Azure DNS Private Resolver's inbound IP.
4. Private Zone Resolution: The Azure resolver looks up the name in the corresponding [[Private DNS Zones Provide Internal Network Name Resolution|Azure Private DNS Zone]] and finds the internal IP address of the target service (e.g., a Kubernetes Ingress Controller).
5. Response: The resolved internal IP is returned along the same path to the initiating application.

This entire flow happens over private connections (VPN/Direct Connect/ExpressRoute), ensuring that no part of the resolution for the private domain is exposed to the public internet. This illustrates a practical application of the concepts in [[Cloud Network]].
