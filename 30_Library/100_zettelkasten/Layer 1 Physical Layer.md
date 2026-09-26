---
aliases: []
conformant: true
created: 2025-05-17T16:32:47+00:00
definition: The Physical Layer is the first and lowest layer of the OSI model. It transmits raw bit streams over a physical medium, dealing with physical characteristics such as voltage levels, data rates, and physical connections.
distinguishes_from: ["[[Layer 3 Network Security Protects IP Routing and Forwarding]]", "[[Layer 5 Session Layer]]", "[[Layer 6 Presentation Layer]]"]
modified: 2026-09-25T16:29:26+00:00
non_conformance_reason: ''
permalink: llmeon/30-library/100-zettelkasten/layer-1-physical-layer
tags: [SoftwareEngineering/Networking]
title: Layer 1 Physical Layer
type: concept
used_in_claims: ["[[An Example of a Tcp Packet With All Layers]]"]
---

The Physical Layer transmits raw bit streams over a physical medium. It deals with physical characteristics such as voltage levels, data rates, and physical connections.

- Problem Solved: Provides the physical means of transmitting data over a network, including cables, wireless signals, and other hardware.

## Related

- [[Layer 3 Network Security Protects IP Routing and Forwarding]]—_higher in the same OSI stack; this note supplies the physical foundation Layer 3's routing/forwarding operations ultimately run over._
- [[Layer 5 Session Layer]]—_sibling OSI-layer concept stub, same format and origin._
- [[Layer 6 Presentation Layer]]—_sibling OSI-layer concept stub, same format and origin._
- [[Layer 7 Application Layer]]—_the layer furthest from this one in the stack; same OSI-layer concept-stub family._
- [[Layer 7 Protocol Elements in Node.js]]—_a worked Layer 7 example from the same stub batch; also ends on the same unresolved `[[OSI model]]` reference as this note._
- [[An Example of a Tcp Packet With All Layers]]—_walks a real packet through all seven layers, naming this one explicitly as "Bits/signals on wire."_
- [[INSIGHT - Networking is data labeling not wires]]—_names this exact layer as the one point where the message actually becomes signals (photons, electrons, radio waves) rather than a label._
- [[MOC - Networking]]—_the vault's networking hub; this stub wasn't linked from it before this refresh._

## See Also

- `[[OSI model]]`—dangling vault-wide, not unique to this note: the same unresolved plain link appears in [[Layer 5 Session Layer]], [[Layer 6 Presentation Layer]], [[Layer 7 Application Layer]], [[Layer 7 Protocol Elements in Node.js]], and [[MOC - Hybrid Cloud Networking]]. No note or alias resolves it anywhere in the vault—flagging rather than fabricating a target. Worth creating as its own SoT/MOC if this OSI cluster gets developed further.
