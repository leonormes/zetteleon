---
conformant: true
contradicts: []
created: 2026-10-21 14:00:00+00:00
epistemic_status: low
evidence_links: []
modified: 2026-10-21 14:00:00+00:00
proposition: A clinical observation that does not conform to the OMOP common data
  model is undefined in the interoperability domain and not a fact the schema failed
  to capture, because the model constitutes the domain of valid clinical facts for
  that purpose.
status: seed
tags:
- formal-methods
- ohdsi
- omop
- topic/data-modelling
title: A Clinical Observation Outside the Common Data Model Is Undefined in That Domain
  Rather Than Poorly Captured
type: claim
permalink: llmeon/30-library/100-zettelkasten/a-clinical-observation-outside-the-common-data-model-is-undefined-in-that-domain-rather-than-poorly-captured
---

## A Clinical Observation Outside the Common Data Model Is Undefined in That Domain Rather Than Poorly Captured

A clinical observation that does not conform to the OMOP common data model is not a fact the schema failed to capture. It is undefined in the interoperability domain the model creates. The model is not approximating clinical reality but constituting the domain of valid clinical facts for shared analysis.

### Scope & Conditions

- The claim is about validity inside the OHDSI interoperability domain, not about clinical truth. The patient and the observation exist whether or not the model can hold them.
- The vault's own ETL guidance shows the model has a slot for the unmappable, so the practice is not purely constitutive. Source codes that cannot be mapped are kept with a placeholder concept id of 0 (see Tensions).
- Without the shared model the SoT says the cost lands on people: engineers reconcile heterogeneous sources by hand and results are ambiguous.

### Evidence

> "A clinical observation that does not conform to CDM is not "a fact the schema failed to capture"—it is undefined in that informatics domain. The schema is not approximating clinical reality; it is constituting the domain of valid clinical facts."
> ([[SoT - Structure is Truth is a Unifying Axiom Across Formal Systems]], §2, Clinical Data row)

> "The derived table `OBSERVATION_PERIOD` defines the "trust interval" for a patient. ... You cannot query for "absence of disease" outside of these dates. If a patient is not in an observation period, they effectively do not exist."
> ([[SoT - OHDSI ETL Process]], §3.2 The Observation Period, abridged)

### Implications

- The observation period is a clean example of constitutive structure: a question about absence is meaningful only inside the interval the model defines.
- Data-quality work then becomes checking conformance to the model and not checking agreement with an outside record.

### Related

[implements:: [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]], strength=4, confidence=medium]

[supports:: [[The Same Constitutive Schema Removes a Class of Runtime Failure in Type Theory, Clinical Data, Infrastructure and Cognitive Scaffolding]], strength=3, confidence=medium]

- [[Structure Constitutes the Domain of Valid Facts Rather Than Representing a Pre-Existing Truth]]—implements: clinical data is one concrete case of the core claim.
- [[The Same Constitutive Schema Removes a Class of Runtime Failure in Type Theory, Clinical Data, Infrastructure and Cognitive Scaffolding]]—supports: this is the clinical row of the cross-domain claim.
- [[SoT - OMOP Common Data Model]]—part of: the model this claim is about.
- [[SoT - OHDSI ETL Process]]—shared mechanism: the process that forces source data into the model.

### Tensions

- [[SoT - OHDSI ETL Process]]—tension, not contradiction: its rule that an unmappable source code is stored with concept id 0, which "is a valid integer", gives the undefined a place inside the model and warns that queries must exclude it, so the model represents its own gaps and does not simply refuse them.