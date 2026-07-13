---
created: 2026-04-14T11:11:48+00:00
created_utc: '2026-04-14T10:35:00Z'
kind: constraint
modified: 2026-07-13T08:52:25+00:00
permalink: llmeon/30-library/100-zettelkasten/custom-port-end-to-end-consistency
source_title: Networking Is Label Transformation Under Policy
source_url: N/A
status: seed
tags: [ingress, load-balancing, ports, redirects]
title: Custom Port End-to-End Consistency
type: atom
upstream: '[[SoT - External Ingress & SSL Architecture]]'
---

## Custom Port End-to-End Consistency

Custom external ports must be consistently supported across every layer of the abstraction stack to prevent URL generation and redirect failures. Technical reachability at a port does not guarantee application-level functionality if redirects fall back to standard ports (80/443).

### Scope & Conditions

Crucial when 443/80 cannot be used and traffic traverses firewalls, load balancers, and ingress controllers.

### Evidence

> "The externally correct port must survive URL generation, redirects, and proxy behaviour."

### Implications

- Ingress controllers must be configured to preserve the external port in their redirect logic.
- Applications must use the correct external URL (including the custom port) when generating absolute links.

### Related

- [[SoT - Kubernetes Networking Model]]—shared mechanism: ingress and service abstractions must align on custom port definitions.
- [[Protocol - HIE--NNUH Network Debugging]]—failure mode: identifies custom port mismatches as a source of broken connectivity.

### See Also

- [[SoT - External Ingress & SSL Architecture]]
