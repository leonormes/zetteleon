---
created: 2026-04-17T06:56:43+00:00
modified: 2026-06-08T11:49:16+00:00
project_category: omop
project_name: "OMOP"
project_status: active
title: Expanded Analysis OMOP Synthetic Data Generation Project
type: project
---

Based on your long-term memory, I can see this project has evolved significantly from your initial vision of high-fidelity clinical data to a more pragmatic "fit-for-purpose" approach. Here's an expanded breakdown with context from your discussions:

---

## Questions and Deliberations—Expanded Context

### Do We Need Realistic Data?

This is the central tension in your project. Your LTM shows you initially advocated for clinical fidelity using tools like NHSSynth or SynthVAE to ensure synthetic data "behaves like real NHS primary care records." However, Ollie Rushton (around 2:00 PM–3:00 PM on April 16th) stated: _"Sounds like we only need realistic overlap in cohorts - not realistic data."_

The Trade-off:

- Your Position (Fidelity): Clinically accurate data ensures the pipeline properly exercises algorithmic tracing, name normalization, and linkage edge cases—especially the ~20,000 records requiring Algorithmic tracing seen in real 2021/2022 HES data.
- Team Position (Speed): The priority is infrastructure stress-testing and DAR workflow validation, not epidemiological research accuracy. As long as cohort overlap patterns are realistic (70-85% single-trust, 15-30% multi-trust, 5-10% complex multi-site), the data serves its purpose.

Implications:

- If you skip fidelity validation, you risk Type 1 errors (the pipeline handles "clean" synthetic data but fails on real-world messiness).
- You won't be able to validate the MatchedConfidencePercentage thresholds used by the MPS logic.

---

### Should Realistic Scenarios Be Required for Stress Testing?

Your LTM reveals two competing definitions of "stress testing":

1. Infrastructure Stress (Team's Focus): Can the system handle 12 billion clinical rows and ~30 TiB of storage? This doesn't require clinical realism—it requires volume.
2. Algorithmic Stress (Your Focus): Can the linkage logic handle patients with:
   - Missing NHS numbers?
   - Superseded identifiers?
   - Name variations ("Jon" → "Johnny")?
   - Typos in postcodes or DOB?

Evidence from LTM:

On April 16th at 10:06 AM, you received guidance that "Algorithmic tracing is computationally expensive" and that generating records that fail Cross-check is necessary to validate the MPS architecture. This suggests realistic scenarios are required—but the team may not have prioritized them.

---

### Should there Be Separate Databases for More Realistic Performance?

This question appears repeatedly in your Miro board discussions. The context:

- 5 nodes in the SDE network by year-end
- Each data provider has 1M–3M patients
- Patient distribution: 70-85% use one main trust; 15-30% interact with 2+ trusts

The Dilemma:

- One Large Dataset (30 TiB): Easier to manage but doesn't test multi-node query federation or reflect real-world data silos (GP systems, A&E, Mental Health).
- Multiple Smaller Datasets: More realistic for testing the FITFILE application's ability to "select multiple data providers" and handle distributed queries, but increases orchestration complexity.

Unresolved in LTM:

You asked: _"When does the OMOP flow break regarding node/database count and dataset sizes?"_ This appears unanswered, and there's uncertainty about whether The Hyve or your team owns DBA-level specs for each node.

---

### Is Creating One Large Dataset a Good Idea, or Would Multiple Smaller Sets Be Better and More Agile?

This is directly tied to the "separated by Nodes" question. Your LTM shows:

Arguments for Multiple Datasets:

- Mirrors real SDE architecture (5 nodes = 5 databases)
- Tests cross-node linkage using `Token_Person_ID`
- Validates UI's "high volume query warnings" when selecting multiple sites
- Allows incremental deployment (1M patient pilot → 12M full scale)

Arguments for One Large Dataset:

- Faster generation (30 workers, parallel processing)
- Simpler RAP pipeline (single Kedro DAG)
- Easier to achieve the 60 TiB total footprint estimate (raw + OMOP)
- Reduces risk of "run failure recovery" during the 280-hour generation run

Your Team's Likely Decision (from LTM):

The focus on "ability to test new DARs from clients" and "cohort filtering, selection, and linkage considering volume and number of sites" suggests they're leaning toward node separation to validate multi-site workflows—but this may not have been formalized.

---

## Claims and Strategic Rationale—Critical Analysis

### "Synthetic Data Moves from Theory to Practicality and Identifies Edge cases"

Robin Mofakham's statement (April 16th, 2:00 PM–3:00 PM) is correct, but there's a hidden assumption: edge cases only emerge if the data intentionally creates them.

Your LTM shows you advocated for:

- Name normalization logic (mapping "Jon" to "Johnny")
- Introduced typos and missing NHS numbers via data degradation layers
- Sensitive/Legacy Sensitive flags

If the team skipped these features for speed, the synthetic data won't reveal edge cases—it will only test the "happy path."

---

### "Infrastructure Scalability: ~30 TiB Data Processing Identifies Hardware bottlenecks"

This is the team's strongest justification for prioritizing speed over fidelity. However, your LTM raises an important nuance:

From April 16th, 9:58 AM:

- Raw FHIR: 26.4 TiB
- Parquet compression: ~2 TiB (13x reduction)
- Total footprint (raw + OMOP): ~60 TiB

The Bottleneck Question:

Is the bottleneck in generation (280-hour run) or transformation (ETL to OMOP)? If it's the latter, clinical fidelity doesn't slow you down—only generation does. This suggests you could have generated slower but higher-fidelity data without impacting the infrastructure testing timeline.

---

### "Linkage Validation: Measure Accuracy and Error Rates without Privacy risk"

This claim only holds if the synthetic data has realistic error rates. Your LTM shows:

- 2021/2022 HES data: 99% Cross-check, ~20,000 records required Algorithmic tracing
- Your requirement (April 16th, 10:06 AM): "Confirm the synthetic engine produces 'messy' enough demographics to trigger Alphanumeric and Algorithmic traces."

Did the team implement this?

Your LTM doesn't confirm whether the `swpc_synthea` engine was configured to inject realistic errors. If not, the linkage validation claim is aspirational, not actual.

---

### "Privacy-First Development: Gold Standard Testbed without High-level clearances"

This is a critical non-negotiable and appears to be the team's primary driver. The faster you generate synthetic data, the sooner developers can:

- Build cohort filters
- Test k-anonymity protocols
- Debug `Token_Person_ID` joins across HES/MHSDS/Maternity

However: If the data lacks clinical realism, developers may build queries that work on synthetic but fail on real data—a false sense of security.

---

## Technical and Operational Statements—Missing Details

### Statistical Integrity: Cryptographic Seed Offset (1,000,003)

Your LTM confirms this ensures statistical independence across 30 parallel workers. However, there's no mention of:

- Reproducibility: Can the same seed regenerate identical datasets for QA validation?
- Determinism: If a worker crashes, does the pipeline resume with the same seed or skip to the next offset?

This is a RAP compliance gap that could undermine auditability.

---

### QA and Testing: `omock` R Package

Your LTM mentions this for "rapid unit testing before the 30 TiB production run," but doesn't clarify:

- What are the unit tests? (Schema validation? Referential integrity? Concept mapping coverage?)
- Who owns this? (The Hyve? Your team?)

The statement _"The Hyve should own Methodological Transparency"_ suggests a handoff boundary that may not be clearly defined.

---

## The Core Tension: Your Vision vs. Team Reality

### What You Wanted

1. Clinical fidelity using NHSSynth/SynthVAE validation
2. Edge case stress (messy demographics, Algorithmic tracing triggers)
3. Name mapping diversity beyond the current `NAME_MAPPING.csv`
4. Sensitive flag simulation to test privacy redaction logic

### What the Team Prioritized

1. Volume and speed (12M patients, 280-hour run)
2. Infrastructure benchmarking (30 TiB → 60 TiB footprint)
3. DAR workflow testing (cohort filtering, multi-site selection)
4. Node separation (5 databases, not clinical realism)

---

## Recommendations Based on Your LTM

### 1. Document the Fidelity Trade-off

Your Miro board asks: _"Are we measuring success based on fidelity (how real it looks) or utility (how research-ready it is)?"_

Action: Create a "Success Criteria" post-it (as suggested on April 16th at 9:44 AM) defining:

- Acceptable false positive/negative rates for linkage
- Minimum MatchedConfidencePercentage thresholds
- Required error injection rates (e.g., 1% missing NHS numbers)

### 2. Pilot with 1M Patients First

Before committing to the 280-hour, 12M patient run, validate:

- Does the `swpc_synthea` UK fork actually trigger Algorithmic tracing?
- Can you measure `MatchedAlgorithmIndicator` distribution?
- Does the data "feel" realistic to clinical staff?

Justification: The LTM shows each trust has 1M–3M patients, so a 1M pilot is production-representative.

### 3. Clarify Ownership with The Hyve

Your LTM mentions: _"The Hyve should own Methodological Transparency."_ But also asks: _"Are we responsible for each DBA team specs/indices?"_

Action: Define a RACI matrix for:

- Who validates SNOMED/dm+d → OMOP concept mapping?
- Who benchmarks query performance on 4M patient databases?
- Who documents the RAP compliance level (Level 2 vs. Level 3)?

### 4. Protect Your Technical Anchor Role

As the "Staff Technical Anchor" and "Forensic Lead", your concern about clinical fidelity isn't pedantry—it's risk mitigation. If the synthetic data produces "vibe-based" validation instead of ground truth, the pipeline becomes a zombie infrastructure (something you're explicitly intolerant of).

Your Leverage: Frame fidelity as a determinism requirement, not a quality preference. If the data can't reproduce real-world linkage errors, the pipeline isn't deterministic—it's drift-prone.

---

## Final Thought: The Speed vs. Fidelity Paradox

Your LTM shows the team chose speed because they need to test DARs "considering the data volume and number of sites expected by year-end." But here's the paradox:

If the synthetic data doesn't reflect real-world complexity, any DAR tested on it will need re-validation on production data anyway.

You're not just generating test data—you're building institutional knowledge about how NHS data behaves. That knowledge is only as good as the data's fidelity.

Bottom line: You were right to push for clinical accuracy. The team's decision to prioritize speed is defensible for infrastructure testing, but it's a tactical win at the expense of strategic robustness.
