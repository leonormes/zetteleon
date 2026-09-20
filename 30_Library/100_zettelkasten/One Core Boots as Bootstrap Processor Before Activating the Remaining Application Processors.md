---
conformant: true
contradicts: []
created: 2026-09-18T00:00:00+00:00
created_utc: 2026-09-18 00:00:00+00:00
epistemic_status: high
evidence_links: []
modified: 2026-09-19T15:44:40+00:00
permalink: llmeon/30-library/100-zettelkasten/one-core-boots-as-bootstrap-processor-before-activating-the-remaining-application-processors
prodos.atomic.form: mechanism
prodos.kind: atomic
proposition: In a multi-core or multi-processor system, one core—the Bootstrap Processor (BSP)—initialises the system and boots the OS kernel on its own, and only once the kernel is running does it explicitly activate the other cores (Application Processors) so they can begin executing tasks.
source_title: Defining One Computer Concept
status: seed
tags: [computer-architecture, computer-science, operating-systems]
title: One Core Boots as Bootstrap Processor Before Activating the Remaining Application Processors
type: claim
---

## One Core Boots as Bootstrap Processor Before Activating the Remaining Application Processors

In a multi-core or multi-processor system, one core—the Bootstrap Processor (BSP)—initialises the system and boots the OS kernel on its own. Only once the kernel is running does it explicitly activate the other cores—the Application Processors (APs)—so they can begin executing tasks.

### Scope & Conditions

Describes the boot-time sequencing of core activation in SMP-style systems; doesn't cover the scheduling policy the OS then uses to distribute work across the activated cores.

### Evidence

> "In many systems, one core (the Bootstrap Processor or BSP) initializes the system and boots the OS. Once the kernel is running, it then explicitly activates the other cores (Application Processors or APs) to begin executing tasks."

### Implications

- A multi-core machine doesn't come up "all at once": there's a brief window during boot where the system is genuinely single-core, before the kernel it just booted brings the rest of the hardware online.
- This sequencing is what makes a single OS kernel instance—rather than some pre-boot arbiter—the thing that ultimately establishes control over every core, consistent with the kernel being the definition of the logical boundary in [[SoT - The Logical Definition of a Computer]].

### See Also

- [[SoT - The Logical Definition of a Computer]]
