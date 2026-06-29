---
aliases:
- SSL Termination
created: 2025-10-31 09:25:29+00:00
last_reviewed: ''
modified: 2026-02-01 15:08:27+00:00
status: seedling
tags:
- load-balancing
- SoftwareEngineering/Networking
- SoftwareEngineering/Security
- ssl
- tls
title: SSL Offloading Centralises Certificate Management on the Load Balancer
type: concept
updated: null
permalink: llmeon/30-library/100-zettelkasten/ssl-offloading-centralises-certificate-management-on-the-load-balancer
---

## SSL Offloading Centralises Certificate Management on the Load Balancer

Summary: SSL offloading (or SSL termination) is the process where a load balancer handles the encryption and decryption of HTTPS traffic, relieving backend servers of this computationally expensive task.

Details: The load balancer terminates the incoming SSL connection from the client, decrypts the request, and then forwards it to the backend server as unencrypted HTTP traffic. This simplifies certificate management, as SSL certificates only need to be installed and renewed on the load balancer instead of on every individual server.

For end-to-end encryption, many load balancers also support re-encryption, where the load balancer initiates a new SSL connection to the backend server, ensuring traffic is encrypted both in transit from the client and within the internal network.