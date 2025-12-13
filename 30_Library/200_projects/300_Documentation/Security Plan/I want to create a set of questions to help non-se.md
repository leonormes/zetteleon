---
aliases: []
confidence: 
created: 2025-03-18T11:14:47Z
epistemic: 
last_reviewed: 
modified: 2025-12-13T11:39:43Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: I want to create a set of questions to help non-se
type:
uid: 
updated: 
version:
---

I want to create a set of questions to help non-security concerned developers uncover assumptions they are making about how secure the data is. I want to get them to state what their beliefs are so we can validate claims. The devs tend to think they have done some authentication work, so the whole system is safe. How can I get them thinking about the broader security risks of distributed systems

To help developers uncover security assumptions in distributed systems, focus on questioning areas beyond authentication while addressing common distributed computing fallacies. Here's a structured set of questions organized by risk category:

## Network Assumptions

**1. "How do we handle network partitions or dropped connections?"**
Probe assumptions about the network being always available[^1]. Ask for specific retry mechanisms and circuit-breaker implementations.

**2. "What happens if a malicious actor spoofs IP addresses between our nodes?"**
Challenge assumptions about topology stability[^1][^3] and explore ARP spoofing/DNS poisoning protections.

---

## Data Flow Risks

**3. "Where is data unencrypted in transit? How do we verify TLS certificates?"**
Target assumptions about transport security[^1][^3]. Example:

```bash
# Check certificate pinning in configs
grep -r "sslVerify" /etc/nginx/
```

**4. "How do we validate data integrity when multiple nodes modify the same record?"**
Expose assumptions about consistency using real conflict scenarios[^4]:

```json
// Sample conflict in distributed DB
{
  "nodeA": {"version": 3, "data": "X"},
  "nodeB": {"version": 2, "data": "Y"}
}
```

---

## Authentication Blind Spots

**5. "If our OAuth provider goes down, what services become vulnerable?"**
Test assumptions about centralized auth reliability[^1][^3]. Have them diagram service dependencies.

**6. "How do we detect credential reuse across staging/prod environments?"**
Challenge homogeneity assumptions with a table comparison:

| Environment | Access Scope | Credential Rotation |
| :-- | :-- | :-- |
| Production | Global | 90-day rotation |
| Staging | Regional | No rotation |

---

## Systemic Risks

**7. "Which compliance requirements apply when data crosses EU/US/APAC nodes?"**
Reveal jurisdictional assumptions[^3][^4]. Provide a GDPR/HIPAA checklist.

**8. "How would we identify a 2% data discrepancy across nodes?"**
Test monitoring assumptions with a breach simulation:

> *"Thursday 2AM: Cloud logs show Asian nodes processing 18% more payments than European counterparts..."*

**9. "What third-party libraries in our pipeline have write access to production?"**
Expose supply chain assumptions via dependency audit:

```python
# Pipfile example with vulnerable lib
[packages]
requests = "==2.19.1"  # CVE-2018-18074
```

**10. "If a node is compromised, how quickly can we rotate all shared secrets?"**
Quantify response assumptions:
`Secrets rotated: ███ 34% complete | ETA: 2h17m`

---

## Validation Techniques

Use these methods to pressure-test answers:

1. **"Show me last month's access logs where authZ failed"** - Validate monitoring claims
2. **Red team exercise**: *"We've injected 5 vulnerabilities - find them in 45 minutes"*
3. **Cost analysis**: *"A DDoS adding \$12k/day in cloud egress fees - what's our mitigation path?"*

By combining technical specifics with breach simulations and compliance checklists, these questions reveal hidden assumptions about attack surfaces, data flows, and operational realities in distributed environments[^1][^3][^4].

<div style="text-align: center">⁂</div>

[^1]: <https://en.wikipedia.org/wiki/Fallacies_of_distributed_computing>

[^2]: <http://www0.cs.ucl.ac.uk/staff/s.wilbur/3c31/z08notes.pdf>

[^3]: <https://cybersecurity-magazine.com/distributed-applications-security/>

[^4]: <https://www.linkedin.com/pulse/security-challenges-distributed-systems-safeguarding-integrity-kabir-ucele>

[^5]: <https://blog.uxtweak.com/assumption-testing/>

[^6]: <https://www.linkedin.com/pulse/tale-software-architecture-part-5-wrong-assumption-fallacies-rasel-yp64c>

[^7]: <https://blogs.oracle.com/developers/post/fallacies-of-distributed-systems>

[^8]: <https://newsletter.enginuity.software/p/overcoming-the-8-fallacies-of-distributed>

[^9]: <http://wp.doc.ic.ac.uk/hipeds/research-descriptions/distributed-systems-security-and-privacy/>

[^10]: <https://purplesec.us/learn/common-network-vulnerabilities/>

[^11]: <https://multishoring.com/blog/distributed-database-security-issues/>

[^12]: <https://www.isaca.org/resources/isaca-journal/issues/2022/volume-6/essential-assumptions-for-effective-data-security>

[^13]: <https://www.linkedin.com/pulse/ask-you-shall-receive-top-3-questioning-techniques-hidden-kincaid>

[^14]: <https://www.linkedin.com/advice/3/what-most-effective-ways-identify-underlying-jbzfe>

[^15]: <https://www.reddit.com/r/programming/comments/pinh52/reviewing_the_eight_fallacies_of_distributed/>

[^16]: <https://wickr.com/how-to-define-a-robust-data-security-strategy-within-distributed-computing/>

[^17]: <https://www.getambassador.io/blog/distributed-network-systems-8-fallacies-guide>

[^18]: <https://www.linkedin.com/pulse/how-secure-your-distributed-system-system-design-us>

[^19]: <https://www.cybok.org/media/downloads/Distributed_Systems_Security_issue_1.0.pdf>

[^20]: <https://www.tripwire.com/state-of-security/overlooked-risks-open-source-software-industrial-security>

[^21]: <https://www.tutorchase.com/answers/ib/computer-science/what-security-challenges-does-distributed-computing-face>

[^22]: <https://www.cs.purdue.edu/homes/bb/bhargava-vuln-threats.pdf>

[^23]: <https://ceur-ws.org/Vol-3018/Paper_8.pdf>

[^24]: <https://www.boost.co.nz/blog/2022/02/security-in-agile-software-development>

[^25]: <https://www.linkedin.com/pulse/8-terrible-assumptions-youre-making-data-security-becker>

[^26]: <https://www.uxpin.com/studio/blog/assumptions-mapping/>

[^27]: <https://cora.ucc.ie/server/api/core/bitstreams/31d9ca12-678c-45d2-b9af-93c5ef40be34/content>

[^28]: <https://www.lepide.com/blog/5-assumptions-cisos-make-that-may-threaten-data-security/>

[^29]: <https://learningloop.io/glossary/assumption-mapping>

[^30]: <https://oro.open.ac.uk/14906/1/ICSE2009_SHARK_3004_Ostacchini_Ireo.pdf>
