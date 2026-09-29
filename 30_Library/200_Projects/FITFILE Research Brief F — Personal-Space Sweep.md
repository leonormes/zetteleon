---
conformant: false
created: 2026-09-28T01:00:00+00:00
modified: 2026-09-29T10:37:42+00:00
non_conformance_reason: Raw agent research brief kept as source material for the FITFILE
  context brief; awaiting review, not a canonical source note.
permalink: llmeon/00-inbox/fitfile-research-briefs/fitfile-research-brief-f-personal-space-sweep
project_name: FITFILE
source: FITFILE Confluence, read-only sweep on 2026-09-28 by a Claude Code research
  agent
source_url: null
status: draft
tags: [fitfile, source/llm, topic/data-linkage]
title: FITFILE Research Brief F — Personal-Space Sweep
type: source
---

%% Raw agent research brief (Claude Code, 2026-09-28), kept as source material for the FITFILE context brief. Not your own writing, so no own_words property. Page IDs link to Confluence. Redacted for the vault where needed: personal names, a prospect's name, page-hygiene and security-debt specifics. %%

Part of: [[FITFILE Context Brief — What We Do and How We Link Data Silos]]

## F—Personal-space Sweep (Read by Main Agent, 2026-09-28)

Personal spaces checked (page trees): all 18. Most are empty templates.

### Pages Read

- OMOP Flow: Irreversible Pseudonymisation and Central Hashicorp Vault Configuration [2869297153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2869297153), personal space, 2026-06-15
  - Pseudonymisation secrets held in FITFILE's central HashiCorp Vault; nodes fetch as needed; auto-synced on rotation; never exposed via UI/API.
  - All nodes in the network share one common secret used in HMAC-SHA-256 hashing → same identifier gives same pseudonym on every node (Inference: this is what makes cross-node deterministic pseudonymous linkage possible; also a single shared key across the whole network).
  - OMOP end-to-end workflow: irreversible pseudonymisation only. Query Plans: reversible or irreversible, chosen by user per operation.
- HDRS TT project [3034906637](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034906637), personal space, 2026-09-14 (live doc)
  - Federated node network across Eastern England, North West, West Midlands, South West SDEs; EE node = coordinating node routing authorised queries to other SDE nodes.
  - Use case: Chronic Kidney Disease (CKD), pharma partner input + registry requirements; synthetic CKD datasets generated at each SDE from a "Minimally Transformed Data Extract" (MTDE).
  - Shared OMOP mapping spec authored by The Hyve (CDM version, vocab release, standard concepts, units); each SDE uses own or FITFILE ETL; The Hyve assesses conformance/DQ (OHDSI DQD).
  - EE node remotely queries OMOP and MTDE at other SDE nodes; privacy-preserving outputs; "data remains at source wherever possible".
  - Gates: ≥2 SDEs by early Dec 2026 (mid-project gate); full network Feb 2027; final report 31 Mar 2027; reusable blueprint aligned to "multi-SDE blueprint" for HDRS "Data Driver" projects.
- FITFILE/EOE - De-identification & Linkage Test Plan [2085650437](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2085650437), personal space, 2025-02-25
  - NHS number (or direct identifier) → "fit token"; determinism checked by re-running and comparing MD5 of outputs.
  - IG rules: small number suppression (threshold set in Bunny), removal of restricted codes (CUH list), NDOO records excluded.
- AHS Architecture [2951675906](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2951675906), personal space, 2026-09-18
  - Capabilities: RBAC (Auth0 + SpiceDB), pipeline (harmonisation, OMOP mapping, linkage, privacy treatment), federation, scalability.
  - Flow: data source → Node (local compute/query) → federation layer (query distribution + result aggregation) → presentation/analytics → identity/access wrapping.
  - "Draw the boundary of what sits inside [customer] environment vs central/shared FITFILE infrastructure"—the point people get lost. "It's all about Linkage, Treatment, non-Structured data, ETL'ing, interoperability."
- Convincing EOE and CUH about ATLAS [2573565954](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2573565954), personal space, 2026-01-20
  - Data provider (CUH) pushed back on OHDSI Atlas needing a write schema on a busy production clinical informatics server: load, unplanned/uncosted work, security/governance review.
  - FITFILE position: execution and results stay at source; Atlas only generates cohort definitions; isolated schema; cohort rows deleted after extract.
  - Illustrates provider-side silo friction: operational ownership + change control, not just IG.
- Research on [vaccines manufacturer] - September 2026 [3034710017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034710017), personal space, 2026-09-08 (pharma prospect; keep commercial detail out)
  - FITFILE self-assessment: data-type agnostic (files or DBs); linkage with anonymised or pseudonymised IDs, deterministic or probabilistic; "previously linked records across different hospital datasets"; query at source, only privacy-treated records/results retrieved.
  - Platform has no native longitudinal patient record—datasets are stored independently, not organised into patient timelines; longitudinal views need query-time linkage + temporal logic.
  - Multinational: no common identifier (NHS number) across jurisdictions → linkage feasibility per country/dataset; alternative = common analysis per country, no cross-border patient linkage.
  - Genomic formats (VCF) not yet tested; derived variables could be linked as structured fields.
  - "Strongest proposition": person-level linkage of vaccination + primary care + secondary care + lab + mortality, plus registries/genomics on demand.
- Source Data Querying - prep for workshop [2985361409](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2985361409), personal space, 2026-08-26
  - EE SDE wants researchers to access non-OMOP "source" data alongside OMOP outputs.
  - Linkage blocker: OMOP data carries hashed NHS numbers; source data has untreated NHS numbers; "we do not have lookup tables" → can't join them without re-treating.
  - Question whether linkage applies to source-data queries "in the same way it is to DAR-driven outputs … linked across multiple providers" (Inference: DAR outputs are already linked across providers).
  - Privacy treatment may not apply identically to non-OMOP data → leakage risk; DSA coverage unclear; provider load not yet communicated.
- Upcoming technical work [3034906629](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034906629), personal space, 2026-09-23 (live)
  - "Installing our Nodes into the largest NHS organisations"; HDRS support is top in-house priority.
  - Networking architecture: improve Node-to-Node (data provider/consumer) comms and centralise support access—heavily tied to HDRS inter-node connectivity options.
  - Release coupling: a release to one customer goes to all (POC of per-customer release done for NUH). Node divergence at MKUH/NNUH.
  - (Security backlog items deliberately not copied.)
- NHS-PET Schedule 2, Appendix 2A: Technical Specification [1601208321](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1601208321), your personal space, 2023-08-10—copy of NHS England tender spec (Zühlke bid docs)
  - NHS-PET = NHS England privacy enhancing technology for the Federated Data Platform (FDP-AS): classify, protect (anonymise, pseudonymise, hash, tokenise, encrypt, redact, mask, generalise), audit, manage.
  - Patterns: Runtime (fail-closed), Data Interface, Service (incl. re-identification), Hidden.
  - Joining across trusts at ICB/ICS tenant level: key identifiers (NHS number) privacy-treated with a common key or seed.
  - Re-identification authorised by role + purpose agreed with the data controller.
  - PDS as national truth for matched patients; pseudonymised PDS must join with other pseudonymised national datasets; PET must not build its own siloed PII registry.
  - Keys: external KMS/HSM, rotation with re-tokenisation at low downstream impact.
- OHDSI 2026 [3059875842](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3059875842), personal space, 2026-09-23—conference takeaways: Lettuce (source-term → OMOP concept matching), OmopIndices, FastSSV (catch analytically wrong OMOP queries; relevant for NL querying), TRExt (DARE UK, federated privacy-preserving unstructured text). Pharma prospects similar to existing pharma partner.
- Testing the New PET [1597800449](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1597800449), your personal space, 2023—bid answer draft on testing approach (low relevance).
- Brain dumps [2340028421](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2340028421), personal space—empty.

### Found, not Read

- FITFILE / EOE SDE Testing Strategy [2082537473](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2082537473); Cohort Discovery Test Plan [2086240257](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2086240257); Data Harmonisation Test Plan (draft) [2086305793](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2086305793)—personal space
- Data Provider Preparation and Actions [2613018641](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2613018641)—personal space
- Demo de-identification Tools [2427027457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2427027457); Demo complex queries [2403794945](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2403794945)—personal space
- Governance support and activities [2695069697](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2695069697); SOC for FITFILE [3002433543](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3002433543); ISO270001 workload [2687926273](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2687926273)—personal space
- FITFILE Node Deployment - Technical Pack [2352873473](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2352873473); Anonymization Keywords [1597308934](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1597308934)—your personal space
