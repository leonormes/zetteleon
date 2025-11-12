---
aliases: []
confidence: 
created: 2025-11-03T15:47:05Z
epistemic: 
last_reviewed: 
modified: 2025-11-12T14:24:30Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: What Does Company Apex Mean in DNS
type: 
uid: 
updated: 
---

## What Does Company Apex Mean in Dns

base_domain: "acme.example" \# company apex or subdomain root

The term "company apex" in DNS refers to the root of a registrable domain, also called the apex domain, base domain, bare domain, naked domain, or zone apex domain. For your example, the apex domain is `acme.example`—this is the highest level address for the domain and does not include any prefixes like "www".[^1][^2][^6][^7]

### Apex Domain Characteristics

- **Definition**: The apex domain is the main domain in a DNS zone, not a subdomain—it is the core address without anything before the first dot except the zone or domain itself.[^2][^8][^9]
- **Purpose**: Apex domains are used for the primary web presence of a company or organization and serve as the authoritative root for all subdomains (e.g., `acme.example` instead of `www.acme.example`).[^9][^1][^2]
- **DNS Records**:
    - Apex domains typically use A or AAAA records to directly point to an IP address.
    - CNAME records are not permitted at the apex due to DNS protocol restrictions, but some DNS providers support ALIAS or ANAME records as CNAME-like solutions for apex domains.[^5][^2]

### Apex Vs Subdomain

| Type | Example | DNS Record Usage | Purpose |
| :-- | :-- | :-- | :-- |
| Apex/Root | acme.example | A/AAAA, ALIAS/ANAME | Main website, brand identity[^2][^5] |
| Subdomain | <www.acme.example> | CNAME, A/AAAA | Specific sections/services[^2][^5] |

### Why It Matters

- The apex domain is where most key DNS records are managed for core services and where the primary branding sits.[^6][^1][^2]
- When configuring DNS, it's important to recognize constraints at the apex (e.g., no CNAME allowed) and know which records to use for reliable resolution.[^2][^5]
- Examples of apex domain records:
    - `acme.example` → A record to `192.0.2.10`
    - `www.acme.example` → CNAME to `acme.example`

### Action Steps for DNS Setup

- Use an A or AAAA record for apex domains.
- Avoid using CNAME records at the apex—consider ALIAS or ANAME if your DNS provider supports them.
- Ensure consistent branding by redirecting subdomains (e.g., www) to the apex or vice versa, as preferred.

If you need code or shell examples for configuring DNS for apex domains, let me know your specific DNS provider or environment.

<span style="display:none">[^3][^4]</span>

<div align="center">⁂</div>

[^1]: <https://www.urllo.com/resources/learn/what-is-an-apex-domain>

[^2]: <https://www.networksolutions.com/blog/what-is-apex-domain/>

[^3]: <https://learn.microsoft.com/en-us/azure/dns/dns-zones-records>

[^4]: <https://news.ycombinator.com/item?id=8825519>

[^5]: <https://docs.netlify.com/manage/domains/get-started-with-domains/>

[^6]: <https://hostadvice.com/blog/domains/what-is-apex-domain/>

[^7]: <https://www.ans.co.uk/docs/domains/safedns/apexdomain/>

[^8]: <https://learn.microsoft.com/en-us/azure/frontdoor/apex-domain>

[^9]: <https://cloudsoft.io/blog/aws-dns-domain-apex>

## Explain the Difference between Apex Domain and Subdomain in DNS

An apex domain is the root address of a registrable domain in DNS, while a subdomain is any division beneath that main domain used to separate sections, services, or environments.[^2][^3][^5][^6]

### Apex Domain

- **Definition**: The root name of your domain without any prefix (e.g., `acme.example`) is the apex domain.[^3][^5][^2]
- **DNS Record Constraints**: Only A, AAAA, ALIAS, or ANAME records can be used at the apex because a CNAME record is not permitted at the root level by DNS standards.[^1][^2][^3]
- **Purpose**: Represents your website’s core public identity, used for branding and centralized access.[^5][^3]

### Subdomain

- **Definition**: Any domain that is derived from the apex by adding a prefix, such as `www.acme.example`, `blog.acme.example`, or `dev.acme.example`.[^6][^2][^3]
- **DNS Record Flexibility**: Subdomains can use CNAME records, as well as A or AAAA records, allowing for easier redirection and aliasing of services.[^1][^2][^3]
- **Purpose**: Used to separate content, services, or different environments within an organization, such as blogs, shops, APIs, or staging websites.[^3][^5]

### Direct DNS Configuration Differences

| Type | Example | Record Type Restrictions | Typical Usage |
| :-- | :-- | :-- | :-- |
| Apex Domain | acme.example | A, AAAA, ALIAS, ANAME (no CNAME) [^3] | Main website, brand, authoritative root |
| Subdomain | <www.acme.example> | CNAME, A, AAAA allowed [^3] | Blogs, staging, APIs, microservices |

### Practical Insights

- Use the apex domain for your primary brand address (e.g., `acme.example`) and subdomains for specialized functions (e.g., `shop.acme.example` for an e-shop).[^7][^5][^3]
- Choose A/AAAA records for apex due to protocol limitations, but you can use CNAME records freely with subdomains for greater flexibility in pointing to services.[^2][^1]
- Proper organization improves both DNS management and user navigation.

This distinction is foundational in DNS architecture and a common consideration in systems design and workflows.[^5][^6][^7][^2][^3]

<span style="display:none">[^4][^8][^9]</span>

<div align="center">⁂</div>

[^1]: <https://www.reddit.com/r/Netlify/comments/1ex2veq/difference_between_subdomains_and_apex_domains_in/>

[^2]: <https://www.urllo.com/resources/learn/what-is-an-apex-domain>

[^3]: <https://www.networksolutions.com/blog/what-is-apex-domain/>

[^4]: <https://www.namehero.com/blog/domain-vs-subdomain-a-complete-guide/>

[^5]: <https://hostadvice.com/blog/domains/what-is-apex-domain/>

[^6]: <https://en.wikipedia.org/wiki/Subdomain>

[^7]: <https://www.hosted.com/blog/domain-vs-subdomain-whats-the-difference/>

[^8]: <https://www.seoqueen.com/a-beginners-guide-to-understanding-root-domain-vs-subdomain/>

[^9]: <https://www.youtube.com/watch?v=B3R34MH7EU8>
