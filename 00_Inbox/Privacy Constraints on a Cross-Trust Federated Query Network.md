---
conformant: false
created: 2026-09-29 11:20:00+01:00
modified: 2026-09-29 11:20:00+01:00
non_conformance_reason: Agent-drafted constraint catalogue awaiting review in 00_Inbox;
  intended to become an SoT once validated with an IG or DPO reviewer. Not legal advice.
project_name: FITFILE
source: UK legislation and NHS England, DHSC, NDG, HRA and ICO guidance (checked 2026-09-29),
  plus FITFILE Confluence research (2026-09-28)
source_url: null
status: draft
tags:
- source/llm
- fitfile
- topic/privacy
- topic/information-governance
- topic/data-linkage
- topic/secure-data-environments
- topic/problem-definition
title: Privacy Constraints on a Cross-Trust Federated Query Network
type: sot
permalink: llmeon/00-inbox/privacy-constraints-on-a-cross-trust-federated-query-network
---

%% Agent-drafted (Claude Code, 2026-09-29), not your own writing, so no own_words property. Not legal advice: validate with a DPO or Caldicott Guardian before relying on it. Legal and policy points were checked against the linked sources on 2026-09-29. Field evidence comes from the FITFILE research briefs. Triage with Prompt - Vault Ingest Router. %%

## Privacy Constraints on a Cross-Trust Federated Query Network

> [!summary] The problem, stated at privacy level
> Many independent organisations hold health data about the same people. Each is separately accountable for that data in law and owes the patients a duty of confidence. The research value comes from combining the data across organisational boundaries — and combining is exactly what the rules restrict, because it raises identifiability, crosses a controller boundary and can break patients' reasonable expectations.
>
> **So the problem is:** let an approved user ask one question of many organisations' data, for an approved public-benefit purpose, so that:
> - each organisation keeps control of its data and decisions;
> - each patient's choices are honoured;
> - nobody sees more identifiable data than their role and approval allow;
> - identities are re-joined only by authorised parties, for authorised reasons;
> - only non-disclosive answers leave;
>
> — all while every organisation applies its own rules on its own timescale.

**How to read this.** Constraints are numbered (C1.1, C1.2 …) so design work can refer to them. Each carries a type:
- **Law:** statute or common law. Not negotiable.
- **Policy:** national NHS, DHSC or NDG policy for SDEs. Binding in practice, with defined exceptions.
- **Local:** set by each trust or SDE. Varies, and is negotiated one organisation at a time.
- **Trust:** social licence. Not codified, but binding in effect.

Field evidence comes from [[FITFILE Research Brief C — Privacy, IG and Security Posture]], [[FITFILE Research Brief D — Record Linkage and Pseudonymous Identity]], [[FITFILE Research Brief E — Programmes and Data Silos in the Field]] and [[FITFILE Research Brief F — Personal-Space Sweep]].

### Why the "public data" design fails

| If the data were public, we would… | …but these constraints forbid it |
|---|---|
| Put every site on the public internet | C6 (where data may live and travel), C8.5 (assurance), C6.5 (each trust decides what touches its data) |
| Query every database in the clear | C1 (legal basis and confidentiality), C4 (minimum necessary, de-identified access), C3 (opt-outs), C7 (need to know) |
| Join records on names or NHS numbers wherever convenient | C5 (where linkage happens, who may re-identify), C1.2 (s251) |
| Let one operator run any query for anyone | C2 (approved purpose), C7.3 (controllers decide), C8.2 (joint-controller risk), C9 (transparency) |
| Send results straight to the user | C4.6 (output checking), C6.1 (data access, not data sharing) |
| Set it up once and leave it | C3.2 (opt-outs refresh), C10 (time), C11 (every trust differs) |

### C1. Legal basis: the right to use the data at all

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C1.1 | Two separate legal tests apply to every use, and passing one does not pass the other. **Data protection** needs a UK GDPR lawful basis plus an Article 9 condition, because health data is special category. The **common law duty of confidentiality** needs consent, s251 support, a legal requirement or an overriding public interest — unless the data is anonymised and therefore not confidential. | Law | UK GDPR Arts 6 and 9; DPA 2018 Sch 1; HRA | |
| C1.2 | Using identifiable data for research without consent needs s251 support: an application to the HRA's Confidentiality Advisory Group for that specific activity. Support is given only where consent is not practicable and anonymised data will not do. | Law | NHS Act 2006 s251; COPI Regulations 2002 reg 5 | |
| C1.3 | Consented data may be used only within the scope of the consent. Broad consent to an area of research is now lawful, subject to recognised ethical standards. | Law | DUAA 2025 | Consented cohorts and the opt-out interact (EE NDOO & LDOO discussion) |
| C1.4 | Research processing must not be likely to cause substantial damage or distress, and must include data-minimisation measures. It must not support measures or decisions about particular people unless it is REC-approved medical research. | Law | UK GDPR research safeguards (formerly DPA 2018 s19; unchanged in substance by DUAA) | Re-contact for trials is pitched as a benefit of linkage in EE |
| C1.5 | Research needs ethics approval: either per project, or under the SDE's research-database approval. The latter covers projects that use non-identifiable data within its approved terms, for five years at a time. | Law / Policy | HRA | |
| C1.6 | Non-NHS data (council, DWP, employer HR, national registers) sits under its own controllers' legal gateways. NHS routes such as s251 and the SDE policy do not automatically cover it. | Law | Controller-specific | LCRCA (DWP data) and Mersey Care (staff HR data) both stalled at governance |

### C2. Purpose: why the data is used

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C2.1 | Every query must trace to a specific, approved purpose, such as a Data Access Request approved by the SDE's Data Access Committee. Open-ended querying is not allowed. | Law / Policy | UK GDPR Art 5(1)(b); Caldicott 1; SDE guideline 5 | |
| C2.2 | Use must be for public good — never for marketing or insurance — and public benefit should be evaluated explicitly. | Policy | SDE guideline 11; NDG public-benefit guidance (2022) | |
| C2.3 | Commercial research is legitimate. But NHS data may not be hosted solely in a commercial or academic SDE, and NHS organisations keep decision-making power over access. | Law / Policy | DUAA 2025; DHSC data access policy (2023) | HDRS TT is pharma-backed |
| C2.4 | Direct care and research are separate regimes. Re-contacting patients is a new purpose that needs its own route, and research results cannot feed decisions about individuals (see C1.4). | Law | Common law confidentiality; NDOO policy ("consent for consent") | |
| C2.5 | Continuing uses must be reviewed regularly. | Policy | Caldicott 1 | |

### C3. Patient choice: opt-outs and objections

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C3.1 | Apply the national data opt-out wherever it is in scope: confidential patient information used beyond individual care, which for research means where s251 is the basis. All SDEs are expected to comply. | Policy | NDOO operational policy; DHSC data access policy | |
| C3.2 | Apply it at each disclosure: the opt-out check must be no more than 20 days old, or 13 days where a local cache is refreshed at least weekly. Remove the whole record, not just its identifiers, and re-apply the opt-out at every onward disclosure. It is not retrospective for data already processed. | Policy | NDOO policy §8 | The EE protocol expects a check at every data pull; the current design checks once, in the ETL |
| C3.3 | It does not apply to data anonymised to the ICO standard, to aggregate or count data, or where the person has given explicit consent. So where "pseudonymised" ends and "anonymised" begins decides whether opt-outs apply at all. | Policy | NDOO policy | Custom-transformed OMOP outputs are classed as identifiable |
| C3.4 | Opt-out lists may be used only to apply opt-outs — never to select people for research or judge their suitability. | Policy | NDOO policy §8 | |
| C3.5 | Type 1 (GP-level) objections still apply to GP data, because their retirement has been deferred. Programme-specific and local opt-outs also exist and differ between organisations. | Policy / Local | NHS England GP guidance; NDOO policy §7 | EE keeps an SDE-level local list; CUH filters its own data; NUH applies its own opt-outs |
| C3.6 | Individuals' rights (access, objection and so on) continue unless a research exemption is properly relied on, with safeguards in place. | Law | UK GDPR; DPA 2018 Sch 2 | |

### C4. Identifiability: what may be seen

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C4.1 | Minimum necessary: only the fields each approved purpose needs, and only when it needs them. | Law | Caldicott 2–3; UK GDPR data minimisation | |
| C4.2 | SDE users see only de-identified data — aggregated, anonymised or pseudonymised, depending on their role. Identifiable data is not disseminated. | Policy | SDE guideline 7 | |
| C4.3 | Pseudonymised data is personal data for anyone who holds, or can reasonably obtain, the means to re-identify it. It may be anonymous in the hands of a recipient who cannot. So the same dataset has a different legal status depending on who holds it. | Law | ICO pseudonymisation guidance | NUH releases data that is already pseudonymised |
| C4.4 | Anonymity is judged in context against a "motivated intruder", taking into account what else the recipient can access. De-identified data for limited access counts as anonymised only with added controls on access, purpose and contracts. | Law | ICO anonymisation guidance; NDOO policy | |
| C4.5 | Linking datasets adds attributes about the same person and raises identifiability, so the assessment must be made on the linked result, not on each source separately. | Law (applied) | ICO identifiability principles | |
| C4.6 | Everything that leaves the SDE must be checked, aggregated, non-identifiable and consistent with the project's approval, with small numbers suppressed. Repeated or overlapping queries can reveal what no single output does. | Policy | SDE guideline 12 | Small-number suppression proposed at the provider and again after de-duplication; TRE output checks (ACRO/SACRO) |
| C4.7 | Some categories carry extra legal or national restrictions, for example the ISB 1572 Sensitive Data standard (IVF, sexually transmitted infections) and gender-recognition information. Trusts also keep their own restricted-code lists. | Law / Local | ISB 1572; Gender Recognition Act 2004 s22; trust lists | Restricted-code lists differ between providers |
| C4.8 | Free text, genomic data, images, rare conditions and small populations are hard or impossible to de-identify reliably. | Principle | ICO anonymisation guidance | UCL POC included omics; the EE "deep data" plans need CAG/REC amendments |

### C5. Identity and linkage: recognising the same person across silos

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C5.1 | No common identifier spans the silos. The NHS number exists only in NHS data, and some providers will not release it, or any other direct identifier. | Fact | — | DWP and HR data have no NHS number; NUH supplies none; LCRCA withheld names, then postcodes |
| C5.2 | Linkage must happen inside the secure environment and be done by qualified people. | Policy | SDE guideline 8 | |
| C5.3 | Re-identifying de-identified data without the controller's consent is a criminal offence. The ability to reverse pseudonyms therefore needs explicit authorisation from every controller concerned, and must stay within that authorisation. | Law | DPA 2018 s171 | |
| C5.4 | The information that reverses pseudonyms must be kept separately and securely. Whoever holds it holds personal data — custody of that information is custody of identity. | Law | ICO pseudonymisation guidance | One linkage secret is shared across a whole network and held centrally |
| C5.5 | Pseudonyms should be scoped so that datasets link only as far as an approval allows. | Practice | FITFILE linkage comparison (NHS tokens differ by sharing domain) | NWSDE PseudoIDs; WMSDE project keys |
| C5.6 | A wrong link attaches one person's data to another, which breaches the accuracy principle. Linkage quality therefore has to be demonstrable. | Law | UK GDPR Art 5(1)(d) | Linkage-quality metrics are still largely undefined |
| C5.7 | A linked dataset is a new dataset. It needs its own approval, DPIA coverage, retention terms and opt-out handling. | Law / Policy | UK GDPR Art 35; NDOO onward-disclosure rule | |
| C5.8 | Separation of functions: whoever handles identifiers for matching should not see clinical content, and vice versa. | Policy (verify) | Common approval condition; confirm with IG | |

### C6. Location and movement: where data may be and go

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C6.1 | Data access, not data sharing: record-level data stays in the secure environment, users come to the data, and only approved outputs leave. | Policy | SDE guidelines 1 and 12; DHSC data access policy | |
| C6.2 | Moving record-level personal data from one organisation to another is a disclosure. It needs a legal basis, opt-out handling, an agreement and an audit trail. This includes intermediate results assembled during a federated query. | Law | Common law confidentiality; UK GDPR | Pseudonymised record-level results are merged at the SDE's coordinating node |
| C6.3 | Data may be hosted only in the UK, the EEA or UK-adequate countries. Hosting or access from outside the UK needs SIRO approval and a transfer risk assessment. | Policy | NHS off-shoring and public cloud guidance | |
| C6.4 | Moving UK patient-level data abroad needs a lawful transfer mechanism. Multinational studies should expect analysis to take place in each country. | Law | UK GDPR Chapter V | Vaccines-prospect research: no common identifier across countries |
| C6.5 | Each trust decides which environments and connections may touch its data: on-premises or cloud, whose tenancy, what connectivity, and whether anything may write to its systems. | Local | Trust policy and risk appetite | CUH refused a write schema on its production server; NUH moved from on-premises to hybrid to managed cloud |
| C6.6 | Data must be protected by appropriate security wherever it is held or moved. | Law | UK GDPR Arts 5(1)(f) and 32 | |

### C7. Access: who may see what

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C7.1 | Only verified, trained and authorised users, for approved purposes. | Policy | SDE guideline 5; Caldicott 4–5 | |
| C7.2 | Suppliers act only on each controller's documented instructions, and their staff get need-to-know access only. | Law | UK GDPR Arts 28–29 | FITFILE ran the NWSDE matching as a managed service and handled the match files |
| C7.3 | Each controller keeps the decision on who accesses its data and what is released, through the SDE's Data Access Committee. | Policy | DHSC data access policy | Data Disclosure lets one controller's refusal fail a multi-source query |
| C7.4 | Every access, query and release must be attributable and auditable. | Law | UK GDPR accountability; DSPT | |

### C8. Accountability and agreements

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C8.1 | Each trust is an independent controller with its own DPO, Caldicott Guardian and SIRO. Each must be satisfied separately; there is no network-wide sign-off. | Law | UK GDPR; Caldicott Guardian role | |
| C8.2 | Roles must be explicit. A party that decides the purposes or means of cross-trust processing risks becoming a joint controller, with a joint controller's duties. | Law | UK GDPR Arts 26 and 28 | Pages disagree on whether FITFILE or CUH carries the opt-out duty |
| C8.3 | A chain of agreements is needed: processing terms with each supplier (including approved sub-processors), sharing agreements between controllers, and access agreements with users. Every new party or purpose means new or varied agreements. | Law / Policy | UK GDPR Art 28; DSAs | HDRS TT needs contract variations for EE, NW and WM plus a new contract for SW; a host CSU being decommissioned forces new DSAs |
| C8.4 | A DPIA is needed for large-scale processing of health data and for matching or linking datasets. Each controller owns its own. | Law | UK GDPR Art 35 | MKUH's DPIA took three months; NUH is amending a vendor-agnostic DPIA |
| C8.5 | Every organisation processing NHS patient data must provide DSPT assurance each year (by 30 June). SDE accreditation is expected. | Policy | DSPT; SDE guideline 2 | |
| C8.6 | Records of processing are required, breaches must be notified within 72 hours, and Freedom of Information applies to NHS-controlled SDEs. | Law | UK GDPR Arts 30 and 33; DHSC data access policy | |

### C9. Transparency and trust

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C9.1 | No surprises: each controller's privacy information must describe the network's processing, and SDEs must publish who accesses data and why. | Law / Policy | Caldicott 8; SDE guideline 4; UK GDPR Arts 13–14 | |
| C9.2 | Patients and the public must be involved in decisions about data access. | Policy | SDE guideline 6 | |
| C9.3 | The research exemption from notifying individuals, where notification would take disproportionate effort, still requires the information to be made public. | Law | DUAA 2025 | |
| C9.4 | Public trust can be withdrawn at scale: care.data closed in 2016, and the 2021 GP data programme was paused after a surge in opt-outs. Commercial involvement draws extra scrutiny. | Trust | NDG public-benefit guidance | Mersey Care's executive declined, citing "nervousness" about staff data |

### C10. Time

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C10.1 | Keep identifiable and linked data only as long as the purpose needs it, and delete it at the end of the project. | Law | UK GDPR storage limitation | |
| C10.2 | Opt-outs, approvals and agreements change or expire, so data that is held or reused must be re-checked: opt-outs at each new disclosure, research-database approvals every five years. | Policy | NDOO policy; HRA | Linked data held past the opt-out grace period needs opt-outs re-applied |
| C10.3 | The ability to re-identify or re-link must not outlast the authorisation that justified it. | Principle | Derived from C5.3–C5.4 | |

### C11. Every trust is different

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C11.1 | Each trust applies national rules through its own policies and risk appetite. That covers suppression thresholds, restricted-code lists, which identifiers may leave, how opt-outs are applied, refresh cadence, query windows, hosting, supplier assurance, and the sequence and timescales of approvals. | Local | Trust policy | k thresholds of 1, 5, 10 and 11 appear across pages; MKUH allows extracts only between 2pm and 10pm; opt-out handling differs at every EE site |
| C11.2 | In a combined output, each contributing controller's rules apply to its share. In practice the strictest rule governs the whole output. | Local | Derived | |
| C11.3 | Participation is voluntary. A provider must see value in taking part, and can decline or withdraw. | Local | — | NUH says the project is for the SDE's benefit, and won't use the platform itself |
| C11.4 | The same data can sit under several governance regimes at once. A query spanning SDEs needs approval from each SDE's DAC, unless they agree mutual recognition. | Local / Policy | DHSC data access policy (regional DACs) | MKUH also supplies the Thames Valley SDE; HDRS TT spans four SDEs |

### C12. Special populations and data types

| # | Constraint | Type | Source | Seen in the field |
|---|---|---|---|---|
| C12.1 | Children's data needs extra protection, and consent or assent must be handled appropriately for young people. | Law | UK GDPR (children merit specific protection) | Adolescent health study (AHS) |
| C12.2 | Staff data (HR, occupational health) is employee data with a built-in power imbalance, and employers treat it with great caution. | Law / Trust | UK GDPR; employment context | Mersey Care |
| C12.3 | For deceased patients, UK GDPR does not apply, but NHS guidance holds that the duty of confidentiality continues after death. | Law / Policy | NHS confidentiality guidance | Mortality linkage sought for vaccine evidence |
| C12.4 | Genetic data is special category and inherently identifying — including of relatives. | Law | UK GDPR Art 9 | UCL POC (omics) |

### Questions to settle with IG before design

1. **The pivotal question.** Does pulling pseudonymised record-level results into the SDE count as a disclosure of confidential patient information, triggering s251 and the opt-out? Or are those results anonymised in the SDE's hands? The answer shapes most of the design (C3.3, C4.3, C6.2).
2. **Control of outputs.** Who is the controller of the linked dataset and of the outputs: each trust, the SDE lead, or all of them jointly (C8.2)?
3. **Opt-out at each boundary.** Who applies the opt-out at each hand-off — trust to SDE, SDE to SDE, and SDE to researcher (C3.2)?
4. **Re-identification rights.** Who may hold the means to re-identify or re-link, on whose authority, and for how long (C5.3, C5.4, C10.3)?
5. **Cross-SDE approval.** For queries that span SDEs (HDRS TT), whose DAC approves them, and is there mutual recognition (C11.4)?
6. **Non-NHS data.** What legal gateway lets non-NHS data (DWP, council, HR) join NHS data (C1.6)?
7. **Combined-output rules.** Which suppression and restricted-code rules govern an output built from several trusts' data (C11.2)?

### Sources

- [The Caldicott Principles](https://www.gov.uk/government/publications/the-caldicott-principles) — National Data Guardian, Dec 2020
- [Secure data environment policy guidelines](https://www.gov.uk/government/publications/secure-data-environment-policy-guidelines/secure-data-environment-for-nhs-health-and-social-care-data-policy-guidelines) — DHSC, Dec 2022
- [Data access policy update](https://www.gov.uk/government/publications/data-access-policy-update/data-access-policy-update) — DHSC, Oct 2023
- [National data opt-out operational policy: applying the opt-out](https://digital.nhs.uk/services/national-data-opt-out/operational-policy-guidance-document/applying-the-national-data-opt-out) and [policy considerations](https://digital.nhs.uk/services/national-data-opt-out/operational-policy-guidance-document/policy-considerations-for-specific-organisations-or-purposes) — NHS England
- [National data opt-out: supplementary information for research organisations](https://www.hra.nhs.uk/about-us/committees-and-services/confidentiality-advisory-group/national-data-opt-out-supplementary-information-for-research-organisations/) — HRA
- [Confidential patient information and s251](https://www.hra.nhs.uk/about-us/committees-and-services/confidentiality-advisory-group/confidential-patient-information-and-regulations/) — HRA
- [Research tissue banks and research databases](https://www.hra.nhs.uk/planning-and-improving-research/policies-standards-legislation/research-tissue-banks-and-research-databases/) — HRA
- [Pseudonymisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/pseudonymisation/) and [anonymisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/) guidance — ICO
- [DUAA 2025: summary of data protection changes](https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-duaa-summary-of-the-changes/data-protection/) — ICO
- [What are the appropriate safeguards?](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/the-research-provisions/what-are-the-appropriate-safeguards/) — ICO
- [Data Protection Act 2018, s171](https://www.legislation.gov.uk/ukpga/2018/12/section/171) — re-identification offence
- [NHS and social care data: off-shoring and the use of public cloud services](https://digital.nhs.uk/data-and-information/looking-after-information/data-security-and-information-governance/nhs-and-social-care-data-off-shoring-and-the-use-of-public-cloud-services) — NHS England
- [What do we mean by public benefit?](https://www.gov.uk/government/publications/what-do-we-mean-by-public-benefit-evaluating-public-benefit-when-health-and-adult-social-care-data-is-used-for-purposes-beyond-individual-care/what-do-we-mean-by-public-benefit-evaluating-public-benefit-when-health-and-adult-social-care-data-is-used-for-purposes-beyond-individual-care) — National Data Guardian, Dec 2022
- [Data Security and Protection Toolkit](https://digital.nhs.uk/cyber-and-data-security/cyber-security-services/data-security-and-protection-toolkit) — NHS England
- [Information for GP practices (Type 1 opt-outs)](https://digital.nhs.uk/services/national-data-opt-out/information-for-gp-practices) — NHS England
- [ISB 1572 Sensitive Data reference codes](https://isd.digital.nhs.uk/trud/users/guest/filters/0/categories/8/items/97/releases) — NHS TRUD

### Related notes

- [[FITFILE Context Brief — What We Do and How We Link Data Silos]]: what FITFILE does, and where linkage stands
- [[MESH vs DSPT compliance status]]
- [[SoT - Digital Identity]]

### Next action

- **10 minutes:** go down the tables and strike out any constraint you disagree with, and mark the ones you're unsure of. Those become the agenda for your IG lead.