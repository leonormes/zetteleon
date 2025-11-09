---
aliases: ["SSL Termination"]
confidence: 0.8
created: 2025-10-31T09:25:29Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T09:31:41Z
purpose: "Define SSL offloading and its benefits."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [load-balancing, networking, security, ssl, tls]
title: SSL Offloading Centralises Certificate Management on the Load Balancer
type: concept
uid: 
updated: 
---

## SSL Offloading Centralises Certificate Management on the Load Balancer

**Summary:** SSL offloading (or SSL termination) is the process where a load balancer handles the encryption and decryption of HTTPS traffic, relieving backend servers of this computationally expensive task.

**Details:** The load balancer terminates the incoming SSL connection from the client, decrypts the request, and then forwards it to the backend server as unencrypted HTTP traffic. This simplifies certificate management, as SSL certificates only need to be installed and renewed on the load balancer instead of on every individual server.

For end-to-end encryption, many load balancers also support **re-encryption**, where the load balancer initiates a new SSL connection to the backend server, ensuring traffic is encrypted both in transit from the client and within the internal network.
