---
created: 2026-06-05T09:05:54+00:00
modified: 2026-06-05T09:56:07+00:00
type: project
project_category: refined_deployment
project_status: active
project_name: "Refined Deployment"
---
*Shared Message from Pieces (https://pieces.app) by Leon Ormes (leonormes@gmail.com) on Friday Jun 5, 2026 - 10:05 AM*
---
Memory is now exhausted (`sufficient`). Here's the full synthesis.

---

## Faro Receiver Authentication All Options Ranked by Security

The core context from your LTM and Alloy docs: you're running `otelcol.receiver.faro` (the experimental OTel-style component used in your k8s-monitoring Helm setup) as an in-cluster Alloy receiver, exposed via Ingress, with the Faro SDK in your Next.js InsightFILE frontend sending telemetry to it. The question of auth on that receiver is a real open loop — your current config has `allowed_origins = ["*"]` with no auth at all.

There are **two distinct Alloy Faro receiver components**, and they have different auth capabilities:

---

## The Two Receiver Components (Critical Distinction)

| Component | Built-in auth | Notes |
|---|---|---|
| `faro.receiver` | ✅ `api_key` field (native, simple) | Older component, non-OTel pipeline |
| `otelcol.receiver.faro` | Pluggable `auth` + `tls` blocks | What you're actually using via k8s-monitoring chart — marked **experimental** |

Your current setup uses `otelcol.receiver.faro` via the `alloy-faro` preset in `k8s-monitoring`. The auth options below apply to that component unless noted.

---

## Auth Options Ranked: Most Secure → Least Secure

### 🥇 1. mTLS + OAuth2/Bearer Token (Most Secure)

**What it is:** Two-factor auth at the transport level (client presents a certificate) AND at the application level (client presents a signed JWT/bearer token). Both must pass.

**How to configure:**

```hcl
otelcol.receiver.faro "default" {
  endpoint = "0.0.0.0:12347"

  tls {
    cert_file       = "/etc/alloy/tls/server.crt"
    key_file        = "/etc/alloy/tls/server.key"
    client_ca_file  = "/etc/alloy/tls/client-ca.crt"  # enables mTLS
    min_version     = "TLS 1.2"
  }

  auth = otelcol.auth.oauth2.faro_jwt.handler

  output {
    logs   = [otelcol.processor.batch.default.input]
    traces = [otelcol.processor.batch.default.input]
  }
}

otelcol.auth.oauth2 "faro_jwt" {
  client_id     = "faro-frontend"
  token_url     = "https://fitfile-test.eu.auth0.com/oauth/token"  # your Auth0
  grant_type    = "client_credentials"
  # tls block for the token endpoint connection
}
```

**Practical caveat:** mTLS is very hard to make work directly from browser JavaScript — the browser controls client cert selection via OS cert store, and the Faro Web SDK has no mechanism to send client certificates. **In practice, mTLS from a browser frontend is not viable directly.** The workaround is to terminate mTLS at an intermediate proxy (e.g. your nginx Ingress or a service mesh sidecar) and then have the proxy forward to Alloy using mTLS, while the browser-to-proxy leg uses HTTPS + a token.

---

### 🥈 2. TLS (HTTPS) + Short-Lived Bearer Token / Auth0 Token

**What it is:** The frontend obtains a short-lived access token from your Auth0 instance (you already use Auth0: `fitfile-test.eu.auth0.com`) and sends it as a custom header with each telemetry payload. The Alloy receiver validates it via `otelcol.auth.oauth2`.

**How to configure on Alloy side:**

```hcl
otelcol.receiver.faro "default" {
  endpoint = "0.0.0.0:12347"

  tls {
    cert_file = "/etc/alloy/tls/server.crt"
    key_file  = "/etc/alloy/tls/server.key"
    min_version = "TLS 1.2"
  }

  auth = otelcol.auth.oauth2.auth0.handler

  output {
    logs   = [otelcol.processor.batch.default.input]
    traces = [otelcol.processor.batch.default.input]
  }
}
```

**How to configure in `FaroProvider.tsx`:**

```typescript
initializeFaro({
  url: process.env.NEXT_PUBLIC_FARO_COLLECTOR_URL,
  app: { name: 'insightfile-frontend', version: '1.0.0' },
  // Pass the Auth0 access token as a custom header
  beforeSend: (event) => {
    // inject Authorization: Bearer <token> on each payload
  },
});
```

**Why it's strong:** Tokens are short-lived (minutes/hours), scoped, and revocable. Since you already have Auth0 as your IDP, this is architecturally consistent.

---

### 🥉 3. TLS (HTTPS) + Static API Key via `faro.receiver`

**What it is:** Switch from `otelcol.receiver.faro` to the `faro.receiver` component, which has a native `api_key` field. The SDK sends the key in the `X-API-Key` header. HTTPS (TLS on the Ingress) encrypts the key in transit.

**How to configure:**

```hcl
faro.receiver "default" {
  server {
    listen_address = "0.0.0.0:12347"
    api_key        = sys.env("FARO_API_KEY")  # pulled from K8s secret

    cors_allowed_origins = [
      "https://your-app.fitfile.net",
      "https://staging.fitfile.net",
    ]
  }

  output {
    logs   = [loki.write.default.receiver]
    traces = [otelcol.exporter.otlp.grafana_cloud.input]
  }
}
```

**SDK side:**

```typescript
initializeFaro({
  url: process.env.NEXT_PUBLIC_FARO_COLLECTOR_URL,
  app: { name: 'insightfile-frontend' },
  // Faro SDK sends X-API-Key automatically when configured
  apiKey: process.env.NEXT_PUBLIC_FARO_API_KEY,
});
```

**Trade-off vs OAuth2:** A static API key that lives in an env var is long-lived. If it leaks (e.g. via browser devtools — it's exposed in the network request headers), it must be rotated manually. Mitigate with **tight CORS** (`cors_allowed_origins` to your exact domains, not `"*"`) and **K8s secret rotation**. This is the simplest option to implement.

---

### 4. TLS (HTTPS) + Tight CORS Only (Weakest — Not True Auth)

**What it is:** Your current config but with TLS on the Ingress and CORS restricted to your actual domains.

```hcl
cors {
  allowed_origins = [
    "https://your-app.fitfile.net",
    "https://staging.fitfile.net",
  ]
  allowed_headers = ["X-Faro-Session-Id", "Content-Type"]
}
```

**Why it's weak:** CORS is enforced by browsers, not by the receiver itself. Any non-browser client (curl, Postman, a scraper) can POST to your collector endpoint freely. It provides zero protection against deliberate abuse or metric spam. **Do not rely on CORS alone as your auth mechanism in production.**

---

## Recommendation for FITFILE

Given your stack (Auth0 IDP, K8s + Ingress via nginx, Next.js frontend, `otelcol.receiver.faro` via k8s-monitoring helm chart), the **pragmatic best option** is:

**Option 2: TLS + Static API Key via `faro.receiver` first, migrating to Auth0 bearer tokens later.**

- Switch from `otelcol.receiver.faro` to `faro.receiver` in your `alloy-faro` extraConfig — it gives you the `api_key` field without needing to wire up an OAuth2 auth handler.
- Store the key in a K8s secret (you already have the `remote.kubernetes.secret "monitoring"` pattern in your config).
- Tighten `cors_allowed_origins` to your actual domains (remove the `"*"`).
- The Ingress already handles TLS termination (cert-manager + Let's Encrypt per your config), so HTTPS is already in play.

**Longer term:** Wire up `otelcol.auth.oauth2` pointing at your Auth0 `fitfile-test.eu.auth0.com` token endpoint and inject short-lived client-credentials tokens from the frontend — this gives you token rotation and revocation for free via Auth0's existing infrastructure.

---

## Quick Reference

| Option | Mechanism | Browser-Compatible | Security Level | Complexity |
|---|---|---|---|---|
| mTLS + Bearer Token | Client cert + JWT | ❌ Not directly | ⭐⭐⭐⭐⭐ | Very High |
| HTTPS + OAuth2/Bearer | Short-lived JWT | ✅ Yes | ⭐⭐⭐⭐ | Medium |
| HTTPS + API Key | Static `X-API-Key` | ✅ Yes | ⭐⭐⭐ | Low |
| HTTPS + CORS only | Browser enforcement | ✅ Yes | ⭐ | Very Low |