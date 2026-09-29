---
conformant: false
created: 2026-09-28T01:00:00+00:00
modified: 2026-09-29T10:37:45+00:00
non_conformance_reason: Raw agent research brief kept as source material for the FITFILE
  context brief; awaiting review, not a canonical source note.
permalink: llmeon/00-inbox/fitfile-research-briefs/fitfile-research-brief-a-business-and-value-proposition
project_name: FITFILE
source: FITFILE Confluence, read-only sweep on 2026-09-28 by a Claude Code research
  agent
source_url: null
status: draft
tags: [fitfile, source/llm, topic/business, topic/secure-data-environments]
title: FITFILE Research Brief A — Business and Value Proposition
type: source
---

%% Raw agent research brief (Claude Code, 2026-09-28), kept as source material for the FITFILE context brief. Not your own writing, so no own_words property. Page IDs link to Confluence. Redacted for the vault where needed: personal names, a prospect's name, page-hygiene and security-debt specifics. %%

Part of: [[FITFILE Context Brief — What We Do and How We Link Data Silos]]

## Brief A: what FITFILE Is, the Problem it Solves, and Its Value Proposition

This is a read-only review of FITFILE's Confluence, made on 2026-09-28.

- Citations. The first time a page is cited, it appears as (Title, ID, last modified). Later citations give the ID only. Section 6 lists every page.
- Inferences. "Inference:" marks my own interpretation.
- People are named by role, not by name.

### 1. Summary

- What it is. FITFILE sells a federated platform that accesses record-level health data, privacy-treats it and links it across organisations.
  - A Node runs inside each data controller's GDPR perimeter.
  - A coordinating Node queries the other Nodes and links their privacy-treated outputs.
  - Raw data is never pooled (1. Introduction & Goals, [1696727046](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1696727046), 2024-09-04; Technical Overview, [2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026), 2025-04-25).
- The problem it names. Health data sits in unconnected silos. Uniting it without consent is hard, consent does not scale, and data controllers are risk-averse (Tier 1 - Business Requirements, [521699377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521699377), 2023-01-13).
- Who buys and who uses. NHS Secure Data Environment (SDE) programmes buy—mainly the Eastern England SDE, which "has contracted FITFILE". NHS trusts host the Nodes. SDE data managers and researchers use them (Eastern England SDE - Project Summary (Internal), [2829516801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2829516801), 2026-09-27).
- How the positioning shifted (HDRS TT Federated Linkage - Kick-Off Meeting, [3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130), 2026-09-25):
  - 2020–22: pharma real-world-evidence (RWE) SaaS;
  - 2022–23: single-trust projects;
  - 2024–25: SDE infrastructure;
  - 2026: federation across several SDEs, funded by HDRS and backed by pharma.
- Claimed differentiators:
  - data stays at source;
  - patented linkage based on zero-knowledge proofs (ZKP), with no central token store;
  - privacy treatment that keeps data useful;
  - modular, vendor-agnostic integration;
  - identical Nodes built from Terraform.
- Delivery. FITFILE deploys and runs each Node, using GitOps, in the customer's own Azure or AWS subscription. The customer pays the cloud costs. On-premise deployment is a last resort.
- Charging. Inference from invoicing pages: milestone-based, with usage-linked elements and service credits under the SLA.
- Partners.
  - The Hyve maps provider data to OMOP, a common data model, as a subcontractor.
  - The University of Nottingham's Relay+Bunny connects Nodes to HDR UK.
  - OHDSI, the community behind OMOP, supplies the analysis tools.
- Gaps.
  - There is no competitive analysis.
  - The "What does FITFILE do" page is a stub.
  - The overview, pre-sales and pricing documents sit in SharePoint.
  - SLA and compliance claims conflict between pages.

### 2. Findings

#### 2.1 What FITFILE Does

- Goal: to "support parties' use of healthcare data in a meaningful way, and support the data suppliers' need for security and privacy of each data record". In practice FITFILE:
  - accesses data at source;
  - pseudonymises or anonymises it;
  - links it across sources;
  - audits all of this ([1696727046](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1696727046)).
- Components (Glossary, [1699348489](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1699348489), 2025-05-27; FITFILE SDE Technical Glossary, [2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881), 2025-02-14):
  - FITConnect connects to data sources, runs ELT (extract, load, transform) jobs and applies privacy treatment;
  - FITCoordinator coordinates queries ("FF Cloud" is its deprecated name);
  - a Node is one or more FITConnects, optionally with a Coordinator;
  - central services are Auth0, SpiceDB, Vault and Grafana.
- Demonstrated capabilities (AHS Demo, [2918547484](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2918547484), 2026-07-13; HDRS Demo Script, [2930802691](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2930802691), 2026-07-16):
  - cohort counts and record-level "QueryPlans";
  - an OMOP workflow with the Atlas cohort-building tool embedded;
  - data profiling;
  - detection of personally identifiable information (PII);
  - custom transformations and linkage;
  - governed re-identification at the provider;
  - provider approval before any disclosure;
  - audit.
- Governance model: the Tenant (Node) is the GDPR boundary and the Project defines the purpose. Whichever of Tenant, Project and Data Source is most restrictive decides compliance (TLDR, [2156429316](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2156429316), 2025-04-17).

#### 2.2 The Problem, and for Whom

- 2021. Silos could not be united in a GDPR-compliant way without consent. Consent is "difficult, time-consuming and expensive". Data partners are risk-averse, and paying them for data ("dollars for data") is not feasible (BR-001/002, [521699377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521699377)).
- 2025. Rich access has to be balanced against "the absolute requirement to protect individual patient privacy" (RQ-1.1.1 Privacy Treat a Dataset, [2201288746](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2201288746), 2025-06-10).
- What SDE operators need (06.05.2026 - FITFILE Notes (internal consolidated version), [2804449281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2804449281), 2026-05-14):
  - feasibility checks on completeness and coverage;
  - handling of unmapped source values—the SDE doubted OMOP mapping accuracy above 75%;
  - validation of extracts before release and before charging;
  - reproducibility;
  - attribution of each record to its provider.
- Complex OMOP extracts have needed "managed service"-style support (FITFILE complex relational data processing capabilities–roadmap of planned enhancements, [2549448706](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2549448706), 2026-01-16).
- Two SDE models (UHB Product Gap, [2053996548](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2053996548), 2025-02-06; WMSDE Product Development Plan, [2080014337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2080014337), 2025-08-28):
  - "Data Curator": a central warehouse (West Midlands);
  - "Data-On-Demand": data stays at source (East of England).
  - FITFILE fitted the second model and had gaps against the first.
- Policy framing. Sales notes on the Sudlow Review stress fragmentation, UK-wide linkage including non-health data, and accredited SDEs (Sudlow-Review-lead demo page, [2368897027](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2368897027), 2025-10-28).

#### 2.3 Who Buys and Who Uses

- 2020–21 (Tier 2 - User Requirements, [521896132](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521896132), 2021-04-01; BR-007, [521699377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521699377)):
  - InsightFILE was "SaaS to paying PharmaCo customers";
  - HealthFILE served clinicians and ran inside the organisation that controls the data;
  - the consumers were pharma Market Access, Medical Affairs and R&D teams.
- 2023–24.
  - Personas: Data Admin Manager, Data Set Manager, Project Coordinator, Data Controller and Data User.
  - Target organisations: providers, data aggregators, payors, contract research organisations (CROs) and pharma (Personas, [1572864001](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1572864001), 2024-04-04; archived).
- 2025–26.
  - The Eastern England SDE contracts FITFILE. MKUH, NNUH and CUH are live, NUH is onboarding, and more trusts are in the pipeline ([2829516801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2829516801)).
  - NUH will "NOT use the FITFILE platform once the project is live", describing the project as "for the SDE's benefit" (NUHProject Summary (Internal), [2727673857](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2727673857), 2026-09-27).
  - Inference: the SDE, or whoever funds it, is the buyer. Providers have to be won over, and researchers use the platform indirectly.
- HDRS funding flow ([3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130)):
  - HDRS funds the Eastern England SDE, which in turn funds the other SDEs and FITFILE;
  - AstraZeneca contracts FITFILE directly;
  - FITFILE subcontracts The Hyve.
- Other buyers:
  - Liverpool City Region Combined Authority (LCRCA), together with the NHS AGEM commissioning support unit (CSU), for the North West SDE (NWSDE);
  - Mersey Care (High Level Design Document - LCRCA Probabilistic Data Linkage, [2417065986](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2417065986), 2026-04-08; Mersey Care - Project Summary (Internal), [2824241153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241153), 2026-09-27).
- Live projects in September 2026: the Eastern England SDE and its trusts, NWSDE, Mersey Care, LCRCA and HDRS (FITFILE Project Names, [3036839937](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3036839937), 2026-09-09).

#### 2.4 Value Proposition

- 2021 vision: "the leading trusted health information platform for united patient-level evidence" (Business Goals, [771620870](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=771620870), 2021-03-30).
- 2026 pitch ([2930802691](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2930802691); [2918547484](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2918547484); HDRS Tech Demo, [2966552577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2966552577), 2026-08-05):
  - "vendor-agnostic and built for interoperability";
  - "HDRUK is a discovery gateway—FITFILE goes further";
  - "a modular, federated layer that plugs into what already exists", with data not pooled;
  - each Node is "a blueprint, not a bespoke build".
- Linkage options ([2966552577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2966552577)):
  - FITanon;
  - FITtoken (HMAC-SHA256);
  - project salts;
  - pre-agreed keys;
  - NHS PET;
  - probabilistic matching with Bloom filters.
- Linkage claim. FITFILE says it needs no central lookup table, unlike the NHS token store. The accuracy figures on that page are still placeholders (Comparison of data linkage approaches, [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497), 2026-02-04).
- Privacy treatment:
  - automated k-anonymity that minimises loss of analytical value;
  - field-level custom transformations for wide OMOP outputs ([2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026); [2549448706](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2549448706)).
- Self-assessed gaps (Pharma prospect research (vaccines), [3034710017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034710017), 2026-09-08; draft in a personal space):
  - no longitudinal patient record;
  - VCF genomic files are untested;
  - linkage across countries needs a feasibility check.

#### 2.5 Delivery and Business Model

- Deployment ([2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026)):
  - Nodes sit in the controller's perimeter, usually on Azure or AWS;
  - on-premise is "a last course resort";
  - host naming distinguishes FITFILE-hosted from provider-hosted Nodes.
- Responsibilities (Data Provider Onboarding Plan for FITFILE Cloud Deployment, [2170519555](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2170519555), 2025-05-01; [2417065986](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2417065986)):
  - the provider provisions and pays for the cloud subscription;
  - FITFILE runs the Terraform, and patches and monitors the Nodes centrally;
  - the provider owns the network, the data and local compliance.
- Earlier variants:
  - SaaS ([521896132](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521896132));
  - a Barts Node hosted on FITFILE's own cluster (Barts, [1492090881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1492090881), 2022-11-18), still running in May 2026 (260528 - Barts QueryPlan failure, [2832793601](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2832793601), 2026-05-28);
  - an SLA in the style of a managed service (Platform Service Level Agreement, [1600028673](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1600028673), 2023-08-16).
- Engagements run in seven stages:
  1. contract;
  2. information governance;
  3. IT approval;
  4. installation;
  5. networking;
  6. synthetic data;
  7. live data ([2829516801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2829516801)).

  Standard pre-sales documents come first (Customer Artefacts, [2629206021](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629206021), 2026-04-29). Bespoke adapters sit outside the core product ([2080014337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2080014337)).

- Charging (qualitative):
  - invoicing counts live Nodes and their uptime, with service credits, plus active users and projects, unique patients extracted, and newly onboarded datasets (Platform Monitoring (invoicing & customer facing), [2765422594](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2765422594), 2026-05-12);
  - pages mention "monthly data pool calculations" (2026-09-08 roadmap review meeting, [3035693057](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3035693057), 2026-09-09);
  - invoices are adjusted to reflect each provider's completion (Monthly Account Meeting - August 2026, [3025633281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3025633281), 2026-09-07);
  - contracts include scale-test milestones (FFNode Stress Testing—Proposal & Business Case, [2875686914](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2875686914), 2026-06-18);
  - licensing is left to the "commercial department" ([2080014337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2080014337)).

#### 2.6 Market Context

- Sub-national SDEs exist for Eastern England, the North West, the West Midlands and the South West ([3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130)).
- HDR UK Gateway—the UK's national discovery portal:
  - FITFILE connects SDE collections to it through Relay+Bunny, and the Gateway returns counts only (National Portal Integration, [2016477190](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016477190), 2025-01-15);
  - FITFILE moved to HDR UK's new Cohort Discovery service in 2026 (HDR UK Cohort Discovery Transition meeting, [2723545089](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2723545089), 2026-03-30);
  - SDE staff find the Gateway too coarse for feasibility checks ([2804449281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2804449281)).
- Frameworks and rules:
  - Five Safes, SATRE (a standard architecture for trusted research environments) and TRE-FX (Health Innovation East Design Document, [1912242177](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1912242177), 2024-11-27);
  - the National Data Opt-Out, applied through NHS MESH;
  - restricted terms;
  - small number suppression ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
- HDRS funds the "Federated, Harmonised, and Pharma-Backed Multi-SDE Linkage" project, and that project has roadmap priority ([3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130); [3035693057](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3035693057)). Inference: HDRS is the Health Data Research Service; no page expands the acronym.
- Standards. OMOP is the chosen data model, but "the CDM from the FDP bid" is being pushed as an alternative ([2804449281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2804449281)). Inference: FDP is NHS England's Federated Data Platform.
- Europe. German hospitals are less mature and are interested in the UK model (Future4Care Conference - notes & updates, [2320990210](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2320990210), 2026-01-22).
- AI regulation. An EU AI Act assessment is still open (AI Impact on FITFILE, [2222194689](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2222194689), 2025-07-24).

#### 2.7 How the Positioning Evolved

| Period | Positioning | Evidence |
|---|---|---|
| 2020–21 | ZKP proof of concept, then "PharmaCo Service", organised around pharma "Products" | PharmaCo Service, 33010, 2024-06-05 (obsolete); Products, [114327553](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=114327553), 2021-04-09 |
| 2021–22 | Markets: study feasibility and recruitment, observational studies, payors (SimplyHealth), NHS | Five Use Case Demos, [1405026305](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1405026305), 2022-06-22; SimplyHealth Technical Onboarding, [1313341441](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1313341441), 2021-12-09 |
| 2022–23 | Single-trust projects: St George's, King's College Hospital (KCH), Barts | St.Georges TDA, [1419870209](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1419870209), 2022-07-18 |
| 2024 | Medtech-sponsored multi-site RWE feasibility study; Eastern England tender bid with Evidentli | Multi-site Project, [1729495041](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1729495041), 2024-10-06; [1912242177](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1912242177) |
| 2025 | Eastern England SDE delivery; West Midlands SDE (WMSDE) proof of concept; linkage projects with LCRCA and Mersey Care | HIE 19th Demo: Presenter Notes, [2123923457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2123923457), 2025-03-19; [2053996548](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2053996548) |
| 2026 | HDRS project with AstraZeneca (a chronic kidney disease registry); adolescent-health pitch; vaccines-prospect research | [3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130); [2918547484](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2918547484); [3034710017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034710017) |

Inference: pharma is back, but as a funder reached through SDE networks rather than a direct SaaS buyer.

#### 2.8 Partners and Alternatives

- Partners:
  - The Hyve ([2829516801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2829516801));
  - Relay+Bunny, chosen over an unnamed alternative judged "not practical to implement" (Value and Impact of Bunny Tooling in Our Organisation, [2554527745](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2554527745), 2026-01-09);
  - OHDSI's Atlas, Achilles and Athena tools;
  - CogStack and NHS PET ([2966552577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2966552577));
  - AGEM CSU ([2417065986](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2417065986));
  - Evidentli, in the 2024 bid ([1912242177](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1912242177)).
- Alternatives named:
  - an "OpenSAFELY-style model", which the adolescent-health stakeholders prefer to avoid ([2918547484](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2918547484));
  - warehouse SDEs ([2053996548](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2053996548));
  - the NHS token store ([2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497));
  - Presidio, Macie and Azure PII tools, as build-versus-buy options ([2080014337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2080014337)).
- No competitive analysis page exists.

#### 2.9 Roadmap

- January 2026. One OMOP workflow: Atlas cohort → discovery → templated privacy treatment → linkage across providers → export. The aim is "a self-service, scalable model" ([2549448706](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2549448706)).
- May 2026 priorities ([2804449281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2804449281)):
  - Achilles summary statistics inside Atlas;
  - completeness metrics;
  - querying of source values;
  - data models beyond OMOP;
  - a sandbox for validating extracts;
  - governance reporting;
  - attribution of records to sites.
- Vision. Add clinical-domain concepts to the FITFILE Data Schema, so that data-quality analytics generalise ([2966552577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2966552577)).
- September 2026.
  - HDRS work comes first; then query tagging, local opt-out, stress testing and delivery of source data ([3035693057](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3035693057)).
  - A multi-SDE blueprint and a four-SDE network are due by March 2027 (HDRS TT project, [3034906637](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034906637), 2026-09-14; personal space).
  - The formal roadmap lives in Jira Product Discovery and Miro (5. Roadmap Priotarisation, [1718943745](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1718943745), 2024-04-03).

### 3. Glossary

- FITFILE Node: one or more FITConnects plus an optional Coordinator, inside one GDPR perimeter ([1699348489](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1699348489)).
- Coordinating (Master) Node: the SDE hub that distributes queries and collates results (Use Of "Federated" Across the EoE SDE Project, [2016706564](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016706564), 2025-01-02).
- InsightFILE / HealthFILE: first the interfaces for anonymous and identifiable users; later the anonymisation and pseudonymisation paths (FITFILE Service Demo, [1320386561](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1320386561), 2023-05-31; [2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026)).
- UDE: "United Data Engine", the linkage component (UDE CLI Component, [1834582019](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1834582019); search excerpt only).
- FITanon / FITtoken: an irreversible ZKP cipher that changes on every run / a deterministic token that allows re-identification ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
- Custom Transformations: field-level treatments whose output is "not considered fully privacy-treated" (WMSDE Progress Presentation, [2243723270](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2243723270), 2025-07-13).
- Data Curator / Data-On-Demand: the two SDE models ([2053996548](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2053996548)).
- SNSDE: Sub-National SDE ([2829516801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2829516801)).
- PRE / DAR / DAC: Project Research Environment / Data Access Request / Data Access Committee ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
- SDE Concierge: prepares de-identified extracts from approved requests ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
- National Portal: the HDR UK Gateway ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
- MTDE: Minimally Transformed Data Extract ([3034906637](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034906637)).

### 4. Tensions, Contradictions, Open Questions

1. No authoritative overview. [2782756865](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2782756865) (2026-04-29) is a placeholder. The Technical Solution Overview ([2705195022](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2705195022), 2026-08-28) only points to SharePoint.
2. Uptime targets conflict: 98% ([521699377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521699377)), 95% ([1600028673](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1600028673)), 99.0% ([2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026)), and 99.9% (FITFILE Node Deployment - Technical Pack, [2352873473](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2352873473), 2025-10-18; a personal draft).
3. Compliance and privacy claims need verifying with the governance owner.
   - [2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026) appears to tick SOC 2 and HIPAA, and lists differential privacy.
   - The Technical Pack claims "Pre-certified for GDPR, HIPAA, ISO27001", but it contains template text.
   - [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497) still shows the placeholder "[AES-256 hashing, CE+, ISO27001, etc. etc. etc.]".
   - The demos show only k-anonymity and custom transformations.
4. "Federated" is qualified. There is a central Coordinator, and pseudonymised data moves to the SDE ([2016706564](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016706564)).
5. Provider engagement constrains delivery.
   - NUH will not use the platform ([2727673857](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2727673857)).
   - Several sites are blocked ([2829516801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2829516801)).
   - A workshop asks "how to energise engagement" (FITFILE/EE SDE Workshop on 7th October 2026 - Agenda, [3036774414](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3036774414), 2026-09-22).
   - Mersey Care's executive did not approve the project in May 2026, yet its page still says "Node Installation" ([2824241153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241153)).
   - Barts is missing from the live list ([3036839937](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3036839937)) but was operating in May 2026 ([2832793601](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2832793601)).
6. OMOP dependence conflicts with the aim of being model-agnostic, and vocabulary versions differ by site ([3035693057](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3035693057)).
7. The longitudinal promise outruns experience. A note behind the adolescent-health pitch admits "we have not done a lot of longitudinal studies" ([2918547484](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2918547484)).
8. Unexplained changes.
   - The partner changed from Evidentli to The Hyve.
   - A milestone is labelled AS04 in one place and AS05 in another ([3025633281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3025633281); [2875686914](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2875686914)).
   - How data partners benefit (BR-002) is unresolved.
9. Page hygiene. Issues on two pages were reported separately and are not recorded here.

### 5. Relevance to Linking Data Silos

- The pattern. Each controller runs a Node, and privacy treatment and linkage keys are created at source. The Coordinator then joins records on those keys. Only aggregates, or privacy-treated records, leave a site, and only after provider approval and under audit ([2966552577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2966552577); [2918547484](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2918547484)).
- Choice of key depends on what the silos share ([2417065986](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2417065986); [2824241153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241153)):
  - salted FITtokens: repeatable, and re-identifiable under governance;
  - FITanons: irreversible;
  - existing keys, such as NHS PET or NWSDE pseudonymous IDs;
  - probabilistic matching where there is no common ID—for example, DWP data linked to integrated care board (ICB) data for LCRCA, and HR data linked to ICB data for Mersey Care.
- Shared meaning matters as much as keys: OMOP harmonisation, a union of vocabularies, data-quality gates, and attribution of records to providers ([2804449281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2804449281)).
- The critical path is organisational ([3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130); [2727673857](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2727673857)):
  - a contract with each SDE;
  - data sharing agreements between SDEs;
  - data protection impact assessments (DPIAs) and data access committee (DAC) notifications;
  - clear ownership of opt-outs;
  - network approvals.
- The design must fit the SDE's model. Federating on demand (Eastern England) differs from salted hashing in a warehouse (West Midlands) ([2080014337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2080014337)).
- The frontier is federation across four regional SDEs. Linking across countries cannot assume a shared identifier ([3034906637](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034906637); [3034710017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034710017)).

### 6. Pages Read, and Relevant Pages not Read

Pages cited in §1–5 are given their full title at first use, so here they are listed by ID and last-modified date only. Pages not cited carry a short title.

FITFILE space, cited:

- [1696727046](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1696727046) (2024-09-04)
- [2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026) (2025-04-25)
- [1699348489](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1699348489) (2025-05-27)
- [2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881) (2025-02-14)
- [2918547484](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2918547484) (2026-07-13)
- [2930802691](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2930802691) (2026-07-16)
- [2368897027](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2368897027) (2025-10-28; title paraphrased)
- [2156429316](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2156429316) (2025-04-17)
- [2804449281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2804449281) (2026-05-14)
- [2053996548](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2053996548) (2025-02-06)
- [2080014337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2080014337) (2025-08-28)
- [3036839937](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3036839937) (2026-09-09)
- [2966552577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2966552577) (2026-08-05)
- [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497) (2026-02-04)
- [2170519555](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2170519555) (2025-05-01)
- [2832793601](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2832793601) (2026-05-28)
- [2629206021](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629206021) (2026-04-29)
- [2765422594](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2765422594) (2026-05-12)
- [2875686914](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2875686914) (2026-06-18)
- [2016477190](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016477190) (2025-01-15)
- [1912242177](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1912242177) (2024-11-27)
- [2320990210](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2320990210) (2026-01-22)
- [2222194689](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2222194689) (2025-07-24)
- [1729495041](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1729495041) (2024-10-06)
- [2123923457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2123923457) (2025-03-19)
- [1718943745](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1718943745) (2024-04-03)
- [2016706564](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016706564) (2025-01-02)
- [2243723270](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2243723270) (2025-07-13)
- [2782756865](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2782756865) (2026-04-29)
- [2705195022](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2705195022) (2026-08-28)

FITFILE space, read but not cited:

- Home, [1696366661](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1696366661) (2026-09-01)
- Where to start, [2784067595](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2784067595) (2026-09-01)
- AHS query example, [2945744897](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2945744897) (2026-07-24)
- Presentation Plan, [2113765377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2113765377) (2025-03-14)
- Researcher journey, [2173140993](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2173140993) (2025-05-04)
- Exploratory Roadmap, [2227437570](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2227437570) (2025-06-26)
- Solution Strategy, [1702658075](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1702658075) (2024-10-05)
- Invoicing investigation, [2779152386](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2779152386) (2026-05-21)
- UCL walkthrough, [2186182662](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2186182662) (2025-05-21)
- Partner deployment docs, [2163834884](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2163834884) (2025-04-29)
- Kickoff prep, [2347925506](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2347925506) (2025-10-16)
- What needs to be covered, [2390556675](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2390556675) (2026-01-13)
- Product Planning, [1761640449](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1761640449) (2024-05-16)
- User Journey Map, [1718779932](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1718779932) (2024-04-04)
- Empty or stub pages: [1926234113](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1926234113), [2793996290](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2793996290), [2902163457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2902163457)
- Unused AI-style draft: [2600173569](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2600173569) (2026-01-30)

PS space, cited:

- [521699377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521699377) (2023-01-13)
- [521896132](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521896132) (2021-04-01)
- [1572864001](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1572864001) (2024-04-04)
- [771620870](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=771620870) (2021-03-30)
- 33010 (2024-06-05)
- [114327553](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=114327553) (2021-04-09)
- [1405026305](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1405026305) (2022-06-22)
- [1313341441](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1313341441) (2021-12-09)
- [1419870209](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1419870209) (2022-07-18)
- [1492090881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1492090881) (2022-11-18)
- [1600028673](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1600028673) (2023-08-16)
- [1320386561](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1320386561) (2023-05-31)

PS space, read but not cited:

- Product Documentation, [522027263](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=522027263) (2021-03-03)
- Product Strategy, [521437213](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521437213) (2021-01-25)
- Definition Hierarchy, [563904513](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=563904513) (2021-02-03)
- Business Milestones, [543195210](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=543195210) (2021-03-09)
- User Roles, [330825729](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=330825729) (2021-04-14)
- Customers, [1340047361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1340047361) (2022-02-16)
- St Georges, [1459159041](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1459159041) (2022-09-29)
- STG Data Processing, [1474985985](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1474985985) (2023-01-28)
- Pharmaceutical Flow, [327221266](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=327221266) (2021-12-13)
- Intro to Anonymisation, [755040265](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=755040265) (2021-03-22)
- Client Deployment Requirements, [1302495233](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1302495233) (2021-11-10)
- High Level Overview, [1252524037](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1252524037) (2021-09-10)
- ABPI checklist, 360456 (2020-08-14)
- Empty pages: [117047304](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=117047304), [1478787073](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1478787073)

Other spaces, cited:

- CDH: [2549448706](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2549448706) (2026-01-16), [2554527745](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2554527745) (2026-01-09)
- EOE: [2829516801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2829516801) (2026-09-27), [2727673857](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2727673857) (2026-09-27), [3035693057](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3035693057) (2026-09-09), [3036774414](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3036774414) (2026-09-22), [2723545089](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2723545089) (2026-03-30), [3025633281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3025633281) (2026-09-07)
- NP: [2824241153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241153) (2026-09-27), [2417065986](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2417065986) (2026-04-08)
- HDRSTT: [3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130) (2026-09-25)
- PRODDOCS: [2201288746](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2201288746) (2025-06-10)
- Personal spaces:
  - [2352873473](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2352873473), an engineer's (2025-10-18)
  - [3034710017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034710017), the Head of Data's (2026-09-08)
  - [3034906637](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034906637), the Head of Data's (2026-09-14)

Other spaces, read but not cited:

- CDH hub, [2391278122](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2391278122) (2025-12-03)
- CDH catalogue, [2399928323](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2399928323) (2025-11-11)
- HDRSTT summary, [3073245215](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3073245215) (2026-09-25; template only)
- PRODDOCS index, [2199060952](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2199060952) (2025-07-11)
- AHS Architecture, [2951675906](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2951675906) (Head of Engineering, 2026-09-18)

Relevant but not read:

- [2067267585](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2067267585) and [2285764609](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2285764609) (WMSDE)
- [2519433236](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2519433236), [2603417659](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2603417659), [2788950017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2788950017), [2575368202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2575368202) and [2568847361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2568847361) (Configured Solution Designs)
- [2778365953](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2778365953) and [2471034898](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2471034898) (NWSDE)
- [2588180481](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2588180481), [2233270273](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2233270273), [2944303107](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2944303107)
- The UDE and ZKP pages

Attachments, not downloaded:

- "Pharma Opportunity 21 Nov 25 (2).pptx" (att2529099812, 2025-12-19). A search excerpt mentions an "SDE Network" "Concierge Service".
- A FARAPULSE feasibility statement of work (on [1729495041](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1729495041)).
- A WMSDE proof-of-concept report on privacy-enhancing technology (on [2053996548](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2053996548)).
- "[20210302](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=20210302)_Anonymisation.pptx" (on [755040265](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=755040265)).
- An EE-SDE workshop transcript (on [2804449281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2804449281)).

Held only in SharePoint:

- The Technical Solution Overview.
- The pre-sales Technical Overview.
- Technical Solution Detail.
- The discovery questionnaire.
- The Eastern England tender documents.
- Per-project "Pricing" documents.
