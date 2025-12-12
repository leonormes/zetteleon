---
aliases: []
confidence:
created: 2025-10-31T09:25:39Z
criteria: Steps and concepts directly related to the NetworkChuck tutorial on Kemp LoadMaster.
epistemic:
exclusions: General load balancing theory or other vendor products.
last_reviewed:
modified: 2025-12-07T18:13:51Z
purpose:
review_interval:
scope: A procedural guide for setting up a Kemp LoadMaster in a home lab for secure service exposure.
see_also: []
source_of_truth: []
status:
tags: [homelab, kemp, networking, tutorial]
title: MOC - Setting up a Kemp Load Balancer in a Home Network
type: map
uid:
updated:
---

## MOC - Setting up a Kemp Load Balancer in a Home Network

This map of content outlines the process for setting up a Kemp LoadMaster virtual appliance in a home network to securely expose multiple internal services. It is based on the walkthrough provided by NetworkChuck.

### Core Concepts

- [[A Load Balancer Distributes Traffic for Reliability and Scale]] rel:: foundation
- [[A Load Balancer Centralises and Secures Home Network Services]] rel:: goal
- [[Content Switching Allows Layer 7 Routing Based on Hostname or URL Path]] rel:: mechanism
- [[Load Balancer Health Checks Ensure Traffic is Routed Only to Healthy Servers]] rel:: feature
- [[SSL Offloading Centralises Certificate Management on the Load Balancer]] rel:: feature
- [[Cloudflare Can Proxy Traffic to a Load Balancer to Obfuscate a Public IP]] rel:: strategy

### Setup and Configuration Sequence

1.  **Installation**: Download and deploy the free Kemp LoadMaster virtual appliance on a hypervisor (e.g., Proxmox, ESXi).
2.  **Initial Setup**: Configure the admin credentials and create a **Virtual Service** with a Virtual IP (VIP) on port 443.
3.  **Backend Configuration**: Add backend "real" servers (e.g., Plex, NAS) to the virtual service, specifying their internal IP addresses and ports.
4.  **DNS and SSL**:
    - Point your domain's A records to your public IP using [[Cloudflare Can Proxy Traffic to a Load Balancer to Obfuscate a Public IP|Cloudflare's proxy]] to hide your real IP.
    - Generate a Certificate Signing Request (CSR) in Kemp and use Cloudflare's Origin CA to create a free SSL certificate.
    - Import the certificate and keys into Kemp and enable [[SSL Offloading Centralises Certificate Management on the Load Balancer|SSL offloading]] (with re-encryption for full security).
5.  **Port Forwarding**: On your router, forward TCP port 443 to the load balancer's VIP.
6.  **Routing Rules**: Set up [[Content Switching Allows Layer 7 Routing Based on Hostname or URL Path|content switching rules]] to route requests for specific hostnames (e.g., `plex.yourdomain.com`) to the correct backend server.
7.  **Health & Monitoring**: Enable [[Load Balancer Health Checks Ensure Traffic is Routed Only to Healthy Servers|health checks]] for each backend service to ensure automatic failover.
