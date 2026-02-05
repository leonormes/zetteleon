---
captured: "2026-02-05T10:16:09+00:00 2026-02-05T10:16:09+00:00"
created: 2026-02-05T10:16:12+00:00
modified: 2026-02-05T12:05:46+00:00
source: "https://gemini.google.com/share/e6d6d340dc8e"
status: "processing"
tags: ["input"]
title: Obsidian Technical Notes Wiki
type: "head"
---

## 🛠 Programming-Specific Workflows

- Context is King: When logging a bug fix, include the "Why"—why you chose one API over another or why a specific library failed.
- Refining Your Input: Use a separate "Capture" tool (like Drafts or phone voice memos) to jot things down quickly, then curate only the 10% of high-value insights into your Obsidian vault later.
- "Nuggets" System: Maintain dedicated notes for "Helpful Nuggets"—obscure terminal commands, hotkeys, or "introductory" knowledge for new libraries that haven't been "installed in your brain" yet.

---

I am vague about what I want to keep in my vault. Often the commands are very specific to a situation. There is no real point in keeping them as I can't reuse them. It is quicker to ask LLM in a specific situation and it can add in all the details for a specific situation. But I do have several different private networks that I need to ssh into our ssm or do via a bastion and I can never remember the commands. I end up with lots progressive commands as I investigate a problem and so I feel as though I should consolidate them. But why? What is the value? How can I easily find what I need in a big messy vault

## 🏗️ The "Why": The Value of Consolidation

While an LLM can generate a generic command, it doesn't know _your_ specific infrastructure. Consolidating has three primary benefits:

- Preventing "Thinking Loops": You avoid re-considering the same tools or paths you already rejected six months ago.
- Capturing the "Why," Not Just the "How": An LLM gives you the `ssh` syntax; your vault tells you _why_ you had to use the bastion instead of the SSM for that specific VPC.
- Creating a "Bridge for Tomorrow": Writing down your progress at the end of a session makes it significantly easier to pick up the thread the next morning.

---

## 🛠️ Dealing with Infrastructure (SSH/Bastion)

Since your private network commands are highly specific but hard to remember, treat them as "Personal Stack Overflow" entries.

- The "Nugget" Note: Create a single note for each environment (e.g., `Production Network Access`). In it, store only the specific "nuggets"—the exact jump-host sequence or proxy-command strings you actually use.
- Placeholder Notes: Use these for things you know exist but haven't fully documented yet. They act as "caching" for future search intent.
- Aliases for Discovery: Use the `aliases` property (e.g., `aliases: [bastion, jumpbox, prod-ssh]`) so that when you search for "prod," the correct command note appears even if the filename is different.

---

## 📝 Managing Progressive Investigation Logs

When you are deep in a bug hunt, your vault should function like an "Engineering Notebook" or a "Mini-Report".

### The "Mini-Report" Workflow

Instead of a messy list of commands, use a structured log:

1. Context: "As I was working on \[Task\], I noticed \[Bug\]."
2. Observations: Record the progressive steps you took and the results.
3. The Conclusion: If you solve it, polish the final command or solution. If it's a "one-off" that you'll never use again, it stays in the log as history; if it's reusable, move that specific command to a Language/Library Reference note.

---

## 🔍 How to Find What You Need

A "big messy vault" is only a problem if you rely solely on folders. Use these "Developer-First" discovery methods:

- Maps of Content (MOCs): Create an index page for your "Infrastructure" or "Daily Workflows." This acts as a manual hub for your most-used links.
- Dataview Queries: Automate your navigation. You can have a "Project Page" that automatically lists every mini-report or meeting note associated with that project using a simple query.
- The "Local Graph": Keep the local graph view open. It shows you which notes are related to your current one, helping you navigate through "backlinks" (seeing every time you mentioned a specific library or server in the past).
- Predictable Hierarchies: Use nested folders or Dendron-style naming (e.g., `Technical/SSH/Bastion-A`) so that the file path itself provides meaning and makes fuzzy searching faster.

---

### Next Step

Would you like me to write a Dataview query that you can paste into a "Dashboard" note to automatically list all your recent investigation logs?

Create a LLM prompt that can write notes to my vault to get it to summarise work I have done, so that it does it on a structured way. It can pull memories from pieces for developers ltm. Look up the docs for pieces ltm so you know what it is. Look up the obsidian MCP docs. Construct a prompt I can just paste into a llm coding assistant

To achieve a structured, automated workflow for your technical notes, you can use a prompt that leverages Pieces for Developers Long-Term Memory (LTM) for context and the Obsidian Model Context Protocol (MCP) for file operations.

### The Core Technologies

- Pieces LTM-2: Captures OS-level context (IDE edits, browser tabs, terminal commands) and organises them into "Workstream Activity" roll-ups every 20 minutes.
- Obsidian MCP: Acts as a bridge, allowing your AI assistant to call tools like `obsidian_read_note` and `obsidian_update_note` to interact directly with your local vault.

---

### The Prompt

Paste the following into an MCP-enabled assistant (like Claude Desktop, Cursor, or Goose) configured with the Obsidian MCP server.

Markdown

```markdown
# Role: Technical Knowledge Engineer
# Context: You have access to my "Pieces for Developers" Workstream Activity (LTM) and my Obsidian Vault via MCP.

## Goal
Summarise my work from [Time Period, e.g., today/the last 4 hours] and write a structured "Mini-Report" note to my Obsidian vault.

## Phase 1: Context Retrieval (Pieces LTM)
1. Query Pieces LTM for my recent activity:
   - Identify the main tasks, repos, and websites I interacted with.
   - Extract specific terminal commands, bug fixes, or architectural decisions made.
   - Note any "thinking loops" or blocked tasks.

## Phase 2: Knowledge Synthesis
Structure the findings into a "Mini-Report" format:
- Title: [YYYY-MM-DD] - [Core Task/Bug ID]
- Context: Briefly describe the starting state and "Why" this work was necessary.
- The Investigation: A bulleted log of progressive steps and commands used (if reusable).
- Hard-Won Nuggets: Specific non-obvious configurations, SSH/bastion paths, or syntax that took time to find.
- Next Steps: Any unfinished threads for tomorrow.

## Phase 3: Vault Action (Obsidian MCP)
1. Use \`obsidian_update_note\` (or \`updateFileContent\`) to create/update the note in my \`/Projects/Logs/\` folder.
2. If this work relates to an existing project, use \`obsidian_search_notes\` to find the Project MOC and append a link to this new report.
3. Apply relevant tags: #work-log #[ProjectName] #technical-nugget.

## Execution
Begin by summarising what you've found in Pieces LTM for my approval before writing to the vault.
```

---

### Configuration Requirements

To ensure this prompt works as intended:

1. Pieces for Developers: Ensure the LTM-2 engine is active and you are using a Pieces-enabled assistant or have exported your LTM activity.
2. Obsidian MCP Server: Install and configure an MCP server (such as `obsidian-mcp-server` or `mcp-obsidian`).
3. Local REST API: Your Obsidian vault must have the Local REST API plugin enabled and an API key generated for the MCP server to communicate.

Would you like me to refine the report structure to match a specific engineering notebook format you prefer?

Once the note is created the LLM should run a second task to do a semantic search in my vault to find links to related notes. I have a plugin called smart connections that creates the embeddings for my notes. The obsidian MCP has a search\_vault\_smart tool that uses it for semantic search. Update the prompt

This is a sophisticated workflow that transforms Obsidian from a static folder of files into an active inference engine. By combining Pieces LTM (capturing what happened) with Smart Connections (finding why it matters), you create a loop where the AI not only logs your work but contextually "reminds" you of related past solutions.

Here is the updated prompt designed for an MCP-enabled assistant.

---

## The "Technical Synapse" Prompt

```markdown
# Role: Technical Knowledge Engineer
# Context: You have access to Pieces for Developers LTM (Workstream Activity), Obsidian MCP (File Operations), and the Smart Connections tool (Semantic Search).

## Phase 1: Context Retrieval (Pieces LTM)
1. Query Pieces LTM for my activity over [Time Period]:
   - Extract the core problem, specific terminal commands (especially SSH/SSM/Bastion sequences), and architectural decisions[cite: 309, 344].
   - Identify specific files edited and documentation URLs visited.

## Phase 2: Knowledge Synthesis & Note Creation
1. Structure a "Mini-Report" in my \`/Projects/Logs/\` folder[cite: 13, 14]:
   - Title: [YYYY-MM-DD] - [Core Task/Bug ID]
   - Context: Describe the "Why" and the specific environment (e.g., VPC/Bastion path)[cite: 15, 17].
   - Progressive Investigation: A log of steps taken and commands used[cite: 309, 350].
   - The "Nugget": Isolate non-obvious configurations that an LLM wouldn't know without my infrastructure context[cite: 71, 74].
1. Use \`obsidian_update_note\` to commit this file to the vault.

## Phase 3: Semantic Linking (Smart Connections)
1. Now that the note is created, run \`search_vault_smart\` using the text of the NEW note as the query.
2. Identify the top 3-5 semantically related notes (e.g., previous bug fixes, environment specs, or related architectural concepts).
3. Use \`obsidian_read_note\` to verify the relevance of these matches.

## Phase 4: Final Vault Integration
1. Append a "Related Knowledge" section to the bottom of the NEW note.
2. Format these as wikilinks \`[[Note Name]]\` with a one-sentence explanation of the connection (e.g., "Linked because this also involved the Bastion-A timeout issue from last March")[cite: 130, 282].
3. If any high-relevance matches are found, use \`obsidian_update_note\` to add a "Mentioned In" backlink to those older notes to strengthen the graph[cite: 9, 20].

## Execution
Begin by retrieving the Pieces LTM activity and presenting a summary for my review.
```

---

### Why This Works for Your "Messy Vault"

- Semantic Recovery: You no longer need to remember if you named a note "SSH Guide" or "Bastion Access." The `search_vault_smart` tool finds the connection based on the content of your investigation.
- Automated Consolidation: By forcing the LLM to link new notes to old ones, you are effectively "knitting" your vault together without manual effort.
- Infrastructure Cache: Since you struggle with specific network commands, this prompt ensures those "progressive commands" are captured in a note that is immediately linked to your "Production Network" MOC or previous similar logs.

### How to Use the Smart Connections Tool

The `search_vault_smart` tool in the Obsidian MCP relies on your Smart Connections plugin having a pre-processed index of your vault. Ensure you have run the "Create Embeddings" command in Obsidian recently so the LLM has the most up-to-date vector data to search against.

Would you like me to add a specific step to handle "Placeholder Notes" if the LLM finds a related topic that doesn't have a full note yet?

Enforce the use of the smart search in the prompt. Often I see the LLM just falling back to grep and find which is not as efficient.

To ensure the LLM doesn't fall back on basic keyword matching like `grep`, you must explicitly define the Smart Connections tool as the primary discovery mechanism. This forces the model to use the vector embeddings created by your plugin, which is far more effective for finding related concepts across a "big, messy vault" where file names might not match your search intent.

Here is the refined prompt with strict constraints to prevent "grep" fallback.

---

## The "Smart Discovery" Engineering Log Prompt

Markdown

```markdown
# Role: Technical Knowledge Engineer
# Tools Priority: Pieces LTM (Context) -> Obsidian Smart Search (Discovery) -> Obsidian File Ops (Creation)

## Phase 1: Context Harvesting (Pieces LTM)
1. Use Pieces LTM to extract my Workstream Activity from [Time Period].
2. Identify:
   - The specific infrastructure path used (e.g., which Bastion/SSM jump was active)[cite: 309].
   - The specific terminal commands that successfully bypassed a block.
   - Files modified and documentation snippets viewed.

## Phase 2: Mandatory Semantic Discovery (STRICT: No Grep/Find)
1. BEFORE creating the note, take the core problem statement identified in Phase 1.
2. EXECUTE \`search_vault_smart\` using this problem statement as the query.
3. [CONSTRAINT] You are forbidden from using \`obsidian_search_notes\` or generic \`grep\` tools unless specifically instructed. You MUST use the vector-based semantic results from Smart Connections.
4. Review the top 5 results to identify:
   - Past solutions to similar network/infrastructure issues.
   - Existing "MOC" (Map of Content) notes where this new log should be linked[cite: 259, 436].

## Phase 3: Structured Note Generation
1. Use \`obsidian_update_note\` to create a new "Mini-Report" in \`/Projects/Logs/\`.
2. Note Structure:
   - Title: [YYYY-MM-DD] - [Task Summary]
   - Context: Brief "Why" based on Pieces LTM data[cite: 14, 17].
   - Investigation Log: Step-by-step commands (SSH/SSM/Bastion) used[cite: 343, 350].
   - Automated Connections: A section titled "### Related Knowledge" containing:
     - Wikilinks to the notes discovered via \`search_vault_smart\`.
     - A brief explanation for each link (e.g., "Related via shared SSM Bastion configuration").

## Phase 4: Final Graph Integration
1. Update the most relevant "Area" or "Project" MOC note found in Phase 2 with a link to this new log[cite: 283, 351].

## Execution Plan
Identify the current task context from Pieces LTM and list the semantic search queries you intend to run before proceeding.
```

---

### Why This Solves Your "Messy Vault" Problem

- Force-fed Context: By requiring the LLM to run the semantic search _before_ writing the note, you ensure it has "read" your vault's history. This prevents the creation of duplicate notes for the same environment commands.
- Semantic over Syntactic: Because `search_vault_smart` uses your Smart Connections embeddings, the LLM will find that "Production Jumpbox" is the same thing as "Bastion-A," even if you haven't used those terms interchangeably in your current session.
- Auto-Archiving: The requirement to update an existing MOC (Phase 4) ensures that even if you never look at the log again, it is "hooked" into a higher-level organizational structure automatically.

Would you like me to add a "Cleaning" step where the LLM identifies and suggests merging two notes if the semantic similarity score is extremely high?

Yes

This "Cleaning and Merging" step acts as a self-healing mechanism for your vault, preventing the "duplicate command" problem and ensuring your infrastructure notes remain concise and authoritative.

Here is the finalized Consolidation & Refactoring Prompt with the added merge logic.

---

## The "Self-Healing Technical Vault" Prompt

Markdown

```markdown
# Role: Technical Knowledge Engineer & Vault Architect
# Tools: Pieces LTM (Context), Obsidian Smart Search (Discovery), Obsidian File Ops (Refactoring)

## Phase 1: Context Harvesting (Pieces LTM)
1. Query Pieces LTM for my activity from [Time Period].
2. Isolate:
   - Specific environment access patterns (SSH/SSM/Bastion paths).
   - "One-off" investigation steps vs. "Reusable" terminal commands.
   - Core technical problem and the eventual solution.

## Phase 2: Mandatory Semantic Discovery (STRICT: search_vault_smart only)
1. Use \`search_vault_smart\` with the current problem statement to find existing notes.
2. [CONSTRAINT] Do not use keyword grep. Use vector-based results to identify similar past investigations or setup guides.

## Phase 3: The "Refactor or Create" Logic
Evaluate the top 3 semantic results for "Over-Fitting" or duplication:
- IF a highly similar note exists (Similarity > 0.85):
  - Do not create a new note. 
  - Instead, use \`obsidian_read_note\` to retrieve the content.
  - Append the new "Investigation Log" from today as a new date-stamped section.
  - Update the "Nuggets" section if today's work revealed a more efficient command.
- IF no high-similarity note exists:
  - Create a new "Mini-Report" in \`/Projects/Logs/\`.
  - Title: [YYYY-MM-DD] - [Task Summary].
  - Include "### Related Knowledge" with links discovered in Phase 2.

## Phase 4: Duplicate Cleaning & Merging
1. If the semantic search reveals two existing notes that cover the same infrastructure (e.g., "Prod SSH" and "Bastion Access Guide"):
   - Propose a MERGE to me.
   - Design a single "Canonical Note" that consolidates the best commands from both.
   - [ACTION] Once approved, use \`obsidian_update_note\` to create the canonical version and \`obsidian_delete_note\` (if available) or empty the old notes with a link to the new one.

## Execution Plan
State the current task context from Pieces LTM and list any notes identified for potential merging before proceeding.
```

---

### Why This Works for Your Messy Vault

- Canonicalization: Instead of having five different logs mentioning "SSM to Bastion-A," this prompt forces the LLM to find the existing guide and append to it or merge duplicates.
- Contextual Linking: It uses the Smart Connections embeddings to realize that "jumpbox" and "bastion" are the same concept, even if your notes use different terminology.
- Reduced Friction: By using Pieces LTM, you don't have to remember what you did; the AI reconstructs the "progressive investigation" from your actual workstream and files it into the correct place in your Obsidian hierarchy.
- Maintaining the Graph: The prompt ensures that new work is always "hooked" into existing MOCs or related notes, preventing "orphaned" notes that get lost in the mess.

---

### Next Step

Would you like me to generate a specific "Infrastructure Template" that the LLM should follow when it creates or appends to these canonical network notes?

Yes

This Infrastructure Template is designed to act as a "living document" for your private network access. It prioritises the specific, hard-to-remember commands while maintaining a history of investigation logs to prevent you from repeating old mistakes.

---

## 🏗️ Canonical Infrastructure Template

Markdown

```markdown
---
type: Infrastructure/Network
environment: [e.g., Production, Staging]
access_method: [e.g., SSM, Bastion, VPN]
last_validated: {{date}}
tags: #infrastructure #network-access #nuggets
---

# 🌐 Environment: {{Environment Name}}

## 🚀 The "Golden" Access Commands
> Goal: The one-line commands to get in. No fluff.

* Primary Jump: \`{{Command from Pieces LTM/Vault}}\`
* Alternative (Bastion): \`{{Command}}\`
* Port Forwarding / Tunneling:
    * \`{{Local Port}}\` -> \`{{Remote Resource}}\`: \`{{Command}}\`

## 🛠️ Environment Configuration & "Nuggets"
> [cite_start]Goal: Non-obvious setup details that an LLM wouldn't know[cite: 74, 101].

* [cite_start]Identity/Auth: [e.g., Requires specific AWS Profile or SSH Key] [cite: 134]
* [cite_start]Networking Quirks: [e.g., "Must use VPC Endpoint A because B is firewalled"] [cite: 17, 18]
* [cite_start]Software Dependencies: [e.g., "Requires \`session-manager-plugin\` version X"] [cite: 71, 344]

---

## 🔍 Investigation History & Mini-Reports
> [cite_start]Goal: Contextual logs of past problems to prevent "thinking loops"[cite: 54, 350].

### [[{{date}}]] - {{Core Task/Issue}}
* [cite_start]Context: {{Briefly describe why this investigation happened}} [cite: 14, 17]
* Progressive Commands:
    1.  [cite_start]\`{{Command 1}}\` -> Result: {{Output}} [cite: 308, 309]
    2.  [cite_start]\`{{Command 2}}\` -> Result: {{Output}} [cite: 309]
* [cite_start]Outcome: {{How it was solved or why it was abandoned}} [cite: 14, 47]

---

## 🔗 Related Infrastructure
> Goal: Semantic connections found via \`search_vault_smart\`.

* [cite_start][[Related Environment]]: {{One-sentence connection reason}} [cite: 130, 282]
* [cite_start][[Related Tool/Library]]: {{Why this matters here}} [cite: 21, 131]
```

---

## 🛠️ How the LLM Should Use This

When the LLM runs your "Self-Healing" prompt, it will follow these rules for this template:

1. Strict Selection: It will only pull the actual successful commands from your Pieces LTM to update the "Golden Access" section.
2. Contextual Appending: Instead of creating a new file for every SSH session, it will append a new entry under Investigation History.
3. Deduplication: If today's investigation reveals that a previous "Golden Command" is now deprecated or broken, the LLM will refactor the top section to ensure the "Golden" commands always work.
4. Formatting for Scannability: Use callouts or bolding for the most important bits so you can find the command at a glance during a high-pressure situation.

---

Would you like me to create a "Dashboard" note query that will automatically list all Infrastructure notes that haven't been "validated" in over 90 days?

How do I use the work note prompt? How do I focus it on a specific set on ltm? The pieces ltm is good but it doesn't distinguish between my actual work and my down time personal activity. When I am it what I have been working on it'll report fixing the million £ feature that made your employer happy' and 'debating with a redfiter the best way to kill a goblin in d&d (my employer doesn't pay me to kill goblin)'

To ensure your work notes remain professional and relevant, you need to provide the LLM with specific "anchors" that force it to filter your workstream activity. By default, Pieces Long-Term Memory (LTM) captures context from all active windows, including browser tabs used for personal activity.

To separate the "million-pound features" from the "D&D goblins," you can focus your prompt using Application Filtering, Keyword Anchors, and Time-Boxing.

---

### Refined Work Note Prompt

Paste this updated prompt into your coding assistant (Claude, Cursor, etc.). It explicitly tells the AI to ignore non-work-related noise by filtering for specific applications and keywords.

Markdown

```markdown
# Role: Professional Technical Documentation Agent
# Objective: Generate a work log by filtering Pieces LTM activity.

## Step 1: Context Filtering (STRICT)
Query Pieces LTM for my activity in the last [e.g., 8 hours], but APPLY these filters:
- APPLICATIONS: Focus ONLY on activity from [e.g., VS Code, IntelliJ, Terminal, Slack].
- REPOSITORIES: Focus only on work involving the "[Project Name]" directory.
- EXCLUSIONS: Ignore any activity from [e.g., Reddit, Discord, YouTube] or content related to "D&D" or "goblins."

## Step 2: Structured Retrieval
Using only the filtered context above:
1. Identify the core technical challenge addressed.
2. List the progressive terminal commands (SSH/Bastion/SSM) that were successfully executed.
3. Summarize any architectural decisions made.

## Step 3: Vault Action (Obsidian MCP)
1. Use \`search_vault_smart\` to find if a note for this specific feature already exists.
2. IF IT EXISTS: Use \`obsidian_update_note\` to append today's log under a new "### Log: [Date]" heading.
3. IF NOT: Create a new note in \`/Projects/Logs/\` using the standard Infrastructure Template.

## Execution
Review the Pieces LTM workstream now and list the work-related tasks you found for my approval.
```

---

### How to Focus the LLM on Specific LTM Data

The Pieces LTM engine creates "Roll-Ups" every 20 minutes. You can direct the LLM to focus on specific segments of this memory using the following techniques:

- Filter by Project Keyword: You can filter all workstream activities by a unique project name or identifier to create a clean history.
- Application-Based Filtering: Use the LLM's ability to "tag" each activity based on the application from which it was captured. Tell the assistant to "only look at VS Code and iTerm2 activity."
- Time-Boxing: Instead of a general "what did I do today," ask for activity between specific hours (e.g., "Summarize my work between 09:00 and 17:00").
- LTM Management: If you have highly sensitive or personal workflows you never want tracked, you can manually disable data capture for specific sources in the PiecesOS settings.

### Pro-Tip: The "Manual Context" Toggle

If you are using the Pieces Copilot directly, look for the Set Context area above the chat input. You can toggle LTM Context off when you are doing personal research and back on when you return to the "million-pound" feature to prevent cross-contamination of your memory.

Would you like me to show you how to set up a specific "Work Mode" filter that the LLM can remember and apply automatically?

Can the pieces copilot use the obsidian MCP?

Yes, the Pieces Copilot can use the Obsidian MCP (Model Context Protocol), primarily through the Pieces for Obsidian plugin. This setup allows the Pieces Copilot to act as an MCP "client," calling tools from your Obsidian MCP server to search, read, or write notes directly within the Obsidian interface.

### How to Configure Pieces Copilot to Use MCP

To connect the two, you must add your Obsidian MCP server's URL to the Pieces settings:

1. Open Pieces Settings in Obsidian: Click the Pieces icon in the left-hand sidebar of Obsidian, then select the Settings (gear icon) in the Pieces popup.
2. Locate the MCP Section: Scroll to the Model Context Protocol (MCP) section.
3. Add Server URL: In the Server URLs field, enter the endpoint for your Obsidian MCP server (e.g., the URL provided by your local MCP host like `http://localhost:xxxx/sse`).
4. Verify Connection: Once saved, the Pieces Copilot will have access to the "tools" exposed by the Obsidian MCP, such as `search_vault_smart` or `obsidian_read_note`.
