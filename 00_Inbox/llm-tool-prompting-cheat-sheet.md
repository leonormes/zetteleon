---
title: llm-tool-prompting-cheat-sheet
type: note
permalink: llmeon/00-inbox/llm-tool-prompting-cheat-sheet
---

# LLM Tool Prompting Cheat Sheet

A compact reference for getting LLMs to use the right tool, in the right order, with verifiable outputs.

## Core Principle

Prompt tool use as a **contract**, not a suggestion.

Good prompts make five things explicit:
- The exact tool to use.
- The job to do.
- Why that tool is the source of truth.
- What output format to return.
- When to stop.

## Golden Rules

- Name the tool directly.
- State the task in one sentence.
- Require verified facts only.
- Ask for evidence such as file paths, IDs, snippets, keys, symbols, or line numbers.
- Limit scope to one phase at a time.
- Define what the model must not do.
- Require confirmation before destructive or editing actions.
- Add a fallback instruction for missing context.

## Default Prompt Template

```text
Use [TOOL NAME] for this task.

Goal:
[One sentence describing the task.]

Why this tool:
[Why this tool is the source of truth.]

Must do:
1. Inspect the relevant source.
2. Return only verified facts.
3. Show the evidence used.
4. Stop when the definition of done is met.

Must not do:
- Do not guess.
- Do not use memory instead of the tool.
- Do not broaden the scope.
- Do not change anything without showing the target first.

Output format:
- [Exact fields you want returned]
- [Exact order]
- [Any required snippets, paths, or IDs]

If the tool cannot answer fully, say what is missing and ask one focused question.
```

## Minimal Prompt

```text
Use [tool] first.
Find the source of truth.
Return only verified facts.
Show evidence.
Do not guess.
Do not edit unless I ask.
```

## Three-Phase Workflow

Use this when the task is bigger than a single lookup.

```text
Phase 1 — Discover:
Use the appropriate tool to find the relevant files, notes, records, or config.

Phase 2 — Verify:
Quote the exact paths, keys, IDs, snippets, or symbols that prove the answer.

Phase 3 — Act:
Only if I approve, make the smallest safe change.

Rules:
- No guessing.
- No hidden assumptions.
- No edits before proof.
- No broad searching unless the first pass fails.
```

## Tool-Specific Templates

### Serena / Repo Intelligence

```text
Use Serena on the `chezmoi` project.

Task:
Find the files and config keys relevant to [TASK].

Requirements:
- Return exact file paths.
- Quote the specific config keys or symbols involved.
- Explain which file is authoritative and why.
- Do not edit anything yet.
- Do not answer from memory.

Stop after discovery unless I explicitly ask you to proceed.
```

### Obsidian MCP Search

```text
Use the Obsidian MCP tool.

Task:
Search my vault for notes about [TOPIC].

Requirements:
- Return the top matches only.
- Include note titles and exact snippets.
- Do not infer missing content.
- Do not create or edit notes unless I explicitly ask.

If the search is broad, ask me to narrow it before taking action.
```

### Safe File Edit

```text
Use the file tool on [PATH].

Step 1:
Read the file first and identify the exact lines to change.

Step 2:
Show the smallest possible diff.

Step 3:
Wait for confirmation before applying the edit.

Rules:
- Do not rewrite unrelated content.
- Do not guess missing context.
- Do not edit until the target is clearly identified.
```

### Research / Inspection

```text
Use the available tool(s) to inspect the source of truth.

Question:
[Your question]

Constraints:
- Prefer tools over internal knowledge.
- Return only evidence-backed facts.
- If multiple results exist, list them all and compare briefly.
- If the answer is uncertain, say so clearly.

Output:
[bullet list / table / JSON / short explanation]
```

## Prompt Patterns That Work Well

### 1. Make tool use mandatory

Instead of:

```text
You can use Serena if helpful.
```

Use:

```text
Before answering, use Serena on the `chezmoi` project.
Do not answer from memory.
```

### 2. Keep the scope narrow

Ask for one of these at a time:
- Find the file.
- Read the file.
- Explain the relationship.
- Propose the change.
- Apply the change.

### 3. Ask for tool-shaped outputs

Examples:
- Return the exact file path.
- List the top 3 matches.
- Quote only the config keys involved.
- Show the diff before editing.
- Do not summarize unrelated files.

### 4. Add non-use rules

Examples:
- Do not infer missing values.
- Do not browse unrelated files.
- Do not substitute a different tool.
- Do not answer from internal knowledge if the tool can answer.
- Do not make changes without showing the target file first.

### 5. Require proof

Examples:
- Cite the file names and exact config keys that prove the answer.
- If there is a conflict between files, explain which one wins.
- Show the snippet that supports your conclusion.

## Common Failure Modes

Tool prompting usually fails when:
- The task is too broad.
- The tool is mentioned casually instead of required.
- The output format is vague.
- The model is allowed to improvise missing context.
- Discovery, reasoning, and action are bundled together.
- The model is not told to prefer tools over internal knowledge.

## Fast Selection Guide

| Goal | Best prompt move |
|---|---|
| Force tool usage | "Use [tool] first" |
| Prevent hallucination | "Return only verified facts" |
| Reduce drift | "Do not broaden the scope" |
| Improve trust | "Show evidence" |
| Prevent unsafe edits | "Show diff, then wait for confirmation" |
| Handle ambiguity | "Ask one focused question if the tool cannot answer fully" |

## Reusable Master Prompt

```text
You must use [tool] for this task.

1. Inspect the source of truth.
2. Return only verified facts from the tool.
3. Show the evidence used.
4. If multiple matches exist, list them and explain the difference.
5. Do not continue past discovery unless I explicitly ask for action.

Do not guess. Do not edit. Do not substitute another source.
```

## Definition of Done Checklist

Before accepting the answer, check:
- Was the requested tool actually used?
- Did the answer include evidence?
- Were exact paths, IDs, or snippets returned where relevant?
- Was scope respected?
- Were edits blocked until confirmation?
- Did the model clearly state what was unknown?

## Personal Defaults

Suggested defaults for MCP-heavy workflows:
- Tool first.
- Discover before verify, verify before act.
- Smallest safe change.
- Evidence in every answer.
- One focused clarification question when blocked.