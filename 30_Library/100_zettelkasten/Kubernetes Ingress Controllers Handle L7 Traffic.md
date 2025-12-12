---
aliases: [Ingress Controller]
confidence: 
created: 2025-07-16T17:30:03Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T10:27:46Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [http, ingress, topic/technology/kubernetes, topic/technology/networking]
title: Kubernetes Ingress Controllers Handle L7 Traffic
type:
uid: 
updated: 
version:
---

An Ingress Controller (like NGINX) is a component within a Kubernetes cluster that manages external access to the services in the cluster, typically handling HTTP and HTTPS traffic (Layer 7).

When a DNS query, such as for `app.privatelink.fitfile.net`, resolves to the Ingress Controller's internal IP address, the controller receives the subsequent traffic. It then uses the rules defined in an Ingress resource to route the request to the correct internal service based on the hostname or URL path.

The primary protocols handled are HTTPS (port 443) and HTTP (port 80). This aligns with the [[Layer 7 Application Layer]] of the OSI model, where application-specific protocols are managed.

**Prerequisite Knowledge:**
- [[30_Library/100_zettelkasten/Containers Within a Pod Share Network Namespace and IP Address]]
- Ingress operates at cluster edge while pod networking handles internal traffic
