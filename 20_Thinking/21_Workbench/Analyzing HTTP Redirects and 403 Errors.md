---
title: "‎Gemini – direct access to Google AI"
source: "https://gemini.google.com/share/95efcf948cdc"
captured: "2026-02-05T17:07:31+00:00 2026-02-05T17:07:31+00:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
curl -kIL nnuh-prod-1.fitfile.net

HTTP/1.0 301 Moved Permanently

Location: https://nnuh-prod-1.fitfile.net/

  

HTTP/1.1 302 Found

Date: Wed, 04 Feb 2026 17:33:33 GMT

Server: CPWS

Strict-Transport-Security: max-age=31536000; includeSubDomains

X-Frame-Options: SAMEORIGIN

Location: /sslvpn/Login/Login

Pragma: no-cache

Cache-Control: no-store

Vary: User-Agent

Content-Length: 147

Connection: close

Content-Type: text/html; charset=UTF-8

  

HTTP/1.1 302 Found

Date: Wed, 04 Feb 2026 17:33:33 GMT

Server: CPWS

Strict-Transport-Security: max-age=31536000; includeSubDomains

X-Frame-Options: SAMEORIGIN

X-Content-Type-Options: nosniff

Content-Security-Policy: default-src 'self' wss: localhost:14186 www.google.com www.gstatic.com 'unsafe-inline' 'unsafe-eval'; img-src https: 'self' data:; font-src 'self' data: fonts.gstatic.com

Pragma: no-cache

Cache-Control: no-store

Location: https://supplierportal.nnuh.nhs.uk/sslvpn/Login/BrowserSupport

Vary: User-Agent

Connection: close

Content-Type: text/html; charset=UTF-8

  

HTTP/1.1 403 Forbidden

Date: Wed, 04 Feb 2026 17:33:33 GMT

Server: CPWS

Strict-Transport-Security: max-age=31536000; includeSubDomains

X-Frame-Options: SAMEORIGIN

Pragma: no-cache

Cache-Control: no-store

Vary: User-Agent

Content-Length: 2842

Connection: close

Content-Type: text/html; charset=utf-8

Based on the `curl` output provided, you are witnessing a multi-step redirection chain that ultimately results in a **403 Forbidden** error. This suggests that while the server is reachable, it is intentionally blocking the request—likely due to security policies or a lack of proper browser credentials.

Here is the breakdown of what happened during that request:

### The Redirection Chain

---

### Why did it fail?

The **403 Forbidden** error in this specific context (an NHS supplier portal) is usually triggered by one of the following factors:

- **User-Agent Filtering:** Many VPN and portal gateways (like Check Point, indicated by the "CPWS" server header) block non-browser traffic. Because `curl` identifies itself as `curl/x.x.x`, the server may be rejecting it automatically.
- **Security Policy (Geo-blocking/IP):** Given this is an NHS-related portal, it may only allow traffic from specific UK-authorised IP ranges or internal networks.
- **Missing Session Cookies:** The final hop to the `/BrowserSupport` page often expects a session cookie or a specific header that was supposed to be set in the previous redirects, which `curl` does not handle automatically unless configured to do so.
- **WAF/Bot Protection:** The `Content-Security-Policy` and `X-Frame-Options` headers show a hardened environment. A Web Application Firewall (WAF) might have flagged the automated nature of the request.

### Troubleshooting Steps

If you need to verify if the site is actually "up" or if it is just blocking `curl`, you can try "masking" your request to look like a standard web browser:

1. **Impersonate a Browser:**Use a common User-Agent string to see if the server relaxes the restriction:`curl -kIL -A "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0" https://nnuh-prod-1.fitfile.net`
2. **Check for Cookie Requirements:**If the site requires session persistence to move through the redirects, use a cookie jar:`curl -kILc cookies.txt -b cookies.txt https://nnuh-prod-1.fitfile.net`

Would you like me to help you draft a specific command to test if the 403 is IP-based or client-based?

Google Account

Leon Ormes

leonormes@gmail.com
