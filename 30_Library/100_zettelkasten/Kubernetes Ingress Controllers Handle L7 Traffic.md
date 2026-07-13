---
aliases: [Ingress Controller]
created: 2025-07-16T17:30:03+00:00
last_reviewed: 'null'
modified: 2026-07-13T08:44:57+00:00
permalink: llmeon/30-library/100-zettelkasten/kubernetes-ingress-controllers-handle-l7-traffic
status: 'null'
tags: [http, ingress, SoftwareEngineering/Kubernetes, SoftwareEngineering/Networking]
title: Kubernetes Ingress Controllers Handle L7 Traffic
type: 'null'
updated: null
---

An Ingress Controller (like NGINX) is a component within a Kubernetes cluster that manages external access to the services in the cluster, typically handling HTTP and HTTPS traffic (Layer 7).

When a DNS query, such as for `app.privatelink.fitfile.net`, resolves to the Ingress Controller's internal IP address, the controller receives the subsequent traffic. It then uses the rules defined in an Ingress resource to route the request to the correct internal service based on the hostname or URL path.

## In-cluster vs. External Ingress Solutions

Broadly, there are two types of Ingress solutions:

- In-cluster (e.g., NGINX, Traefik, Contour): Software proxies running as Pods within the cluster. They offer horizontal scalability and rich features (canary, rate limiting) but require exposing themselves via a `LoadBalancer` or `NodePort` service.
- External (e.g., AWS ALB Ingress Controller, GKE Ingress): The control plane provisions a cloud-managed load balancer (ALB) _outside_ the cluster. This reduces operational complexity but may be limited by cloud provider feature sets.

## Protocol & Use Cases

The primary protocols handled are HTTPS (port 443) and HTTP (port 80), aligning with the [[Layer 7 Application Layer]].

- For non-HTTP protocols (gRPC, raw TCP), a Network Load Balancer (NLB) or specific ingress support (like NGINX's stream module) is required.
- TLS Termination: Ingress controllers often offload SSL/TLS decryption, delivering plaintext traffic to the backend services.

EKS Private Cluster Note: When using the AWS ALB Ingress Controller in a private VPC, the `alb.ingress.kubernetes.io/scheme: internal` annotation is mandatory to ensure the ALB is not exposed to the public internet.
