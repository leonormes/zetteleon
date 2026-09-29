---
title: FITFILE Research Brief E — Programmes and Data Silos in the Field
type: source
status: draft
created: '2026-09-28T21:21:00+01:00'
modified: '2026-09-29T08:34:03+01:00'
tags:
- source/llm
- fitfile
- topic/secure-data-environments
- topic/programmes
project_name: FITFILE
conformant: false
non_conformance_reason: Raw agent research brief kept as source material for the FITFILE
  context brief; awaiting review, not a canonical source note.
source: FITFILE Confluence, read-only sweep on 2026-09-28 by a Claude Code research
  agent
source_url: null
permalink: llmeon/00-inbox/fitfile-research-briefs/fitfile-research-brief-e-programmes-and-data-silos-in-the-field
---

%% Raw agent research brief (Claude Code, 2026-09-28), kept as source material for the FITFILE context brief. Not your own writing, so no own_words property. Page IDs link to Confluence. Redacted for the vault where needed: personal names, a prospect's name, page-hygiene and security-debt specifics. %%

Part of: [[FITFILE Context Brief — What We Do and How We Link Data Silos]]

# Brief E: Programmes, customers and data silos in the field

*Prepared 2026-09-28 from FITFILE Confluence (read-only). People are named by role only. The first citation of a page gives its short title, page ID and last-modified date; later citations use the short title alone. §6 lists every page. "Inference:" marks my own reasoning.*

## 1. Summary

- **Where the business is.** FITFILE's live portfolio centres on secure data environments (SDEs). There are three live programmes: the Eastern England SDE (CUH, MKUH, NNUH, NUH), the North West SDE (LCRCA, Mersey Care) and the new multi-SDE HDRS programme (Project Names, [3036839937](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3036839937), 2026-09-09).
- **One deployment pattern recurs.** Each data controller hosts a FITFILE Node inside its own perimeter, usually its own Azure or AWS tenancy. At the SDE, a co-ordinating Node issues queries and collates results. FITFILE runs the central services (EE Summary, [2829516801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2829516801), 2026-09-27; CSD NUH, [2788950017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2788950017), 2026-08-27).
- **Eastern England is the reference programme.** It combines OMOP harmonisation (delivered by The Hyve), HDR UK cohort discovery, OHDSI Atlas/Achilles and opt-out handling. As of 2026-09-25, CUH and MKUH are live, NNUH is at go-live and NUH is stuck at contract. A pipeline of six further trusts is mostly blocked by site engagement (EE Summary; NNUH Summary, [2716499969](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2716499969), 2026-09-25; NUH Summary, [2727673857](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2727673857), 2026-09-27).
- **The North West SDE is the cross-sector case.** It links combined-authority DWP data and trust staff HR data to ICB health data, without NHS numbers. Both projects stalled on partner governance, not technology (LCRCA Summary, [2816245762](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2816245762), 2026-09-25; Mersey Care Summary, [2824241153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241153), 2026-09-27).
- **HDRS TT extends the model to four SDEs.** It kicked off on 2026-09-25. AstraZeneca is building a CKD registry on synthetic data, and Eastern England co-ordinates. Contracts, DAC and DPIA must clear before a mid-December gate (HDRS Kick-Off, [3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130), 2026-09-25).
- **Most blockers are organisational.** They include trust IT and IG processes, staff turnover, missing project managers, DPIAs, in-year funding, CSU decommissioning and EPR or cloud migrations (Lessons Learnt, [2999484417](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2999484417), 2026-08-20; NWSDE Update, [2798223361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2798223361), 2026-08-21).
- **Technical silos are tractable but site-specific.** Egress, certificates, DNS, authentication and hosting differ at every site, and OMOP vocabulary versions drift between them (CUH Deployment Status, [2261712911](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2261712911), 2025-09-11; Roadmap Review, [3035693057](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3035693057), 2026-09-09).

## 2. Programmes

### 2.1 Eastern England SDE (EE SDE; formerly "East of England")

**Parties**

| Party | Role |
|---|---|
| Sub-National SDE for R&D | Contracted FITFILE for federated harmonisation, cohort discovery, de-identification and linkage (EE Summary) |
| Health Innovation East (HIE) | Its teams run onboarding, data management and IG, and meet FITFILE monthly (Monthly Jan 2026, [2585034753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2585034753), 2026-01-26) |
| CUH ("lead organisation") | Its legal team issues provider contracts; it curates the local opt-out list (NDOO & LDOO, [2786525192](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2786525192), 2026-05-05; NUH Summary) |
| The Hyve | OMOP subcontractor (EE Summary) |
| HDR UK | Moved to a new Cohort Discovery service in 2026 (Cohort Discovery Transition, [2723545089](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2723545089), 2026-03-30) |
| Telefonica Tech | CUH's infrastructure partner (Fabric Update Sep, [3029631125](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3029631125), 2026-09-08) |

The East Midlands SDE was being absorbed into the CUH-led SDE in October 2025, which explains why NUH is in scope (NNUH Kick-off, [2362966017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2362966017), 2025-10-27). FITFILE's 2024 bid assumed Evidentli would provide the OMOP layer (HIE Design Document, [1912242177](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1912242177), 2024-11-27); the pages I read do not explain why The Hyve replaced it. The co-ordinating Node went into the SDE's AWS account in early 2025 after landing-zone friction (Timeline of Events, [2072543234](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2072543234), 2025-02-11; Master Node Acceptance, [2098692097](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2098692097), 2026-01-22).

**Data sources**

Trust EPR data are mapped to OMOP and provisioned to researchers' Project Research Environments (EE Summary).

- **CUH** harmonises its own data on an on-prem SQL Server that it calls not fit for purpose, and plans to move to MS Fabric (Fabric Mar, [2705948675](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2705948675), 2026-03-24).
- **MKUH** shares tables directly each month; it refuses Java, so White Rabbit was not used (MKUH Summary, [2696708097](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2696708097), 2026-09-27). Its first extract was about half complete (MKUH Handover, [2926837809](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2926837809), 2026-07-14).
- **NNUH's** new EPR database slipped to September 2026 (NNUH Kick-off).
- **NUH** supplies demographics, diagnoses, admissions and outpatient data, already privacy-treated and without NHS numbers (CSD NUH; Monthly Aug 2026, [3025633281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3025633281), 2026-09-07).

National inputs are the NDOO (via NHS MESH), the SDE's restricted-code list and HDR UK collections (SDE Nodes Configuration, [2698412033](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2698412033), 2026-03-24). HIE's "deep data" plans (genomics, imaging, free text) need CAG/REC amendments. Primary care was judged high-risk, and EMIS/TPP market shares differ by region (Monthly Jan 2026).

**Deployment**

- **MKUH:** Node in its own Azure subscription; MKUH manages DNS and certificates (CSD MKUH, [2603417659](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2603417659), 2026-02-03).
- **NNUH:** Node in its own Azure subscription, via its change board (NNUH Kick-off).
- **CUH:** Node in an Azure subscription provisioned by Telefonica Tech. Egress goes through CUH's on-prem firewall and a non-transparent proxy, and the Node reads an on-prem SQL Server (CUH Deployment Status).
- **NUH:** Node in an SDE-provided AWS account, peered to the SDE, with a VPN to NUH's on-prem database. NUH moved from on-prem to hybrid to managed-cloud options before this settled (CSD NUH; NUH On-prem Discussion, [2669707265](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2669707265), 2026-04-07; Cloud Architecture, [2753789953](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2753789953), 2026-05-07).
- **Co-ordinating Node:** has a TEST environment (synthetic data, HDR UK pre-production) and a PROD environment (remote provider Nodes, HDR UK production). FITFILE runs the Nodes; the SDE team runs projects, users, exports, disclosure and small-number suppression (SDE Nodes Configuration).

**Federation and linkage**

- Queries fan out from the co-ordinating Node. Cohort discovery uses Bunny in each provider Node and a Hutch relay at the SDE (CSD MKUH).
- NHS numbers never reach the SDE's PROD Node; they are pseudonymised for linkage and de-duplication (NDOO & LDOO).
- NUH's initial data cannot yet be linked across providers because it has no NHS number (CSD NUH).
- Small-number suppression is applied centrally to cohort discovery, not to extracts (HIE Explanation Draft, [2170552391](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2170552391), 2025-05-06).

**Status as of 2026-09-25**

| Provider | Stage | Notes |
|---|---|---|
| CUH | Live | Fabric move paused by a CUH financing issue; Achilles re-run awaited (CUH Summary, [2824241202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241202), 2026-09-25) |
| MKUH | Live, signed off | HDR UK Gateway connection planned for 14/09 (MKUH Summary; Data Managers Sep, [3040968705](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3040968705), 2026-09-11) |
| NNUH | Stage 7 | Data quality signed off; HDR UK connection planned for 28/09 (NNUH Summary) |
| NUH | Stage 1 | Waiting on contract and internal study set-up; now expected mid-November; NUH will not use the platform itself (NUH Summary; NUH Update, [3062071379](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3062071379), 2026-09-22) |

The pipeline covers CPFT, Leicester, Derby & Burton (waiting for a new EPR), Sherwood Forest, East Midlands Ambulance Service and Royal Papworth (EE Summary). Two studies are nearing DAC: renal/CKD (~60k patients) and surgical procedures (~170k cases, ~500k controls). The HDR UK collection is being updated to about 1.5M patients (Data Managers Sep). HDRS now takes priority over the EE roadmap (Roadmap Review).

**Pain points and lessons**

- **Onboarding lessons.** The MKUH/NNUH lessons-learnt workshop asked for (Lessons Learnt):
  - a contractual minimum dataset (outpatient data had been missed);
  - a combined DCA/DSA;
  - the DPIA as a contractual deliverable (MKUH's took three months);
  - stage-gated data quality;
  - an empowered project manager at each trust;
  - synthetic data made by the trust itself;
  - live mapping workshops;
  - researcher utility over strict OMOP compliance;
  - no onboarding during EPR migrations.
- **Opt-outs vary by site** (NDOO & LDOO; Data Managers Sep):
  - FITFILE applies the NDOO at MKUH and NNUH.
  - CUH filters its own data from a list.
  - NUH applies its own opt-outs.
  - The local list cannot be applied to NUH's pseudonymised data.
  - CUH's ad hoc refresh was judged unacceptable for opt-out compliance.
- **Vocabulary versions differ.** CUH uses the August 2025 release and NNUH/MKUH the February 2026 release, so FITFILE is building a vocabulary union (Roadmap Review).
- **Usability and performance.**
  - Users want source-value search, joins and faster runs (Platform Feedback, [2760376324](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2760376324), 2026-04-29).
  - CUH cohort queries exceeded HDR UK's five-minute limit in April 2026 (Stress Testing v3, [2839871490](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2839871490), 2026-06-02; search excerpt only).
  - The July incidents included CUH network instability (Incident Summary, [2977038337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2977038337), 2026-08-11).
- **Operational constraints.** MKUH allows extracts only between 2pm and 10pm, and it also supplies the Thames Valley SDE (MKUH Handover). Invoicing follows provider milestones, and funding is in-year (Monthly Aug 2026; Monthly Jan 2026).

### 2.2 North West SDE: LCRCA and Mersey Care

**Parties and data.** NHS Arden & Greater East Midlands CSU (AGEM) operates the SDE. Its DSCRO holds Personal Demographics Service (PDS) data for Cheshire & Merseyside, and the health data come from the Cheshire & Merseyside ICB (CSD NWSDE, [2575368202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2575368202), 2026-03-03; UR LCRCA, [2605842433](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2605842433), 2026-02-04).

- **LCRCA project.** Liverpool City Region Combined Authority DWP/worklessness data (~40k records, 4–5 years old, Excel/CSV, no NHS number) are linked to ICB mental-health data for a population of about 600k. The aim is to inform economic and mental-health support. The University of Liverpool is a research partner (Technical Overview, [2450259975](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2450259975), 2026-04-27; LCA Kick-off, [2360180760](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2360180760), 2025-11-12; LCRCA Update, [2774532097](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2774532097), 2026-04-24).
- **Mersey Care project.** About 11k staff HR records (name, date of birth, postcode) are linked to the ICB long-term-conditions register, to inform workforce wellbeing (CSD Mersey Care, [2568847361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2568847361), 2026-02-16).

**Deployment and linkage**

- A DSCRO Azure Node co-ordinates the LCRCA project and supplies data to Mersey Care. LCRCA and Mersey Care host their own Azure Nodes. Data arrive by file upload, and outputs go to AGEM blob storage (CSD NWSDE; Mersey Care Kick-off, [2531098663](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2531098663), 2026-01-19).
- Because the Node can reach identifiable DSCRO data, FITFILE had temporary access only and runs matching as a managed service (UR LCRCA; CSD NWSDE).
- **LCRCA:** probabilistic matching on hashed name, date of birth, postcode and gender, mapped to existing PseudoIDs. Only PseudoIDs and aggregates leave the Node (Tech Kick-off, [2472607753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2472607753), 2026-02-04).
- **Mersey Care:** deterministic matching of irreversible FITanon ciphers, returning aggregates only (Mersey Care Summary).

**Status**

- **NWSDE (Stage 7).** Synthetic end-to-end testing succeeded in May 2026. The combined authority's governance team then excluded postcodes, and synthetic data was proposed instead (NWSDE Update).
- **LCRCA.** File-sharing approval has not been given; the next step waits on FITFILE leadership (LCRCA Summary).
- **Mersey Care (Stage 4).** The executive rejected the March submission over "nervousness" about staff data, not security, and did not approve the project in May 2026 (Mersey Care Update, [2693922817](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2693922817), 2026-03-15; Mersey Care Summary).
- **HDRS link.** The NWSDE team has joined HDRS TT, and the DSCRO Node stays in place (NWSDE Summary, [2778365953](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2778365953), 2026-09-28).

**Pain points**

- The local-authority lead called public-sector bureaucracy the biggest barrier. Governance staff changes blocked adding names to the DSA (LCRCA Update).
- Without names and postcodes, the POC became a technical validation only (NWSDE Update).
- The host CSU is being decommissioned; a new host would need new DSAs (NWSDE Update).

### 2.3 HDRS TT Federated Linkage

**What it is.** A "Federated, Harmonised, and Pharma-Backed Multi-SDE Linkage project" connecting the Eastern England, North West, West Midlands and South West SDEs. AstraZeneca is building a CKD registry, and OMOP is the primary data standard (HDRS Kick-Off).

**Funding and roles** (HDRS Kick-Off; HDRS TT Plan, [3034906637](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034906637), 2026-09-14):
- HDRS funds EESDE through an MOU.
- EESDE funds the other SDEs and FITFILE.
- AstraZeneca contracts FITFILE directly.
- The Hyve writes a shared OMOP mapping specification and independently checks data quality.

**Data and deployment.** Each SDE generates synthetic CKD data from a "Minimally Transformed Data Extract" (MTDE), and the EE Node queries those data remotely (HDRS TT Plan). FITFILE deploys by script. SDEs create restricted service principals and cannot see each other's environments. SWSDE's supplier must review the architecture (HDRS Kick-Off).

**Status as of 2026-09-25: Stage 1.**
- Contract variations are needed for EE, NW and WM, and a new contract for SW.
- DAC notifications are due in October.
- DPIAs for synthetic data, DSAs and PPIE are still open questions.
- Technical discovery starts on 28/09 (HDRS Summary, [3073245215](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3073245215), 2026-09-25; HDRS ST Notes, [3071967233](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3071967233), 2026-09-25).

**Timeline.** Phase 1 is due by mid-December and releases Phase 2 funding. It requires at least two SDEs connected and queried, an OMOP reference implementation, a DQ dashboard and a deployment pattern. Phase 2 ends in March 2027 (HDRS Kick-Off).

Inference: HDRS is the Health Data Research Service recommended by the Sudlow Review, which a FITFILE demo page summarises (Sudlow Demo, [2368897027](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2368897027), 2025-10-28). No page I read expands "TT".

### 2.4 Earlier and smaller engagements

- **WMSDE/UHB (2024–25).** A 2025 privacy-enhancing technology (PET) PoC at UHB exposed product gaps. WMSDE is a "Data Curator": it runs a lightly pseudonymised warehouse with project keys, whereas EE is "Data-On-Demand". FITFILE responded with custom transformations, token-based multi-modal linkage, SQL adapters and PII detection (UHB Product Gap, [2053996548](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2053996548), 2025-02-06; WMSDE Plan, [2080014337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2080014337), 2025-08-28; WMSDE Presentation, [2243723270](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2243723270), 2025-07-13). WMSDE is returning through HDRS TT (HDRS Kick-Off).
- **Barts.** A Barts Node runs on FITFILE's production cluster (Barts, [1492090881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1492090881), 2022-11-18). It feeds a PowerBI dashboard that includes stem-cell data (Barts Postmortem, [1715634177](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1715634177), 2024-03-28), and the dashboard was still refreshing in May 2026 (Barts QueryPlan Failure, [2832793601](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2832793601), 2026-05-28). The "Barts & PowerBI" page holds only account references ([1851260929](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1851260929), 2024-08-05).
- **UCL POC (2025).** The POC tested de-identification of EHR and omics (VCF) data, plus EHR linkage. UCL preferred on-prem hosting, a UCLH Node met governance hurdles, and AWS guardrails constrained deployment (UCL POC Feb, [2069200899](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2069200899), 2025-02-07; UCL POC May, [2181103618](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2181103618), 2025-05-13). Users wanted a self-service UI and plain-language privacy settings (UCL Workshop, [2199289870](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2199289870), 2025-05-29). The outcome is not documented, and the POC plan page is empty ([2189459457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2189459457), 2025-05-20).
- **2021–23 deployments.**
  - KCH: on-prem VM, with FITConnect connectors feeding InsightFILE (anonymised) or HealthFILE (identifiable) (KCH Deployment, [1347190785](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1347190785), 2022-05-05).
  - St George's: TDA approval and an IBD dataset (STG TDA, [1419870209](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1419870209), 2022-07-18; STG Data Processing, [1474985985](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1474985985), 2023-01-28).
  - SimplyHealth: Azure deployment with CSV import (SimplyHealth Onboarding, [1313341441](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1313341441), 2021-12-09).
  - PRUH: an anonymised maternity-inequalities study (attachment, seen only as a search excerpt).
- **GP data.** Each EMIS extract needs a DSA for every GP organisation, activated by its Caldicott Guardian (IM1 EMIS, [1548255233](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1548255233), 2023-03-21). TPP SystmOne needs consent from each practice, a gateway PC per practice and HSCN connectivity (TPP SystmOne, [1986166786](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1986166786), 2025-05-16).
- **2026 prospects.**
  - AHS, an adolescent health study across 4–7 UK sites, wants data kept at the sites rather than an OpenSAFELY-style model (AHS Demo, [2918547484](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2918547484), 2026-07-13; AHS Demo Data, [2945744897](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2945744897), 2026-07-24).
  - FITFILE's vaccines-prospect research notes two gaps: no longitudinal patient record, and untested VCF querying (vaccines-prospect research, [3034710017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034710017), 2026-09-08).

## 3. Key terms

- **Co-ordinating (Master) Node / Data Provider Node:** the SDE's query distributor and aggregator / the Node inside each provider (EE Summary; Use of "Federated", [2016706564](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016706564), 2025-01-02).
- **DCA/DSA:** "Data Centre Agreement" (as expanded on that page) / Data Sharing Agreement (Lessons Learnt).
- **NDOO/LDOO:** national / local data opt-out; the NDOO check uses the NHS MESH API (CSD MKUH; NDOO & LDOO).
- **Restricted Codes:** the SDE's list of sensitive codes, filtered out in provider ETL (CSD NUH).
- **SNS:** small-number suppression, distinct from k-anonymity (HIE Explanation Draft).
- **Custom transformations:** per-field treatments; their outputs remain classed as identifiable (WMSDE Presentation).
- **FITtoken / FITanon:** deterministic pseudonymised token / non-deterministic anonymised cipher built on a zero-knowledge proof (ZKP) (Linkage Comparison, [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497), 2026-02-04).
- **PseudoID / DSCRO:** the NWSDE's existing pseudonyms / the CSU office holding PDS data; no page expands "DSCRO" (UR LCRCA).
- **NHS-PET:** external NHS pseudonyms, used for linkage where FITFILE is absent (NHS-PET Integration, [2318106625](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2318106625), 2025-09-30).
- **MTDE:** Minimally Transformed Data Extract (HDRS TT Plan).
- **Data Curator / Data-On-Demand:** warehouse-first / query-at-source SDE models (UHB Product Gap).

## 4. Cross-programme patterns, tensions, open questions

**Patterns**

1. **Governance sets the pace more than software.** This holds for the EE lessons, the NUH contract, LCRCA governance, the Mersey Care executive and the HDRS DAC/DPIA path (§2).
2. **"Blueprint" in theory, bespoke in practice.** The Node is pitched as "a blueprint, not a bespoke build" (HDRS Tech Demo, [2966552577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2966552577), 2026-08-05). Yet every site needed its own networking, certificate, identity and hosting work (CUH Deployment Status; CSD MKUH; CSD NUH).
3. **Institutions keep shifting.** Examples: CSU decommissioning, EPR go-lives, CUH's cloud move, and departures of sponsors and governance leads (NWSDE Update; EE Summary; HDRS ST Notes).
4. **Source-data problems surface late.** Examples: MKUH's partial extract, NNUH's implausible dates and CUH's ad hoc refresh (MKUH Handover; Monthly Aug 2026; NDOO & LDOO).

**Tensions**

- **"Data stays where it is" versus the architecture.** That message (AHS Demo) sits awkwardly with a co-ordinating Node and with pseudonymised extracts reaching the SDE. FITFILE's own note concedes this (Use of "Federated").
- **OMOP conformance versus researcher utility** (Lessons Learnt; Platform Feedback).
- **Provider value versus SDE value.** NUH joins only for the SDE's benefit (NUH Update).
- **EE roadmap versus HDRS priority** (Roadmap Review).

**Contradictions and stale content**

- **CUH Fabric date.** It moved from "April" (Monthly Jan 2026) to "6+ months" (Fabric Mar), and the move is now paused (Fabric Update Sep).
- **Mersey Care tokens.** The kick-off describes pseudonymised "fit tokens", but the summary describes irreversible FITanons (Mersey Care Kick-off; Mersey Care Summary).
- **Royal Papworth.** It went from "close to signing" to "blocked" (Monthly Jan 2026; EE Summary).
- **MKUH NDOO cadence.** Different pages give 7 days and 14 days (MKUH Handover; NDOO & LDOO).
- **LCRCA staging.** Its summary lists five stages but reports "Stage 7" (LCRCA Summary).
- **SDE Nodes Configuration.** Its connected-source list is out of date.

**Open questions**

- What does "TT" stand for?
- Who will host the NWSDE after the CSU?
- Will the CUH, LCRCA and Mersey Care work resume?
- What is Barts' current contractual status?
- What did WMSDE do between August 2025 and September 2026?
- What was the outcome of the UCL POC?

## 5. Relevance to linking data silos: silo map

FITFILE's founding requirement described health and activity data held "in unconnected silos" that could not be united lawfully without consent, and consent is costly to obtain at scale (Tier 1 Business Requirements, [521699377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521699377), 2023-01-13).

| Silo type | Field examples | Response seen |
|---|---|---|
| Organisational | Each trust has its own change board, IG team and gaps in project management (Lessons Learnt). MKUH sits in two SDEs (MKUH Handover). A CSU, ICB, combined authority and trust HR team share one flow (UR LCRCA; CSD Mersey Care). GP practices consent one by one (IM1 EMIS; TPP SystmOne). Four SDEs work with a pharma sponsor (HDRS Kick-Off). | A Node per controller; a co-ordinating Node per SDE; SDE-to-SDE federation |
| Technical/schema | CUH's proxied on-prem SQL moving to Fabric; Azure vs AWS; NUH's Postgres over VPN; LCRCA's Excel/CSV; PDS extracts in blob storage (Blob Storage, [2591522817](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2591522817), 2026-01-27); EPR changes; vocabulary drift; EMIS vs TPP; VCF omics | OMOP via The Hyve; a vocabulary union; Achilles/DQ checks; per-site network designs |
| Legal/IG | A DCA/DSA/DPIA per provider and a DAC per SDE; CAG/REC limits (Monthly Jan 2026); opt-outs applied at different points; refusal of names and postcodes; the Mersey Care executive's refusal; consented cohorts vs NDOO (NDOO & LDOO) | Opt-out at source; SNS and disclosure controls; aggregate-only outputs; synthetic data first |
| Identity | No NHS number in DWP or HR data (NWSDE Two Projects, [2611576835](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2611576835), 2026-02-04); NUH pre-pseudonymised (CSD NUH); DSCRO PseudoIDs; NHS tokens that differ by sharing domain (Linkage Comparison); WMSDE project keys (UHB Product Gap); SDEs without FITFILE (NHS-PET Integration) | Non-UID probabilistic and deterministic matching; FITtoken/FITanon; project salts; NHS-PET pseudonyms |

Inference: the IG and identity silos decide whether linkage happens at all. Both NWSDE projects passed their technical tests and then stopped at governance.

## 6. Pages read and pages found

Last-modified dates for cited pages appear at first citation above.

**EOE**
- Summaries: EE [2829516801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2829516801), CUH [2824241202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241202), MKUH [2696708097](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2696708097), NNUH [2716499969](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2716499969), NUH [2727673857](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2727673857)
- Configuration and designs: SDE Nodes Configuration [2698412033](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2698412033); CSD NUH [2788950017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2788950017); CSD MKUH [2603417659](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2603417659); CUH synthetic-to-live [2363785218](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2363785218)
- Fabric meetings: [2705948675](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2705948675), [2887909377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2887909377), [3029631125](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3029631125)
- Programme meetings: Cohort Discovery Transition [2723545089](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2723545089); Platform Feedback [2760376324](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2760376324); Lessons Learnt [2999484417](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2999484417); Monthly Aug [3025633281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3025633281) and Jan [2585034753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2585034753); 7 October agenda [3036774414](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3036774414); Roadmap Review [3035693057](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3035693057)
- Operations and providers: Incident Summary [2977038337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2977038337); MKUH Handover [2926837809](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2926837809); Cloud Architecture [2753789953](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2753789953) and [2796552193](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2796552193); NUH On-prem [2669707265](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2669707265); Feedback Questionnaire [2517499905](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2517499905); MKUH Kick-off [2348384261](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2348384261); NNUH Kick-off [2362966017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2362966017); NDOO & LDOO [2786525192](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2786525192); NUH Update [3062071379](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3062071379); Data Managers Sep [3040968705](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3040968705)
- Indexes and home: [2916876289](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2916876289), [2915598337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2915598337), [2340553253](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2340553253)

**NP**
- NWSDE: Summary [2778365953](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2778365953); Technical Overview [2450259975](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2450259975); CSD [2575368202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2575368202); Additional Tech Requirements [2450423809](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2450423809); UR LCRCA [2605842433](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2605842433)
- LCRCA: Summary [2816245762](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2816245762); Updates [2774532097](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2774532097) and [2634809345](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2634809345); LCA Kick-off [2360180760](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2360180760)
- Mersey Care: Summary [2824241153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241153); CSD [2568847361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2568847361); UR [2632712194](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2632712194); Update [2693922817](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2693922817); Kick-off [2531098663](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2531098663)
- Other: Key Usability Decisions [2631827457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2631827457); Blob Storage [2591522817](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2591522817); Two Projects [2611576835](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2611576835); NWSDE Update [2798223361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2798223361); Tech Kick-off [2472607753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2472607753); home [2358379050](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2358379050)

**HDRSTT**
- Summary [3073245215](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3073245215); Kick-Off [3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130); ST Notes [3071967233](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3071967233); home [3071738149](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3071738149)

**FITFILE**
- EE history: HIE Design Document [1912242177](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1912242177); Timeline of Events [2072543234](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2072543234); Master Node Acceptance [2098692097](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2098692097); HIE Explanation Draft [2170552391](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2170552391); Sprint Summary [1875378177](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1875378177); Use of "Federated" [2016706564](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016706564); CUH Deployment Status [2261712911](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2261712911)
- WMSDE/UHB: WMSDE Plans [2080014337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2080014337) and [2067267585](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2067267585); UHB Product Gap [2053996548](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2053996548); WMSDE Presentation [2243723270](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2243723270); WMSDE UHB [1925480451](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1925480451)
- Barts: Barts & PowerBI [1851260929](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1851260929); postmortems [1715634177](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1715634177) and [2832793601](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2832793601)
- UCL: POC notes [2069200899](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2069200899) and [2181103618](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2181103618); UCL Workshop [2199289870](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2199289870); UCL Deployment Status [2268758017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2268758017); POC Plan [2189459457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2189459457)
- HDRS: HDRS Demo Script [2930802691](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2930802691); HDRS Tech Demo [2966552577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2966552577); Sudlow Demo [2368897027](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2368897027)
- Linkage and GP data: NHS-PET Integration [2318106625](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2318106625); Linkage Comparison [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497); TPP SystmOne [1986166786](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1986166786); EMIS Transfer [1659305985](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1659305985)
- Prospects and portfolio: AHS Demo [2918547484](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2918547484); AHS Demo Data [2945744897](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2945744897); Project Names [3036839937](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3036839937)
- Near-empty pages: [2697887745](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2697887745), [2629763084](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629763084), [2902163457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2902163457), [2720792584](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2720792584), [1926234113](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1926234113), [2151219202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2151219202) and children

**PS**
- Customer pages: SimplyHealth [1313341441](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1313341441); STG TDA [1419870209](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1419870209); STG Data Processing [1474985985](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1474985985); KCH Deployment [1347190785](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1347190785); Barts [1492090881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1492090881)
- Other: IM1 EMIS [1548255233](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1548255233); Five Use Case Demos [1405026305](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1405026305); Tier 1 Business Requirements [521699377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521699377)
- Containers: [1340047361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1340047361), [1459159041](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1459159041), [1478787073](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1478787073), 33010

**Personal spaces**
- AHS Architecture [2951675906](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2951675906); HDRS TT Plan [3034906637](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034906637); vaccines-prospect research [3034710017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034710017)

**Found but not read, or seen only in search excerpts**
- Stress-testing pages: [2839871490](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2839871490) (excerpt only), [2861498370](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2861498370), [2876309505](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2876309505)
- St George's SLA: [1600028673](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1600028673) (excerpt only)
- PRUH attachment (excerpt only)
- Linkage HLDs: [2471034898](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2471034898), [2417065986](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2417065986) (left to the linkage brief)
- Mersey Care meetings from January and February 2026
- Achilles demo: [3034742870](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3034742870)
- Restricted Codes meeting: [2956328999](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2956328999)
- NUH demo: [2570158081](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2570158081)
- CUH networking pages: [2293399554](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2293399554), [2256142353](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2256142353), [2259288072](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2259288072), [2150891521](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2150891521)
- LDOO implementation: [3049160707](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3049160707)
- Project directories: skipped because they contain contact details