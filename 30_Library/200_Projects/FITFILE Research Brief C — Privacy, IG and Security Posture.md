---
conformant: false
created: 2026-09-28T01:00:00+00:00
modified: 2026-09-29T10:37:44+00:00
non_conformance_reason: Raw agent research brief kept as source material for the FITFILE
  context brief; awaiting review, not a canonical source note.
permalink: llmeon/00-inbox/fitfile-research-briefs/fitfile-research-brief-c-privacy-ig-and-security-posture
project_name: FITFILE
source: FITFILE Confluence, read-only sweep on 2026-09-28 by a Claude Code research
  agent
source_url: null
status: draft
tags: [fitfile, source/llm, topic/information-governance, topic/privacy]
title: FITFILE Research Brief C — Privacy, IG and Security Posture
type: source
---

%% Raw agent research brief (Claude Code, 2026-09-28), kept as source material for the FITFILE context brief. Not your own writing, so no own_words property. Page IDs link to Confluence. Redacted for the vault where needed: personal names, a prospect's name, page-hygiene and security-debt specifics. %%

Part of: [[FITFILE Context Brief — What We Do and How We Link Data Silos]]

## Brief C: Privacy Treatment, IG, compliance and Security Posture

_Researched 2026-09-28, read-only. In-text citations are Confluence page IDs; §6 gives each ID's title, space and last-modified date. "Inference:" marks my own interpretation. People are referred to by role. The brief contains no secrets, hostnames, contact details, patient data or detailed vulnerability findings._

### 1. Summary

- Operating model. FITFILE is a Data Processor. A FITFILE Node runs inside each Data Controller's perimeter and treats the data there. Raw or identifiable results should not leave that perimeter without the controller's authorisation ([1699741697](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1699741697); [2155118598](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155118598)).
- Classification drives treatment. Each field is classed as a direct, indirect, nonor encoded identifier ([2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252)):
  - direct identifiers are kept, pseudonymised (a reversible FITtoken), anonymised (an irreversible FITanon) or removed;
  - indirect identifiers go through an optimised k-anonymity protocol (optionally with l-diversity) or through custom transformations.
- Stated baseline and actual practice differ. The baseline is anonymisation with k ≥ 5. For wide OMOP extracts, the guidance instead sets k = 1 and relies on custom transformations, because full k-anonymity destroys too much utility ([2431680531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431680531)).
- Fixed minimisation rules. Small number suppression (SNS), national and local opt-outs, and a restricted-codes list apply on top of treatment ([2098167827](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2098167827)).
- Re-identification. Only FITtokens can be re-identified, only by users with identifiable-data permission, and across sites only within a sharing agreement ([1590296577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1590296577)).
- Controller approval. Controllers can require approval of every release ("Data Disclosure"); one refusal fails a multi-source query ([2148499464](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2148499464)). Output checking of final research outputs happens in the SDE/TRE, not in FITFILE.
- Opt-out timing gap. The national data opt-out (NDOO) is checked through NHS MESH, currently inside the ETL before harmonisation. The EoE SDE protocol requires a check at every data pull, which the current design does not meet. A redesign, including local opt-outs, is under way ([2860285962](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2860285962); [3049160707](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3049160707)).
- IG framing. Pages follow the ICO's 2025 anonymisation guidance (anonymity depends on context; the "motivated intruder" test) and the Five Safes/SATRE frameworks. FITFILE argues that anonymisation is not legally required for SDE research. It still recommends privacy-enhancing techniques (PETs) and leaves the decision to controllers ([2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252)).
- Certification. The certificate list shows ISO 27001:2022, Cyber Essentials, Cyber Essentials Plus (CE+) and NHS DSPT 2024-25 "standards exceeded" ([2586411009](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2586411009)). The page looks out of date.
- Weak spots: inconsistent thresholds and terminology; unfinished limitations documentation; unresolved status of custom-transformed outputs; opt-out timing versus the protocol.

### 2. Findings

#### 2.1 IG Framing, Roles and Legal Basis

- Processor constraints. FITFILE "has all the constraints of a Data Processor", including not disclosing identifiable data "without an appropriate legal basis" ([1699741697](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1699741697)). Clients usually supply the DPIA template. FITFILE keeps its own DPIA and DSA templates and REC/CAG guidance ([1780056065](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1780056065)).
- IG comes first. The "IG Approvals" stage (DPIA and supplier/cyber assessments issued by the controller) comes before IT approval, installation and live data. The provider's data manager approves how each field is classified ([2840264705](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2840264705)). Example: at NNUH, the DPIAs were approved and the DCA and DSA signed before live data ([2716499969](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2716499969)).
- Controllership is set per site. At NUH the trust stays controller until data moves to an approved project. NUH is amending a vendor-agnostic DPIA using FITFILE's summary of its processing ([2899443716](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2899443716); [2908586007](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2908586007); [2955804715](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2955804715)).
- FITFILE's draft position ([2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252)):
  - a lawful basis is enough for SDE use;
  - ISB1523 governs publication of data;
  - a dataset can count as anonymous inside an SDE but as personal data if published;
  - the overall likelihood of re-identification inside an SDE is "Unlikely" but not zero, so PETs are still recommended.
- Earlier notes record a view that pseudonymised data in accredited TREs can be "effectively anonymised" ([2140798977](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2140798977)).
- Accountability. SDE data managers are "accountable for the data made available to researchers" ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).

#### 2.2 Classification and Techniques

- Classes: direct; indirect (strong, moderate or weak); non-identifier; encoded (a token that maps one-to-one to a direct identifier) ([2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252); [2028666883](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2028666883)).
- Direct identifiers: identifiable, FITtoken, FITanon or removed. Anonymisation is the baseline unless a Data Access Committee (DAC) approves identification ([2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252)). Direct identifiers can still be used internally for joins but must not appear in de-identified output. At one point query authors could override the classification ([2028666883](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2028666883)).
- Indirect identifiers: a k threshold and a suppression limit are required; l-diversity is optional. The algorithm generalises each type step by step (intervals; postcode unit up to area; strings removed) and picks the combination that loses least information ([2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252); [2162425858](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2162425858); [1695678466](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1695678466)).
- Custom transformations (about 20) include date shift, bucketing, noise, shuffle, low-count suppression, salted hashing, encryption, removal and postcode trimming ([2162130950](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2162130950); [2431680531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431680531)).
- OMOP defaults by type: strings are removed, concept IDs get low-count suppression, numbers are bucketed and dates are shifted. Related fields are treated together, and `*_source_value` fields are excluded ([2518417409](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2518417409)).
- Choosing settings. Inspect the Data Profiler first (k-distribution, entropy, completeness). For OMOP, use k = 1 so the NHS number is treated before it leaves the provider Node, then apply custom transformations ([2431680531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431680531)). Parameters can be a baseline or set per DAR/DAC ([2140798977](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2140798977)).
- Hidden identifier ("leaky PID") detection. Uses Presidio with UK recognisers and custom patterns. Found values can be replaced, redacted, hashed, masked or encrypted ([2232778753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2232778753); [2704310273](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2704310273)).
- Warehousing. Light pseudonymisation is applied for storage, with full de-identification at extraction. Salts are scoped to a project and permission-controlled ([2065924099](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2065924099); [2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).

#### 2.3 Fixed Minimisation Rules

- SNS suppresses counts of individuals below a threshold ([2164883457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164883457)). An April 2026 proposal ([2739273729](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2739273729); see also [2170552391](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2170552391)):
  - providers suppress before results leave their boundary;
  - the SDE applies its own threshold after linkage and de-duplication;
  - users see a generic "no results" message;
  - project extracts get no SNS; SDE managers review them instead, with TRE output checks (ACRO/SACRO).
- Restricted codes (the SUS/NHS Digital list, plus descendant and mapped codes) are removed in the ETL as a second check ([2098167827](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2098167827); [2856812545](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2856812545)). Lists differ between providers. The protocol only requires DAC approval before these codes are released, not their removal, so filtering may move to the delivery stage ([2956328999](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2956328999)).
- NDOO rules as FITFILE reads them ([2247655425](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2247655425)):
  - NDOO applies to confidential patient information (CPI) disclosed under s251 for research or planning;
  - it does not apply to anonymised or aggregate data, so cohort counts are exempt;
  - it applies at every controllership boundary, and whole records are removed;
  - data must be disclosed within 20 days of a direct check, or 13 days with a 7-day cache;
  - DSPT includes an NDOO evidence item.
- How NDOO is run. MESH returns the NHS numbers that have not opted out. FITFILE passed the NHS witness test and holds live credentials ([2098167827](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2098167827)).
  - A 2025 decision runs NDOO in The Hyve's ETL before harmonisation, so opted-out records are never stored, and the pipeline must stop if the check fails ([2247655425](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2247655425)). Earlier designs are superseded ([1417478145](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1417478145); [1954578436](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1954578436)).
- Site constraints:
  - CUH filters its own data using FITFILE's list, because FITFILE has no write access. The SDE flagged CUH's irregular refresh as a patient-rights concern.
  - The SDE Node cannot re-check, because NHS numbers never reach it ([2786525192](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2786525192)).
  - NUH runs its own checks, because its OMOP data lacks NHS numbers ([2899443716](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2899443716)).
- Local data opt-out (LDOO). CUH curates the EE SDE list, which is held centrally as plain NHS numbers and is currently empty. The redesign adds ([3049160707](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3049160707)):
  - multiple sources and opt-in overrides;
  - audit counts and minimal retention;
  - re-application once the disclosure grace period passes.

  The page also records a MESH mailbox limitation.

#### 2.4 Re-identification

- The 2023 design ([1590296577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1590296577)):
  - a permitted user submits tokens and retrieves the matching source records;
  - users on multi-site projects see only their own tenant's records, unless a consent or sharing agreement covers overlapping populations;
  - re-identified records must stay within the tenant or agreement;
  - tokens are stored apart from source data;
  - "re_identify" is a project permission.

  By 2024 the UI could re-identify a single token or a whole dataset ([1740374020](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1740374020)).

- Token types. FITanons are irreversible and non-deterministic (based on a zero-knowledge proof, ZKP). FITtokens are deterministic and can be regenerated ([2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026); [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497)). A salted SHA-256 hash can be re-identified only by re-hashing retained source data ([2065924099](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2065924099)).
- Engineer access. Engineers with system-level cloud access could reach a Node's database. This is used only for audited admin work with the provider's permission; otherwise staff follow RBAC. Providers grant read-only database access, and The Hyve has none ([2901737478](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2901737478)).

#### 2.5 Controller Controls and Output Checking

- Purpose. Controller approval shifts responsibility to the controller and guards against schema errors or faults releasing identifiable data ([1786249217](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1786249217)).
- Data Disclosure is set per tenant and is off by default. The approver sees the project, dataset, query and a downloadable preview, and the feature has its own RBAC permissions. A bypass for cohort discovery is being refined ([2148499464](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2148499464)).
- IG QA tools: Data Disclosure, a transformation report, the Data Profiler and Data Lineage. The page recommends manual output checking and motivated-intruder tests ([2099871745](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2099871745)).
- Export requires the export permission plus read access to each artefact. Destinations are allow-listed per project, and manifests are signed ([2652667916](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2652667916)).

#### 2.6 Access Control and Audit

- Access stack. Login uses Auth0 with MFA; permissions use RBAC and Zanzibar-style authorisation (SpiceDB). Projects give purpose-based access control, and an audit page logs user, data-access and query events ([2097872915](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2097872915); [2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026); [2704310273](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2704310273)).
- Between Nodes. A consumer sees provider data only within a project, and only the datasets the provider has attached. Datasets may need controller approval, and results can optionally be restricted to anonymised output. Network project set-up by request and approval, replacing manual work by staff, was still open ([2033123333](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2033123333)).
- RBAC redesign. A draft says providers, not consumers, should set per-project access policy: identifiable, anonymised or pseudonymised ([2681077761](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2681077761)).
- Internal privileged access requires a justified request, a signed policy, an entry in the access register and periodic review ([2977955842](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2977955842)).

#### 2.7 Security Posture and Certification

- Architecture:
  - Nodes run in the provider's cloud with no inbound path from the public internet;
  - Nodes talk to each other over private links, and polling for national portal queries is outbound only;
  - data is encrypted in transit and at rest;
  - infrastructure and deployment are managed as code (IaC/GitOps), with secrets held in Vault;
  - image scanning, a software bill of materials (SBOM), static analysis and a SIEM are in place;
  - only sanitised telemetry leaves the Node ([2155118598](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155118598); [2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026); [2471034898](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2471034898)).
- Certificates: ISO 27001:2022 (2024-06-30), Cyber Essentials (2025-07-04), CE+ (2025-08-08) and DSPT 2024-25 (2025-06-27) ([2586411009](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2586411009)). Evidence gathering for the 2026 CE+ and DSPT is documented ([2923429890](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2923429890); [2997813250](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2997813250)).
- Ongoing security work. Recurring InfoSec reviews support ISO 27001 control A.8.8 (technical vulnerabilities). Pen-test actions are complete, a retest is being scheduled and a security operations centre (SOC) provider is being chosen ([2846556161](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2846556161)). A roadmap proposes reserving about 20% of sprint capacity for security ([2786230276](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2786230276)). Open findings are recorded in those pages and not repeated here.

#### 2.8 Documented Limitations

- k-anonymity:
  - it ignores population size, which is why SNS exists ([2164883457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164883457));
  - allowing suppression gives up the optimal result, and the search cap can drop columns ([1695678466](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1695678466));
  - it is unsuitable for transactional OMOP data ([2428370946](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2428370946)) and costly in utility ([2431680531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431680531)).
- OMOP leakage paths: untreated `*_source_value` fields, date and datetime pairs, birth-date integers, era tables and the public concept table ([2518417409](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2518417409)). Many transformations also break OMOP data types ([2431680531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431680531)).
- Custom-transformed outputs are "not considered fully privacy-treated" and are classed as identifiable ([2065924099](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2065924099)). This was still open in 2026 ([2681077761](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2681077761)).
- Restricted-code filtering misses uncoded, malformed or embedded codes ([2856812545](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2856812545)).
- Opt-out checks need NHS numbers; tables without them can defeat the check ([1954578436](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1954578436); [3049160707](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3049160707)).
- Documentation stubs. The requirement to document limitations for SDE data managers is only a stub ([2351071235](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2351071235)), as are [2350743563](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2350743563) and [2350940169](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2350940169).

### 3. Key terms

- Direct / indirect / non- / encoded identifier: the schema classes that decide treatment ([2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252)).
- FITtoken: a deterministic, re-identifiable pseudonym ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
- FITanon: an irreversible, non-deterministic cipher based on a zero-knowledge proof ([2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497)).
- k-anonymity; suppression limit: each record matches at least k−1 others; the suppression limit is the share of rows that may be dropped to reach this ([2245394443](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2245394443); [2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252)).
- l-diversity: at least l distinct sensitive values in each group ([2245361665](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2245361665)).
- SNS: counts of individuals below a threshold are suppressed ([2164883457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164883457)).
- Data minimisation rules: SNS, opt-outs and the SUS restricted terms ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
- Data Disclosure: the controller approves each release of its data ([2148499464](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2148499464)).
- NDOO / LDOO: the national opt-out, checked via MESH / a local or SDE-level opt-out ([2247655425](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2247655425); [3049160707](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3049160707)).
- Disclosure grace period: the time after an opt-out check within which data may cross a boundary ([3049160707](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3049160707)).
- CPI / s251: confidential patient information / the legal gateway that triggers NDOO ([2247655425](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2247655425)).
- Motivated intruder, singling out, linkage: the ICO's tests of whether someone can be identified ([2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252)).
- Leaky PID: identifiers hidden in fields not labelled as identifiers ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
- Light pseudonymisation: masking for warehousing, before full de-identification ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
- PBAC: purpose-based access control, applied through projects ([2704310273](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2704310273)).
- DAC / DAR: Data Access Committee / Data Access Request ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
- ACRO / SACRO: output-checking tools used in the TRE ([2739273729](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2739273729)).

### 4. Tensions, Contradictions and Open Questions

1. k thresholds differ across pages:
   - k ≥ 5 ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881); [2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252));
   - treat groups under 10 and require at least 10 records ([1341128707](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1341128707), 2022);
   - groups over 5 ([1591115777](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1591115777));
   - k = 11 ([2428370946](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2428370946));
   - k = 1 for OMOP ([2431680531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431680531));
   - described as "mandatory" in a demo ([2704310273](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2704310273)).
2. Where k = 5 comes from. One page attributes it to the ICO ([2247655425](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2247655425)); another suspects ISB1523 ([2140798977](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2140798977)). Inference: verify before using it externally.
3. Custom-transformed outputs are classed "identifiable" ([2065924099](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2065924099)) yet are now the recommended OMOP method ([2431680531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431680531)). Their classification, and whether NDOO applies to them, needs a decision.
4. FITanon is described two ways: as a ZKP cipher that changes on every run ([2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026); [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497)), and as "created by hashing direct identifiers" ([2704310273](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2704310273)).
5. FITtoken reversal. Page [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497) says both "lookup table if required" and "not dependent on lookup … tables". It also says "no additional identifiable data is persisted", yet the 2023 design keeps the loaded data for re-identification ([1590296577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1590296577)).
6. Staff access. "FITFILE staff cannot access the inner workings" of Nodes ([2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497)) conflicts with the documented system-level access and manual set-up ([2901737478](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2901737478); [2033123333](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2033123333)).
7. Who owns the opt-out duty. One page says FITFILE "does not carry the legal obligation" ([2153349158](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2153349158)); another that it "would be held responsible" ([2247655425](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2247655425)). The EoE protocol names CUH as the controller running NDOO ([2860285962](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2860285962)).
8. NDOO frequency is quoted as every 9 ([1954578436](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1954578436)), 14 ([2786525192](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2786525192)), 20 ([2860285962](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2860285962)) and about 22 days ([2098167827](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2098167827)). Inference: 22 days would exceed the 20-day disclosure window. Pages from February 2025 describe checks after harmonisation and local opt-outs as working ([2096726017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2096726017); [2096922625](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2096922625)); later decisions supersede them ([2247655425](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2247655425)).
9. Filtering stage unsettled. Whether SNS applies to extracts, and where restricted codes are filtered, are both undecided ([2739273729](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2739273729); [2956328999](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2956328999)).
10. Certification freshness. The CE+ certificate's file name implies expiry in August 2026, but the page was last updated in January 2026 ([2586411009](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2586411009); [2923429890](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2923429890)). A compliance matrix ticks SOC 2, HIPAA and ISO 27017/27018, which the certification page does not list ([2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026)). Inference: these ticks may cover third-party components or aims; verify.
11. Terminology. Customers use "pseudonymised" and "anonymised" interchangeably ([2955804715](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2955804715)). The glossary says pseudonymised data remains personal data ([2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881)).
12. Unverified claim. "The ICO recommends FITFILE" rests on a screenshot I did not review ([2128445442](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2128445442)).
13. Embedded secrets. Findings were reported separately and are not recorded here.
14. Empty or skeleton pages: [2217279539](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2217279539), [2431352836](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431352836), [2999123969](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2999123969), and the regulatory section of the opt-out draft.

### 5. Relevance to Linking Data Silos

- Who may join what. The provider is the controller and FITFILE the processor. The DPIA and DCA/DSA come before live data ([2840264705](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2840264705); [2716499969](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2716499969)). Joins happen in the consumer or coordinating Node, and only across datasets the provider has attached to the project ([2033123333](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2033123333)). With Data Disclosure on, every controller must approve ([2148499464](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2148499464)).
- Linkage key. Linkage needs a common key: the NHS number in `person_source_value`. It is classed as a direct identifier and must become a FITtoken or FITanon inside the provider Node before transfer ([2155315202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155315202); [2431680531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431680531)).
  - Pre-tokenised inputs would break NDOO and re-identification ([2155315202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155315202)).
  - Projector SDE-specific salts limit what can be linked, and access to salts is permission-controlled ([2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497); [2065924099](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2065924099)).
- No common key. Probabilistic matching then runs on ciphers of name, date of birth and postcode. The ciphers are destroyed after matching and only aggregates leave ([2471034898](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2471034898)). This follows the 2021 rule that no personal information passes between sources or leaves a controller's perimeter ([1302003713](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1302003713)).
- Re-identifying linked data. Only FITtokens can be re-identified, only by permitted users, and only for their own records unless a sharing agreement covers overlap ([1590296577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1590296577)). Links made with FITanons cannot be reversed.
- Before linked data is released:
  - apply opt-outs at each boundary, ideally at delivery ([2247655425](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2247655425); [2860285962](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2860285962));
  - remove restricted codes ([2098167827](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2098167827));
  - apply SNS at the provider and again after de-duplication ([2739273729](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2739273729));
  - privacy-treat the linked data again before anyone views or stores it ([2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026));
  - obtain controller approval and DAR/DAC approval ([2148499464](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2148499464); [2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252));
  - leave final output checks to the SDE/TRE ([2739273729](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2739273729)).
- Retention. Pseudonymised linked data kept past the grace period needs opt-outs re-applied, for example by re-tokenising at source ([3049160707](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3049160707)). Inference: this is the main open IG risk for linked data held over time.

### 6. Pages

Read (ID, short title, last modified):

- FITFILE:
  - Anonymisation technique pages: [1695678466](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1695678466) K-Anonymity 2025-04-29; [1812135937](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1812135937) Parameter benchmark 2025-04-24 (attachment not read); [2162425858](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2162425858) Transformation Series 2025-04-24; [2162130950](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2162130950) Transformations 2025-04-24; [2128445442](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2128445442) De-identification process 2025-03-24 (images not viewed); [2140798977](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2140798977) Privacy Treatment Guidelines 2025-04-04.
  - SNS pages: [2164883457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164883457) (Archived) SNS Design 2026-04-09; [2170552391](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2170552391) HIE explanation draft 2025-05-06; [2739273729](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2739273729) SNS updated feature 2026-04-09.
  - Opt-out pages: [2247655425](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2247655425) National Data Opt-Out 2026-05-05; [1954578436](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1954578436) (Legacy) NDOO 2025-07-22; [3049160707](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3049160707) LDOO/NDOO evolution 2026-09-24; [2153349158](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2153349158) Opt-out DRAFT 2025-05-16; [2096726017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2096726017) NHS Opt-Out Process 2025-02-26; [2096922625](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2096922625) Local NHS Opt-Outs 2025-02-26; [1679163403](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1679163403) Opt-out Service 2024-03-13 (container); [1417478145](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1417478145) NHS Data Opt-Out Checks 2022-08-26; [1696235521](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1696235521) Opt out Process 2024-03-13; [2652405762](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2652405762) Node Installation–Opt-Out 2026-02-24 (empty).
  - Controls, disclosure and access pages: [1786249217](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1786249217) Data Controller Controls 2024-06-04; [2148499464](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2148499464) Data Disclosure 2025-08-05; [2028666883](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2028666883) Removal of Direct Identifiers 2025-01-27; [2232778753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2232778753) PII Detection 2025-08-21; [2901737478](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2901737478) Data Access Principles and Roles 2026-07-02.
  - Security, platform and compliance pages: [2097872915](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2097872915) Deployment Guide 2025-02-28; [2105180161](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2105180161) Requirements of a Secure Platform 2025-03-04; [2098167827](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2098167827) Fixed IG rules plan 2026-06-09; [2997813250](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2997813250) For NHS DSPT 2026-08-20; [2999123969](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2999123969) For ISO27001 2026-08-20; [2997583874](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2997583874) For CE and CE+ 2026-09-11; [2923429890](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2923429890) CE+ preparation 2026 2026-07-21; [2786230276](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2786230276) Security & Maintenance Roadmap 2026-04-30.
  - Document management, not patient-data IG: [2390556675](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2390556675) What needs to be covered 2026-01-13; [2314764290](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2314764290) Approach to Information Management 2026-01-12.
  - Further pages:
    - [2856812545](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2856812545) Restricted codes 2026-06-09;
    - [1740374020](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1740374020) Re-identification incident 2024-04-24;
    - [2025652226](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2025652226) ENCRYPTED DATA 2025-01-16;
    - [2518417409](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2518417409) OMOP custom treatment 2026-02-04;
    - [2155118598](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155118598) Technical Implementation Overview 2025-04-30;
    - [2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881) SDE Technical Glossary 2025-02-14;
    - [1780056065](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1780056065) Governance, Tech & Data Prep 2024-06-19;
    - [2099871745](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2099871745) QA tools v2.0 2025-04-30;
    - [2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026) Technical Overview 2025-04-25;
    - [2155315202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155315202) Minimum fields for linkage 2025-04-16;
    - [2065924099](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2065924099) Custom Transformation Operation 2025-09-30;
    - [1699741697](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1699741697) 2. Constraints 2024-10-05;
    - [2704310273](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2704310273) Platform Walkthroughs 2026-03-19;
    - [2977955842](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2977955842) Privileged Access SOP 2026-08-20;
    - [2033123333](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2033123333) Multi-Tenanted Access Control 2025-06-30;
    - [2681077761](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2681077761) RBAC DRAFT 2026-03-10;
    - [1670479880](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1670479880) Viewing Audit Logs 2024-02-06;
    - [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497) Comparison of linkage approaches 2026-02-04 (draft with placeholders);
    - [2840264705](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2840264705) Node Implementation stages 2026-06-18;
    - [2652667916](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2652667916) Data Export (revisited) 2026-02-24.
- PRODDOCS: [2217082892](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2217082892), [2217345026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2217345026), [2217377802](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2217377802) (catalogue 1.3.0–1.3.2) 2025-06-13; [2208530436](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2208530436) 1.3.3 Custom Transformation 2025-06-13; [2245394443](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2245394443) k-anonymity FAQ and [2245361665](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2245361665) l-diversity FAQ 2025-07-14; [2211479571](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2211479571) field-level anonymisation FAQ 2025-06-12; [2201288746](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2201288746) RQ-1.1.1 2025-06-10; [2351071235](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2351071235), [2350743563](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2350743563), [2350940169](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2350940169) requirement stubs 2025-10-17; [2217279539](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2217279539) 1.7.1 Auditing 2025-06-13 (empty).
- CDH: [2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252) Privacy treatment guide (in progress) 2026-02-11; [2431680531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431680531) Privacy treating OMOP data 2025-11-19; [2431352836](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431352836) Privacy Treatment User Guide 2025-11-11 (skeleton); [2428370946](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2428370946) Complex-query de-identification guide 2025-11-11.
- FG: [2586182209](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2586182209) FITFILE Governance 2026-01-23 (template home page); [2586411009](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2586411009) Platform certification 2026-01-23.
- PS:
  - [1341128707](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1341128707) Anonymisation Protocol 2022-03-14;
  - [786989068](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=786989068) Compliance and Governance 2021-04-07;
  - [1359151114](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1359151114) Security 2023-07-10 (container);
  - [354254866](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=354254866) InfoSec 2020-12-10 (empty);
  - [1327202305](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1327202305) and [1326612485](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1326612485) access-to-data stubs 2022-01-21;
  - [1230569473](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1230569473) Authentication/authorisation requirements 2021-10-18;
  - [1186889729](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1186889729) Security Questions 2021-11-22;
  - [2271674369](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2271674369) InfoSec Review August 2025, 2025-08-11;
  - [2846556161](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2846556161) InfoSec Review September 2026, 2026-09-11 (newer than the review named in the task);
  - [1590296577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1590296577) Pseudonymisation and re-identification design 2023-06-30;
  - [1591115777](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1591115777) Pseudonymisation Notes 2023-07-03;
  - [754319363](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=754319363) Statistical Disclosure Controls 2022-02-23;
  - [1302003713](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1302003713) Anonymisation requirements 2021-11-09.
- EOE: [2786525192](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2786525192) NDOO & LDOO discussion 2026-05-05; [2860285962](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2860285962) roadmap review 2026-06-11; [2899443716](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2899443716) NUH IG meeting 2026-07-01; [2908586007](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2908586007) NUH IG meeting 2026-08-26; [2955804715](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2955804715) NUH update 2026-08-26; [2956328999](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2956328999) restricted codes meeting 2026-07-30; [2716499969](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2716499969) NNUH summary 2026-09-25.
- Other: NP [2471034898](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2471034898) NWSDE linkage HLD 2026-02-03; HDRSTT [3073245215](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3073245215) federated linkage summary 2026-09-25 (whether a DPIA is needed is still under review); personal space [2427027457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2427027457) Demo de-identification Tools 2025-11-17.

Found, not read:

- PS: [3042017283](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3042017283) (InfoSec Review June 2026); [1448017921](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1448017921) and [1581580289](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1581580289) (pen tests); [1423343624](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1423343624), [1506476033](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1506476033) and [1410859009](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1410859009) (risk assessments); [704249864](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=704249864); [700055553](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=700055553); [755040265](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=755040265); [871006219](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=871006219); [521699377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521699377) (search excerpt only).
- FITFILE: [2978447361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2978447361) and [2977955850](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2977955850) (SOPs); [2597683214](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2597683214); [1701314562](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1701314562); [1453522945](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1453522945); [1621032961](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1621032961); [2332000261](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2332000261); [2187296770](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2187296770); [2536996871](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2536996871); [2313125893](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2313125893); [2024898561](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2024898561); [2503376897](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2503376897).
- NP: [2417065986](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2417065986).
- EOE: [2788950017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2788950017).
- Not viewed anywhere: embedded images, PDFs and HTML attachments.
