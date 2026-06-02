---
title: FITFILE Node — Data Processing, Privacy Treatment & Architecture Diagrams
created: 2026-06-02T10:51:00+00:00
source: pieces-ltm
pieces_ids:
  - b2cfd536-ad7f-4561-bada-86c7f9d4d5e0
  - 66a5cedf-bdf5-4ad6-a802-77244634444e
  - 98b9c075-5a51-4801-9614-0ce4eada14b5
tags: [raw, pieces]
---

## Asset 1 (Pieces: b2cfd536-ad7f-4561-bada-86c7f9d4d5e0)

## FITFILE Node — Data Processing, Privacy Treatment & Architecture Diagrams

**Wiki page synthesised from email chain (oldest → newest). Duplicated emails have been collapsed. The final section captures the open questions directed at Leon and Ollie.**

---

## Background & Trigger

**Laura** (EoE/EaHSN) raised a concern after meetings with CUH and WSH: the existing architecture diagrams do not make sufficiently clear (a) what direct identifiers are present in the system at any point, and (b) where each privacy treatment is applied. She linked to EoE's simplified SDE architecture deck as a starting point.

**Philip** reviewed the deck, found issues with how FITFILE Node data storage is depicted and the ambiguity of the "OMOP and Data Extract" arrows. He drafted amendments (Slides 6–13) and a parallel Miro diagram, then circulated both for feedback ahead of a Monday noon deadline to respond to Laura.

**Key artefacts in play:**

- PowerPoint deck (EaHSN SharePoint): [200502_Simplfied_SDE_architecture_diagrams - Copy.pptx](https://eahsn.sharepoint.com/:p:/r/sites/EoESub-NationSDEWP2-12_DataHarmonisation2/Shared%20Documents/12_Data%20Harmonisation/06_DataProvider_info_pack/20250502_Simplfied_SDE_architecture_diagrams%20-%20Copy.pptx?d=w47c9b8af49f546c5b4c9a1d77f91ce32&csf=1&web=1&e=FS2KsX)
- Miro detailed diagram: [miro.com/app/board/uXjVI50q-Wc=/?share_link_id=175974256305](https://miro.com/app/board/uXjVI50q-Wc=/?share_link_id=175974256305)
- Original Miro working board: [miro.com/app/board/uXjVIBT7wpc=/](https://miro.com/app/board/uXjVIBT7wpc=/)

---

## Participants

| Name | Role / Organisation |
|---|---|
| **Philip Russmeyer** | Founder & CEO, FITFILE |
| **Weronika Jastrzebska** | Product Manager, FITFILE |
| **Enric** | Technical lead (authored the original processing summary) |
| **Robin** | Authored the formalised rewrite of Enric's summary |
| **David Reeves** | Governance / compliance perspective |
| **Laura** | EoE / EaHSN — data harmonisation workstream |
| **Gareth** | Referenced in relation to data destruction timelines (not directly quoted) |
| **Leon & Ollie** | Technical team — see open questions section |
| **Darren, Rehema** | CC'd on Robin's rewrite for visibility |

---

## Established Technical Claims

### Processing Environments (Enric → formalised by Robin)

There are two processing environments. The principle is to use native database processing wherever possible and fall back to Node compute only when necessary.

**Native Database Environment (e.g. PostgreSQL)**

All operations expressible as database queries execute here. No data movement is required. This covers:

- Column selection
- Row-level filtering (e.g. age thresholds, demographic attributes)
- Aggregation (average, min, max)
- Any query expressed in native SQL or **FQL** (FITFILE Query Language)

**FITFILE Node Compute Environment**

Used only where database-native processing is not reasonably applicable. A **transient, ephemeral copy** of the relevant data is staged to the Node's local storage for the duration of processing. Operations handled here include:

- FITanon and FITtoken generation
- Privacy treatment (K-anonymity, L-diversity, and related methods)
- Data profiling
- Small number suppression

**Federated Deployment Model**

FITFILE seeks to deploy within the organisational perimeter, as close to the data source as possible. This means the Node compute environment is physically adjacent to the data — eliminating the need for data movement across network boundaries. The transient copy produced during Node compute processing normally resides on the same physical infrastructure as the source database.

> Note from Robin's draft: a transient copy of the data also exists within the local database technology regardless of the processing path taken.

---

### NDOO (National Data Opt-Out) — Agreed Position

Philip clarified the dual-layer NDOO approach after David raised inconsistency in the diagrams:

- **Data Controllers** are expected to perform NDOO themselves before any secondary use.
- **FITFILE** also performs NDOO as a "belts and braces" check — either because the Trust is unsure of their own setup, or to periodically re-check any persisted data that falls beyond the approximately 2-week NDOO window.
- **Both parties therefore do it.** The inconsistency across slides (NDOO before the FITFILE node on Slide 7 vs. within the Node on other slides) should reflect this dual-layer reality.

---

### Data Language & Legal Terminology (David's Governance Points)

David raised three substantive points that have been broadly accepted:

1. **"No identifiable data stored in FITFILE Nodes" is inaccurate** — NHS Numbers *are* transferred for NDOO purposes, which contradicts the claim directly.
2. **"Identifiable" ≠ "not directly identifiable"** — data in the Node, prior to (and possibly after) privacy treatment, can still be identifiable. The correct legal terminology is **pseudonymised** or **anonymised**, not a blanket "identifiable/not identifiable" binary.
3. **Processing vs. storing** — even if data is only stored ephemerally, it is still *processed*. In legal, regulatory, and governance terms the key concept is *processing*, not *storing*. The "no storage" headline is a useful security control but it must not be presented as if it resolves the governance and legal questions, which remain in play regardless.

**Philip's agreed position:** "Green" data (genuinely in the clear) should not be persisted any longer than absolutely necessary and should only exist "on the fly" inside the Node.

---

## Diagram-Specific Issues

### Slide 12 — Data Flows and Privacy Treatment

| Issue | Raised by | Status |
|---|---|---|
| Difference between "Data Extract" and "MTDE" (Minimally Transformed Data Extract) is unclear from the diagram alone | Weronika | Philip clarified: Data Extract is the initial raw pull; MTDE is produced by combining tables. **Open:** When should Restricted Terms be applied — in the OMOP ETL pipeline or before it (as HIE showed on Slide 7)? Directed at Weronika. |
| Restricted Terms are shown being removed between MTDE and OMOP on Slide 13 — inconsistent with Slide 12 | Weronika | Needs reconciling with the above |
| SDE FITFILE Node has no Query Interface shown | Weronika | Philip pushed back: SDE Data Manager *is* supposed to use the SDE Node to interpret PRE queries — this needs clarifying |
| Cohort Validation and Project Extract not shown as happening inside the SDE FITFILE Node; only Project Extracts shown reaching PRE | Weronika | Philip: "Let's discuss" — unresolved |

### Slide 13 — Data Flows and Privacy Treatment

| Issue | Raised by | Status |
|---|---|---|
| Project Extract and Cohort Discovery shown inside the FITFILE Data Provider node without a "local" label — risks implying external access | Weronika | Philip agreed to think about presentation and discuss |
| Arrow labelled "query" between SDE Node and Data Provider Node implies the Data Provider Node *must exist* for the SDE Node to execute a query — inconsistent with previous diagrams where querying linked SDE directly to MTDE/OMOP databases in the staging site | Weronika | Acknowledged by Philip — flagged as potentially confusing; not yet resolved in diagrams |

### Philip's Key Architectural Question (unresolved)

> "Does a FITFILE Node take a temporary copy of identifiable data into itself in order to e.g. do a count, to execute The Hyve code, or to privacy treat it — **or** are the processing instructions from the Node executed on the dataset *in situ* outside of the Node?"

Philip explicitly stated he is *not* asking about Project Extract flows (where ephemeral in-flight storage is understood). This is about standard query/processing operations. **No answer is on record in this chain.**

---

## Robin's Rewrite — Status

Robin produced a formalised version of Enric's technical summary intended for the **Technical Solution Detail** document and for use in the NUH call if the "where is data processed?" question arises.

Philip accepted it with minor tweaks (described as "bold green" edits, not visible in plain text). Philip also flagged one editorial note Robin had raised:

> Robin queried: why "applicable" rather than "possible" in the Node Compute section — *why is 'not reasonably applicable' preferred over 'not reasonably possible'?* This is unresolved.

Philip then asked three further questions of the technical team (see next section).

---

## ❓ Open Questions — For Leon & Ollie

Robin has escalated the following directly to you both:

> *"I'm being asked to clarify data ephemerality during Node processing. I attempted a rewrite of Enric's email so that it can be included in our documentation and Philip has some questions. I'm happy to take answers over email but a conversation might be easier. I think that an inclusion such as: 'when data is processed by a Node it is kept in **X location** (MinIO? encrypted?) until the query plan is complete / deleted / as applicable… and is **re-fetched each time the query is run**' would work well."*

The specific technical questions to answer are:

### From Robin
1. **Where is the transient data copy stored during Node processing?** (e.g. MinIO? Is it encrypted at rest?)
2. **Until when is it retained?** (Until query plan is complete? Until explicitly deleted? Other?)
3. **Is it re-fetched fresh each time the query is run**, or can it persist across runs?

### From Philip (directed at the technical team via Robin)
4. **How transient is "transient"?** Can we give a concrete time window or benchmark to convey a meaningful sense of ephemerality to external stakeholders?
5. **How automated is the destruction** of any data copies used by the Node once processing is complete?
6. **Is there anything else in Robin's rewrite that can be updated with current detail?** Philip noted that Enric's original document dates from last May and may be stale.

---

## Suggested Next Steps

- [ ] **Leon / Ollie** — answer the six questions above (email or call, per Robin's preference)
- [ ] **Philip / Weronika** — reconcile NDOO positioning across Slides 7, 12, 13
- [ ] **Weronika** — clarify when Restricted Terms should be applied (OMOP ETL stage or earlier)
- [ ] **Philip** — confirm whether diagram query-interface/SDE Node issue on Slide 12 is resolved post-call with Weronika
- [ ] **Robin / Philip** — finalise the Technical Solution Detail wording once Leon/Ollie answer above; file in Confluence
- [ ] **All** — agree on consistent language throughout all diagrams: use **pseudonymised / anonymised** rather than "identifiable / not identifiable" framing, per David's guidance

## Asset 2 (Pieces: 66a5cedf-bdf5-4ad6-a802-77244634444e)

User prompt: "this is a chain of emails. I copied and pasted them to a md file. I think they are duplicated. I put them in order so that the top entry is the oldest. There is a question at the bottom for Leon and Ollie (Me and Ollie). Go through the chain, pull out all the relevant claims and questions and create a clean and clear wiki page of what is going on and any open questions"

## Asset 3 (Pieces: 98b9c075-5a51-4801-9614-0ce4eada14b5)

Agent working note: "The user wants me to go through this email chain, identify all relevant claims and questions, deduplicate the content (since they mentioned it's duplicated), and create a clean wiki page. There's also a final question directed at Leon and Ollie (the user is Ollie/Leon based on the query - 'Me and Ollie')."
