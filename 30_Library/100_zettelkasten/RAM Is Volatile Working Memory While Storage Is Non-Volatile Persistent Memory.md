---
conformant: false
created: 2026-09-18T00:00:00+00:00
created_utc: 2026-09-18T00:00:00Z
modified: 2026-09-26T08:45:36+00:00
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/ram-is-volatile-working-memory-while-storage-is-non-volatile-persistent-memory
prodos.atomic.form: distinction
prodos.kind: atomic
source_title: Defining One Computer Concept
status: seed
tags: [computer-architecture, computer-science, hardware]
title: RAM Is Volatile Working Memory While Storage Is Non-Volatile Persistent Memory
type: concept
---

## RAM Is Volatile Working Memory While Storage Is Non-Volatile Persistent Memory

RAM is volatile: it holds the data and instructions currently in use by the CPU, but loses its contents the moment power is removed. Storage (HDD/SSD) is non-volatile: it holds data persistently, without power, which is why the operating system, applications, and user files live there rather than in RAM.

### Scope & Conditions

Describes the volatility distinction itself. Doesn't cover the specific technologies (magnetic platters vs. flash) or performance characteristics beyond what follows directly from volatility.

### Evidence

> "RAM serves as the computer's primary workspace–a volatile (temporary) storage area holding data and instructions currently in use by the CPU and software… RAM is distinct from persistent storage; its contents are lost when power is removed… [Storage] provide[s] non-volatile, long-term storage for the operating system, applications, user files, and other data that must persist even when the computer is powered off."

### Implications

- Anything that must survive a reboot or power loss—the OS itself, saved files, installed applications—has to live on storage, not RAM, regardless of how much faster RAM is to access.
- The speed/persistence trade-off this creates is why databases and other systems that want RAM-like speed with disk-like durability need an explicit durability mechanism (write-ahead logs, battery-backed RAM, NVM) rather than getting both properties for free.

### Related

- [[SoT - The Functional Anatomy of a Computer]]—related but distinct: that SoT covers CPU↔memory addressing (MMIO), and CPU↔RAM translation is covered by [[The Memory Management Unit Translates Logical Addresses to Physical Addresses]]; this note covers the volatility property of RAM itself, not how it's addressed.

#### Further Reading

- [Database Internals: A Deep Dive Into How Distributed Data Systems Work — Alex Petrov, "Durability in Memory-Based Stores"](calibre://view-book/GCcalibreBooks/1278/PDF)—_lays out exactly why RAM's volatility is the limiting factor for in-memory databases, and what it costs to work around it._
