---
aliases: [Auth0 Authentication Strategy, FitFile Identity Architecture]
created: 2025-09-23T08:41:59Z
last_reviewed: "2026-03-28"
modified: 2026-04-10T16:52:07+00:00
see_also: ["[[SoT - FitFile Deployment - Implementation Manual]]", "[[SoT - FitFile Deployment - Strategy & Architecture]]", "[[SoT - FitFile VSO Secrets Management]]"]
status: evergreen
tags: [auth0, ff_deploy, identity, security, sot]
title: SoT - FitFile Identity & Access Management (Auth0)
type: SoT
updated: 2026-03-28
---

## 1. Executive Summary

This document defines the identity architecture for the FITFILE platform. We utilize Auth0 as the centralized Identity Provider (IdP) for all deployments, enforcing a strict separation between _Authentication_ (Who you are) and _Authorization_ (What you can do).

- Topology: A single multi-tenant Auth0 tenant (`fitfile-prod.eu.auth0.com`) serves the entire estate.
- Unified Model: Cross-tenant access is governed by a central "Product Graph" defining which APIs can talk to each other.

---

## 2. Configuration Layers

Auth0 management is split between tenant-wide governance and per-deployment clients.

### 2.1 Central Services (`auth0-unified`)

The central stack (`/central-services/auth0/`) manages the tenant-level configuration and the Shared Hub SPA (client ID: `5vGsI7q0…`).

- Product Graph (`locals.tf`): A map of FITFILE tenants (`fitfile_tenant_applications`) defining:
    - `api_audience`: The resource server identifier (usually `https://{host}`).
    - `enabled_apis`: Cross-API access permissions (e.g., NWSDE can talk to LCA).
    - `whitelist_api_audience_for_login_redirect`: Policy flag for unified redirect behavior.

### 2.2 Per-Deployment Consumer (`auth0-consumer`)

Each cluster's Terraform creates a separate Auth0 application scoped to that specific customer's URLs.

- Constraint: The `audience` string in the consumer module must match the `api_audience` registered in the central Product Graph.

---

## 3. Object Architecture & Ownership

| Resource Type | Central Services (Shared) | Deployment (Per-Customer) | Notes |
|:---|:---:|:---:|:---|
| Tenant | ✅ Owns | ❌ References | MFA, Branding, Global sessions. |
| API (Resource Server) | ✅ Registers | ❌ References | The `api_audience` string. |
| Connection | ✅ Owns | ❌ References | Shared DB or Enterprise OIDC. |
| SPA Client | ❌ Unified Hub | ✅ Owns Local | The customer-specific web app. |

---

## 4. Split-Horizon & Private DNS Logic

A common failure mode involves clients accessing the app via private links.

### 4.1 The Redirect URI Mismatch

LCA Ingress is often published as: `lca-prd-2.privatelink.fitfile.net`.

- Root Cause: Auth0 defaults only allow `lca-prd-2.fitfile.net`. If a user opens the private link, the browser sends a `redirect_uri` that Auth0 rejects.
- Fix: `auth0_oauth_origin_urls` must include both the public FQDN and the `.privatelink.` FQDN.

### 4.2 Pattern Comparison

| Pattern | Source | URL Strategy |
|:---|:---|:---|
| Unified Hub SPA | Central | Long callback list; wildcard web origins (`*.fitfile.net`). |
| Per-Deployment Client | Cluster | Scoped strictly to that cluster's public and private URLs. |

---

## 5. Security Invariants

1. MFA Enforcement: All production access requires MFA.
2. Audience Isolation: Tokens issued for Deployment A cannot be used against Deployment B unless explicitly permitted in the Product Graph (`enabled_apis`).
3. Phishing Resistance: Browser OAuth URLs for private links must be explicitly whitelisted to prevent origin spoofing.

---

## 6. Troubleshooting

| Error | Cause | Fix |
|:---|:---|:---|
| 401 Unauthorized | `aud` claim mismatch. | Ensure Cluster TF `audience` matches Central `api_audience`. |
| Callback Error | `redirect_uri` mismatch. | Whitelist `https://{host}.privatelink.fitfile.net/…` in Auth0. |
| CORS Error | Origin not whitelisted. | Add both Public and Private FQDNs to "Allowed Web Origins". |
| 403 Forbidden | Missing API Grant. | Add the target API to `enabled_apis` in the central Product Graph. |

## Related Documentation

- [[SoT - FitFile Deployment - Networking and Security]]
- [[SoT - Microsoft Entra Application Model]]
