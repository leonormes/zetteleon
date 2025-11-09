---
aliases: []
confidence: 0.8
created: 2025-10-31T09:25:33Z
epistemic: fact
last_reviewed: 
modified: 2025-10-31T09:31:41Z
purpose: "Describe the strategy of using Cloudflare with a self-hosted load balancer."
review_interval: 90
see_also: []
source_of_truth: []
status: seedling
tags: [cloudflare, dns, homelab, networking, security]
title: Cloudflare Can Proxy Traffic to a Load Balancer to Obfuscate a Public IP
type: concept
uid: 
updated: 
---

## Cloudflare Can Proxy Traffic to a Load Balancer to Obfuscate a Public IP

**Summary:** By enabling Cloudflare's proxy (the orange cloud) for DNS A or CNAME records, you can hide your home network's public IP address, adding a significant layer of security when self-hosting services.

**Details:** When the proxy is enabled, DNS queries for your domain resolve to a Cloudflare IP address, not your own. Cloudflare then forwards the traffic to your origin server (e.g., your home load balancer). This prevents attackers from directly targeting your network's public IP. Cloudflare also provides benefits like a universal SSL certificate, caching for static content, and DDoS protection, even on its free tier. This makes it a powerful tool to use in front of a home lab load balancer.
