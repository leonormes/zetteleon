---
conformant: false
created: 2026-09-18T00:00:00+00:00
created_utc: 2026-09-18T00:00:00Z
modified: 2026-09-26T08:45:39+00:00
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/type-1-hypervisors-run-directly-on-hardware-while-type-2-hypervisors-run-as-host-applications
prodos.atomic.form: distinction
prodos.kind: atomic
source_title: Defining One Computer Concept
status: seed
tags: [computer-science, operating-systems, virtualization]
title: Type 1 Hypervisors Run Directly on Hardware While Type 2 Hypervisors Run as Host Applications
type: concept
---

## Type 1 Hypervisors Run Directly on Hardware While Type 2 Hypervisors Run as Host Applications

A Type 1 (bare-metal) hypervisor runs directly on the physical hardware with no host operating system underneath it, giving high performance and strong isolation (e.g. VMware ESXi, Xen, KVM). A Type 2 (hosted) hypervisor instead runs as an ordinary application on top of a conventional host OS, which is easier to manage but typically has slightly lower performance and isolation (e.g. VirtualBox, Parallels, VMware Workstation).

### Scope & Conditions

Describes the classical Type 1/Type 2 split. Modern implementations (e.g. KVM using kernel modules) increasingly blur this line, so treat it as a useful conceptual distinction rather than a strict taxonomy of every hypervisor shipping today.

### Evidence

> "Type 1 (Bare-Metal) Hypervisors: Run directly on the host hardware, without a conventional host OS underneath… They offer high performance and strong isolation. Type 2 (Hosted) Hypervisors: Run as applications on top of a standard host operating system… They are generally easier to manage but may have slightly lower performance and isolation compared to Type 1."

### Implications

- Either type produces the same logical outcome described in [[SoT - The Logical Definition of a Computer]]'s abstraction table—one physical box hosting N distinct guest kernels—but Type 1 removes the host OS's overhead and attack surface from the equation entirely, which is why it's the default choice for production virtualization at scale.
- Choosing Type 2 for local development (VirtualBox, Parallels) trades some performance and isolation for the convenience of running virtualization as just another application on a normal desktop OS.

### Related

- [[SoT - The Logical Definition of a Computer]]—extends: splits the "Virtual Machine" row of that SoT's abstraction table (1 Box → N Computers via the Hypervisor) into the two concrete ways a hypervisor itself can be deployed. [extends:: [[SoT - The Logical Definition of a Computer]], strength=3, confidence=high]

#### Further Reading

- [Container Security: Fundamental Technology Concepts That Protect Containerized Applications — Liz Rice, "Type 1 VMMs, or Hypervisors"](calibre://view-book/GCcalibreBooks/720/EPUB)—_gives the clearest technical account of the split, down to the privilege-ring level (hypervisor at Ring 0, guest kernel at Ring 1 under Type 1)._
