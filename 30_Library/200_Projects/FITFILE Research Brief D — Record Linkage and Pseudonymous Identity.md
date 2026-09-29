---
title: FITFILE Research Brief D — Record Linkage and Pseudonymous Identity
type: source
status: draft
created: '2026-09-28T21:23:00+01:00'
modified: '2026-09-29T08:34:03+01:00'
tags:
- source/llm
- fitfile
- topic/data-linkage
project_name: FITFILE
conformant: false
non_conformance_reason: Raw agent research brief kept as source material for the FITFILE
  context brief; awaiting review, not a canonical source note.
source: FITFILE Confluence, read-only sweep on 2026-09-28 by a Claude Code research
  agent
source_url: null
permalink: llmeon/00-inbox/fitfile-research-briefs/fitfile-research-brief-d-record-linkage-and-pseudonymous-identity
---

%% Raw agent research brief (Claude Code, 2026-09-28), kept as source material for the FITFILE context brief. Not your own writing, so no own_words property. Page IDs link to Confluence. Redacted for the vault where needed: personal names, a prospect's name, page-hygiene and security-debt specifics. %%

Part of: [[FITFILE Context Brief — What We Do and How We Link Data Silos]]

# Brief D: record linkage and pseudonymous identity across datasets, projects and organisations

This is a read-only review of FITFILE Confluence, carried out on 28 September 2026.

- The first citation of a page gives its title (sometimes shortened), ID and last-modified date; later citations give the ID only. Section 6 groups the IDs by space.
- "Inference:" marks my own analysis. People are named by role only.

## 1. Summary

- **Five linkage families appear in the pages:**
  - FITtokens: deterministic HMAC-SHA256 pseudonyms. These are the production route.
  - Salted SHA-256 tokens, scoped to a project.
  - FITanons: non-deterministic zero-knowledge proofs. They grew out of a 2020 proof of concept (POC), are heavily marketed, and are slow at scale.
  - Bloom-filter probabilistic matching, now based on the ONS PPRL toolkit. This is still at POC stage.
  - External pseudonyms, either from NHS-PET or held by a Secure Data Environment (SDE).
- **Deterministic linkage needs a common identifier.** In practice this is the NHS number, carried in OMOP `person_source_value` and tokenised at source for each query (Minimum fields required for linkage, [2155675649](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155675649), 2025-04-22; Demonstration 3A - 14th of May Notes, [2177105921](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2177105921), 2025-05-14).
- **Keys are held centrally.** Each network has one HMAC secret, kept in FITFILE's central Vault. The ZKP curve point G is shared across the network and injected from Vault in the same way (OMOP Flow: Irreversible Pseudonymisation…, [2869297153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2869297153), 2026-06-15; UDE CLI Component, [1834582019](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1834582019), 2024-10-06). Inference: who holds the keys is a bigger open question than which algorithm to use.
- **PPRL outperformed the in-house matcher.** On FEBRL4 it found 99.8% of true matches, against 95.9% for the in-house matcher, and was adopted. It is run from a command-line script (Validation of probabilistic matching tool, [2321645572](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2321645572), 2025-12-24; 2026-04-15 Probabilistic Matching Meeting, [2753789967](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2753789967), 2026-04-16).
- **No page read shows linkage between organisations running on live data.**
  - NWSDE/LCRCA is blocked by LCRCA's information governance (LCRCA - Project Summary (Internal), [2816245762](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2816245762), 2026-09-25).
  - Mersey Care's executive group did not approve its project (Mersey Care - Project Summary (Internal), [2824241153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241153), 2026-09-27).
  - NUH holds no NHS numbers (2026-07-21 NUH In-person Workshop, [2937847809](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2937847809), 2026-08-26).
  - NHS-PET is marked "Done but Unauthorised" (1.8.1 NHS PET Pseudo ID, [2979233793](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2979233793), 2026-08-12).
- **HDRS TT has no linkage method yet.** Its "Federated Linkage" project started on 25 September 2026 and connects four SDEs using synthetic OMOP data (HDRS TT Federated Linkage - Kick-Off Meeting, [3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130), 2026-09-25).
- **The customer-facing comparison page is still a draft.** Its accuracy fields are blank placeholders, and reviewers have flagged contradictions (Comparison of data linkage approaches, [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497), 2026-02-04). Linkage-quality metrics are largely undefined.

## 2. Findings

### 2.1 Deterministic pseudonymous linkage

- **Requirement.** The identifier must be unique across the pipeline and common to every provider. The NHS number goes into `person_source_value` as a direct identifier ([2155675649](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155675649)).
  - NHS numbers pseudonymised before they arrive "would impair" opt-out and re-identification.
  - Linkage across regions awaits national guidance.

  (INTERNAL…Minimum fields required for linkage, [2155315202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155315202), 2025-04-16.)
- **Construction.** A FITtoken is "a simple HMAC hash". It is deterministic, and a record can be re-identified by recomputing it ([1834582019](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1834582019)). A June 2026 draft adds that all nodes in a network share one HMAC-SHA-256 secret. The secret is held in the central Vault, kept in sync when it is rotated, and never exposed. The OMOP workflow offers only "irreversible pseudonymisation" ([2869297153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2869297153)). A comment confirms that an SDE and its trusts share one secret (comment 2480111619, 2025-11-28).
- **Re-identification.** In the 2023 design, tokens are recomputed against source data kept by the provider, so no mapping table is needed. Tokens were not to be shown to end users (Pseudo-anonymisation (Pseudo) + re-identification Implementation, [1590296577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1590296577), 2023-06-30). Rotating the secret breaks re-identification; this was still an open risk in October 2025 (Resolved Risks and Technical Debt, [2202238978](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2202238978), 2025-10-09).
- **Project scoping.** The FAQ recommends SHA-256 with a salt for each project; two datasets hashed with the same salt become linkable (How can we link patient data across projects…, [2211250188](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2211250188), 2025-06-10). Custom Transformations offer project or custom salts. Access to salts is permission-controlled "to prevent unauthorised data linkage" (1.3.3 Custom Transformation Operation, [2208530436](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2208530436), 2025-06-13). WMSDE hashes identifiers with a project key ((Internal) WMSDE Product Development Plan, [2067267585](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2067267585), 2025-07-07).
- **In use.**
  - The EoE demo tokenised NHS numbers at the CUH and NNUH nodes and deduplicated cohort counts. It also contrasted two ways of combining data: merge, which keeps the intersection, and concatenation, which keeps the union ([2177105921](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2177105921); Cohort Concatenation, [2139488258](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2139488258), 2025-04-02).
  - OMOP-workflow tests reproduced the expected overlap between tenants. However, "FITanon linkage is not available" there, and deduplication was missing (19 Feb - OMOP Workflow, [2642149377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2642149377), 2026-02-27).
- **Options considered in 2023** were Merkle trees, accumulators, public-key tokens, and proxy re-encryption through the coordinator (Pseudonymisation Notes, [1591115777](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1591115777), 2023-07-03).

### 2.2 FITanon, ZKP, UDE and PKI

- **2020 POC.** An external contractor built it in about six weeks, with three provider servers and a central server. The aim was matching "without sharing identifying information", with "zero mismatched rows" (ZKP POC Home, [127139970](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=127139970), 2020-10-07; Project Acceptance Criteria, [159744001](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=159744001), 2020-10-07; Project Roadmap, [158728304](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=158728304), 2020-10-23).
- **Method.** It uses a Schnorr non-interactive zero-knowledge proof over Curve25519, made non-interactive with the Fiat–Shamir transform (RFC 8235).
  - The prover sends {r, vG}, derived from its hashed identifier.
  - The verifier recomputes the proof using its own identifier.
  - The shared point G is agreed by elliptic-curve Diffie–Hellman.

  (ZKP component description, [158761006](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=158761006), 2020-10-27; PKI component description, [194838531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=194838531), 2020-12-08.)
- **2021 product: the UDE.** It offered three levels: identifiable, "basic" (random IDs, which cannot be linked) and UDE proofs (which can be linked). There was one common key per network (UDE Decisions/questions, [558071824](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=558071824), 2021-02-02).
- **Scale.** Verification compares every record with every other record.
  - Linking 10k × 10k records took about 17 hours on one replica and 1.1 hours on sixteen (30/09/2022 - UDE Replica Performance Tests, [1459552257](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1459552257), 2022-11-30).
  - The team called it "too slow for more than a few thousand records" (Challenges & Objectives, [1393786903](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1393786903), 2022-06-10).
  - A Bloom-filter pre-filter was proposed (Bloom Filters, [1393721373](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1393721373), 2023-03-06). The team accepted that people "could brute force nhs_numbers" to test membership (UDE Improvements, [1464827905](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1464827905), 2023-03-20).
- **Current positioning.**
  - FITanon is described as a "patented application" of ZKP. It changes on every run and is "not meant for onward linkability" (Technical Overview, [2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026), 2025-04-25).
  - Anonymised linkage is deterministic only (FITFILE Node Component Overview, [2164260868](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164260868), 2025-04-25).
- **Inference, needing cryptographic review.** Any node that holds G can test every possible NHS number against a proof it receives, because there are few enough NHS numbers to try them all. The same is true for anyone holding the HMAC secret and a set of FITtokens.

### 2.3 Probabilistic matching

- **Origin, 2024–25.** A client wanted records like those in the Personal Demographics Service (PDS) linked to unemployment records. Neither side had direct identifiers, the data quality was poor, and the client hoped for at least a 60% match rate. The pages describe two approaches (Probabilistic Matching Method & Implementation, [1924038657](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1924038657), 2025-01-13; On the clear (splink), [2025127937](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2025127937), 2025-01-13; ENCRYPTED DATA, [2025652226](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2025652226), 2025-01-16):
  - matching "in the clear", with Splink-style weights;
  - matching "encrypted" data, using bigram Bloom filters, Hamming distance, LSH blocking and a classifier.

  The in-house matcher, run on 5k × 20k records, had a precision of 0.98. It missed 1,046 matches, a recall of about 79% by my calculation.
- **ONS PPRL toolkit.** It is open source and compares Bloom-filter embeddings, with features that handle name variants. It normally needs a trusted third party; FITFILE's evaluator argued that its nodes remove that need (PPRL toolkit, [2302181378](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2302181378), 2025-09-11).
- **FEBRL4 validation.** PPRL found 99.8% of true matches using all fields, and 96.0% using four. The in-house matcher found 95.9%, but it had been trained on FEBRL4. No false positives were found, though this was checked by eye. On noisier North Carolina Voters data, many records matched several candidates. The decision was to adopt PPRL only ([2321645572](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2321645572)).
- **Delivery, March to May 2026.** A script calls the FITFILE API. Post-processing then produces three result sets, each with a histogram used as a quality signal (Run febrl4 test mimicking customer, [2710732801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2710732801), 2026-04-20; Plots and tables…, [2719252481](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2719252481), 2026-04-20; 2026-04-20 Probabilistic Matching Meeting, [2766864385](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2766864385), 2026-04-27):
  - naive: pairs with probability above 0.6;
  - weighted: a one-to-one assignment using the Hungarian algorithm (recommended);
  - greedy: each record's best match.

  A zero-based row index is "the only link" back to the source data. FITFILE post-processed the outputs ([2753789967](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2753789967)), which ran to several hundred MB for 5,000 records ([2766864385](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2766864385)). NWSDE's synthetic run found 4,612 matches (2026-05-07 NWSDE Project Update, [2798223361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2798223361), 2026-08-21).

### 2.4 External and customer-held pseudonyms

- **NHS-PET.** NHS numbers go out by SFTP, and the Pseudo IDs that come back are mapped onto the data. The UI calls this "External Pseudonymisation" (NHS-PET Integration, [2318106625](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2318106625), 2025-09-30, with comments). It was built for an SDE-to-SDE POC requested by a lead at the Eastern England SDE, and tested in staging on 30 September 2025. It is now blocked because FITFILE's access has expired ([2979233793](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2979233793)).
- **NHS Person_ID.** This is described as a service based on a mapping table, and FITFILE does not know its algorithm ([2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497)).
- **NWSDE.** NWSDE first planned a "rainbow table" of pseudo-IDs against NHS numbers. It then decided to pseudonymise NHS numbers itself before passing them on (2025-11-26 NWSDE technical kick-off, [2472607753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2472607753), 2026-02-04; Configured Solution Design - NWSDE, [2575368202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2575368202), 2026-03-03).

### 2.5 Active projects

- **NWSDE/LCRCA.**
  - The project would link about 40k LCRCA worklessness records to about 600k Cheshire & Merseyside population records. Each match would get a pseudo-ID for mental-health analysis, and only aggregates would be released.
  - LCRCA runs a spoke node and NWSDE the coordinating hub (HLD - NWSDE Probabilistic Data Linkage, [2471034898](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2471034898), 2026-02-03; LLD - Liverpool City Authority Probabilistic Linkage, [2432401409](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2432401409), 2026-04-08).
  - The planned fields were postcode, date of birth, names and gender, with "only hashes of matching fields" leaving the node ([2575368202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2575368202)).
  - LCRCA's governance withheld names, then postcodes. FITFILE warned that "matching accuracy will be low" ([2798223361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2798223361)).
  - As at 25 September 2026, approval to share the file had not been given. NWSDE's DPIA is complete, but its host organisation is changing ([2816245762](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2816245762); NWSDE - Project Summary (Internal), [2778365953](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2778365953), 2026-09-28).
- **Mersey Care.** About 11k HR records would have been matched deterministically on name, date of birth and postcode, using FITanon proofs checked at the NWSDE node. Existing PseudoIDs would then link each match to the long-term conditions register. The trust's executive group did not approve this in May 2026, and FITFILE is waiting to hear whether it will be resubmitted ([2824241153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241153); Configured Solution Design - Mersey Care, [2568847361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2568847361), 2026-02-16).
- **EoE SDE.** NHS-number linkage is called a "key benefit" because it removes duplicate patients and allows them to be re-contacted for trials. At NNUH it was deferred so as not to hold up go-live (2026-01-09 HIE/NNUH weekly meeting, [2563899393](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2563899393), 2026-01-14). NUH's data is anonymised and has no NHS numbers, so linkage is "not currently possible" (2026-08-14 NUH Data meeting, [2990538753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2990538753), 2026-08-18).
- **HDRS TT.** EESDE, NWSDE, WMSDE and SWSDE are working with an industry partner. Phase 1, due by mid-December 2026, needs one query that runs across two SDEs. Contracts, data sharing agreements (DSAs), DPIAs and Data Access Committee (DAC) notices are on the critical path ([3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130); HDRS TT…Project Summary (Internal), [3073245215](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3073245215), 2026-09-25). Inference: the NHS-PET SDE-to-SDE POC is the closest precursor, and the lead who requested it attended the kick-off.

### 2.6 Multi-site mechanics and QA

- **"Federated" setup.** Data stays at source and a coordinating node sends out the queries. Pseudonymised record-level data does, however, move to the SDE (Use Of "Federated" Across the EoE SDE Project, [2016706564](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016706564), 2025-01-02).
- **Coordinator and providers.** The coordinator pulls in the providers' intermediate datasets. Providers cannot see or govern the project (Inter node communication, [2147385345](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2147385345), 2025-04-09). Connections between tenants are set up manually ([2202238978](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2202238978)).
- **QA.** The QA tools check for "correct keys and join types" (…Linkage QA tools v.2.0, [2099871745](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2099871745), 2025-04-30). The uniqueness-validation page is marked "Released", but its links are still placeholders (1.2.1 Validate Patient Identifier Uniqueness, [2201223171](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2201223171), 2025-06-08).

## 3. Glossary

- **FITtoken:** a deterministic, re-identifiable HMAC pseudonym. In the schema it is an "Encoded Identifier" (FITFILE SDE Technical Glossary, [2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881), 2025-02-14; Removal of Direct Identifiers from Query Output, [2028666883](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2028666883), 2025-01-27).
- **FITanon:** a non-deterministic ZKP proof ([2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026)).
- **UDE ("United Data Engine"):** the component that unites, anonymises and joins data (UDE, [499482625](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=499482625), 2021-01-25).
- **G / UDE secret:** the network-shared curve point and HMAC key, injected from Vault ([1834582019](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1834582019); [2869297153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2869297153)).
- **Project salt:** a salt that restricts SHA-256 tokens to one project ([2208530436](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2208530436)).
- **External Pseudonymisation:** keys generated by NHS England's PET service ([2318106625](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2318106625)).
- **PPRL:** privacy-preserving record linkage, done by comparing Bloom-filter encodings ([2302181378](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2302181378)).
- **Merge / Concatenate:** merge joins column-wise and keeps the intersection; concatenate stacks rows and keeps the union ([2139488258](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2139488258)).

## 4. Tensions, contradictions and open questions

1. **Lookup tables.** The comparison page says FITtokens can be "reversed using a lookup table", and also that FITFILE is "not dependent on lookup or mapping tables". A reviewer flagged this. The 2023 design recomputes tokens instead of looking them up ([2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497), with its comments; [1590296577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1590296577)).
2. **Two constructions.** Salted SHA-256 appears in PRODDOCS and Custom Transformations. HMAC-SHA256 appears in the UDE CLI page, the OMOP draft and the HDRS Tech Demo ([2966552577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2966552577), 2026-08-05). No page says which one a FITtoken uses.
3. **"Irreversible".** The OMOP draft says HMAC values cannot be reversed even by someone holding the secret; the UDE CLI page says they can be recreated to re-identify a record. The pages also call tokens "encrypted", although FITFILE has decided internally that the word implies reversibility ([2869297153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2869297153); [1834582019](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1834582019); comment on [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497)). Inference: anyone holding the secret and a list of candidate identifiers can reverse either kind of token.
4. **Claims against evidence.** The comparison page mentions "AES-256 hashing", though AES is a cipher rather than a hash. It leaves its accuracy ranges blank, and it claims NHS-consistent algorithms while admitting the NHS algorithm is unknown ([2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497)).
5. **Custody.** The page claims FITFILE staff cannot access nodes and that no central token store exists. Yet the secret is central and shared across the network, and FITFILE planned to run NWSDE matching as a managed service and post-processed the match files ([2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497); [2869297153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2869297153); [2575368202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2575368202); [2753789967](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2753789967)).
6. **"No data leaves".** The discussion of NWSDE's data processing agreement assumes that no data leaves either organisation. Yet hashes leave LCRCA, and the result files were moved through SharePoint ([2753789967](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2753789967); [2766864385](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2766864385)). Inference: the encodings, and match tables keyed to row indexes, are probably personal data.
7. **Token visibility.** A 2023 requirement says end users should never see tokens, but in the 2025 demo researchers group results by FITtoken ([1590296577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1590296577); [2177105921](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2177105921)).
8. **NWSDE design drift.** The HLD matched ciphers of concatenated fields; later designs use PPRL embeddings. NHS-number handling moved from NWSDE's lookup table to NWSDE pseudonymising the numbers itself. One page says both that FITFILE runs the matching as a managed service and that NWSDE runs the scripts ([2471034898](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2471034898); [2472607753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2472607753); [2575368202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2575368202)).
9. **Weak or stale evidence.** The in-house matcher was trained and tested on the same data. One test run appears to have compared two identical datasets ([2719252481](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2719252481)). Several pages are empty or placeholders: 1.8.0 Linkage, 1.3.2, RQ-1.2.3 and 1.2.1. Two ZKP pages are also empty, and "10 Linking tables with Query plans" contains only a video.

## 5. Relevance to linking data silos

| Approach | Where identifiers and keys live | Who can link or re-identify | Det./Prob. | Status (Sep 2026) | Known limitations | Sources |
|---|---|---|---|---|---|---|
| Identifiable join on a raw key | Raw keys sent to the coordinating node | Project users with the identifiable role | Det. | Built | Identifiers leave the source | [2749792257](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2749792257) |
| FITtoken: HMAC-SHA256 of the NHS number | Data at the provider; one secret per network in FITFILE's Vault | Any node in the network; providers can re-identify. Inference: so can any holder of the secret | Det. | Built; in EoE workflows (live use across sites not shown) | Needs a common unique ID; rotating the secret breaks re-identification. Inference: linkable across the whole network, and the NHS-number space can be enumerated | [1834582019](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1834582019), [2869297153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2869297153), [2202238978](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2202238978) |
| Salted SHA-256 | Salt in the platform, permission-controlled | Anyone with the same salt | Det. | On the SDE node by Nov 2025 | Inference: can be brute-forced if the salt leaks | [2208530436](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2208530436), [2211250188](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2211250188), [2450194433](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2450194433) |
| FITanon: Schnorr ZKP (UDE) | Identifiers at source; G in Vault | Verifying nodes. Inference: also any holder of G | Det. | POC 2020; product 2021–22; demoed 2025; not in the OMOP workflow | Pairwise cost (about 17 h for 10k × 10k); exact matches only | [158761006](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=158761006), [1459552257](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1459552257), [2642149377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2642149377) |
| ZKP plus Bloom pre-filter | As FITanon, plus Bloom bitmaps | As FITanon; membership test by brute force accepted | Det. with Prob. filter | Idea, 2022–23 | Reveals who is present in a dataset | [1393721373](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1393721373), [1464827905](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1464827905) |
| Probabilistic matching in the clear | Both datasets pooled | Whoever holds the pooled data | Prob. | Method note | Moves identifiable data | [2025127937](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2025127937) |
| In-house encrypted matcher | Encodings leave the source | The comparing party; row index | Prob. | Superseded | Recall about 79% | [1924038657](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1924038657) |
| ONS PPRL toolkit workflow | Encodings; the row index is the only link | Each party locally; FITFILE handled the files | Prob. | Synthetic POC done; live use blocked; no UI | Large files moved by hand; weak without names or postcodes | [2321645572](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2321645572), [2753789967](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2753789967), [2798223361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2798223361) |
| NHS-PET Pseudo ID | NHS numbers sent to NHS-PET, a trusted third party | NHS-PET; parties in the same NHS-PET domain | Det. | Built; access lapsed | External credentials | [2318106625](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2318106625), [2979233793](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2979233793) |
| Customer-held pseudonyms | The data controller's key or lookup table | The data controller | Det. | Appears in NWSDE, Mersey Care and WMSDE designs | Blocks FITFILE opt-out handling and re-identification | [2155315202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155315202), [2472607753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2472607753) |
| Deterministic cipher on name, date of birth and postcode | Quasi-identifiers at source | As FITtoken or FITanon | Det. | Designed; not approved | Typos defeat the match | [2471034898](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2471034898), [2568847361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2568847361) |
| Proxy re-encryption via the coordinator | Per-site keys; the coordinator holds re-encryption keys | The coordinator | Det. | 2023 idea | Not pursued | [1591115777](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1591115777) |

**Unresolved design questions**

1. **Key scope.** Should keys belong to the network, the project or the data controller? Who legally holds them, and can a controller revoke linkability?
2. **Cross-SDE identity.** Should HDRS TT use NHS-PET, one shared FITFILE secret, or re-keying between SDEs? It needs an answer before Phase 1.
3. **Probabilistic comparison.** Which party sees the encodings and match tables, and are they personal data?
4. **Minimum identifiers.** What is the smallest set that governance will release, what accuracy follows, and how can quality be estimated without ground truth?
5. **PPRL as a product.** It needs a UI, clerical review, agreed thresholds and manageable file sizes, and it should not depend on FITFILE staff handling files.
6. **FITanon.** Can it scale, and does it protect identities against nodes inside the network?
7. **Tokens over time.** Can secret rotation coexist with longitudinal linkage? Should researchers see tokens at all?
8. **Linkage QA metrics.** Candidates include duplicate tokens, invalid NHS numbers and checks that overlaps are plausible.

## 6. Pages read, and pages found but not read

Pages cited above are listed by ID only; their title and date appear at first citation.

**Read**

- **PRODDOCS:** [2211250188](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2211250188), [2979233793](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2979233793), [2201223171](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2201223171), [2208530436](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2208530436). Also:
  - 1.0.0 FAQ, [2222817288](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2222817288) (2025-06-20)
  - 1.8.0 Linkage, [2979069953](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2979069953) (2026-08-12, empty)
  - RQ-1.2.3, [2351529990](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2351529990) (2025-10-17, stub)
  - 1.3.2, [2217377802](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2217377802) (2025-06-13)
  - RQ-1.1.2, [2208071681](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2208071681) (2025-06-10)
- **FITFILE:** [2612330497](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2612330497), [1924038657](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1924038657), [2025127937](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2025127937), [2025652226](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2025652226), [2302181378](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2302181378), [2710732801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2710732801), [2719252481](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2719252481), [2155675649](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155675649), [2155315202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2155315202), [2321645572](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2321645572), [2318106625](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2318106625), [2099871745](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2099871745), [2139488258](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2139488258), [2016706564](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016706564), [1834582019](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1834582019), [2147385345](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2147385345), [2164097026](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164097026), [2164260868](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2164260868), [2016378881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2016378881), [2966552577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2966552577), [2177105921](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2177105921), [2202238978](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2202238978), [2067267585](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2067267585), [2028666883](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2028666883), [2642149377](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2642149377). Also:
  - Resources, [2720890881](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2720890881) (2026-04-10)
  - Synthetic-data meeting, [2742124549](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2742124549) (2026-04-14)
  - Performing Probabilistic matching, [2747662337](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2747662337) (2026-04-14)
  - NWSDE instructions, [2749792257](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2749792257) (2026-04-29)
  - Multi-site Project, [1729495041](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1729495041) (2024-10-06)
  - 10 Linking tables with Query plans, [2188541966](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2188541966) (2025-05-19, video)
  - CSD Master, [2519433236](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2519433236) (2026-05-06)
  - Health Innovation East Design Document, [1912242177](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1912242177) (2024-11-27)
  - 06.05.2026 notes, [2804449281](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2804449281) (2026-05-14)
  - Stress Testing v1.1.0, [2896068618](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2896068618) (2026-07-10)
  - FFNode test specification, [2876211201](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2876211201) (2026-06-18)
  - Re-identification postmortem, [1740374020](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1740374020) (2024-04-24)
- **NP:** [2471034898](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2471034898), [2432401409](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2432401409), [2753789967](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2753789967), [2766864385](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2766864385), [2575368202](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2575368202), [2568847361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2568847361), [2778365953](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2778365953), [2816245762](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2816245762), [2824241153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2824241153), [2472607753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2472607753), [2798223361](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2798223361). Also:
  - LCRCA HLD, [2417065986](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2417065986) (2026-04-08)
  - Two projects page, [2611576835](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2611576835) (2026-02-04)
  - LCRCA/NWSDE requirements, [2605842433](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2605842433) (2026-02-04)
  - Mersey Care requirements, [2632712194](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2632712194) (2026-02-16)
  - Usability decisions, [2631827457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2631827457) (2026-02-12)
  - LCA kick-off, [2360180760](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2360180760) (2025-11-12)
  - Data discovery, [2507767809](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2507767809) (2025-12-12)
  - Mersey Care update, [2634186753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2634186753) (2026-02-17)
- **HDRSTT:** [3072688130](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3072688130), [3073245215](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3073245215). Also:
  - Space home, [3071738149](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3071738149) (2026-09-25)
  - ST notes, [3071967233](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=3071967233) (2026-09-25)
- **ZKP:** every page in the space was read, last modified October 2020 to March 2023. These are the cited IDs, plus [158728250](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=158728250), [159055953](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=159055953), [159121472](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=159121472), [159121538](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=159121538), [159121545](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=159121545), [159121409](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=159121409) and [160727051](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=160727051). Five were empty or held only media: [1393295371](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1393295371), [159121436](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=159121436), [159055873](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=159055873), [163938305](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=163938305) (PDF) and [194904067](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=194904067) (diagram).
- **PS:** [1591115777](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1591115777), [1590296577](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1590296577), [499482625](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=499482625), [558071824](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=558071824), [1464827905](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1464827905), [1459552257](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1459552257). Also:
  - Matching proofs, [1312489473](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1312489473) (2021-12-09)
  - Common key generation, [753926176](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=753926176) (2021-03-25)
  - PKI & Common Key Generation, [521404444](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=521404444) (2021-03-01)
- **EOE:** [2937847809](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2937847809), [2563899393](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2563899393), [2990538753](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2990538753). Also:
  - CSD NUH, [2788950017](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2788950017) (2026-08-27)
  - Complex Query Plans workshop, [2450194433](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2450194433) (2025-11-20)
  - EE SDE summary, [2829516801](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2829516801) (2026-09-27)
- **Personal space:** [2869297153](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2869297153).
- **Comments:** [2480111619](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2480111619); comment 2254471173 (2025-07-23).

**Found but not read**

- NHS-PET specification, [1601208321](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1601208321) (2023)
- Testing the New PET, [1597800449](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1597800449)
- PS pages on joining and UDE flows: [1338671105](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1338671105), [1338998785](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1338998785), [522027109](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=522027109), [517603359](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=517603359), [1364131855](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1364131855)
- 15 million rows challenges, [1643839489](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=1643839489)
- HIE demo notes, [2123923457](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2123923457)
- Functional Test Plan M3, [2196340737](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2196340737)
- CDH privacy guides: [2629173252](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2629173252), [2431680531](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2431680531)
- NDOO & LDOO discussion, [2786525192](https://fitfile.atlassian.net/wiki/pages/viewpage.action?pageId=2786525192)
- Documents held only in SharePoint