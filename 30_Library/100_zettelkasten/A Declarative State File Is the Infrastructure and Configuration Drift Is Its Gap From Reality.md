---
conformant: true
contradicts: []
created: 2026-10-21 14:00:00+00:00
epistemic_status: medium
evidence_links: []
modified: 2026-10-21 14:00:00+00:00
proposition: In declarative infrastructure the target state file is the definition
  of the environment and not a description of it, so configuration drift is the gap
  between the structure and the reality it is meant to constitute.
status: seed
tags:
- formal-methods
- topic/software-architecture
- infrastructure-as-code
- devops
title: A Declarative State File Is the Infrastructure and Configuration Drift Is Its
  Gap From Reality
type: claim
permalink: llmeon/30-library/100-zettelkasten/a-declarative-state-file-is-the-infrastructure-and-configuration-drift-is-its-gap-from-reality
---

## A Declarative State File Is the Infrastructure and Configuration Drift Is Its Gap From Reality

In declarative infrastructure the target state file is the definition of the environment, not a description of what should be running. Configuration drift is therefore the name for the gap between the structure and the reality it is supposed to constitute, and the structure is treated as the reference. Where the structure is absent, infrastructure state lives in operators' memory and ticket systems.

### Scope & Conditions

- "The structure wins" is a policy that mature teams adopt and not a law. A running system can legitimately diverge, for example after an emergency fix, and the divergence may be resolved by updating the file. The claim holds where the team has chosen to treat the file as the reference.
- It is stated for declarative tools that reconcile a running system toward a target. It is weaker for imperative scripts, where no standing target exists to drift from.
- The same split appears in Kubernetes, where desired state is declared and actual state is observed ([[Kubernetes State Comes in Three Kinds Desired Actual and Implicit]]).

### Evidence

> "The IaC state file IS the infrastructure. The target state is not a description of what should be running—it IS the definition of the environment. "Configuration drift" is the technical name for the gap between structure and the reality it is supposed to constitute."
> ([[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]], §2, Declarative Infrastructure row, emphasis markers omitted)

> "Manual change-control procedures. Infrastructure state lives in operators' memory and ticket systems. Each incident requires archaeology."
> (same row, "Runtime Pays When Absent")

The library offers only a publisher description saying that infrastructure as code lets a reader "safely make infrastructure changes, and prevent configuration drift" (*Azure Infrastructure as Code*, "about this book"). It is not evidence for the constitutive reading.

### Implications

- Drift is a defect report against reality, not against the file. The fix is to reconcile the running system to the file, or to change the file deliberately.
- The reference signal that control loops steer toward is the structure, which is the role [[etcd and the API Server Hold the Authoritative Reference Signal for Every Control Loop]] describes for Kubernetes.

### Related

[implements:: [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]], strength=4, confidence=medium]

[supports:: [[The Same Constitutive Schema Removes a Class of Runtime Failure in Type Theory, Clinical Data, Infrastructure and Cognitive Scaffolding]], strength=3, confidence=medium]

- [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]]—implements: infrastructure is one concrete case of the core claim.
- [[The Same Constitutive Schema Removes a Class of Runtime Failure in Type Theory, Clinical Data, Infrastructure and Cognitive Scaffolding]]—supports: this is the infrastructure row of the cross-domain claim.
- [[Kubernetes State Comes in Three Kinds Desired Actual and Implicit]]—shared mechanism: the desired and actual split behind drift.
- [[etcd and the API Server Hold the Authoritative Reference Signal for Every Control Loop]]—shared mechanism: the structure as the reference signal.
- [[How to Test Whether a Structure Is Constitutive or Merely Representational]]—implements: this is the clearest case for the Drift Test.

### Tensions

- [[Kubernetes State Comes in Three Kinds Desired Actual and Implicit]]—tension, not contradiction: that note adds a third kind, implicit state derived from relationships, which the two-way split of structure and reality leaves out.