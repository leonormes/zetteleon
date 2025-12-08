---
aliases: []
confidence:
created: 2025-12-08T14:16:00Z
epistemic:
last_reviewed:
modified: 2025-12-08T14:19:01Z
purpose:
review_interval:
see_also: []
source_of_truth: []
status: raw
tags: [state/thinking]
title: HEAD - Set up postgres for testing
type: head
uid:
up: "[[00_Workbench]]"
updated:
---

> [!abstract] The Spark (Contextual Wrapper)
> Ticket: [FFAPP-4635](https://fitfile.atlassian.net/browse/FFAPP-4635) - End-to-end SDE Project Extract (write & test): A0025.
> We need to set up a database to test large datasets in our staging environment to ensure all features and data pipeline steps can work with expected volumes.
>
> **Core Goal:** Verify the SDE Manager can handle the specific "Live Data Volumes" from CUH, particularly the ~508 million measurement records.

> [!info] Data Volume Requirements (Live Data from CUH)
> | Table Name | No of records |
> | :--- | :--- |
> | **measurement** | **507,750,094** |
> | **drug_exposure** | **102,268,852** |
> | condition_occurrence | 24,626,962 |
> | visit_occurrence | 21,547,274 |
> | visit_detail | 8,359,106 |
> | concept | 4,802,681 |
> | observation | 2,091,481 |
> | procedure_occurrence | 1,673,318 |
> | person | 1,067,532 |
> | observation_period | 1,057,960 |

## 🧠 My Current Model (The Blind Write)
*Instructions: Write this section BEFORE looking at documentation. How do you think it works? What is your logic? be messy.*

**I think it works like this:**

**I am assuming that:**