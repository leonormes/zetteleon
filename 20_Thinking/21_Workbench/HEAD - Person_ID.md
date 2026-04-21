---
aliases: []
created: 2026-04-16T00:00:52+00:00
modified: 2026-04-20T13:21:27+00:00
tags: [prodos/head, state/thinking]
title: HEAD - Person_ID
---

The Person_ID is important because it serves as a standardised "master key" for linking patient data across different NHS datasets, even when a reliable NHS number is missing or incorrectThe Person_ID is important because it serves as a standardised "master key" for linking patient data across different NHS datasets, even when a reliable NHS number is missing or incorrect`Person_ID`standardised "master key".

While the NHS number is the primary identifier for healthcare in England, relying on it alone for data analysis presents several challenges that the `Person_ID` system is designed to solve.

## 1. Coverage: Not Everyone Has an NHS Number

A significant limitation of using only the NHS number is that not every person treated by the NHS possesses one. This includes:

- Overseas visitorsOverseas visitors receiving care.
- Private patientsPrivate patients.
- Newborn babiesNewborn babies who have not yet been assigned a number.
- Long-term mental health patientsLong-term mental health patients who may not have a recorded number.

By using Person_ID, the system can assign a unique, persistent identifier (an MPS_ID) to these individuals, allowing researchers to track their care journey across different datasets without an NHS numberBy using Person_ID, the system can assign a unique, persistent identifier (an MPS_ID) to these individuals, allowing researchers to track their care journey across different datasets without an NHS number`Person_ID``MPS_ID`.

## 2. Data Quality and Consistency

In real-world data, identifiers like the NHS number are often:

- Missing or incompleteMissing or incomplete in the submitted recordsMissing or incomplete in the submitted records.
- Recorded inconsistentlyRecorded inconsistently or with typographical errorsRecorded inconsistently or with typographical errors.
- Superseded:Superseded: An NHS number can become invalid and be replaced by a new one (e.g., due to adoptions or identity changes)Superseded: An NHS number can become invalid and be replaced by a new one (e.g., due to adoptions or identity changes).

The Master Person Service (MPS) uses complex "algorithmic tracing" to compare other details—like date of birth, gender, and postcode—to confirm a person's identity and link them to the correct Person_ID, even if the submitted NHS number is wrong or missingThe Master Person Service (MPS) uses complex "algorithmic tracing" to compare other details—like date of birth, gender, and postcode—to confirm a person's identity and link them to the correct Person_ID, even if the submitted NHS number is wrong or missingThe Master Person Service (MPS) uses complex "algorithmic tracing" to compare other details—like date of birth, gender, and postcode—to confirm a person's identity and link them to the correct Person_ID, even if the submitted NHS number is wrong or missing`Person_ID`.

## 3. Enabling Secure Research (Tokenisation)

For security and privacy, most researchers and analysts are not permitted to see "identifiable" information like a real NHS number.

- Token_Person_ID:Token_Person_ID: The Person_ID acts as a stable foundation that can be "tokenised" (anonymised) into a 32-digit string`Person_ID`.
- Privacy-Preserving Linkage:Privacy-Preserving Linkage: This allows analysts to count unique people or link a person's hospital records with their mental health records without ever knowing who that person actually is.
- Domain Isolation:Domain Isolation: The same person is given different tokenised IDs for different research projects, ensuring they cannot be "re-identified" by combining data from multiple sources.

## Summary: Person_ID vs. NHS Number

|Feature|NHS Number|Person_ID|
|---|---|---|
|Source|Assigned at birth/registration|Derived via the Master Person Service (MPS)|
|Availability|Not held by everyone (e.g., overseas visitors)|Always available for every record|
|Reliability|Subject to data entry errors or changes|Verified against a national database (PDS)|
|Research Use|Highly sensitive; restricted access|Can be safely tokenised for broad analytical use|

In essence, the `Person_ID` is the reliable version of a patient's identity. It combines the NHS number (when available and correct) with other identifiers to ensure that every patient in the system can be accurately and safely followed through their healthcare journey.
