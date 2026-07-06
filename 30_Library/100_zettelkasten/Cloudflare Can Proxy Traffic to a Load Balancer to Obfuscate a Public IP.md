---
aliases: []
created: 2025-10-31T09:25:33+00:00
last_reviewed: ''
modified: 2026-07-04T10:51:53+00:00
permalink: llmeon/30-library/100-zettelkasten/cloudflare-can-proxy-traffic-to-a-load-balancer-to-obfuscate-a-public-ip
status: seedling
tags: [cloudflare, homelab, SoftwareEngineering/Networking, SoftwareEngineering/networking/dns, SoftwareEngineering/Security]
title: Cloudflare Can Proxy Traffic to a Load Balancer to Obfuscate a Public IP
type: concept
updated: null
---

## Cloudflare Can Proxy Traffic to a Load Balancer to Obfuscate a Public IP

Summary: By enabling Cloudflare's proxy (the orange cloud) for DNS A or CNAME records, you can hide your home network's public IP address, adding a significant layer of security when self-hosting services.

Details: When the proxy is enabled, DNS queries for your domain resolve to a Cloudflare IP address, not your own. Cloudflare then forwards the traffic to your origin server (e.g., your home load balancer). This prevents attackers from directly targeting your network's public IP. Cloudflare also provides benefits like a universal SSL certificate, caching for static content, and DDoS protection, even on its free tier. This makes it a powerful tool to use in front of a home lab load balancer.
