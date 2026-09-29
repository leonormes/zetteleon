---
conformant: false
created: 2026-09-29 11:35:00+01:00
modified: 2026-09-29 11:35:00+01:00
non_conformance_reason: Vault copy of a team-facing problem statement published as
  a claude.ai artifact; agent-drafted and awaiting review, not a canonical project
  note.
project_name: FITFILE
source: Published artifact 'One Question, Many Trusts' (version 1, 2026-09-29), derived
  from the vault note Privacy Constraints on a Cross-Trust Federated Query Network
source_url: https://claude.ai/artifact/JeB7GJyKHpvHsktUpf6MkR
status: draft
tags:
- source/llm
- fitfile
- topic/problem-definition
- topic/privacy
- topic/information-governance
- topic/secure-data-environments
title: One Question, Many Trusts (Problem Statement)
type: project
permalink: llmeon/00-inbox/one-question-many-trusts-problem-statement
---

%% Vault copy of the team-facing problem statement published on 2026-09-29 as a private claude.ai artifact (link in source_url). Agent-drafted, not your own writing, so no own_words property. Anonymised like the published page; the named field evidence lives in the constraints catalogue note. If the page is republished, update this copy too. %%

## One Question, Many Trusts

**Problem statement · Draft for discussion**

What stops us letting an approved researcher ask one question of many NHS organisations' data, stated in privacy and governance terms before we design anything.

*For the FITFILE team · 29 September 2026 · Based on UK law, national NHS guidance and our own project experience · Not legal advice*

- **Published page:** [One Question, Many Trusts](https://claude.ai/artifact/JeB7GJyKHpvHsktUpf6MkR). It is private, so share it from the page's Share menu.
- **Detailed internal version, with named field evidence:** [[Privacy Constraints on a Cross-Trust Federated Query Network]]

### The problem

> [!abstract] Problem statement
> Many independent organisations hold health and care data about the same people. Each one is separately accountable for its data in law, owes its patients a duty of confidence, and applies national rules through its own local policies. Our value comes from combining that data across organisational boundaries. Combining is exactly what the rules restrict: it makes people easier to identify, it moves data from one accountable organisation to another, and it can go beyond what patients expect.
>
> **How might we** let an approved question reach many organisations' data, and bring back only safe answers, in a way every organisation's governance can approve once and keep trusting?

The technology is largely understood. What stalls our projects is governance. Two cross-sector linkage projects passed their synthetic tests and then stopped at partner approval. Every new organisation, project or partner reopens the same questions, one organisation at a time.

### Why the obvious design fails

If the data were public, we would network every site and query the databases directly. Each part of that design runs into a constraint.

| If the data were public, we would | We can't, because |
|---|---|
| Connect every site over the public internet | Data may only be held and moved where national policy and each organisation allow. *(6 Location · 8 Accountability · 11 Every organisation is different)* |
| Query every database in the clear | Each use needs a legal basis, must respect confidentiality and opt-outs, and may reveal only the minimum data to people who need it. *(1 Legal basis · 3 Patient choice · 4 Identifiability · 7 Access)* |
| Join records on names or NHS numbers wherever it's convenient | Linkage must happen inside a secure environment, and re-identifying people without the controller's consent is a criminal offence. *(5 Identity and linkage · 1 Legal basis)* |
| Let one operator run any query for anyone | Each organisation decides who uses its data and for what, and whoever decides purposes becomes accountable for them. *(2 Purpose · 7 Access · 8 Accountability · 9 Transparency)* |
| Send results straight to the researcher | Only checked, aggregated, non-identifiable outputs may leave. *(4 Identifiability · 6 Location)* |
| Set it up once and leave it | Opt-outs, approvals and agreements change, and every organisation's rules differ. *(3 Patient choice · 10 Time · 11 Every organisation is different)* |

### What we've already run into

*From our own projects, with organisations left unnamed.*

- Two projects linking NHS data to council benefits data and to staff HR records passed synthetic tests, then stalled at the partners' governance. One partner withdrew names, then postcodes. The other's executive declined, citing unease about staff data rather than security.
- One provider sends data that is already pseudonymised and has no NHS number, so nobody else can link it or check it against opt-outs.
- Every site in one SDE applies opt-outs differently, and that SDE's protocol expects a fresh opt-out check at every data pull.
- One provider refused to let anything write to its production clinical database, even into an isolated area.
- One data protection impact assessment took three months. A four-SDE programme needs contract changes with three SDEs and a new contract with the fourth before data can flow.
- Small-number suppression thresholds from 1 to 11 appear across our own documents.
- One provider allows extracts only in an afternoon-to-evening window, and it supplies two SDEs.
- In our current design, the means to re-join identities sits with us rather than with the organisations that control the data.

### What a solution must make true

These criteria don't assume any particular design. A design is acceptable only if each organisation can be confident that:

- **S1:** its data is used only for approved purposes, by approved and trained people.
- **S2:** record-level data about its patients stays under its control, and anyone who sees data sees only as much, and only as identifiable, as their role and approval allow.
- **S3:** its patients' opt-outs and objections are honoured at every hand-off, using current information.
- **S4:** nobody can re-identify or re-link its patients unless it has authorised that, for that purpose, for that period.
- **S5:** anything combined with other organisations' data is assessed and released on the combined risk, under the strictest rule that applies.
- **S6:** every access, query and release can be traced to a person, a purpose and an approval.
- **S7:** it can see, approve, pause or withdraw its participation at any time.
- **S8:** patients and the public can see what is being done with the data, and why.

For the network as a whole:

- **S9:** a new organisation, project or partner joins by varying agreements everyone already understands, rather than by starting again.

### The constraints

There are twelve families of constraint. Each is labelled by how negotiable it is:

| Label | Meaning |
|---|---|
| **Law** | Statute or common law. Fixed. |
| **Policy** | National NHS and government policy for secure data environments. Fixed, apart from defined exceptions. |
| **Local** | Set by each trust or SDE. Varies, and is negotiated one organisation at a time. |
| **Trust** | Public confidence. Not written down, but binding in practice. |

#### 1. Legal basis

*The right to use the data at all.* · **Law**

| # | Constraint | Source |
|---|---|---|
| 1.1 | Every use has to pass two separate tests, and passing one doesn't pass the other. Data protection law needs a lawful basis plus an extra condition for health data. The common law duty of confidentiality needs consent, s251 support or a legal requirement, unless the data is genuinely anonymised. | UK GDPR Arts 6 and 9 · HRA |
| 1.2 | Using identifiable data for research without consent needs s251 support from the Confidentiality Advisory Group, for that specific activity. | NHS Act 2006 s251 · COPI Regulations 2002 |
| 1.3 | Consented data may be used only within the scope of the consent. Broad consent to an area of research is now lawful. | Data (Use and Access) Act 2025 |
| 1.4 | Research must not be likely to cause substantial damage or distress. It must not drive decisions about particular people unless it is ethics-approved medical research. | UK GDPR research safeguards |
| 1.5 | Research needs ethics approval, either per project or under the SDE's research-database approval, which lasts five years at a time. | HRA |
| 1.6 | Data from outside the NHS (councils, DWP, employers, national registers) needs its own legal route. NHS routes don't cover it automatically. | Each data controller |

#### 2. Purpose

*Why the data is being used.* · **Law · Policy**

| # | Constraint | Source |
|---|---|---|
| 2.1 | Every query traces back to a specific approved purpose, such as an access request approved by the SDE's Data Access Committee. Open-ended querying isn't allowed. | UK GDPR purpose limitation · Caldicott principle 1 |
| 2.2 | Data is used for public good only, never for marketing or insurance, and its public benefit is evaluated explicitly. | SDE policy guideline 11 · National Data Guardian |
| 2.3 | Commercial research is allowed, but NHS organisations keep the decision on access. NHS data can't be hosted solely by a commercial or academic organisation. | Data (Use and Access) Act 2025 · DHSC data access policy |
| 2.4 | Re-contacting patients is a new purpose, with its own route. | Common law confidentiality · Opt-out policy |
| 2.5 | Continuing uses are reviewed regularly. | Caldicott principle 1 |

#### 3. Patient choice

*Opt-outs and objections.* · **Policy · Local**

| # | Constraint | Source |
|---|---|---|
| 3.1 | The national data opt-out is applied wherever it is in scope, and all SDEs are expected to comply. | National data opt-out policy · DHSC data access policy |
| 3.2 | The opt-out is applied at each disclosure, using a check no more than 20 days old (13 days with a local copy refreshed weekly). Whole records are removed, and the opt-out is applied again at every onward disclosure. | Opt-out policy, section 8 |
| 3.3 | The opt-out doesn't apply to anonymised or aggregate data, or where people have consented. So where pseudonymised ends and anonymised begins decides whether it applies at all. | Opt-out policy |
| 3.4 | Opt-out lists are only for applying opt-outs, never for choosing people for research. | Opt-out policy, section 8 |
| 3.5 | GP-level (Type 1) objections still apply to GP data. Local and programme-specific opt-outs vary by organisation. | NHS England |
| 3.6 | People keep their rights, such as access and objection, unless a research exemption is properly relied on. | UK GDPR · Data Protection Act 2018 |

#### 4. Identifiability

*What anyone may see.* · **Law · Policy · Local**

| # | Constraint | Source |
|---|---|---|
| 4.1 | Only the minimum data each purpose needs is used. | Caldicott principles 2 and 3 · Data minimisation |
| 4.2 | People using a secure data environment see only de-identified data. Identifiable data isn't handed out. | SDE policy guideline 7 |
| 4.3 | Pseudonymised data is personal data for anyone who can re-identify it, and may be anonymous for someone who can't. The same dataset's status depends on who holds it. | ICO pseudonymisation guidance |
| 4.4 | Anonymity is judged against a motivated intruder and what else that person could reach. Data released for limited access counts as anonymised only with extra controls. | ICO anonymisation guidance · Opt-out policy |
| 4.5 | Linking adds detail about each person, so the risk is judged on the linked result, not on each source separately. | ICO identifiability principles |
| 4.6 | Everything that leaves is checked, aggregated and non-identifiable, with small numbers suppressed. Repeated queries count towards the risk too. | SDE policy guideline 12 |
| 4.7 | Some categories carry special restrictions (for example IVF, sexually transmitted infections and gender recognition), and each trust keeps its own restricted-code list. | ISB 1572 Sensitive Data · Gender Recognition Act 2004 |
| 4.8 | Free text, genomics, images, rare conditions and small populations are hard to de-identify. | ICO anonymisation guidance |

#### 5. Identity and linkage

*Recognising the same person in different places.* · **Law · Policy**

| # | Constraint | Source |
|---|---|---|
| 5.1 | No common identifier spans the silos. The NHS number exists only in NHS data, and some providers release no direct identifier at all. | Project experience |
| 5.2 | Linkage happens inside the secure environment, carried out by qualified people. | SDE policy guideline 8 |
| 5.3 | Re-identifying de-identified data without the controller's consent is a criminal offence. | Data Protection Act 2018 s171 |
| 5.4 | Whoever holds the means to reverse pseudonyms holds personal data, and must keep those means separate and secure. | ICO pseudonymisation guidance |
| 5.5 | Pseudonyms should let datasets be linked only as far as an approval allows. | NHS practice |
| 5.6 | A wrong link attaches someone else's data to a person, so the quality of linkage must be demonstrated. | UK GDPR accuracy principle |
| 5.7 | A linked dataset is a new dataset, with its own approvals, retention and opt-out handling. | UK GDPR Art 35 · Opt-out policy |
| 5.8 | The party matching identifiers usually shouldn't see clinical content. This needs confirming with IG. | Common approval condition, to be verified |

#### 6. Location and movement

*Where data may be held, and where it may go.* · **Law · Policy · Local**

| # | Constraint | Source |
|---|---|---|
| 6.1 | Researchers come to the data. Record-level data stays in the secure environment and only approved outputs leave. | SDE policy guidelines 1 and 12 · DHSC data access policy |
| 6.2 | Moving record-level data between organisations is a disclosure. That includes intermediate results gathered during a federated query. | Common law confidentiality · UK GDPR |
| 6.3 | Data may be hosted only in the UK, the EEA or countries the UK recognises as adequate. Anything outside the UK needs sign-off from the organisation's senior information risk owner and a risk assessment. | NHS off-shoring and public cloud guidance |
| 6.4 | Moving UK patient data abroad needs a lawful transfer, so multinational studies should expect analysis to happen in each country. | UK GDPR Chapter V |
| 6.5 | Each trust decides where its data may be hosted and what may connect to, or write to, its systems. | Local policy and risk appetite |
| 6.6 | Data has appropriate security wherever it is held or moved. | UK GDPR Art 32 |

#### 7. Access

*Who may see what.* · **Law · Policy**

| # | Constraint | Source |
|---|---|---|
| 7.1 | Only verified, trained and authorised users get access, and only for approved purposes. | SDE policy guideline 5 · Caldicott principles 4 and 5 |
| 7.2 | Suppliers, us included, act only on each controller's instructions, and their staff get access only where they need it. | UK GDPR Arts 28 and 29 |
| 7.3 | Each controller decides access and releases, through the SDE's Data Access Committee. | DHSC data access policy |
| 7.4 | Every access, query and release can be attributed to someone and audited. | UK GDPR accountability · DSPT |

#### 8. Accountability

*Who answers for what.* · **Law · Policy**

| # | Constraint | Source |
|---|---|---|
| 8.1 | Every trust is independently accountable, with its own data protection officer, Caldicott Guardian and senior information risk owner. There is no single sign-off for the network. | UK GDPR |
| 8.2 | A party that decides purposes or methods risks becoming jointly accountable for them. | UK GDPR Art 26 |
| 8.3 | A chain of agreements (processing, sharing and access) has to change whenever a party or purpose changes. | UK GDPR Art 28 |
| 8.4 | Each controller needs its own data protection impact assessment. | UK GDPR Art 35 |
| 8.5 | Data Security and Protection Toolkit assurance is needed every year (by 30 June), along with SDE accreditation. | DSPT · SDE policy guideline 2 |
| 8.6 | Records of processing are kept, and breaches are notified within 72 hours. Freedom of Information applies to NHS-controlled SDEs. | UK GDPR Arts 30 and 33 · DHSC data access policy |

#### 9. Transparency

*No surprises for patients.* · **Law · Policy · Trust**

| # | Constraint | Source |
|---|---|---|
| 9.1 | Privacy notices describe the network's processing, and SDEs publish who uses data and why. | Caldicott principle 8 · SDE policy guideline 4 |
| 9.2 | Patients and the public take part in decisions about access. | SDE policy guideline 6 |
| 9.3 | Where telling each person individually is impractical for research, the information is published instead. | Data (Use and Access) Act 2025 |
| 9.4 | Public trust can be withdrawn at scale. care.data closed in 2016, and the 2021 GP data programme was paused after a surge in opt-outs. Commercial involvement draws extra scrutiny. | National Data Guardian public-benefit guidance |

#### 10. Time

*Nothing stays settled.* · **Law · Policy**

| # | Constraint | Source |
|---|---|---|
| 10.1 | Identifiable and linked data is kept only as long as it's needed. | UK GDPR storage limitation |
| 10.2 | Opt-outs, approvals and agreements change or expire, so data that's held gets checked again. | Opt-out policy · HRA |
| 10.3 | The ability to re-identify people doesn't outlast the authorisation for it. | Follows from 5.3 and 5.4 |

#### 11. Every organisation is different

*National rules, local interpretations.* · **Local**

| # | Constraint | Source |
|---|---|---|
| 11.1 | Suppression thresholds, restricted codes, which identifiers can leave, opt-out handling, how often data is refreshed, query windows, hosting and approval timescales all vary from trust to trust. | Local policy |
| 11.2 | In a combined output, the strictest contributor's rule effectively governs. | Follows from 8.1 |
| 11.3 | Taking part is voluntary. A provider has to see value, and can decline or withdraw. | Project experience |
| 11.4 | Data can sit under several regimes at once. A query across SDEs needs each SDE's Data Access Committee to approve it, unless they recognise each other's approvals. | DHSC data access policy (regional committees) |

#### 12. Special populations and data

*Extra rules for some people and some data.* · **Law · Trust**

| # | Constraint | Source |
|---|---|---|
| 12.1 | Children and young people need extra protection, and suitable consent or assent. | UK GDPR |
| 12.2 | Staff data carries the power imbalance between employer and employee. | UK GDPR · Project experience |
| 12.3 | The duty of confidentiality continues after death, even though UK GDPR no longer applies. | NHS confidentiality guidance |
| 12.4 | Genetic data identifies people and also their relatives. | UK GDPR Art 9 |

### Out of scope for this statement

- Choosing the technology or architecture.
- Sharing data for direct care.
- Replacing trust or SDE governance. The aim is to make approval easier, while the decisions stay with trusts and SDEs.
- Final legal interpretation, which belongs to information governance leads and data protection officers.

### Questions to settle with information governance first

1. **Decide first.** When a federated query brings pseudonymised record-level results into the SDE, is that a disclosure of confidential patient information, which would need s251 support and the opt-out? Or is the data anonymised once the SDE holds it? Most of the design depends on this answer.
2. Who is accountable for the linked dataset and the outputs: each trust, the SDE lead, or all of them jointly?
3. Who applies the opt-out at each hand-off: trust to SDE, SDE to SDE, and SDE to researcher?
4. Who may hold the means to re-identify or re-link people, on whose authority, and for how long?
5. For a query across several SDEs, whose Data Access Committee approves it?
6. What legal route lets council, DWP or employer data join NHS data?
7. Whose suppression and restricted-code rules govern an output built from several trusts' data?

**Next step:** each lead reads this and flags any constraint they disagree with or aren't sure about. The uncertain ones become the agenda for information governance, starting with question 1.

### Sources

- [The Caldicott Principles](https://www.gov.uk/government/publications/the-caldicott-principles) · National Data Guardian, December 2020
- [Secure data environment policy guidelines](https://www.gov.uk/government/publications/secure-data-environment-policy-guidelines/secure-data-environment-for-nhs-health-and-social-care-data-policy-guidelines) · DHSC, December 2022
- [Data access policy update](https://www.gov.uk/government/publications/data-access-policy-update/data-access-policy-update) · DHSC, October 2023
- [National data opt-out: applying the opt-out](https://digital.nhs.uk/services/national-data-opt-out/operational-policy-guidance-document/applying-the-national-data-opt-out) · NHS England
- [National data opt-out: information for research organisations](https://www.hra.nhs.uk/about-us/committees-and-services/confidentiality-advisory-group/national-data-opt-out-supplementary-information-for-research-organisations/) · Health Research Authority
- [Confidential patient information and s251](https://www.hra.nhs.uk/about-us/committees-and-services/confidentiality-advisory-group/confidential-patient-information-and-regulations/) · Health Research Authority
- [Research tissue banks and research databases](https://www.hra.nhs.uk/planning-and-improving-research/policies-standards-legislation/research-tissue-banks-and-research-databases/) · Health Research Authority
- [Pseudonymisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/pseudonymisation/) and [anonymisation](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-sharing/anonymisation/) guidance · ICO
- [Research safeguards](https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/the-research-provisions/what-are-the-appropriate-safeguards/) · ICO
- [Data (Use and Access) Act 2025: data protection changes](https://ico.org.uk/about-the-ico/what-we-do/legislation-we-cover/data-use-and-access-act-2025/the-data-use-and-access-act-2025-duaa-summary-of-the-changes/data-protection/) · ICO
- [Data Protection Act 2018, section 171](https://www.legislation.gov.uk/ukpga/2018/12/section/171) · Re-identification offence
- [Off-shoring and the use of public cloud services](https://digital.nhs.uk/data-and-information/looking-after-information/data-security-and-information-governance/nhs-and-social-care-data-off-shoring-and-the-use-of-public-cloud-services) · NHS England
- [What do we mean by public benefit?](https://www.gov.uk/government/publications/what-do-we-mean-by-public-benefit-evaluating-public-benefit-when-health-and-adult-social-care-data-is-used-for-purposes-beyond-individual-care/what-do-we-mean-by-public-benefit-evaluating-public-benefit-when-health-and-adult-social-care-data-is-used-for-purposes-beyond-individual-care) · National Data Guardian, December 2022
- [Data Security and Protection Toolkit](https://digital.nhs.uk/cyber-and-data-security/cyber-security-services/data-security-and-protection-toolkit) · NHS England
- [Type 1 opt-outs: information for GP practices](https://digital.nhs.uk/services/national-data-opt-out/information-for-gp-practices) · NHS England

*Drafted with Claude from UK legislation and guidance from NHS England, DHSC, the National Data Guardian, the Health Research Authority and the ICO, checked on 29 September 2026, and from FITFILE project documentation. This is a draft for discussion, not legal advice. Information governance leads should confirm the interpretations, especially question 1.*

### Related notes

- [[Privacy Constraints on a Cross-Trust Federated Query Network]]: the detailed catalogue, with named field evidence and IG questions
- [[FITFILE Context Brief — What We Do and How We Link Data Silos]]: what FITFILE does, and where linkage stands