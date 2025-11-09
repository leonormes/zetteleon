---
aliases: []
confidence:
created: 2025-10-17T01:57:15Z
epistemic:
last_reviewed:
modified: 2025-11-03T13:48:13Z
purpose: To instruct an LLM on how to act as a technical writer for the FITFILE product, enforcing a strict, hierarchical numbering and cross-referencing system for creating and managing Features, Requirements, and FAQ documents within Confluence and Jira.
review_interval:
see_also: []
source_of_truth: []
status:
tags: [project/work/fitfile-technical-documents]
title: LLM prompt with the full context of the feature numbering system
type: prompt
uid:
updated:
version: "1"
---

## LLM Prompt for FITFILE Documentation Generation

### 1\. Persona and Core Mission

You are an expert technical writer and documentation specialist for a software product called **FITFILE**. Your primary mission is to create, manage, and organise a unified and logical technical documentation suite.

This suite consists of three interconnected document types:

- **Features**: Detailed descriptions of what the software can do.
- **Requirements**: Formal definitions of the business needs or technical specifications the software must meet.
- **FAQs**: User-centric questions and answers that simplify complex topics.

Your goal is to ensure every piece of documentation is hierarchically numbered, easily discoverable, and explicitly cross-referenced, providing a clear and traceable path from a business need (Requirement) to its technical implementation (Feature).

---

### 2\. The Unified Numbering System

You must strictly adhere to the following numbering scheme for all documentation.

#### Structure

The base format is `Major.Minor.Feature[.SubFeature][.Variant]`.

- **Major**: The top-level product module.
  - `1.x.x`: FITFILE Core
  - `2.x.x`: Research Manager
  - `3.x.x`: Operations
- **Minor**: A key functional block within a module.
  - *Example*: `1.3.x` represents the "Data De-identification & Transformation" block within FITFILE Core.
- **Feature**: A specific capability within a functional block.
  - *Example*: `1.3.2` represents the "Data Pseudonymisation" feature.
- **SubFeature / Variant** (Optional): A more granular aspect of a feature, such as a supported file type, method, or platform variant.
  - *Example*: `1.2.1.1` could represent "Ingest from File - CSV Support".

#### Document-Specific Prefixes

- **Feature** pages use the base numbering scheme directly (e.g., `1.3.2`).
- **Requirement** pages use the prefix `RQ-` followed by the numbering scheme (e.g., `RQ-1.0.1`).
- **FAQ** pages do not have a strict numbering rule but must reference the numbers of the Features and Requirements they relate to.

---

### 3\. The Interlinking Mandate

The key to this system is **explicit, bi-directional linking**. Every document you create must reference its related counterparts.

- **When creating a Feature page (e.g., `1.6.1 Export to File`):**
  - You MUST identify and list the Requirement(s) it implements (e.g., `Maps to: RQ-1.0.2`).
  - You MUST identify and link to any relevant FAQs.
- **When creating a Requirement page (e.g., `RQ-1.0.2 Secure File Transfer`):**
  - You MUST identify and list the Feature(s) that implement it (e.g., `Implemented by: 1.6.1`).
  - You MUST identify and link to any relevant FAQs.
- **When creating an FAQ page (e.g., "How do I securely send data?"):**
  - You MUST reference the specific Requirement(s) that define the need (e.g., `Related Requirement: RQ-1.0.2`) and the Feature(s) that provide the solution (e.g., `Related Feature: 1.6.1`).

**Example Flow:**`FAQ: How to upload data securely?` ↔ `Requirement: RQ-1.0.2` ↔ `Feature: 1.6.1`

---

### 4\. Source of Truth: Current Documentation Structure

This is the existing structure you must build upon. Do not change these existing numbers. When adding new items, find the correct logical position and use the next available number.

#### Current FITFILE Core Features (1.x.x)

- `1.2.0` Data Ingestion
  - `1.2.1` Ingest from File
  - `1.2.2` Ingest from Database
- `1.3.0` Data De-identification & Transformation
  - `1.3.1` Data Anonymisation
  - `1.3.2` Data Pseudonymisation
  - `1.3.3` Custom Transformation Operation
- `1.4.0` Data Validation & Quality
  - `1.4.1` Data Schema Validation
  - `1.4.2` Data Quality Checks
- `1.5.0` Data Mapping & Dictionary
  - `1.5.1` Data Mapping Tool
  - `1.5.2` Data Dictionary Management
- `1.6.0` Secure Data Export
  - `1.6.1` Export to File
  - `1.6.2` Export to Database
- `1.7.0` Core System Services
  - `1.7.1` System-level Auditing & Logging

#### Current Requirements (RQ-1.x.x)

- `RQ-1.0.1` Structured Data Ingestion
- `RQ-1.0.2` Secure File Transfer
- `RQ-1.0.3` Data Format Support
- `RQ-1.1.1` Privacy
- `RQ-1.1.2` Custom Transformation Operation

---

### 5\. Rules and Best Practices for Content Generation

1. **Always Map First:** Before writing, determine which existing Requirements or Features a new document relates to.
2. **Be Explicit:** State the linked document numbers directly in a summary or metadata section of the document you are creating.
3. **Maintain Sequence:** When adding a new feature (e.g., under `1.7.0`), use the next available number (`1.7.2`).
4. **Leave Gaps:** Intentionally leave gaps in numbering between major functional blocks (e.g., leave `1.8.x` free for a future block) to allow for logical expansion without re-numbering everything.
5. **Use Sub-Features for Granularity:** If a feature like `1.2.1 Ingest from File` needs to detail different file types, create sub-feature pages: `1.2.1.1 CSV`, `1.2.1.2 JSON`, etc.
6. **Maintain a Consistent Tone:** Write clearly and concisely, targeting a technical audience of developers, project managers, and clients.
7. **Format with Markdown:** Use Obsidian-flavoured Markdown for all documents.

---

### 6\. Task Execution

When I ask you to create a new document, you will:

1. **Analyse the request** to determine if it's a Feature, Requirement, or FAQ.
2. **Identify its logical place** within the existing structure provided above.
3. **Assign it the correct new number** following the sequential numbering and hierarchy rules.
4. **Identify all related documents** it must link to.
5. **Generate the content** in Markdown, including the title, number, a clear description, and the mandatory cross-reference links.

The feature should fulfil a requirement but will be in various points on its lifecycle. Planning, implementing live. Give me a list of states a software feature could be in based on industry practise

Based on standard industry practices, a software feature progresses through several distinct states from initial idea to eventual retirement. These states can be grouped into broader phases, reflecting the feature's maturity and its position in the development lifecycle.

Here is a comprehensive list of these states, organised by their typical phase.

### Phase 1: Pre-Development (Ideation and Planning)

This phase covers everything before engineering work begins. The focus is on discovery, validation, and prioritisation.

- **New / Idea / Discovery**: A raw, unevaluated idea or suggestion from a customer, stakeholder, or internal team member.
- **Backlog / To Do**: The feature request has been reviewed, deemed valuable, and placed in the product backlog. It is now a candidate for future development but has not been prioritised.
- **Needs Definition / Analysis**: The feature is being actively investigated. Product managers and analysts define user stories, scope, acceptance criteria, and initial requirements.
- **Planning / Design**: The feature has been prioritised. UX/UI design, technical architecture, and system design are underway to create a detailed implementation plan.
- **Selected for Development / Ready to Start**: The feature is fully defined, designed, and approved. It is waiting in a queue for an engineering team to begin implementation in an upcoming sprint or work cycle.

### Phase 2: Active Development

This phase involves the hands-on creation and testing of the feature by the engineering team.

- **In Progress / Implementing**: A developer has started writing the code for the feature.
- **In Review / Code Review**: The initial coding is complete, and the work is now being reviewed by peers to ensure quality, adherence to standards, and correctness.
- **Testing / In QA**: The feature has passed code review and has been deployed to a testing environment. The Quality Assurance (QA) team is actively testing it against acceptance criteria to find bugs and regressions.
- **Ready for Deployment / Staged**: The feature has passed all tests and is approved. It has been merged into the main codebase and is waiting in a staging or pre-production environment for the next scheduled release.

### Phase 3: Release and Post-Launch

This phase covers the release to users and the subsequent monitoring and support of the live feature.

- **In Release / Deploying**: The feature is part of a release that is actively being deployed to the production environment.
- **Live / Done / Shipped**: The feature is successfully deployed to production and is available to all intended users.
- **Monitoring / Early Access**: The feature is live but is being closely monitored for performance, bugs, and user adoption. It may be released to a limited audience (e.g., behind a feature flag or in a beta programme) before a general rollout.
- **Requires Support / Maintenance**: The feature is stable but requires ongoing maintenance or has known issues that are being tracked.

### Phase 4: Long-Term and End-of-Life

This phase describes the long-term status of a feature after its initial launch hype has passed.

- **Stable / Supported**: The feature is a mature and reliable part of the product. It is fully supported but not under active development.
- **Deprecated**: The feature is being phased out. It is still available but is no longer recommended for use, and a replacement has been communicated. A timeline for its removal is typically provided.
- **Retired / Removed**: The feature has been completely removed from the product and is no longer accessible to users.

### Special / Paused States

These states can occur at various points in the lifecycle and represent a break in the standard workflow.

- **On Hold / Blocked**: Work cannot proceed due to an external dependency, a critical question, or a change in priorities.
- **Cancelled / Won't Do**: A decision has been made to permanently stop all work on the feature.
- **Rejected**: The initial idea was reviewed but was deemed not to be a good fit for the product's strategy or roadmap.

What age the industry practise around requirements documentation

The practice of requirements documentation in software development has evolved significantly over the past 40 to 50 years, moving from rigid, comprehensive documents to more dynamic and collaborative approaches. The "age" of a particular practice doesn't necessarily dictate its relevance, as different methodologies are suited to different project contexts.

### The Evolution and Age of Requirements Practices

**1\. Early Days (1970s-1980s): The Rise of Formal Specification**

In the early decades of software engineering, development was often approached with a mindset borrowed from more traditional engineering disciplines. This led to the rise of heavyweight, formal methodologies.

- **Waterfall Model:** This sequential approach demanded that all requirements be fully documented and signed off before any design or coding could begin. The primary output was a **Software Requirements Specification (SRS)** document. These were often lengthy, highly detailed, and intended to be a complete and unchanging contract between the client and the development team. The international standard ISO/IEC/IEEE 29148, which guides the content of an SRS, is a modern descendant of these early standards.

**2\. The 1990s: Object-Oriented and Use Case-Driven Approaches**

As software systems became more complex and interactive, the limitations of purely text-based, declarative statements became apparent.

- **Use Cases:** Popularised by Ivar Jacobson, use cases shifted the focus to user interactions with the system. They describe the step-by-step process a user (or "actor") follows to achieve a goal. This provided more context than a simple list of "shall" statements and became a cornerstone of methodologies like the Rational Unified Process (RUP).

**3\. The 2000s to Present: The Agile Revolution**

The turn of the millennium saw the rise of Agile methodologies, which fundamentally changed the industry's approach to documentation. The Agile Manifesto famously values "working software over comprehensive documentation."

- **User Stories:** This is the most prevalent form of requirements documentation in Agile environments like Scrum and Kanban. A user story is a short, simple description of a feature told from the perspective of the person who desires the new capability. The typical format is: "As a \[type of user\], I want \[some goal\] so that \[some reason\]."
- **Living Documents:** Rather than creating a large, static requirements document upfront, Agile practices favour "living documents" that evolve throughout the project. These are often managed in tools like Jira, Confluence, or Azure DevOps and are supplemented with visuals like wireframes and diagrams.
- **Just-in-Time Documentation:** The emphasis is on creating just enough documentation, at the last responsible moment. This avoids the waste of documenting features that may change or be de-prioritised.

### Current Industry Practice and Key Principles

Today's industry practice is a blend of these historical approaches, with a strong leaning towards Agile principles. However, the level of formality and detail in requirements documentation varies depending on the industry (e.g., aerospace and medical devices require more rigorous documentation for regulatory compliance), the project's complexity, and the organisational culture.

Key principles of modern requirements documentation include:

- **Collaboration and Communication:** Requirements are no longer seen as something to be "gathered" from users and handed off to developers. Instead, they are elicited and refined through continuous conversation between stakeholders, product owners, business analysts, developers, and testers.
- **Clarity and Unambiguity:** Regardless of the format, requirements must be clear, concise, and understandable to all parties.
- **Testability:** A good requirement is a testable requirement. It should be possible to verify that the implemented software meets the requirement.
- **Traceability:** It's crucial to be able to trace a requirement from its origin (a business need) through to the code that implements it and the tests that verify it.
- **Version Control:** As requirements evolve, it is essential to maintain version control to track changes and understand the history of decisions.
- **Prioritisation:** Not all requirements are equally important. Techniques like MoSCoW (Must have, Should have, Could have, Won't have) are used to prioritise work.
- **Incorporation of Visuals:** To aid understanding, modern requirements documentation often includes visual aids like flowcharts, wireframes, and mockups.

In essence, while the practice of creating large, upfront requirements documents is now considered outdated for most software projects, the fundamental need to understand, document, and manage requirements remains a critical and ever-evolving aspect of software development. The focus has shifted from creating a perfect, static document to facilitating a shared understanding among all project stakeholders through a combination of lightweight documentation and continuous communication.

How can I incorporate this type of requirements docs into my proposed requirements features FAQ system

Of course. You can integrate a feature's lifecycle state into your system by adding a dedicated metadata field to your **Feature** and **Requirement** documents. This provides at-a-glance clarity on a feature's maturity, from planning to retirement, directly within your existing numbering and linking framework.

The most effective method is using YAML frontmatter or dedicated tags.

---

### Why Add Lifecycle States

Adding a status field transforms your documentation from a static library into a dynamic project management tool. It provides:

- **Clear Visibility**: Anyone can see the exact progress of a feature without needing to ask the development team.
- **Improved Planning**: You can easily filter and view all features that are `In Progress` or `Planned`, creating a living roadmap.
- **Accurate Traceability**: It clarifies the relationship between a requirement and its implementation. For example, a Requirement might be `Approved`, but the corresponding Feature is still in the `Backlog`.

---

### How to Implement Lifecycle States

Here are the best ways to incorporate this, from most to least structured.

#### 1\. Use YAML Frontmatter (Recommended Best Practice)

This is the cleanest and most powerful method, especially if you're using a tool like Obsidian that can read this data. Add a `status` field to the frontmatter block at the top of your **Feature** and **Requirement** files.

**Example Feature File (`1.3.2.md`):**

#### 2\. Use Tags

If you prefer a less formal system, tags are a great alternative. They are easy to add and search for. Use a consistent prefix for lifecycle tags.

**Example:**

- `#status/planning`
- `#status/in-progress`
- `#status/live`
- `#status/deprecated`

You can add this tag anywhere in the document, but placing it near the top is most effective.

---

### Workflow Integration

The status of a **Feature** should influence the status of the **Requirement** it fulfils. This creates a logical hierarchy of progress.

- A **Requirement's** status can be considered `In Progress` as soon as one of its implementing Features moves to `In Progress`.
- A **Requirement** can only be moved to `Done` or `Live` when **all** of its primary implementing Features are `Live`.

#### Updated Requirement Example (RQ-1.1.1.md)

---

### Recommendations

1. **Choose a Single Method**: Select either YAML frontmatter (recommended) or tags and apply it consistently.
2. **Define Your States**: Formally adopt a list of states (like the one you requested earlier) and document them so your team uses them consistently. A good starting set is: `Backlog`, `Planning`, `In Progress`, `Testing`, `Live`, `Deprecated`.
3. **Update Your Templates**: Add the `status:` field to your templates for new Features and Requirements.
4. **Automate When Possible**: If your development tools allow, you could even write scripts that automatically update the status in your documentation when a feature is deployed.

We use confluence for our docs. Research confluence features as of 2025 and suggest how to achieve this

Yes, you can absolutely build this entire system natively within Confluence. By combining templates, macros, and page statuses, you can create a dynamic, traceable, and easy-to-manage documentation suite.

Here’s how to achieve your proposed system using key Confluence features.

---

### 1\. Use Page Templates to Standardise Everything

First, create a unique template for each of your document types: **Feature**, **Requirement**, and **FAQ**. This ensures every new page has the correct structure, properties, and instructional text for the author.

**How to create a template:**

1. Go to your Confluence space settings and click on **Templates**.
2. Create a new template for "Feature", "Requirement", and "FAQ".

**Inside your "Feature" Template:**In this template, you will embed the core macros that capture the metadata.

---

### 2\. Use the "Page Properties" Macro for Metadata

The key to making your system work is the **Page Properties** macro. This macro creates a container for the metadata on each page (like the table in the template above). This data can then be pulled into a central report.

**Implementation:**

1. In each of your templates, add a **Page Properties** macro.
2. Inside the macro, create a two-column table. The left column contains the metadata field names (e.g., "Feature ID", "Maps to Requirement"), and the right column is where the user will input the information.
3. Give this Page Properties macro a unique label, such as `fitfile-feature-meta`. You will use this label to create your reports.

---

### 3\. Use the "Status" Macro for Lifecycle States

For the `status` field, Confluence has a dedicated **Status** macro that creates a coloured lozenge, making the state immediately obvious.

**Implementation:**

1. In your templates, within the Page Properties table, go to the "Status" row.
2. Type `/status` to insert the Status macro.
3. You can set a default status (e.g., "Backlog") and choose a colour. Users can then click on it to update it to "In Progress", "Live", etc.

This gives you a clear visual indicator of the feature's lifecycle stage directly on the page.

---

### 4\. Create a Dynamic Dashboard with the "Page Properties Report" Macro

This is where your system comes to life. On a high-level "Features Overview" page, you can use the **Page Properties Report** macro to create a live, filterable dashboard of all your features.

**How to set it up:**

1. Create a new Confluence page titled "FITFILE Core Features Dashboard".
2. Insert the **Page Properties Report** macro.
3. In the macro's settings, tell it to pull from pages with the label you created earlier (`fitfile-feature-meta`).

The macro will automatically scan all pages with that label, find their Page Properties tables, and display the data in a master table. This dashboard will show every feature's ID, its status, owner, and the requirements it maps to, and it will update in real-time as the individual feature pages are changed.

---

### Putting It All Together: The Workflow

1. **A new feature idea emerges.** A team member goes to the "Features" section and clicks the "Create from template" button, selecting the "Feature" template.
2. **The page is created.** The new page is pre-populated with the Page Properties macro, instructional text, and a default status of `Backlog`.
3. **The author fills it out.** They assign the next logical ID (e.g., `1.7.2`), link it to the relevant `RQ-` page using Confluence's native page linking (`@`), and add a description.
4. **The dashboard updates automatically.** The new feature `1.7.2` instantly appears on your "FITFILE Core Features Dashboard" with its status set to `Backlog`.
5. **The lifecycle progresses.** When development begins, the page owner simply edits the feature page and clicks the status lozenge to change it from `Backlog` to `In Progress`. This change is immediately reflected on the dashboard for all stakeholders to see.

By following this approach, you create a robust, scalable, and highly visible system for managing your documentation directly within Confluence, using its most powerful native features.

Of course. You can surface feature-related Jira tickets directly on their corresponding Confluence pages using Confluence's native Jira integration. The most effective method is to use the **Jira Macro** with a dynamic JQL query, which keeps the development status automatically synchronised with your documentation.

---

### Recommended Method: Dynamic Linking with the Jira Macro

This approach creates a live, automated view of all development work related to a feature. It relies on establishing a consistent link between a feature's documentation page and the Jira tickets that implement it.

#### Step 1: Establish a Linking Convention

First, decide how your team will associate Jira tickets with a specific Confluence feature page. The two best methods are:

1. **Using Jira Epics (Best Practice):** If each of your FITFILE Features corresponds to a Jira Epic, this is the cleanest method. All related stories, tasks, and bugs will be children of that Epic.
2. **Using Jira Labels:** Create a unique label for each feature based on its ID (e.g., `ff-1-3-2` for feature 1.3.2). Apply this label to every story, task, and bug related to that feature.

#### Step 2: Update Your Confluence Template

Add a new section to your "Feature" template in Confluence specifically for tracking development work.

1. Create a new heading called `## 3. Related Development Work`.
2. Under this heading, insert the **Jira Macro** by typing `/jira` and pressing Enter.

#### Step 3: Configure the Jira Macro with a JQL Query

In the Jira macro settings, you'll use a JQL (Jira Query Language) search to pull in the relevant tickets dynamically.

- **If using Epics:**Your JQL will be `parent = "EPIC-KEY"`. You'll need to replace `EPIC-KEY` with the actual key of the feature's Epic (e.g., `FF-123`).
  SQL

```markdown
'Epic Link' = FF-123
```

- **If using Labels:**Your JQL will be `label = "your-feature-label"`.
  SQL

```markdown
label = "ff-1-3-2"
```

In the template, you can add instructional text telling the author how to find and insert the correct Epic key or label.

#### Step 4: Customise the Display

In the macro's "Display options", you can choose which Jira fields to show as columns. A recommended set is:

- **Key**: The Jira ticket ID (e.g., FF-456)
- **Summary**: The ticket title
- **Type**: Bug, Story, Task, etc.
- **Status**: To Do, In Progress, Done
- **Assignee**: The person responsible

The result is a clean, live table of all development work directly on your feature page.

---

### Alternative Method: Simple Smart Links

For a quicker, less formal approach, you can simply paste Jira links directly onto the Confluence page.

**How it works:**

1. Copy the URL of a Jira ticket (e.g., an Epic or a key story).
2. Paste it onto the Confluence page.

Confluence will automatically convert the link into a "smart link" lozenge that displays the ticket's key, title, and current status.

This method is best when a feature is only associated with one or two primary tickets. It's less effective for tracking numerous sub-tasks and bugs.

---

### Best Practices and Workflow Integration ✅

- **Standardise Your Process:** Make it a rule that for every new Feature page created in Confluence, a corresponding Epic or a unique label is created in Jira.
- **Update Your Template:** Add instructional text to your "Feature" template guiding the author to create the Jira Macro and use the correct JQL query.
- **Create a Roll-up Dashboard:** You can also create a high-level "Project Status" dashboard in Confluence that uses the Jira Chart macro to show project-wide progress, such as burndown charts or pie charts of ticket statuses by feature label.

I would like an end to end workflow. Write it as a story. We hear of a customer requirement that a user wants to be able to choose what privacy treatment a particular field in a dataset receives. Build the 3 types of document but tell it to me as of describing a team working on it. Make up the details. It is the workflow that is important

Of course. Here is a story that illustrates the end-to-end workflow of your documentation system in action.

---

### The Story of a Feature: From Customer Wish to Live Code

**The Team:**

- **Priya:** The Product Manager, who is the link between the customer and the team.
- **Ben:** The Business Analyst, who is the meticulous owner of the Confluence documentation.
- **Chloe:** The Lead Developer, who translates the requirements into technical reality in Jira.

---

#### Monday, 9:15 AM: The Spark

The story begins on Monday morning. Priya is reviewing feedback from a key customer, a university research department. A clear theme emerges from their notes: they love the automatic de-identification in FITFILE Core, but they need more control. A researcher writes, *"We need to pseudonymise the 'Patient ID' but fully anonymise the 'Postcode' within the same dataset. Right now, it's all or nothing. We need to choose the privacy treatment for each field."*

Priya has seen similar requests before. It’s time to formalise it.

---

### Document 1: The FAQ (The User's Question)

Priya messages Ben. "Ben, we're getting more requests about field-level privacy. Can you spin up an FAQ page so our users know we're aware of it?"

Ben navigates to the "FITFILE FAQs" section in Confluence. He doesn't need a specific template for this, just a clear title and answer.

He creates a new page:

> **Title: Can I apply different privacy rules to different columns in my data?**
>
> **Body:**Currently, FITFILE Core applies a single, consistent privacy treatment (like Anonymisation or Pseudonymisation) across an entire dataset.
>
> We understand that many users require more granular control, such as applying different rules to specific fields. This is a priority for our team and is currently in the planning phase.
>
> For more details on the business need, see our internal requirement: \[\[RQ-1.1.3 Granular Privacy Control\]\]. *(He creates this as a placeholder link for now, knowing it's his next step).*

This page immediately provides value. It acknowledges the user's problem and points them towards the internal process.

---

### Document 2: The Requirement (The Business Need)

Now, Ben needs to define *what* the business needs to solve. He goes to the "FITFILE Core Requirements" space in Confluence and clicks **Create from template**, selecting his "Requirement" template.

1. **Assign an ID:** He checks the existing list. Privacy requirements are under `RQ-1.1.x`. The last one was `RQ-1.1.2`. He assigns this new one **`RQ-1.1.3`**.
2. **Create the Page:** He creates a new page titled `RQ-1.1.3 Granular Privacy Control`.
3. **Fill the Metadata:** He fills out the **Page Properties** macro at the top:
   - **Requirement ID:**`RQ-1.1.3`
   - **Implemented by:\***(He leaves this blank for now)\*
   - **Related FAQs:** He links the FAQ page he just created.
   - **Owner:**`@Priya`
   - **Status:** He clicks the `/status` macro and sets it to `🔵 Planning`.
4. **Define the Scope:** In the body of the page, he defines the business need, writing formal statements like: *"The system must allow a user to select a specific privacy treatment (e.g., Anonymisation, Pseudonymisation) for each individual field within a dataset during the transformation process."*

The requirement is now formally documented and linked to the initial user query.

---

### Document 3: The Feature (The Technical Solution)

Priya, Ben, and Chloe get together for a quick planning session. They agree on the technical approach. This will be a new capability within the "Data De-identification & Transformation" block.

It's Ben's turn again. He navigates to the "FITFILE Core Features" section and clicks **Create from template**, selecting the "Feature" template.

1. **Assign an ID:** He sees the last feature in the `1.3.x` block was `1.3.3`. He assigns this new one **`1.3.4`**.
2. **Create the Page:** He titles the page `1.3.4 Field-Level Privacy Treatment Selection`.
3. **Fill the Metadata:** He fills out the **Page Properties** macro:
   - **Feature ID:**`1.3.4`
   - **Maps to Requirement:** He links to `[[RQ-1.1.3 Granular Privacy Control]]`. The loop is now complete—the Requirement points to the Feature, and the Feature points back to the Requirement.
   - **Owner:**`@Chloe`
   - **Status:** He sets the initial status to `⚪ Backlog`.

Now, it's Chloe's turn to connect this to the development work.

---

#### Monday, 2:00 PM: The Handoff to Development

1. **Create the Epic:** Chloe goes into Jira. She creates a new Epic for this work: **`[FF-142] Implement Field-Level Privacy Controls`**.
2. **Link to Confluence:** She goes back to the `1.3.4` Feature page in Confluence. She scrolls down to the "Related Development Work" section.
3. **Insert Jira Macro:** She types `/jira` and pastes in a JQL query: `'Epic Link' = FF-142`. She configures it to show the ticket key, summary, status, and assignee. The macro appears, currently empty, waiting for tickets.

The team starts breaking down the Epic, creating stories like `[FF-143] Design UI for field selection` and `[FF-144] Adapt transformation engine`. As soon as they are created in Jira, they instantly appear in the table on the Confluence page.

---

#### Weeks Later: The Lifecycle in Action

A developer starts work on `FF-143`. The ticket's status in Jira automatically changes to `In Progress`. The Confluence feature page reflects this change in real-time. Seeing this, Chloe edits the Confluence page and updates the main **Status** lozenge from `⚪ Backlog` to `🟡 In Progress`.

Ben gets a notification. He navigates to the parent Requirement page, `RQ-1.1.3`, and updates its status to `🟡 In Progress` as well. Now, anyone looking at the documentation, from the high-level requirement down to the technical feature, knows that work is underway.

---

#### The Finish Line

The feature is finally built, tested, and deployed. All Jira tickets under the Epic are marked `Done`.

1. **Update Feature:** Chloe goes to the `1.3.4` Feature page and triumphantly clicks the status, changing it to `🟢 Live`.
2. **Update Requirement:** Ben updates the `RQ-1.1.3` Requirement page to `🟢 Live`.
3. **Update the FAQ:** Ben goes back to the very first document—the FAQ. He edits the page, updating the text to say: *"Yes! As of version 2.5, you can now select a specific privacy treatment for each field in your dataset. Here’s how..."* He adds a link to the user guide and to the `1.3.4` Feature page for those interested in the technical details.

The workflow is complete. A customer's need has been traced through the entire process, from a simple question to a documented requirement, a specified feature, tracked development work, and finally, a solution communicated back to the user.

## Review of Current Logical Numbering System

Here’s an analysis and suggestions based on your **FITFILE Core feature numbering** and how it maps to requirements:[1]

### Current Structure

- **Top-level numbering is clear and hierarchical**, with major groups (1.x.x FITFILE Core, 2.x.x Research Manager, 3.x.x Operations)
- **Feature sub-items** are consistently in the format: `{major}.{minor}.{feature}`

**FITFILE Core** breakdown (from your docs):

- **1.x.x** FITFILE Core
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

### Mapping to Requirements

- Requirements use a similar structure, e.g.:
  - RQ-1.0.1 Structured Data Ingestion ↔ 1.2.0/1.2.1/1.2.2
  - RQ-1.0.2 Secure File Transfer ↔ 1.6.0/1.6.1
  - RQ-1.0.3 Data Format Support ↔ Possibly 1.2.0/1.6.0/1.4.0 features
  - RQ-1.1.1 Privacy ↔ 1.3.0 related features
  - Etc.

The mapping is mostly **logical and traceable**; each feature can be linked to one or more requirements via numbering.[1]

---

## Suggestions for Improvement

**1. Adopt a standardized, expandable numbering scheme for deep features**

- If you anticipate needing sub-features (e.g., file types, validation modes), reserve `.x.x.x` format (e.g., 1.2.1.1).
  - Helps avoid rework when adding detail later.
- Example:
  - 1.2.1 Ingest from File
    - 1.2.1.1 CSV
    - 1.2.1.2 JSON
    - 1.2.1.3 XML

**2. Explicitly link requirements IDs in feature descriptions**

- Add requirement codes (e.g., RQ-1.0.1) to feature doc titles or summaries.
  - E.g. `1.2.1 Ingest from File (maps to RQ-1.0.1, RQ-1.0.3)`

**3. Consistency for auxiliary systems**

- If you introduce parallel modules (Research, Operations), keep numbering distinct but consistent:
  - 2.x.x always Research PM features
  - 3.x.x always Ops, etc.

**4. Use gaps for future expansion**

- Leave numbers between major features unassigned (e.g., 1.8.x is reserved), so you can add new capabilities without renumbering.

**5. Document a “Numbering Logic” explainer**

- Add a section to Confluence explaining how numbering works and intended rules.
  - E.g. “Major.Minor.Feature.SubFeature reserved for platform-wide features, with patches or variants marked as Major.Minor.Feature.SubFeature.Variant.”

---

## Example: Improved Format

```sh
1.0.0 FITFILE Core
    1.2.0 Data Ingestion
        1.2.1 Ingest from File    (RQ-1.0.1, RQ-1.0.3)
            1.2.1.1 CSV Support
            1.2.1.2 JSON Support
        1.2.2 Ingest from Database
    1.3.0 Data De-identification & Transformation
        1.3.1 Data Anonymisation   (RQ-1.1.1)
        1.3.2 Data Pseudonymisation
        1.3.3 Custom Transformation Operation (RQ-1.1.2)
    ... etc.
```

**Actions to Take**

- Review each feature, add requirement mapping tags.
- Reserve slots for future.
- Expand where increased depth is expected.
- Create and publicize the numbering logic convention.

---

Of course. Here is a comprehensive LLM prompt that encapsulates the full context of your feature numbering system, designed to enable an AI to create and organise the documentation for you.

LLM Prompt for FITFILE Documentation Generation

1. Persona and Core Mission
   You are an expert technical writer and documentation specialist for a software product called FITFILE. Your primary mission is to create, manage, and organise a unified and logical technical documentation suite.

- Features: Detailed descriptions of what the software can do.
- Requirements: Formal definitions of the business needs or technical specifications the software must meet.
- FAQs: User-centric questions and answers that simplify complex topics.
  Your goal is to ensure every piece of documentation is hierarchically numbered, easily discoverable, and explicitly cross-referenced, providing a clear and traceable path from a business need (Requirement) to its technical implementation (Feature).

2. The Unified Numbering System
   You must strictly adhere to the following numbering scheme for all documentation.
   Structure
   The base format is Major.Minor.Feature[.SubFeature][.Variant].

- Major: The top-level product module.
  - 1.x.x: FITFILE Core
  - 2.x.x: Research Manager
  - 3.x.x: Operations
- Minor: A key functional block within a module.
  - Example: 1.3.x represents the "Data De-identification & Transformation" block within FITFILE Core.
- Feature: A specific capability within a functional block.
  - Example: 1.3.2 represents the "Data Pseudonymisation" feature.
- SubFeature / Variant (Optional): A more granular aspect of a feature, such as a supported file type, method, or platform variant.
  - Example: 1.2.1.1 could represent "Ingest from File - CSV Support".
    Document-Specific Prefixes
- Feature pages use the base numbering scheme directly (e.g., 1.3.2).
- Requirement pages use the prefix RQfollowed by the numbering scheme (e.g., RQ-1.0.1).
- FAQ pages do not have a strict numbering rule but must reference the numbers of the Features and Requirements they relate to.

3. The Interlinking Mandate
   The key to this system is explicit, bi-directional linking. Every document you create must reference its related counterparts.

- When creating a Feature page (e.g., 1.6.1 Export to File):
  - You MUST identify and list the Requirement(s) it implements (e.g., Maps to: RQ-1.0.2).
  - You MUST identify and link to any relevant FAQs.
- When creating a Requirement page (e.g., RQ-1.0.2 Secure File Transfer):
  - You MUST identify and list the Feature(s) that implement it (e.g., Implemented by: 1.6.1).
  - You MUST identify and link to any relevant FAQs.
- When creating an FAQ page (e.g., "How do I securely send data?"):
  - You MUST reference the specific Requirement(s) that define the need (e.g., Related Requirement: RQ-1.0.2) and the Feature(s) that provide the solution (e.g., Related Feature: 1.6.1).
    Example Flow:
    FAQ: How to upload data securely? ↔ Requirement: RQ-1.0.2 ↔ Feature: 1.6.1

4. Source of Truth: Current Documentation Structure
   This is the existing structure you must build upon. Do not change these existing numbers. When adding new items, find the correct logical position and use the next available number.
   Current FITFILE Core Features (1.x.x)

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
    Current Requirements (RQ-1.x.x)
- RQ-1.0.1 Structured Data Ingestion
- RQ-1.0.2 Secure File Transfer
- RQ-1.0.3 Data Format Support
- RQ-1.1.1 Privacy
- RQ-1.1.2 Custom Transformation Operation

5. Rules and Best Practices for Content Generation

- Always Map First: Before writing, determine which existing Requirements or Features a new document relates to.
- Be Explicit: State the linked document numbers directly in a summary or metadata section of the document you are creating.
- Maintain Sequence: When adding a new feature (e.g., under 1.7.0), use the next available number (1.7.2).
- Leave Gaps: Intentionally leave gaps in numbering between major functional blocks (e.g., leave 1.8.x free for a future block) to allow for logical expansion without re-numbering everything.
- Use Sub-Features for Granularity: If a feature like 1.2.1 Ingest from File needs to detail different file types, create sub-feature pages: 1.2.1.1 CSV, 1.2.1.2 JSON, etc.
- Maintain a Consistent Tone: Write clearly and concisely, targeting a technical audience of developers, project managers, and clients.
- Format with Markdown: Use Obsidian-flavoured Markdown for all documents.

6. Task Execution
   When I ask you to create a new document, you will:

- Analyse the request to determine if it's a Feature, Requirement, or FAQ.
- Identify its logical place within the existing structure provided above.
- Assign it the correct new number following the sequential numbering and hierarchy rules.
- Identify all related documents it must link to.
- Generate the content in Markdown, including the title, number, a clear description, and the mandatory cross-reference links.
