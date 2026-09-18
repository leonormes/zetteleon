---
conformant: true
created: 2026-09-18T00:00:00+00:00
created_utc: 2026-09-18T00:00:00Z
modified: 2026-09-18T00:00:00+00:00
permalink: llmeon/30-library/100-zettelkasten/the-von-neumann-architecture-uses-a-single-memory-for-both-instructions-and-data
prodos.atomic.form: distinction
prodos.kind: atomic
source_title: Defining One Computer Concept
status: seed
tags:
- computer-science
- computer-architecture
- hardware
title: The Von Neumann Architecture Uses a Single Memory for Both Instructions and Data
type: concept
---
## The Von Neumann Architecture Uses a Single Memory for Both Instructions and Data

The Von Neumann architecture stores program instructions and the data they operate on in one unified memory, fetched through the same address space and the same pathway. This is the design underlying most general-purpose computers, and it stands in contrast to a Harvard architecture, which keeps instruction memory and data memory physically separate.

### Scope & Conditions

Describes the memory-organisation choice itself—one memory, one address space, one fetch path—not any specific implementation of the CPU, buses, or I/O built on top of it.

### Evidence

> "The predominant model underlying most modern computers is the Von Neumann architecture, which features a central processing unit (CPU), a unified memory system for storing both program instructions and data, and input/output (I/O) mechanisms."

### Implications

- Sharing one memory and one fetch path for both instructions and data forces the CPU to serialise the two kinds of access—the root cause of the "Von Neumann bottleneck," where a large share of a CPU's cycle time goes to fetching instructions rather than executing them.
- Treating instructions as ordinary data in the same memory is what makes the stored-program concept work at all: it's why a computer can load a new program into RAM, and why self-modifying code and JIT compilation are possible in a way a strict Harvard-architecture machine doesn't support as directly.

### Related

- [[SoT - The Functional Anatomy of a Computer]]—extends: this is the underlying memory-organisation model that Functional Anatomy's CPU↔memory/I/O picture is built on, though that SoT doesn't name the architecture explicitly. [extends:: [[SoT - The Functional Anatomy of a Computer]], strength=3, confidence=high]

#### Further Reading

- [Code: The Hidden Language of Computer Hardware and Software — Charles Petzold, Ch. 18 "From Abaci to Chips"](calibre://view-book/GCcalibreBooks/344/EPUB)—_names the stored-program concept and the "von Neumann bottleneck" directly, and traces both to the EDVAC design decisions._
