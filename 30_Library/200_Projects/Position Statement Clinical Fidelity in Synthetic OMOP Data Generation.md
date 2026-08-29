---
created: 2026-04-17T07:23:48+00:00
modified: 2026-08-29T09:36:21+00:00
permalink: llmeon/30-library/200-projects/position-statement-clinical-fidelity-in-synthetic-omop-data-generation
project_category: omop
project_name: OMOP
project_status: active
title: Position Statement Clinical Fidelity in Synthetic OMOP Data Generation
type: null
---

## My Position

I advocate for clinically realistic synthetic data that exercises the full complexity of NHS primary care records—including name normalization edge cases, missing NHS numbers, superseded identifiers, and demographic messiness that triggers Alphanumeric and Algorithmic tracing in the MPS linkage logic.

### Why Do This Now

We should implement clinical fidelity during initial generation because:

1. Avoiding Rework: If stakeholders request clinically accurate data in 2-3 months (when testing DAR queries against realistic cohort distributions), we will need to regenerate the entire 12M patient dataset—repeating the 280-hour production run and re-importing ~30 TiB of data.
2. Linkage Validation Integrity: The pipeline's core value proposition is validating `Person_ID` and `Token_Person_ID` algorithms. Without realistic error rates (missing identifiers, name variations, postcode typos), we cannot measure the MatchedConfidencePercentage thresholds or confirm that Algorithmic tracing logic works as designed.
3. Institutional Knowledge: This dataset isn't just infrastructure scaffolding—it's the foundation for understanding how NHS data behaves. If we skip fidelity validation, we're building on assumptions rather than evidence.
4. Determinism Over Volume: A pipeline that handles "clean" synthetic data but fails on real-world messiness isn't deterministic—it's drift-prone. We risk Type 1 errors where DAR queries validate successfully in testing but break in production.

---

## The Team's Decision

The team chose to prioritize speed and infrastructure stress-testing over clinical fidelity, focusing on:

- Realistic cohort overlap (70-85% single-trust, 15-30% multi-trust) rather than clinically accurate individual records
- Volume-based validation (12 billion rows, ~30 TiB storage) to identify hardware bottlenecks
- Faster delivery timeline to enable DAR workflow testing before year-end when 5 nodes are expected in the SDE network

---

## The Tradeoffs

| Speed-First Approach (Team's Choice) | Fidelity-First Approach (My Preference) |
|------------------------------------------|---------------------------------------------|
| ✅ Faster generation (280-hour run completed sooner) | ⚠️ Slower generation (additional validation layers) |
| ✅ Meets infrastructure testing timeline | ✅ Exercises full MPS linkage complexity |
| ✅ Enables DAR workflow prototyping immediately | ✅ Validates name normalization/Algorithmic tracing |
| ⚠️ Skips clinical accuracy validation | ✅ Provides measurable MatchedConfidencePercentage data |
| ⚠️ May not trigger Alphanumeric/Algorithmic tracing | ✅ Avoids rework if stakeholders later demand realism |
| ⚠️ Risk of rework if fidelity becomes required | ⚠️ Delayed availability for UI/DAR testing |
| ⚠️ Cannot validate linkage error rates | ✅ Builds institutional knowledge about NHS data behavior |

---

## My Commitment

I disagree with prioritizing speed over fidelity, but I commit to the team's decision. I will support the current approach while documenting this decision and its constraints so that if rework becomes necessary, we have a clear record of the architectural tradeoff that was made.

---

Recommendation for Risk Mitigation:

We should define measurable success criteria for what "realistic cohort overlap" means in practice, and establish a 1M patient pilot to validate whether the simplified approach successfully triggers the MPS logic before committing to the full 12M production run.
