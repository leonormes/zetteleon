---
aliases: ["ARACHNE Network", "OHDSI Execution Engine"]
created: 2026-01-06T19:29:06+00:00
last_reviewed: 
modified: 2026-02-01T15:08:02+00:00
status: "Active"
tags: ["federation", "infrastructure", "ohdsi", "SoftwareEngineering/Security"]
title: SoT - ARACHNE
type: "SoT"
updated: 
---

## SoT - ARACHNE

> Core Function: The logistics layer of the OHDSI network. It manages the orchestration, security, and execution of distributed studies, replacing manual email/FTP workflows with a secure pipeline.

### 1. The Operational Problem

Running a study across 10 hospitals usually involves:

1. emailing SQL scripts.
2. DBAs manually running them.
3. DBAs redacting results.
4. Emailing CSVs back.
_Result:_ High friction, versioning errors, security risks.

### 2. The ARACHNE Solution

ARACHNE acts as a "Data Node Controller."

#### A. Execution Environment

It provides a standard containerized environment (R, Python, SQL) to run the study package. This ensures Reproducibility—the code runs exactly the same way at every site.

#### B. The "Air Gap" Control (Data Custodian)

Crucially, ARACHNE does not give researchers direct access to the data.

1. Request: Researcher sends a "Study Package" (Code) to the Node.
2. Hold: The Node holds the package in a queue.
3. Review: The Local Data Custodian reviews the code/request.
4. Approve: The Custodian approves execution.
5. Run: ARACHNE runs the code against the local OMOP CDM.
6. Redact: ARACHNE holds the _Results_.
7. Release: The Custodian reviews the aggregated results and approves the transfer back to the central hub.

### 3. Network of Networks

ARACHNE enables "Super-Networks." It can bridge OHDSI US, OHDSI EU, and EHDEN, allowing a single study definition to traverse multiple administrative domains while respecting local governance.

### 4. Integration

- Atlas: Can import study designs directly from Atlas.
- Achilles: Can ingest characterization reports to provide network-level metadata.
