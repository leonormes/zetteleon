---
created: 2026-04-14T17:45:34+00:00
created_utc: '2026-04-14T12:20:00Z'
kind: constraint
modified: 2026-08-08T10:29:16+00:00
permalink: llmeon/30-library/100-zettelkasten/byzantine-fault-tolerance-requirements
source_title: The Fundamental Challenge of Concurrent and Distributed Systems
source_url: http://www.youtube.com/watch?v=U719vQz-WFs
status: seed
tags: [byzantine-fault-tolerance, distributed-systems, redundancy, security]
title: Byzantine Fault Tolerance Requirements
type: atom
upstream: '[[SoT - Zero Trust Architecture]]'
---

## Byzantine Fault Tolerance Requirements

To tolerate _n_ arbitrary or malicious (Byzantine) failures, a distributed system requires a minimum of _3n + 1_ nodes when using standard communication. This requirement can be reduced to _2n + 1_ nodes if digital signatures are employed to prevent message forgery and ensure authenticity.

### Scope & Conditions

Applies to systems where components may exhibit arbitrary behaviour rather than simply stopping (fail-stop).

### Evidence

> "to tolerate n arbitrary failures, a system requires 3n + 1 nodes when using standard communication, or 2n + 1 if digital signatures are employed to prevent message forgery."

### Implications

- Defines the minimum redundancy necessary for trustless or safety-critical distributed environments.
- Establishes digital signatures as a primary mechanism for reducing the hardware cost of fault tolerance.

### Related

- [[Encryption vs Digital Signatures - Confidentiality vs Authenticity]]—shared mechanism: signatures provide the authenticity required to reduce node count.
- [[SoT - Network Security Architecture]]—See Also.

### See Also

- [[SoT - Microsoft Entra Identity]]
