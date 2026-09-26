---
conformant: false
created: 2026-09-18T00:00:00+00:00
created_utc: 2026-09-18T00:00:00Z
modified: 2026-09-25T16:29:25+00:00
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/internal-buses-and-external-networks-differ-in-coupling-latency-management-and-power
prodos.atomic.form: distinction
prodos.kind: atomic
source_title: Defining One Computer Concept
status: seed
tags: [computer-architecture, computer-science, distributed-systems]
title: Internal Buses and External Networks Differ in Coupling, Latency, Management, and Power
type: concept
---

## Internal Buses and External Networks Differ in Coupling, Latency, Management, and Power

Internal buses (system, address, data, control) and external networks (Ethernet, Wi-Fi) aren't just "fast vs. slow" versions of the same thing—they differ across several independent dimensions: buses are tightly coupled, low-latency, centrally managed by the motherboard's chipset, give shared direct access to memory, and often carry power to connected components; networks are loosely coupled, higher-latency and variable-bandwidth, managed in a distributed fashion by NICs and switches/routers, communicate by message-passing rather than shared memory access, and carry no power.

### Scope & Conditions

Describes the physical/mechanistic dimensions distinguishing the two communication classes, not their use as a proxy for "one computer vs. many" (that's the kernel-boundary claim in [[SoT - The Logical Definition of a Computer]]).

### Evidence

> "Internal Buses… Tight Coupling… Low Latency & High Bandwidth… Centralized Management… Shared Resource Access… Power Provision… External Networks… Loose Coupling… Higher Latency & Variable Bandwidth… Distributed Management… Indirect Resource Access… No Power Provision."

### Implications

- A component that needs shared, low-latency access to main memory (a GPU, a DMA controller) has to sit on the internal-bus side of this line—no network protocol offers comparable access, however fast.
- The "no power provision" property of networks is why every networked device needs its own power supply, whereas a card plugged into an internal bus (e.g. via PCIe) can draw power directly from the motherboard.

### Related

- [[SoT - The Logical Definition of a Computer]]—extends: gives the concrete engineering dimensions behind that SoT's "Memory Bus (Nanoseconds)" vs. "Network (Milliseconds)" distinction—coupling, management, and power, not just speed. [extends:: [[SoT - The Logical Definition of a Computer]], strength=3, confidence=high]
