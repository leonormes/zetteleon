---
title: MESH API Certificate Renewal
wiki_type: dossier
entity_kind: project
created: 2026-05-12T18:57:00+01:00
modified: 2026-05-12T18:57:00+01:00
tags: [wiki, dossier, project]
sources:
  - raw/2026-05-12-pieces-mesh-api-csr.md
---

## Summary

NHS MESH API certificate renewal project for replacing an expiring client certificate. The work involves generating a new CSR (Certificate Signing Request) using Java keytool and coordinating with the NHS National Service Desk (ticket CS1446557) to obtain the renewed certificate for API-based integration.

## Key Facts

- **Using MESH API, not MESH Client** — The certificate is for API-based integration, not the NHS MESH client software > "We are using the MESH API (not the MESH client), and this is to replace the existing certificate that's expiring" — [[raw/2026-05-12-pieces-mesh-api-csr]] (Pieces: 89eefa6a-2342-4bfc-8470-6c6e2673a7af)

- **CSR successfully generated** — The keytool command completed without errors, only a cosmetic JKS format warning > "The CSR generated successfully — no error, just an informational warning" — [[raw/2026-05-12-pieces-mesh-api-csr]] (Pieces: 880f648a-a7ac-4f9d-983d-0efc9e0ed0e8)

- **CSR location** — `/Volumes/DAL/Fitfile/meshCerts/mesh-api.csr` > "keytool -certreq -alias meshclient -keystore /Volumes/DAL/Fitfile/meshCerts/MESH.keystore -file /Volumes/DAL/Fitfile/meshCerts/mesh-api.csr" — [[raw/2026-05-12-pieces-mesh-api-csr]] (Pieces: e69b17ef-cbec-44d6-9e4e-f471c5b8ee68)

- **Keystore location** — `/Volumes/DAL/Fitfile/meshCerts/MESH.keystore` (JKS format) > "keystore /Volumes/DAL/Fitfile/meshCerts/MESH.keystore" — [[raw/2026-05-12-pieces-mesh-api-csr]] (Pieces: e69b17ef-cbec-44d6-9e4e-f471c5b8ee68)

- **Certificate DN** — `CN=8KM90HC001.8KM90.api.mesh-client.nhs.uk` > "dname CN=8KM90HC001.8KM90.api.mesh-client.nhs.uk" — [[raw/2026-05-12-pieces-mesh-api-csr]] (Pieces: e69b17ef-cbec-44d6-9e4e-f471c5b8ee68)

- **NHS Service Desk ticket** — CS1446557 > "Thank you for contacting the National Service Desk... CS1446557" — [[raw/2026-05-12-pieces-mesh-api-csr]] (Pieces: 01b4c4df-6703-44a5-927c-e2569d8faea4)

- **Contact at NHS** — Peter Begg, National Service Desk > "draft reply to Peter Begg at the NHS National Service Desk" — [[raw/2026-05-12-pieces-mesh-api-csr]] (Pieces: 89eefa6a-2342-4bfc-8470-6c6e2673a7af)

- **JKS warning is cosmetic** — Java 9+ recommends PKCS12 but existing JKS keystore works fine > "The JKS keystore uses a proprietary format warning is cosmetic" — [[raw/2026-05-12-pieces-mesh-api-csr]] (Pieces: 880f648a-a7ac-4f9d-983d-0efc9e0ed0e8)

## Timeline

- **2026-05-12 14:38** — Received email from NHS National Service Desk requesting clarification on certificate use (API vs Client) and FQDN for CSR
- **2026-05-12 14:39** — Drafted reply to Peter Begg confirming API use and intent to regenerate CSR with FQDN
- **2026-05-12 14:40** — Ran keytool command to generate CSR (`mesh-api.csr`)
- **2026-05-12 14:41** — CSR generation confirmed successful; JKS warning documented as non-critical

## Connections

- [[wiki/orgs/NHS National Service Desk]] — External organisation managing certificate requests
- [[wiki/concepts/MESH API]] — NHS Message Exchange for Social Care and Health API
- [[wiki/concepts/X.509 Certificates]] — Certificate standards and CSR generation
- [[Terraform IaC Modules]] — May be related if certificate deployment is automated

## Contradictions

None identified.

## Open Questions

- What is the FQDN that NHS requested for the CSR regeneration?
- Has the new CSR been submitted to the National Service Desk?
- What is the expected turnaround time for certificate issuance?
- Is there a dependency on this certificate for any production systems?
