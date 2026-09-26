---
conformant: false
created: 2026-09-18T00:00:00+00:00
created_utc: '2026-09-18T00:00:00Z'
modified: 2026-09-25T16:29:25+00:00
non_conformance_reason: "missing schema field definition for type concept (required when conformant - true); missing schema field distinguishes_from for type concept (required when conformant - true); missing schema field used_in_claims for type concept (required when conformant - true)"
permalink: llmeon/30-library/100-zettelkasten/iaas-paas-and-saas-progressively-abstract-away-the-underlying-computer
prodos.atomic.form: distinction
prodos.kind: atomic
source_title: Defining One Computer Concept
status: seed
tags: [cloud, computer-science, distributed-systems]
title: IaaS, PaaS, and SaaS Progressively Abstract Away the Underlying Computer
type: concept
---

## IaaS, PaaS, and SaaS Progressively Abstract Away the Underlying Computer

The three cloud service models sit on a single gradient defined by how much of the underlying computer the provider hides from the user. IaaS exposes virtualised hardware, so the user still manages an OS and therefore still deals with "a computer." PaaS abstracts the OS and runtime away entirely, leaving the user to manage only application and data. SaaS hides the whole stack and delivers a finished application. Moving IaaS → PaaS → SaaS, the question "which computer is this running on?" becomes progressively less answerable and less relevant to the user.

### Scope & Conditions

Describes the user-facing abstraction gradient of the three canonical cloud service models, not the provider-side implementation (which still runs on real kernels and hypervisors throughout).

### Evidence

> "Infrastructure as a Service (IaaS): Provides access to fundamental computing infrastructure–virtual machines, storage, networks. The user manages the OS… Platform as a Service (PaaS)… The underlying 'computer' is abstracted away. Software as a Service (SaaS): Delivers ready-to-use software applications… The concept of a 'computer' is entirely hidden."

### Implications

- A debugging or architecture question that is meaningful at one layer can be meaningless at another: "which VM is this on?" is a real question under IaaS but a category error under SaaS, where the right question is "which tenant/request?".
- This is a second, independent abstraction axis from the one in [[SoT - The Logical Definition of a Computer]]'s bare-metal/VM/container/cluster table: that table asks "who runs the kernel?"; this one asks "does the user even interact with the idea of a kernel at all?"

### Related

- [[SoT - The Logical Definition of a Computer]]—extends: adds the cloud-service-model axis to that SoT's existing physical/VM/container/cluster abstraction table. [extends:: [[SoT - The Logical Definition of a Computer]], strength=3, confidence=high]
- [[Cloud Providers Achieve Elasticity Through Resource Pooling and Multi-Tenancy]]—related but distinct: that note describes the provider-side mechanism (resource pooling, multi-tenancy) that makes any point on this abstraction gradient elastic; this note describes what the user sees at each point.
