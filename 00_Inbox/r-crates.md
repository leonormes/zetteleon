---
aliases: []
tags: []
title: r-crates
type: ""
status: ""
confidence: ""
epistemic: ""
purpose: ""
modified: 2026-01-06T07:46:56+00:00
last_reviewed: ""
review_interval: ""
see_also: []
source_of_truth: []
created: 2026-01-06T07:46:48+00:00
---

Based on the sources, **Five Safes RO-Crates** protect federated health data by serving as a standardized "envelope" or carrier for the metadata required to execute analysis within Trusted Research Environments (TREs). Instead of moving sensitive patient data, these crates transport the analysis code (workflows) and governance instructions to the data, ensuring compliance with the "Five Safes" framework throughout the research lifecycle.

Here is how the Five Safes RO-Crate mechanism facilitates protection:

### 1. Enabling "Code-to-Data" (Safe Settings & Safe Data)

The fundamental protection mechanism facilitated by the Five Safes RO-Crate is the enforcement of a **"code only" access model**.

- **Data Stays Put:** The crate does not contain the sensitive health data itself. Instead, it packages a request to execute a computational workflow (e.g., an OHDSI study package) against data that remains resident and secure behind the TRE's firewall,.
- **Pre-Approved Workflows:** To ensure "Safe Data" and "Safe Settings," the crate typically references **pre-approved and pre-installed workflows** rather than arbitrary code. This prevents malicious code from entering the secure environment. The request is expressed as specific input parameters for these vetted workflows,,.

### 2. Mapping Metadata to Governance Principles

The RO-Crate profile explicitly maps metadata fields to the Five Safes framework, allowing TREs to automate verification before any code is executed. According to the sources, this mapping includes:

- **Safe People:** The crate contains metadata identifying the **Requesting Agent** (the researcher) and their organization. This allows the TRE to authenticate the user and verify their authorization level,,.
- **Safe Projects:** The crate links the analysis request to a **Responsible Project** identifier. The TRE checks this against its records to ensure the query allows for the specific permissions granted to that research project,,.
- **Safe Data:** The crate defines the **input parameters** for the workflow. The TRE verifies that the project is authorized to query the specific subset or projection of data requested,,.
- **Safe Settings:** The crate identifies the **Requested Workflow Run**. The TRE ensures this workflow is authorized for execution within its secure environment,,.
- **Safe Outputs:** The crate structures the results as a **Workflow Run Crate**, separating aggregated summary statistics from the execution logs. This structure facilitates the review process (disclosure control) to ensure no identifiable data leaves the TRE,,.

### 3. Enforcing a Secure Execution Workflow

The Five Safes RO-Crate supports a rigorous, multi-phase governance process (often called the "eight steps") that monitors the analysis from entry to exit:

1. **Check & Validation:** Before entering the TRE, the crate is checked for integrity and validity against the profile,.
2. **Sign-off:** The TRE validates that the specific user and project are permitted to run the specific workflow on the specific data,.
3. **Execution:** The workflow runs inside the secure environment (often air-gapped). The crate records provenance data regarding the execution,.
4. **Disclosure Control:** Before the crate is allowed to leave the TRE, its contents (the results) undergo a **disclosure phase**. This can be manual or semi-automated, ensuring that only safe, non-disclosive aggregate results are returned to the researcher,,.

### 4. Auditability and Provenance

The crate acts as a comprehensive **audit trail**. It captures the full provenance of the research activity, including who requested it, what workflow was used, when it was executed, and what disclosure checks were applied,. This allows auditors to trace exactly who accessed which data and ensures transparency, which is critical for maintaining the trust of data custodians and patients,.

In summary, the Five Safes RO-Crate protects data by **standardizing the bureaucracy of trust**. It replaces ad-hoc, manual permission checks with a machine-readable structure that enforces strict access controls, keeps raw data stationary, and ensures that only safe, aggregated results are released,,.
