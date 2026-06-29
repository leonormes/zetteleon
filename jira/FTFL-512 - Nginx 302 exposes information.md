---
tags:
- jira
- fitfile
- bug
- security
- API
- nginx
- cloudflare
status: In Progress
priority: Low
issuetype: Bug
assignee: Leon Ormes
reporter: Ollie Rushton
labels:
- API
created: 2026-03-24
updated: 2026-05-18
jira_id: '28767'
jira_key: FTFL-512
jira_url: https://fitfile.atlassian.net/browse/FTFL-512
permalink: llmeon/jira/ftfl-512-nginx-302-exposes-information
---

# FTFL-512 — [API-6] Nginx 302 exposes information

| Field | Value |
|---|---|
| **Jira ID** | [28767](https://fitfile.atlassian.net/browse/FTFL-512) |
| **Status** | In Progress |
| **Priority** | Low |
| **Issue Type** | Bug |
| **Assignee** | Leon Ormes |
| **Reporter** | Ollie Rushton |
| **Labels** | API |
| **Created** | 2026-03-24 |
| **Updated** | 2026-05-18 |

## Summary

Nginx 302 redirect exposes environment information via response headers, which may help attackers perform more focused attacks.

## Description

**API-6**
[SharePoint Proof Document](https://fitfileltd.sharepoint.com/:b:/s/FitfileTeam/IQD*mi2t-qYxTaz9IyQ4c7uTAVY-IRoSIUweZLh9-aQb7u4)

The target discloses environment information which may help attackers perform more focused attacks. Once the software version number is obtained, attackers would be able to look up any known vulnerabilities associated with that particular version on numerous publicly available vulnerability databases. This helps attackers choose specific exploits better and provides a higher probability for a successful attack.

## Results

The server makes use of Cloudflare and Nginx. The application stack includes Next.js (evidenced by `RSC`, `Next-Router-State-Tree`, and `Next-Router-Prefetch` headers).

### Example Request/Response

```
GET /fitfile/api/auth/session HTTP/2
Host: http://sandbox-testing-1.fitfile.net

HTTP/2 200 OK
Date: Mon, 09 Mar 2026 14:37:59 GMT
Content-Type: application/json
Content-Security-Policy: default-src 'self'; script-src 'self' ...
Vary: RSC, Next-Router-State-Tree, Next-Router-Prefetch
Cache-Control: private, no-cache, no-store
Expires: 0
Pragma: no-cache
Set-Cookie: __Host-next-auth.csrf-token=...
Strict-Transport-Security: max-age=...
```

### Key Observations

1. **Server header leakage** — Response headers reveal the server is behind Cloudflare with Nginx upstream.
2. **Next.js fingerprinting** — `Vary: RSC, Next-Router-State-Tree, Next-Router-Prefetch` headers identify the framework as Next.js.
3. **Cookie exposure** — Session cookies are visible in responses to unauthenticated requests against `/fitfile/api/auth/session`.

## Remediation

1. Strip or genericise server-identifying headers at the Cloudflare/Nginx layer.
2. Remove framework-specific `Vary` headers or normalise them.
3. Ensure 302 redirects do not leak internal backend information.
4. Review all authentication endpoints for information disclosure to unauthenticated clients.

## Related

- [[FTFL-511 — Nginx outdated HTTPS connection methods]]