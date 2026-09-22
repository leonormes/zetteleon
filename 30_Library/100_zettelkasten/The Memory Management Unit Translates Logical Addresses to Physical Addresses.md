---
conformant: false
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
created: 2026-09-18T00:00:00+00:00
created_utc: '2026-09-18T00:00:00Z'
modified: 2026-09-19T15:44:44+00:00
permalink: llmeon/30-library/100-zettelkasten/the-memory-management-unit-translates-logical-addresses-to-physical-addresses
prodos.atomic.form: mechanism
prodos.kind: atomic
source_title: Defining One Computer Concept
status: seed
tags: [computer-science, memory-management, operating-systems]
title: The Memory Management Unit Translates Logical Addresses to Physical Addresses
type: concept
---

## The Memory Management Unit Translates Logical Addresses to Physical Addresses

Programs and the CPU operate on logical (virtual) addresses that exist only within the private address space the kernel creates for a process; a dedicated hardware component, the Memory Management Unit (MMU), translates each logical address into the actual physical RAM location, and it does so under the kernel's control rather than the process's.

### Scope & Conditions

Applies to any OS that implements virtual memory (essentially every modern general-purpose kernel). The note is about the translation mechanism itself, not the higher-level policy built on top of it (paging vs segmentation, page-replacement algorithms).

### Evidence

> "Programs and the CPU operate using logical addresses (also called virtual addresses)… They do not directly correspond to hardware memory locations… The translation between the logical addresses used by software and the physical addresses required by the hardware is performed by a specialized hardware component called the Memory Management Unit (MMU), which operates under the control of the OS kernel."

### Implications

- Memory protection—one process being unable to read or corrupt another's memory, or the kernel's—is a direct side-effect of this translation layer, not a separately bolted-on feature: a process simply has no logical address that maps to memory it doesn't own.
- This is the concrete hardware mechanism behind the kernel's "logical sovereignty": a kernel can hand out a private, contiguous-looking address space to every process regardless of how the underlying physical RAM is actually fragmented or shared.

### Related

- [[SoT - The Logical Definition of a Computer]]—extends: this is the specific mechanism by which that SoT's Kernel Litmus Test (§1: "same Kernel Address Space and Scheduler = one computer") is physically enforced at the memory level, not just asserted. [extends:: [[SoT - The Logical Definition of a Computer]], strength=4, confidence=high]
- [[SoT - The Functional Anatomy of a Computer]]—_related but distinct: that SoT's Memory-Mapped I/O covers CPU↔device-register communication; this note covers CPU↔RAM addressing. Both are hardware indirection layers the kernel sits on top of, but they solve different problems (talking to devices vs isolating processes)._
