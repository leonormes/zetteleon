---
created: 2026-04-14T11:11:48+00:00
created_utc: '2026-04-14T10:35:00Z'
kind: failure_mode
modified: 2026-07-28T09:12:51+00:00
permalink: llmeon/30-library/100-zettelkasten/stateful-firewall-flow-observation
source_title: Networking Is Label Transformation Under Policy
source_url: N/A
status: seed
tags: [asymmetric-routing, failure-modes, firewalls, state]
title: Stateful Firewall Flow Observation
type: atom
upstream: '[[SoT - Network Security Architecture]]'
---

## Stateful Firewall Flow Observation

Stateful firewalls drop return traffic if the flow does not match an existing session state entry created by the forward path. A firewall is reactive to observed packets and their specific metadata, not administrative intentions.

### Scope & Conditions

The primary cause of failure in asymmetric routing scenarios or when NAT state expires.

### Evidence

> "A stateful firewall… cares what flow it observed."

### Implications

- If return traffic traverses a different firewall instance than the forward traffic, it will be dropped as unsolicited.
- Connection tracking (conntrack) is the "memory" of the firewall; its state determines the fate of every subsequent packet in a flow.

### Related

- [[SoT - Linux Networking Primitives]]—shared mechanism: discusses the `conntrack` system used for state management.
- [[SoT - Network Segmentation]]—shared mechanism: segmentation often involves stateful boundaries that enforce flow symmetry.

### See Also

- [[SoT - Network Security Architecture]]
