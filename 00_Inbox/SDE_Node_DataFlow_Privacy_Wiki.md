# SDE / FITFILE Node — Data Flows, Privacy Treatment & Ephemerality

> **Status:** Active discussion · **Owner of the open ask:** Leon & Ollie
> **Source:** Email chain compiled 2026-06-02. Duplicated messages have been de-duplicated; canonical version of each message retained.

---

## 1. Why this thread exists

Laura asked the team to **improve the architecture diagrams** so they show, simply and explicitly, *what direct identifiers are needed* and *what privacy treatment happens where*.

The trigger was twofold:

- A conversation about **CUH's** concerns over how identifiable data is **inside the FITFILE Node**.
- A meeting with **WSH**.

The goal: an (admittedly oversimplified, assumption-stated) picture of *how much direct / indirect / non-identifiable data sits in the system at any given point*, to make customer conversations go more smoothly.

Materials in play:

- Simplified SDE architecture diagrams (PPTX, on the EoE SharePoint).
- A detailed **Miro** board that Weronika, Enric and others built up.
- Philip's draft amendments live in **Section 2 (slides 6–10)** of Laura's deck, with a proposed answer to her request in **slides 12 and/or 13**.

This snowballed from "tidy the diagrams" into "nail down the terminology and the processing/storage model" — and finally into a **direct request to Leon & Ollie to specify Node ephemerality precisely** for the documentation (and possibly Confluence). That request is the live item; see §6.

---

## 2. Who's who

| Person | Role / lens in this thread |
|---|---|
| **Laura** | Kicked it off — wants clearer, simpler diagrams. |
| **Philip Russmeyer** | Founder & CEO. Driving alignment; replies in **bold green** inline throughout. |
| **Weronika Jastrzebska** | Product Manager. Diagram semantics (slides 12 & 13). |
| **David Reeves** | Governance / legal lens. Caveats he doesn't yet know the process inside-out. |
| **Enric** | Author of the original "2 environments" processing summary (dates from ~last May). |
| **Robin** | Rewrote Enric's summary into the Technical Solution Detail; **addressed the final ask to Ollie & Leon**. |
| **Gareth** | Referenced re: data-destruction timelines. |
| **Ollie & Leon** | Engineers being asked to clarify Node ephemerality. *(You.)* |
| **Darren, Rehema** | Cc'd for visibility. |

---

## 3. Glossary

| Term | Meaning |
|---|---|
| **SDE** | Secure Data Environment. |
| **FITFILE Node** | FITFILE compute deployed *on-site*, inside the data controller's perimeter, next to the data. |
| **Data Extract (DE)** | An initial extract (Philip's read: close to raw data in the system of record). |
| **MTDE** | Minimally Transformed Data Extract — DE worked further, e.g. by combining tables. |
| **OMOP** | Common data model; data is harmonised into OMOP via an ETL pipeline. |
| **NDOO** | National Data Opt-Out. |
| **PRE** | Downstream environment that receives Project Extracts. *(Acronym not expanded in the thread — see open questions.)* |
| **FQL** | FITFILE Query Language — proprietary abstraction over native SQL. |
| **FITanon / FITtoken** | FITFILE anonymisation / tokenisation routines. |
| **K-anonymity / L-diversity** | Statistical privacy-treatment techniques. |
| **Restricted Terms** | Terms removed at some stage of the pipeline (slide 13 shows removal between MTDE and OMOP). |
| **HIE** | Party whose treatment appears on slide 7. |
| **MinIO** | Object store — raised as a candidate location for transient Node data. |
| **CUH / WSH / NUH / EoE** | Cambridge Univ. Hospitals / West Suffolk / Nottingham Univ. Hospitals / East of England. |

---

## 4. The established processing model ("Where is data processed?")

From **Enric's** summary, rewritten by **Robin** for the Technical Solution Detail. There are **two environments**:

### Native Database Environment *(preferred)*
The primary layer. Anything expressible as a database query runs here:

- Column selection
- Row-level filtering (e.g. age > 60, males)
- Aggregation (average, min, max)
- Anything else that goes in the **QUERY**

Two query interfaces: **native SQL** and **FQL**.

### Node Compute Environment *(fallback)*
Used only when database-native processing is *not reasonably applicable*. A **transient, ephemeral copy** of the relevant data is staged to the Node's local storage for the duration of processing. Handles:

- FITanon / FITtoken generation
- Privacy treatment (K-anonymity, L-diversity, etc.)
- Data profiling
- Small-number suppression

### Federated deployment
FITFILE **seeks to** deploy within the organisational perimeter, as close to the data source as possible — so compute sits next to the data and **nothing moves across network boundaries / outside the data controller's perimeter**.

> ⚠️ **Important caveat from the summary:** a transient copy of the data also exists **within the local database technology regardless of the processing path**, and the ultimate physical support is the same.

---

## 5. Agreed positions / settled claims

- **NDOO is done by both parties.** Data Controllers do NDOO themselves before secondary use, *but* have asked FITFILE to (a) do it for them where they're unsure they're set up, **and/or** (b) act as "belts and braces" — periodically re-checking any data persisted beyond the ~2-week NDOO window. Net: both they *and* FITFILE do it.
- **"Identifiable" language needs tightening.** Agreement that the term is used loosely; prefer the proper legal terms **pseudonymised / anonymised**. Idea: "green" data is genuinely *in the clear* but is **never persisted in that state** — only exists "on the fly" inside the Node for as briefly as possible.
- **"No storage" headline is customer-driven.** Customer conversations suggest it helps to differentiate *temporary processing* from *storage*, hence the "no storage" framing — **though this is contested** (see David, §6A).
- **Pipeline shape:** initial **Data Extract → MTDE** (e.g. by combining tables) **→ OMOP**. Slide 13 shows **Restricted Terms removed between MTDE and OMOP**.

---

## 6. Open questions

### 6A. Terminology & governance — *raised by David*
1. **Where should NDOO sit?** Inconsistent across diagrams: slide 7 places it *before* the FITFILE Node; other slides place it *within* the Node. David's strong preference: do it **Trust-side, before any secondary-use processing**.
2. **"No identifiable data stored in FITFILE Nodes" is questionable** — contradicted by the fact that **NHS Numbers are transferred for NDOO**. Also "identifiable" ≠ "not *directly* identifiable"; data in the Node (before and possibly after treatment) may still be identifiable.
3. **Is ephemeral non-storage really headline-worthy?** David argues it's *merely a security control*. In legal/regulatory/governance terms the key concept is **processing, not storing** — so even ephemeral data is still *processed*, and all the interesting questions remain in play.

### 6B. Diagram semantics — *raised by Weronika (slides 12 & 13)*
1. **DE vs MTDE difference** is unclear from the presentation. Is **Data Extract = raw data in the system of record**? *(Philip: yes, roughly — initial DE worked into MTDE.)*
2. **When are Restricted Terms applied** — in the OMOP ETL pipeline, or before (as HIE put on slide 7)? → *directed to Weronika to decide.*
3. **Query Interface in the SDE FITFILE Node:** Weronika says "we do not have" one. *(Philip pushes back: the SDE Data Manager is supposed to use the SDE Node to interpret PRE queries.)* → **needs reconciling.**
4. **Cohort Validation & Project Extract location:** no indication they happen *inside* the SDE FITFILE Node, with only Project Extracts ending up in PRE. *(Philip: "let's discuss.")*
5. **Add a "local" label** to Project Extract & Cohort Discovery inside the Data Provider node, to make clear it's local exploration within the customer's own perimeter.
6. **The "query" arrow** between SDE Node and Data Provider Node now implies both must exist for the SDE Node to execute a query — whereas previous diagrams linked querying from SDE **directly to data storage** (MTDE / OMOP in the staging site). Risk of misreading.

### 6C. Processing-model confirmations — *asked by Philip*
1. For **any operation** (incl. simply querying a dataset), does the data **temporarily move into the Node, get processed, then get destroyed** (per Gareth's timelines)?
2. Will the **OMOP writeback** in time also apply to **live** data — i.e. run the ETL on a temporary copy of the MTDE in the Node to harmonise, then send harmonised data back?

### 6D. ⭐ THE ASK FOR LEON & OLLIE — Node ephemerality
*Robin attempted a rewrite of Enric's email for the docs; Philip then added questions. Robin is happy to take answers by email or on a call.*

The documentation needs a precise, defensible statement of **how ephemeral Node processing actually is.** Specifically:

1. **Where is data kept while a Node processes it?** Candidate: **MinIO**? Is it **encrypted**?
2. **For how long?** Until the **query plan is complete / deleted / as applicable**.
3. **Is it re-fetched each time the query is run** (rather than persisted between runs)?
4. **How transient is "transient"?** — give a concrete sense of the ephemerality (duration / lifecycle).
5. **How automated is the immediate destruction** of any data copies the Node uses?
6. **Anything else to refresh?** The underlying summary dates from ~last May — what can be augmented with up-to-date granularity to maximise customer comfort?

Robin's proposed sentence shape to aim for:
> *"When data is processed by a Node it is kept in **X** location (MinIO? encrypted?) until the query plan is complete / deleted / as applicable … and is re-fetched each time the query is run."*

Philip's wording nit to resolve on the way through: in "where database-native processing is not reasonably **applicable**", he queried **why "applicable" and not "possible"**.

---

## 7. Loose ends / housekeeping
- Enric's processing summary may **not yet be in Confluence** — Philip suggested filing it there.
- Decide whether the privacy-treatment picture lives in the **WSH slide format**, the **Miro board**, or both.
- Comments must **not** go into the PPT itself (Laura can see them).
