---
aliases: []
confidence: 
created: 2025-10-18T09:58:43Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:13Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [project/work/fitfile-technical-documents, topic/productivity/gtd]
title: Unified Document Numbering System
type:
uid: 
updated: 
version:
---

1. Core Mission & Document Types
   This guide defines the official system for creating and managing all technical documentation for the FITFILE product.
   Our mission is to maintain a single source of truth where every business need is traceably linked to its technical implementation. This system connects three types of documents:

- Requirements (RQ-): The "Why". A formal definition of a business need or technical specification.
  - Example: RQ-1.0.1 Structured Data Ingestion
- Features: The "How". A detailed technical description of the software capability that fulfils a requirement.
  - Example: 1.2.1 Ingest from File
- FAQs: The "User Question". A user-centric question and answer that simplifies a topic, linking to the relevant Requirement and Feature.
  - Example: "How do I upload data?"

2. The Unified Numbering System
   All documents must adhere to this hierarchical numbering scheme.
   3.1. Base Structure
   The format is Major.Minor.Feature[.SubFeature].

- Major (1.x.x): The top-level product module.
  - 1.x.x: FITFILE Core
  - 2.x.x: Research Manager
  - 3.x.x: Operations
- Minor (1.3.x): A key functional block within a module.
  - Example: 1.3.0 is "Data De-identification & Transformation".
- Feature (1.3.2): A specific capability within that block.
  - Example: 1.3.2 is "Data Pseudonymisation".
- SubFeature (1.2.1.1) (Optional): A granular aspect of a feature, such as a supported file type or method.
  - Example: 1.2.1.1 CSV Support (a child of 1.2.1 Ingest from File)
    2.2. Document Prefixes

- Feature pages use the base number directly (e.g., 1.3.2).
- Requirement pages use the prefix RQ- (e.g., RQ-1.1.1).
- FAQ pages use a plain-language title (e.g., "Can I apply different privacy rules to different columns?").

3. The Interlinking Mandate
   Traceability is mandatory. Every document must be bi-directionally linked to its counterparts using Confluence page links.

- A Requirement page (RQ-1.1.3) MUST link to:
  - The Feature(s) that implement it (e.g., Implemented by: 1.3.4).
  - Any relevant FAQs.
- A Feature page (1.3.4) MUST link to:
  - The Requirement(s) it fulfils (e.g., Maps to: RQ-1.1.3).
  - Any relevant FAQs.
- An FAQ page MUST link to:
  - The Requirement that defines the problem.
  - The Feature that provides the solution.

4. Lifecycle & Status Management
   Features and Requirements are not static. Their status must be tracked directly on the Confluence page.
   Use the following core statuses:

- ⚪ Backlog: The idea is valuable and approved but not scheduled for development.
- 🔵 Planning: Actively being defined, scoped, and designed.
- 🟡 In Progress: An engineering team has started implementation.
- 🟣 Testing / In QA: Code complete and being validated by the Quality Assurance team.
- 🟢 Live: Successfully deployed to production and available to users.
- 🔴 Deprecated: Phased out and no longer recommended for use.
- 🔘 Rejected / Won't Do: Reviewed and permanently cancelled.

5. Implementation in Confluence & Jira
   This system is implemented using Confluence templates and Jira integration.
   6.1. Confluence Template Setup
   Create two Confluence templates: "New Requirement" and "New Feature".

- Use the "Page Properties" Macro: At the top of each template, add a Page Properties macro. This feeds our documentation dashboards.
- Add Metadata: Inside the macro, create a table for the core metadata.
- Use the "Status" Macro: For the Status field, use the native Confluence /status macro to create the coloured lozenge.
  Example "New Feature" Template Metadata:

| Field               | Value                                      |
| ------------------- | ------------------------------------------ |
| Feature ID          | 1.x.x (Assign the next sequential number)  |
| Maps to Requirement | Link to the RQpage(s) (e.g., [[RQ-1.1.3]]) |
| Owner               | @Username                                  |
| Status              | /status (Default to ⚪ Backlog)            |

5.2. Jira Integration
The Feature page must display all related development work from Jira.

- Establish a Link: Use a Jira Epic for each Confluence Feature page. This is the simplest and cleanest method. (Alternatively, use a unique Jira Label like ff-1-3-4).
- Add the "Jira" Macro: On the Feature template, add a section titled "Related Development Work".
- Use a JQL Query: Insert the /jira macro and configure it to use a JQL query. This will create a live, dynamic table of all related tickets.
  Recommended JQL for the Jira Macro:
  'Epic Link' = "FF-142"
  or
  label = "ff-1-3-4"

6. End-to-End Team Workflow
   Follow these steps to take a new idea from concept to live documentation.

- Step 1: The Need is Identified
  - A user question or business need arises.
  - Action: A Product Manager or BA creates an FAQ page to capture the user's question.
  - Action: They then create a Requirement (RQ-) page to formally define the business problem. They set its status to 🔵 Planning.
- Step 2: The Solution is Defined
  - The team discusses how to solve the problem.
  - Action: A BA or Tech Lead creates a Feature page, finds the next available number (e.g., 1.3.4), and sets its status to ⚪ Backlog or 🔵 Planning.
- Step 3: The Links are Created
  - Action: The document owner edits all three pages to ensure they are fully bi-directionally linked in their Page Properties sections.
    - The FAQ links to the RQand the Feature.
    - The RQlinks to the Feature.
    - The Feature links to the RQ-.
- Step 4: The Work is Tracked
  - Action: A development lead creates a Jira Epic (e.g., FF-142) for the work.
  - Action: They edit the Confluence Feature page (1.3.4), add the /jira macro, and configure it with the JQL 'Epic Link' = "FF-142". All stories and bugs for that feature will now appear on its documentation page.
- Step 5: The Lifecycle is Managed
  - As development starts, the Jira Epic's child tickets move to "In Progress".
  - Action: The Feature Owner edits the Confluence Feature page and updates its /status macro from 🔵 Planning to 🟡 In Progress.
  - Action: They then update the parent Requirement page's status to 🟡 In Progress as well.
- Step 6: The Feature is Released
  - The code is deployed, and the Jira Epic is "Done".
  - Action: The Feature Owner updates the Feature page status to 🟢 Live.
  - Action: The Requirement page status is also updated to 🟢 Live.
  - Action: The FAQ page is updated with the final answer, explaining how users can now use the new feature.

7. Reference: Current Documentation Structure
   Use this list to find the correct logical position and next available number for new documents.
   FITFILE Core Features (1.x.x)

- 1.2.0 Data Ingestion
  - 1.2.1 Ingest from File
  - 1.2.2 Ingest from Database
- 1.3.0 Data De-identification & Transformation
  - 1.3.1 Data Anonymisation
  - 1.3.2 Data Pseudonymisation
  - 1.3.3 Custom Transformation Operation
- 1.4.0 Data Validation & Quality
  - 1.4.1 Data Schema Validation
  - 1.4.2 Data Quality Checks
- 1.5.0 Data Mapping & Dictionary
  - 1.5.1 Data Mapping Tool
  - 1.5.2 Data Dictionary Management
- 1.6.0 Secure Data Export
  - 1.6.1 Export to File
  - 1.6.2 Export to Database
- 1.7.0 Core System Services
  - 1.7.1 System-level Auditing & Logging
- (Next available block: 1.8.0)
  Requirements (RQ-1.x.x)
- RQ-1.0.1 Structured Data Ingestion
- RQ-1.0.2 Secure File Transfer
- RQ-1.0.3 Data Format Support
- RQ-1.1.1 Privacy
- RQ-1.1.2 Custom Transformation Operation
- (Next available number: RQ-1.1.3 or RQ-1.2.1 for a new block)
