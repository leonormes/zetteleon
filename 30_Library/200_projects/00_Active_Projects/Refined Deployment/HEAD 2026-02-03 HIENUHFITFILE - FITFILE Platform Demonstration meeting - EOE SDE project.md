---
captured: "2026-04-28T13:28:04+01:00 2026-04-28T13:28:04+01:00"
created: 2026-04-28T12:28:06+00:00
modified: 2026-04-28T12:48:01+00:00
source: "https://fitfile.atlassian.net/wiki/spaces/EOE/pages/2608365571/2026-02-03+HIE+NUH+FITFILE+-+FITFILE+Platform+Demonstration+meeting"
status: "processing"
tags: ["input"]
title: HEAD 2026-02-03 HIENUHFITFILE - FITFILE Platform Demonstration meeting - EOE SDE project
type: "head"
---

## Raw Output / Content

## Participants

- FITFILE:,,
- HIE EoE: Mark Dines-Allen
- NUH: Phil Quinlan, Tom Smith, Irene Juurlink, Alex Waldren-Glenn

## Agenda

- Continuation of demo session of the FITFILE platform

## Meeting Recording

Link to recording of the meeting: [FITFILE \_ NUH Follow up demo session](https://fathom.video/share/KhvtPyqZQz9F5yy71pHz9xshUDKGTKVc)

## Meeting Summary

### Key Takeaways

- Automated Date Shifting: ==: NUH raised an improvement to the date shifting transformation to include the randomisation per patient.==
- Automated Data Disclosure: The "Data Disclosure" feature automates the manual approval process for data releases, creating a formal audit trail and mitigating human error.
- Flexible Data Pipeline: A modular pipeline enables data profiling, PII detection, and custom transformations (e.g., bucketing, outlier removal) to meet specific project needs.

### Platform Demonstration

#### Data Profiler

- Assesses data quality, completeness, and distribution.
- Visualises data distribution (e.g., age, region) to help users refine queries and maximise cohort size.
- Shows k-anonymity distribution to predict data transformation impact based on the k-threshold.
	- _Example:_ If k=5 and a group has only 4 people, the protocol transforms their data to prevent re-identification.
- Can run analytics at the source or locally across multiple remote datasets.

#### PII Detection

- Detects PII (e.g., NHS numbers, names) in free-text fields using a third-party tool.
- Could be run before or after the data is pseudonymised/anonymised and subsequently released to data consumers.
- Output is a JSON report detailing detected entities, counts, and field locations.

#### Custom Transformations

- Provides flexible field specific data transformations beyond pre-defined protocol.
- Use Cases:
	- Treating specific PII found via PII detection.
		- Applying data minimisation for OMOP data (e.g., date shifting, bucketing, outlier removal).
		- Transform the specific data fields for the warehousing purpose.
- *Key Feature Request:*Automated Date Shifting
	- NUH's current manual date shifting is a major bottleneck, especially for data refreshes.
		- Currently, date shifting has to be manualy applied to each relevant data field, but FITFILE is working on the querying improvements where relevant transformations like date shifting will be packed together and could be applied as an OMOP recommended custom transformation templates.

#### Platform Controls: Governance & Audit

- Data Disclosure Feature
	- Automates the manual approval process (e.g., Tom's current role) for data releases.
		- Creates a formal audit trail for each decision, mitigating human error.
		- _Workflow:_ A Data Consumer's query generates a pending request for the Data Provider to approve or reject.
		- _Usability Concern_: The current blocking workflow could create a high volume of requests for complex queries (e.g. OMOP).
		- _FITFILE Solution:_ Exempt cohort discovery queries and streamline the approval flow to reduce Data Provider burden.
- Audit Page
	- Logs all platform actions (logins, queries, permission changes) for full traceability.
		- Events can be exported for external review.

### AOB

- Susannah advised that the next step is to hold the Tech and Data Discovery Session with the relevant tech and data staff from NUH. Phil will provide contact details of the tech staff required to join the session.
- Susannah will share the tech and data discovery questions template in advance of the meeting.
- Phil to coordinate with Mark to define SDE roles and responsibilities.
