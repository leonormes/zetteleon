---
conformant: false
created: 2026-09-18T00:00:00+00:00
created_utc: 2026-09-18T00:00:00Z
modified: 2026-09-25T16:29:27+00:00
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/multi-core-and-multi-processor-systems-differ-in-how-chips-package-parallelism
prodos.atomic.form: distinction
prodos.kind: atomic
source_title: Defining One Computer Concept
status: seed
tags: [computer-architecture, computer-science, concurrency]
title: Multi-Core and Multi-Processor Systems Differ in How Chips Package Parallelism
type: concept
---

## Multi-Core and Multi-Processor Systems Differ in How Chips Package Parallelism

A multi-core processor packages two or more independent execution cores onto a single integrated-circuit chip; a multi-processor system instead places multiple distinct physical CPU chips on the same motherboard. Both add parallel execution units to what is still, by the kernel-boundary definition, one computer—they just differ in whether the extra cores share a die or a socket.

### Scope & Conditions

Names the packaging distinction as commonly used. In practice the terminology has not fully settled—vendors increasingly use "processor" for whatever plugs into a socket, which may itself contain multiple chips or multiple cores per chip.

### Evidence

> "Multi-core Processors: These feature a single integrated circuit (IC) chip containing two or more independent processing units, known as 'cores'… Multi-processor Systems: These systems contain multiple distinct physical CPU chips installed on the same motherboard."

### Implications

- Neither arrangement fragments the machine into multiple computers: what matters for the "one computer" question is the single OS kernel instance managing all of them, not whether the extra execution units share a die (see [[SoT - The Logical Definition of a Computer]]'s Multicore Paradox).
- Because the terminology is genuinely unsettled at the vendor level, "how many processors does this have?" can be an ambiguous question in a way "how many cores?" and "how many sockets?" are not.

### Related

- [[SoT - The Logical Definition of a Computer]]—extends: supplies the packaging-level terminology (die vs. socket) underneath that SoT's Multicore Paradox, which uses "128 cores" without distinguishing how they're packaged. [extends:: [[SoT - The Logical Definition of a Computer]], strength=3, confidence=high]

#### Further Reading

- [Programming Language Pragmatics — Michael L. Scott, §12.1.2 "Multiprocessor Architecture"](calibre://view-book/GCcalibreBooks/196/PDF)—_explicitly flags that "processor" terminology hasn't settled in the multicore era, and traces the historical shift from "processor = one chip" to today's ambiguity._
