---
aliases: []
confidence: 
created: 2025-10-17T12:12:21Z
epistemic: 
last_reviewed: 
modified: 2025-10-30T14:24:11Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: [project/work/fitfile-technical-documents]
title: From Customer Wish to Live Code
type:
uid: 
updated: 
version:
---

---

## The Story of a Feature: From Customer Wish to Live Code

**The Team:**

- **WJ:** The Product Manager, who is the link between the customer and the team.
- **RM:** The Business Analyst, who is the meticulous owner of the Confluence documentation.
- **OR:** The Lead Developer, who translates the requirements into technical reality in Jira.

---

### Monday, 9:15 AM: The Spark

The story begins on Monday morning. WJ is reviewing feedback from a key customer, a university research department. A clear theme emerges from their notes: they love the automatic de-identification in FITFILE Core, but they need more control. A researcher writes, *"We need to pseudonymise the 'Patient ID' but fully anonymise the 'Postcode' within the same dataset. Right now, it's all or nothing. We need to choose the privacy treatment for each field."*

WJ has seen similar requests before. It’s time to formalise it.

---

## Document 1: The FAQ (The User's Question)

WJ messages RM. "RM, we're getting more requests about field-level privacy. Can you spin up an FAQ page so our users know we're aware of it?"

RM navigates to the "FITFILE FAQs" section in Confluence. He doesn't need a specific template for this, just a clear title and answer.

He creates a new page:

> **Title: Can I apply different privacy rules to different columns in my data?**
>
> **Body:**
> Currently, FITFILE Core applies a single, consistent privacy treatment (like Anonymisation or Pseudonymisation) across an entire dataset.
>
> We understand that many users require more granular control, such as applying different rules to specific fields. This is a priority for our team and is currently in the planning phase.
>
> For more details on the business need, see our internal requirement: [[RQ-1.1.3 Granular Privacy Control]]. *(He creates this as a placeholder link for now, knowing it's his next step).*

This page immediately provides value. It acknowledges the user's problem and points them towards the internal process.

---

## Document 2: The Requirement (The Business Need)

Now, RM needs to define *what* the business needs to solve. He goes to the "FITFILE Core Requirements" space in Confluence and clicks **Create from template**, selecting his "Requirement" template.

1. **Assign an ID:** He checks the existing list. Privacy requirements are under `RQ-1.1.x`. The last one was `RQ-1.1.2`. He assigns this new one **`RQ-1.1.3`**.
2. **Create the Page:** He creates a new page titled `RQ-1.1.3 Granular Privacy Control`.
3. **Fill the Metadata:** He fills out the **Page Properties** macro at the top:
   - **Requirement ID:** `RQ-1.1.3`
   - **Implemented by:** *(He leaves this blank for now)*
   - **Related FAQs:** He links the FAQ page he just created.
   - **Owner:** `@WJ`
   - **Status:** He clicks the `/status` macro and sets it to `🔵 Planning`.

4. **Define the Scope:** In the body of the page, he defines the business need, writing formal statements like: *"The system must allow a user to select a specific privacy treatment (e.g., Anonymisation, Pseudonymisation) for each individual field within a dataset during the transformation process."*

The requirement is now formally documented and linked to the initial user query.

---

## Document 3: The Feature (The Technical Solution)

WJ, RM, and OR get together for a quick planning session. They agree on the technical approach. This will be a new capability within the "Data De-identification & Transformation" block.

It's RM's turn again. He navigates to the "FITFILE Core Features" section and clicks **Create from template**, selecting the "Feature" template.

1. **Assign an ID:** He sees the last feature in the `1.3.x` block was `1.3.3`. He assigns this new one **`1.3.4`**.
2. **Create the Page:** He titles the page `1.3.4 Field-Level Privacy Treatment Selection`.
3. **Fill the Metadata:** He fills out the **Page Properties** macro:
   - **Feature ID:** `1.3.4`
   - **Maps to Requirement:** He links to `[[RQ-1.1.3 Granular Privacy Control]]`. The loop is now complete—the Requirement points to the Feature, and the Feature points back to the Requirement.
   - **Owner:** `@OR`
   - **Status:** He sets the initial status to `⚪ Backlog`.

Now, it's OR's turn to connect this to the development work.

---

### Monday, 2:00 PM: The Handoff to Development

1. **Create the Epic:** OR goes into Jira. She creates a new Epic for this work: **`[FF-142] Implement Field-Level Privacy Controls`**.
2. **Link to Confluence:** She goes back to the `1.3.4` Feature page in Confluence. She scrolls down to the "Related Development Work" section.
3. **Insert Jira Macro:** She types `/jira` and pastes in a JQL query: `'Epic Link' = FF-142`. She configures it to show the ticket key, summary, status, and assignee. The macro appears, currently empty, waiting for tickets.

The team starts breaking down the Epic, creating stories like `[FF-143] Design UI for field selection` and `[FF-144] Adapt transformation engine`. As soon as they are created in Jira, they instantly appear in the table on the Confluence page.

---

### Weeks Later: The Lifecycle in Action

A developer starts work on `FF-143`. The ticket's status in Jira automatically changes to `In Progress`. The Confluence feature page reflects this change in real-time. Seeing this, OR edits the Confluence page and updates the main **Status** lozenge from `⚪ Backlog` to `🟡 In Progress`.

RM gets a notification. He navigates to the parent Requirement page, `RQ-1.1.3`, and updates its status to `🟡 In Progress` as well. Now, anyone looking at the documentation, from the high-level requirement down to the technical feature, knows that work is underway.

---

### The Finish Line

The feature is finally built, tested, and deployed. All Jira tickets under the Epic are marked `Done`.

1. **Update Feature:** OR goes to the `1.3.4` Feature page and triumphantly clicks the status, changing it to `🟢 Live`.
2. **Update Requirement:** RM updates the `RQ-1.1.3` Requirement page to `🟢 Live`.
3. **Update the FAQ:** RM goes back to the very first document—the FAQ. He edits the page, updating the text to say: *"Yes! As of version 2.5, you can now select a specific privacy treatment for each field in your dataset. Here’s how..."* He adds a link to the user guide and to the `1.3.4` Feature page for those interested in the technical details.

The workflow is complete. A customer's need has been traced through the entire process, from a simple question to a documented requirement, a specified feature, tracked development work, and finally, a solution communicated back to the user.
