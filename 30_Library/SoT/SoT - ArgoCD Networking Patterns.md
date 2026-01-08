---
aliases: ["ArgoCD Ingress", "ArgoCD Split Ingress", "gRPC vs HTTP Ingress"]
confidence: "High"
created: 2026-01-06T19:57:18+00:00
epistemic: "Pattern"
last_reviewed: 
modified: 2026-01-08T10:49:45+00:00
purpose: "To define the specific architectural patterns required to expose ArgoCD's dual-protocol (gRPC and HTTP) API server through standard Kubernetes Ingress controllers."
review_interval: "1 year"
see_also:
  - "[[SoT - GitOps for IAM and Permissions]]"
  - "[[SoT - Kubernetes Networking & DNS]]"
source_of_truth: []
status: "Active"
tags: ["argocd", "grpc", "ingress", "kubernetes", "networking"]
title: SoT - ArgoCD Networking Patterns
type: "SoT"
uid: 
updated: 
---

> **The Problem:** The ArgoCD API server serves both **gRPC** (CLI) and **HTTP/HTTPS** (UI) on the same port (443). Most Kubernetes Ingress controllers (like NGINX) treat a backend as a single protocol type, causing conflicts when trying to route both via a single Ingress object.

## 1. The Core Conflict

- **UI:** Uses standard HTTP/1.1 or HTTP/2.
- **CLI:** Uses gRPC (requires HTTP/2 and specific headers).
- **Constraint:** Standard Ingress definitions bind a specific backend protocol (e.g., `nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"`) to the entire rule set. You cannot easily mix "HTTPS" and "GRPC" on the same host/path combination without special handling.

## 2. Solution A: Split Ingress (The Standard)

The most robust, "Kubernetes-native" approach is to define **two separate Ingress objects** for the same service, usually differentiated by a subdomain for gRPC.

### Mechanism

1. **UI Ingress:**
    - **Host:** `argocd.example.com`
    - **Protocol:** HTTPS/HTTP
    - **Annotation:** `nginx.ingress.kubernetes.io/backend-protocol: "HTTP"` (if TLS disabled on argocd-server)
2. **gRPC Ingress:**
    - **Host:** `grpc.argocd.example.com`
    - **Protocol:** gRPC
    - **Annotation:** `nginx.ingress.kubernetes.io/backend-protocol: "GRPC"`

### Trade-offs

- **Pros:** Clean separation, allows standard TLS termination at the Ingress.
- **Cons:** Requires the CLI user to specify the gRPC URL explicitly or requires extra DNS entries.

## 3. Solution B: SSL Passthrough (Single Host)

If you must use a single hostname (`argocd.example.com`) for both UI and CLI, you must bypass the Ingress Controller's L7 processing logic.

### Mechanism

- **Annotation:** `nginx.ingress.kubernetes.io/ssl-passthrough: "true"`
- **Logic:** The Ingress controller acts as a raw L4 TCP proxy. It sniffs the SNI header to route the packet but **does not decrypt it**.
- **Termination:** TLS is terminated at the `argocd-server` pod itself.

### Trade-offs

- **Pros:** Single URL for users.
- **Cons:** Higher overhead on the pod (CPU usage for crypto). Loss of L7 features at the Ingress level (header manipulation, standard WAF rules).

## 4. Solution C: Protocol Multiplexing (Traefik/Contour)

Newer ingress controllers (Traefik v2+, Contour) can multiplex protocols on the same port more effectively than NGINX.

- **Traefik:** Can match headers (`Content-Type: application/grpc`) to route traffic to a specific backend service configuration without splitting the host.
- **Contour:** Uses `HTTPProxy` CRDs to define multiple services for the same route based on conditions.

## 5. ArgoCD Server Configuration

For these patterns to work, the `argocd-server` must typically be configured to allow insecure traffic if termination happens upstream.

- **Flag:** `--insecure` (Disables internal TLS on the argocd-server pod).
- **Why:** Allows the Ingress Controller to talk to the pod via plain HTTP/h2c, simplifying the "Double TLS" overhead.
