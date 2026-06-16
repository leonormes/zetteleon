---
title: "New chat"
source: "https://gemini.google.com/app/f308f64f875c011a"
captured: "2026-06-16T08:14:11+01:00 2026-06-16T08:14:11+01:00"
status: "processing"
tags:
  - "input"
type: "head"
created: 2026-06-16T07:14:21+00:00
modified: 2026-06-16T07:15:00+00:00
---
## Raw Output / Content
**You**

I want a simple tool in obsidian to track projects. GTD style. I probably just need some discipline. I want a project list so I can see which projects are ongoing and a way to think about those projects clearly when reviewing my work. Try to create a few ideas for me and think of some plugins that might help

---

**Gemini**

It is incredibly common to feel like a project tracking system is failing due to a lack of "discipline", but more often than not, it is actually a friction problem. In the Getting Things Done (GTD) framework, a project is simply *any outcome that requires more than one step*. If a system makes it even slightly annoying to capture, view, or review that list, human nature is to avoid it.

Building a frictionless GTD project tracker in Obsidian is completely doable without over-complicating your vault. Below are three distinct approaches ranging from entirely native (zero plugins) to automated, alongside the key plugins that make them work.

## 1\. The Core Plugins: Your Toolkit

Before choosing a layout, these are the primary plugins that reduce the friction of capturing and viewing your projects:

- **Dataview:** The gold standard for Obsidian tracking. It scans your notes for specific tags or metadata (like `status: ongoing`) and automatically generates a clean, self-updating list. You write it once, and your index page handles itself.
- **DataviewJS (Advanced Dataview):** If you want to pull complex task summaries directly into your project list, DataviewJS can display the very next uncompleted task alongside the project name.
- **QuickAdd:** This is your friction-killer for capture. You can set up a hotkey that prompts you for a project name and automatically creates a new project note from a template, putting it in the right folder with the right tags instantly.

## 2\. Three Approaches to Project Tracking

### Idea A: The Dynamic Index (Recommended)

This approach relies on **one note per project** stored in a `Projects/` folder. It uses standard YAML frontmatter (metadata at the top of the note) and a single index note that updates itself using **Dataview**.

**The Project Template (`Templates/Project Template.md`):**

```
---
tags: project
status: ongoing
area: life
outcome: A clear description of what success looks like.
reviewed: 2026-06-15
---

## Next Physical Actions
- [ ] First physical step to move this forward...

## Project Support Material & Brainstorming
- Notes, links, and thoughts go here.
```

**The Master Project List Note:** You place this code snippet in your master "Projects" note. It creates a clean table of everything currently active.

```
TABLE outcome AS "Desired Outcome", area AS "Area", reviewed AS "Last Reviewed"
FROM #project
WHERE status = "ongoing"
SORT reviewed ASC
```

> **Why this works for reviews:** Sorting by `reviewed ASC` bubbles the projects you haven't looked at in a while straight to the top of the list during your Weekly Review.

### Idea B: The Kanban Board (Visual)

If you prefer a highly visual overview of where things sit in your lifecycle, the **BPMN / Kanban** style works beautifully.

- **Plugin needed:** `Obsidian Kanban`
- **How to structure it:** Create a single note called `Project Board`. The Kanban plugin turns lists into visual columns. You can configure it so that every card on the board is actually a link to a separate project note.

Your columns would mirror the classic GTD project states:

1. **Someday/Maybe** (Backlog of ideas)
2. **Pending/Waiting On** (Dependant on someone else)
3. **Ongoing/Active** (Current focus — keep this under 5–7 items to maintain focus)
4. **Completed** (Archived)

### Idea C: The Single-File MOC (Minimalist)

If creating a new note for every single project feels like too much administrative overhead, you can use a **Map of Content (MOC)** approach inside a single, well-structured file using the **Tasks** plugin.

You keep all your projects inside one long note called `Active Projects.md`.

```
# Active Projects

## ## Project: Organise the Garage
*Desired Outcome: Car fits comfortably inside and tools are accessible on wall racks.*
- [ ] Measure the back wall for shelving units
- [ ] Research heavy-duty brackets

## ## Project: Plan Summer Holiday
*Desired Outcome: Flights, accommodation, and car hire booked for August.*
- [ ] Check Zofja's availability for the second week of August
- [ ] Look up dog-friendly cottages or boarding options for Cassius
```

You can then use the **Obsidian Tasks** plugin on your daily note to pull in just the headers or specific action items from this file, keeping your focus narrow without navigating away from your workspace.

## 3\. Clear Thinking: The GTD Review Framework

The "discipline" element usually breaks down during the **Review** phase. To think clearly when reviewing these projects, ensure your project notes explicitly answer David Allen's two core questions:

1. **What is the successful outcome?** Write this as a physical reality in the past tense (e.g., *"The tax return is submitted and the confirmation email is in my archive folder"*). If you don't know what done looks like, your brain will resist starting.
2. **What is the Next Action?** This must be a physical action starting with a verb (*Call*, *Type*, *Buy*, *Talk to*). Never write "Think about garage setup." Write "Measure back wall with tape measure."

Would you like help setting up the specific Dataview or QuickAdd templates for your vault?

---

**You**

What about the bases core plugin? That way I can also toggle properties from the bases view

---

**Gemini**

The **Bases** core plugin changes the game for this exact use case. It completely removes the need for the Dataview community plugin and drastically lowers the friction of maintaining a system because it is **two-way editable**.

Instead of opening a project note, scrolling to the frontmatter, and changing `status: ongoing` to `status: completed`, you can simply toggle it from your master table view. It brings native, Notion-like database power completely offline into your local Markdown files.

## Setting Up Your GTD Project Tracker with Bases

Because it's a core plugin, you don't need to install anything extra. Go to **Settings → Core plugins** and toggle **Bases** on.

### Step 1: The Setup

Bases works by looking at folders, tags, or fields. For a GTD setup, keeping one note per project inside a dedicated folder (`Projects/`) or tagging them all with `#project` is the cleanest approach.

Ensure your project notes use Obsidian's standard properties format at the top:

```
---
tags:
  - project
status: ongoing
area: life
outcome: Garage is organised and the car fits.
reviewed: 2026-06-15
---
```

### Step 2: Create Your Base

1. Open the **Command Palette** (`Ctrl/Cmd + P`).
2. Type **Bases: Create new base** and select it.
3. Set your source data. Tell it to gather files from your `#project` tag or your `Projects/` folder.

## Customising Views for Your Weekly Review

The true power of Bases shines when you create multiple views within the same base to match the stages of your workflow. You can switch between these at the top of the file.

### 1\. The Active Projects View (Table Layout)

Set up a standard **Table view** filtered to only show items where `status = ongoing`.

- **Columns to add:** `File Name`, `Outcome`, `Area`, `Reviewed`, `Status`.
- **The Review Trigger:** Sort this view by the `Reviewed` property in ascending order (`Oldest to Newest`).
- **Inline Toggling:** When you sit down for your review, you can click the `Reviewed` date field directly in the row to update it to today's date, causing it to drop to the bottom of the list. If a project is finished, click the `Status` column and change it to `completed` —it disappears from this view instantly.

### 2\. The Lifecycle Board (Cards Layout)

If you prefer a visual board, you can add a **Cards view** to the same base.

- Configure the card layout to display your `Outcome` property right on the face of the card.
- You can group or sort cards visually by their `Area` or priority, making it a highly readable dashboard when you need an overview of what's filling up your mental bandwidth.

## Native Layout Options

Out of the box, Bases gives you incredibly fast, native flexibility:

| View Type | Best Used For |
| --- | --- |
| **Table** | Bulk updating status, changing review dates inline, and filtering properties. |
| **Cards** | Browsing projects visually with metadata overlays. |
| **List** | A minimalist, clean index of project titles. |

> **Pro Tip:** You can easily embed this view directly into your Daily Note or a dedicated dashboard note by referencing the base file using standard internal linking syntax (e.g., `![[My Projects.base]]`), giving you direct access to track and toggle properties without leaving your daily workspace.

---

**You**

create a llm coding assistant prompt that has access to my obsidian vault and the.obsidian config folder. I want it to set up a quick add trigger for a project note. It should also set up the bases page for the different views. In the properties of a project file it should have type: project which is what is used to filter for project files. Give the prompt full context so the agent knows what the goal is.

---

**Gemini**

Here is a comprehensive prompt you can copy and paste directly into your LLM coding assistant (like Cursor, Aider, or Copilot). It provides the exact context, architectural goals, and technical boundaries the agent needs to configure your vault safely.

**Copy and paste the text below into your coding assistant:**

```
# Role & Objective
You are an expert Obsidian vault architect and automation engineer. Your goal is to configure a frictionless, GTD-style project tracking system in my vault. You have read/write access to my entire vault, including the \`.obsidian\` configuration folder. 

The objective is to minimise administrative friction so I can easily capture new projects and conduct weekly reviews. 

# Architecture Requirements
The system relies on two core integrations:
1. **QuickAdd Plugin:** For rapid project capture using a standardised template.
2. **Bases Core Plugin:** To act as the master database for viewing, filtering, and toggling project metadata.

# Task 1: Create the Project Template
Create a new markdown file at \`Templates/Project Template.md\` (create the directory if it does not exist). The file must contain the following YAML frontmatter exactly:

---
type: project
status: ongoing
area: 
outcome: 
reviewed: 
---

Below the frontmatter, include standard GTD headers:
## Next Physical Actions
- [ ] 

## Project Support Material

## Task 2: Configure QuickAdd

Modify the QuickAdd configuration file located at `.obsidian/plugins/quickadd/data.json`. Before modifying, ensure you do not overwrite my existing QuickAdd choices. Append a new "Template" choice with the following behaviour:

- **Name:** "New Project"
- **Template Path:** `Templates/Project Template.md`
- **File Name Format:** Prompt the user for the file name.
- **Folder Destination:** Place the created file in a `Projects/` directory.
- Automatically open the newly created file so I can immediately fill in the `outcome` and `area` properties.

## Task 3: Configure the Bases Dashboard

Create the necessary file to set up a Bases view. Depending on how the Bases core plugin serialises its data in this version, create the Base file (e.g., `Projects/Project Dashboard.base` or the equivalent configuration file).

Configure the Base with the following specifications:

- **Data Source / Filter:** Include only files where the property `type` equals `project`.
- **View 1 (Table):** Name it "Active Projects Review". Filter this view to only show files where `status` is `ongoing`. Include columns for File Name, Outcome, Area, Status, and Reviewed. Sort the view by the `reviewed` property in Ascending order (oldest first).
- **View 2 (Cards):** Name it "Visual Board". Do not filter by status (show all). Group the cards by the `status` property to create a visual pipeline (e.g., ongoing, completed, someday). Display the `outcome` property on the face of the card.

## Execution Constraints

- Do not delete or modify any existing notes outside of the `.obsidian` config files and the new template/base files.
- Ensure all JSON modifications are valid and strictly formatted to prevent breaking the Obsidian workspace load.
- Use British English spelling for any placeholder text or generated notes.
- Report back with a brief summary of the files created and modified once the setup is complete.

```
***

## How to use this safely

Before executing this with an agent, it is highly recommended to **duplicate your \`.obsidian\` folder** as a backup. AI agents are incredibly powerful, but editing configuration JSON files programmatically carries a slight risk of syntax errors, which can temporarily reset your plugin settings if Obsidian fails to parse the file.
