---
aliases:
  - Auth0 Authentication Strategy
  - FitFile Identity Architecture
created: 2025-09-23T08:41:59Z
modified: 2026-02-01T15:20:00+00:00
status: evergreen
tags:
  - auth0
  - identity
  - security
  - sot
  - ff_deploy
title: SoT - FitFile Identity & Access Management (Auth0)
type: SoT
updated: 2026-02-01
see_also:
  - "[[SoT - FitFile Deployment - Strategy & Architecture]]"
  - "[[SoT - FitFile Deployment - Implementation Manual]]"
  - "[[SoT - FITFILE Secret Management Architecture]]"
---

## 1. Executive Summary

This document defines the identity architecture for the FITFILE platform. We utilize **Auth0** as the centralized Identity Provider (IdP) for all deployments, enforcing a strict separation between *Authentication* (Who you are) and *Authorization* (What you can do).

- **Authentication:** Handled by Auth0 via OIDC/OAuth2.
- **Authorization:** Handled by the Application (SpiceDB) based on JWT claims.
- **Topology:** A single multi-tenant Auth0 tenant (`fitfile-prod.eu.auth0.com`) serves all customer environments.

---

## 2. Architecture Components

### 2.1 The Central Tenant
- **Domain:** `fitfile-prod.eu.auth0.com`
- **Region:** EU (compliant with GDPR).
- **Management:** Configured via Terraform in `/central-services/auth0/prod/`.

### 2.2 The Resource Server (API)
Each FitFile deployment (e.g., `cuh-prod-1`) is registered as a unique **Resource Server** in Auth0.
- **Identifier (Audience):** `https://{deployment-key}.privatelink.fitfile.net`
- **Signing Algo:** RS256.
- **Token Lifetime:** 300 seconds (5 minutes) for strict security.

### 2.3 The Client Application
- **Type:** Single Page Application (SPA).
- **Grant Type:** Authorization Code Flow with PKCE.
- **Client ID:** Unique per deployment.

---

## 3. Object Architecture & Ownership

We employ a **Shared Infrastructure** pattern to prevent resource conflicts and ensure consistency.

### 3.1 Resource Ownership Matrix

| Resource Type | Central Services (Shared) | Deployment (Per-Customer) | Notes |
|:---|:---:|:---:|:---|
| **Tenant** | ✅ Owns | ❌ References | Global settings (Session life, Support email). |
| **Connection** | ✅ Owns | ❌ References | "Username-Password-Authentication". Shared user DB. |
| **Branding** | ✅ Owns | ❌ Inherits | Logos, colors, universal login theme. |
| **SPA Client** | ❌ None | ✅ Owns | The user-facing web app. |
| **M2M Clients** | ❌ None | ✅ Owns | API Explorer, CI/CD pipelines. |
| **Association** | ❌ None | ✅ Owns | Links the Deployment Clients to the Shared Connection. |

### 3.2 Deployment Requirements (Checklist)

A new deployment **must** create these objects (via Terraform):

1.  **SPA Client**: The User-Facing App (`app_type = "spa"`).
2.  **M2M Clients**: For automated access (e.g., API Explorer).
3.  **Connection Association**: A `auth0_connection_clients` resource that links the *new* clients to the *existing* shared connection ID.
    - *Critical:* Do NOT attempt to create a new `auth0_connection`. This will cause a 409 Conflict.

---

## 4. Authentication Flow (OAuth 2.0 + PKCE)

1. **User Visit:** User accesses `https://{deployment-key}.fitfile.net`.
2. **Redirect:** App redirects to Auth0 Universal Login.
   - `response_type=code`
   - `code_challenge` (PKCE)
   - `scope=openid profile email`
3. **Login:** User authenticates (MFA enforced).
4. **Callback:** Auth0 redirects to `/callback` with an Authorization Code.
5. **Exchange:** App swaps Code + PKCE Verifier for a **JWT Access Token**.
6. **API Access:** App attaches `Authorization: Bearer <token>` to backend requests.

> [!important] Token Validation
> The backend validates the JWT signature against Auth0's public JWKS keys. It strictly checks the `aud` (Audience) claim matches its own Deployment Key.

---

## 4. Deployment Configuration

Identity configuration is injected into the application via Helm values and Vault secrets.

### 4.1 Required Secrets (Vault)
These must be seeded during **Phase 1** of deployment:
- `auth0-client-id`
- `auth0-client-secret` (For M2M flows)
- `auth0-domain`

### 4.2 Application Config (Helm Values)
```yaml
# values.yaml
frontend:
  auth0:
    domain: "fitfile-prod.eu.auth0.com"
    audience: "https://cuh-prod-1.privatelink.fitfile.net"
    clientId: "..." # Injected via secret, or public ID here
```

### 4.3 Redirect URIs
For a successful login, the following must be whitelisted in the Auth0 Client:
- **Callback:** `https://{deployment-key}.fitfile.net/callback`
- **Logout:** `https://{deployment-key}.fitfile.net/`
- **CORS:** `https://{deployment-key}.fitfile.net`

---

## 5. Security Invariants

1. **MFA Enforcement:** All production access requires MFA.
2. **Short-Lived Tokens:** Access tokens expire in 5 minutes. Refresh tokens are used for session maintenance (with rotation).
3. **Audience Isolation:** Tokens issued for `Deployment A` cannot be used against `Deployment B`.
4. **Private Link Audience:** We use the private link DNS (`privatelink.fitfile.net`) as the logical API identifier to align with internal routing.

---

## 6. Troubleshooting

| Error | Cause | Fix |
|:---|:---|:---|
| **401 Unauthorized** | Backend cannot verify JWT signature. | Check `aud` claim in token matches Backend config. |
| **Callback Error** | `redirect_uri` mismatch. | Verify Terraform configuration matches the exact URL (trailing slashes matter). |
| **CORS Error** | Origin not whitelisted. | Add `https://{domain}` to "Allowed Web Origins" in Auth0. |
| **Login Loop** | Silent refresh failing. | Check Refresh Token rotation settings and 3rd-party cookie blocking. |
