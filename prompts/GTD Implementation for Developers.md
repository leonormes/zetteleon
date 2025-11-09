---
aliases: []
confidence:
created: 2025-10-26T10:22:26Z
epistemic:
last_reviewed:
modified: 2025-10-30T14:04:40Z
purpose: Designs a GTD-based Todoist structure for a software developer to solve the '@Computer' context overload by introducing energy-based labels (@DeepWork, @QuickWins) and advanced filters for managing tasks by cognitive state.
review_interval:
see_also: []
source_of_truth: []
status:
tags: []
title: LLM Prompt_ GTD Implementation for Developer W
type: prompt
uid:
updated:
version: "1"
---

**Context and Goal:** I am a software developer leveraging the **Getting Things Done (GTD)** methodology to manage my professional and personal life. My current challenge stems from the fact that most of my actions fall under a single context, `@Computer`, which contains a large volume of disparate tasks. This leads to inefficient **context switching** and inhibits my ability to perform **deep work** on focused outcomes, such as completing a single Jira ticket [i, 624, 635]. My goal is to design a Todoist structure that maintains **project continuity** (vertical coherence) while maximizing the efficiency of **Next Action lists** (horizontal management) [1-4].

**Core Theoretical Frameworks to Emphasize:**

1. **GTD Distinction:** The system separates **Projects** (desired outcomes requiring more than one step, providing coherence/Horizon 1) from **Next Actions** (the single physical, visible action required to move a project forward, organized by context/Ground Level) [5-11].
2. **Horizontal Efficiency vs. Vertical Focus:** Context lists group actions by the available tool or location to enable intuitive selection based on current constraints (Context, Time, Energy) [12-15]. Project continuity is maintained primarily through the **Weekly Review**, which ensures every project has a defined next action in the system [3, 16-20].
3. **WIP Management/Flow:** Excessive Work-In-Progress (WIP) is a major time thief that compromises quality and concentration [21-23]. Maximizing **flow** (focused motivation and complete absorption) requires limiting WIP and maintaining a "do not disturb" ethos for deep work [22, 24, 25].

**Problem Definition: The `@Computer` Overload**

The generic `@Computer` context is insufficient because it groups tasks by **tool** but fails to differentiate by **required cognitive state** or **energy level** [i, 175]. When lists exceed 50–150 items, unproductive time is spent on sorting and deciding [26]. The solution must subdivide the context to reduce **mental friction** and support focused concentration on singular goals, minimizing the time spent thinking about work ("thinking of it") versus engaging in work ("thinking about it") [27-30].

**Proposed Implementation Strategy for Todoist:**

The existing `@Computer` Next Action context must be divided into functional subcategories using Todoist labels or nested projects to categorize tasks by the required effort [15, 26, 31]:

1. **High-Focus Work (Vertical Coherence):** For complex tasks requiring sustained effort, such as completing a specific Jira ticket or drafting a major document [i, 252].
    - *Proposed Context Label:* **`@DeepWork`** (Requires 60+ minutes, high energy, and no interruptions) [32, 33].
2. **Low-Focus Work (Horizontal Efficiency):** For quick, simple tasks that fill "weird time" or low-energy moments [34, 35].
    - *Proposed Context Label:* **`@QuickWins`** (The two-minute rule applies here, or tasks requiring minimal mental horsepower, often referred to as "Brain Gone" or "Less Than 5-Minute" actions) [36-40].
3. **Connectivity Constraint:** To handle time away from connectivity (e.g., plane travel) [41].
    - *Proposed Context Labels:* **`@Online`** (Requires connectivity/Web access) and **`@Offline`** (Requires computer but no internet connection) [41].
4. **Temporary Vertical Focus:** For intense periods, a temporary list or tag (e.g., `@Focus-Ticket-XYZ`) can be used to pull related actions from different contexts into a single view for rapid execution, serving as a self-imposed WIP limit for that period [25, 31, 42].

**Request for Todoist Structure Research:**

Based on the synthesis above, analyze how to best implement this structure in Todoist. Specifically, generate a plan detailing:

1. **Project Structure:** How to organize the *Projects List* (Horizon 1) [5, 8].
2. **Labels (Contexts):** How to define and use the core labels (`@DeepWork`, `@QuickWins`, `@Online`, `@Offline`, `@Calls`, `@Errands`, etc.) [43, 44].
3. **Filters:** How to create Todoist Filters to efficiently retrieve the right tasks based on a combination of project, energy level (labels), and available time, allowing for intuitive, moment-to-moment choices [20, 45].
4. **WIP Mechanism:** How to use Filters or labels to enable a self-imposed WIP limit on the `@DeepWork` list (e.g., showing a maximum of 3 Deep Work tasks at a time) [25, 42].

To implement GTD for developer workloads in Todoist while resolving the `@Computer` context overload, use a combination of refined project organization, energy-based context labels, and focused filters. This approach supports both project continuity (vertical coherence) and next-action efficiency (horizontal management) by enabling rapid task retrieval for deep work, low-energy tasks, and work-in-progress (WIP) control[^1_1][^1_2][^1_3][^1_4][^1_5][^1_6].

## Project Structure (Horizon 1)

- Create top-level *Projects* for all GTD "outcomes" that require more than one step, e.g., "Client Onboarding Workflow," "Upgrade API Authentication," or "Prepare Conference Talk"[^1_1][^1_2][^1_3].
- Use parent projects for "Areas of Focus" (like "Work" and "Personal") and nest actual outcome-driven projects underneath. This helps maintain a clean, context-rich sidebar while highlighting only active projects as needed[^1_2][^1_7].
- Maintain reference Projects for support lists: "Waiting For," "Someday/Maybe," "Reference," and templates for Weekly/Project Reviews[^1_1][^1_3].

## Labels (Contexts/Energy)

- Replace @Computer with more actionable, state-based labels:
  - `@DeepWork`: For cognitively demanding, high-focus sessions (1+ hour, no interruptions)—e.g., completing a feature or debugging a significant issue[^1_8][^1_4].
  - `@QuickWins`: For <5-minute tasks, or those requiring little concentration—e.g., reply to a Slack message, rebase a PR[^1_6].
  - `@Online`: Requires internet (e.g., research stackoverflow, work on a cloud VM)[^1_5].
  - `@Offline`: Purely local work (e.g., code documentation, cleaning filesmill)[^1_5].
  - Commonly used GTD contexts: `@Calls`, `@Errands`, `@Waiting`, etc.[^1_6][^1_9][^1_10].
  - For optional advanced management, use projector ticket-specific WIP labels, e.g. `@Focus-Ticket-1234`, to collect all subtasks/action items needed for a high-priority outcome[^1_3].
- Add and use these labels directly in task quick add (e.g., "Fix bug in login @DeepWork @Online")[^1_6][^1_5].

## Filters (Next-Action and WIP Control)

- Use Todoist’s advanced filter syntax to surface the right Next Actions at the right moment. Example filters include[^1_4][^1_11]:
  - **Deep Work Filter** (show max 3 high-focus items):
    - Query: `@DeepWork & !@Waiting & !@Someday`, with a manual review or "limit to 3 tasks" note in filter description (there is no built-in hard limit; discipline is enforced by process)[^1_4][^1_11].
  - **Quick Wins**:
    - Query: `@QuickWins & today`, or simply `@QuickWins` to list all low-effort candidates.
  - **Offline Coding**:
    - Query: `@Offline & @DeepWork & #Work`, for focused, internet-free sessions.
  - **Project-Specific Focus**:
    - Query: `@Focus-Ticket-1234 & (today | overdue | next 7 days)` or use board view for temporary vertical stacks.
  - Add the most critical filters to Favorites for rapid sidebar access[^1_4][^1_11].

## WIP Mechanisms

- Use a dedicated focus label (e.g., `@Focus`) and apply it to a max of 3 urgent/discretionary items for the next work sprint/block. A weekly/daily review process should enforce clearing/winnowing this focus list before adding new ones[^1_8][^1_4].
- Combine filters for secondary WIP control: e.g., `@DeepWork & !@Focus` (hidden queue), or `@DeepWork & 3` (TODO: Manual sort; describe in review process)[^1_4].
- Emphasize the use of the Weekly Review to adjust, replenish, and clear focus/priority contexts while validating each project’s next action[^1_1][^1_3][^1_12].

***

## Example Structure Overview

| Component | Implementation in Todoist |
| :-- | :-- |
| Projects | Work (parent) → "Feature X Release", "Jira-Ticket-2423", "DevOps Audit"... |
| Reference Lists | Waiting For, Someday/Maybe, Templates (as projects at bottom of sidebar) |
| Labels (Contexts) | @DeepWork, @QuickWins, @Online, @Offline, @Calls, @Errands, @Focus-Ticket-XXXX |
| Filters | Deep Work Today: `@DeepWork & today & !@Waiting` |
|  | Quick Wins: `@QuickWins & today` |
|  | Online Only: `@Online & today` |
|  | Work-In-Progress: manual max 3 using `@Focus` or similar |

This structure maintains clear vertical context for project reviews and maximizes horizontal efficiency when selecting tasks by immediate effort, energy, or location constraints[^1_1][^1_2][^1_3][^1_4]. Filters and labels can be progressively refined to match evolving team habits or work modes, and WIP discipline is maintained via intentional review, not automation[^1_8][^1_4][^1_12].
