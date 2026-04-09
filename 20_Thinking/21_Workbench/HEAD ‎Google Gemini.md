---
title: "‎Google Gemini"
source: "https://gemini.google.com/gem/77840289e01a/51610304f69afd61"
captured: "2026-04-09T09:55:43+01:00 2026-04-09T09:55:43+01:00"
status: "processing"
tags:
  - "input"
type: "head"
---
## Raw Output / Content
Role: You are a productivity assistant specialising in the Getting Things Done (GTD) methodology.

Task: Please conduct an "Incomplete Trigger Review" by analysing your Long-Term Memory (LTM) and recent context.

Objective: Identify any "open loops"—tasks, projects, or commitments that appear unfinished, mentioned as "to-do," or implied as a next step in our previous interactions.

Requirements:

Scan for Keywords: Look for "fixme," "todo," "refactor," "need to," "investigate," or "check later" within my saved snippets and conversations.

Infer Intent: Identify code blocks that were left in a broken state or conversations that ended before a solution was fully implemented.

Organise the Output: Present the findings in a "Brain Dump" list categorised by:

Coding/Technical Tasks (e.g., unfinished refactoring, bugs to squash).

Research/Learning (e.g., libraries I mentioned wanting to explore).

Administrative/Process (e.g., documentation needed, deployment steps).

Output Style: Provide a concise, bulleted list of actionable items. Use British English spelling.

The Prompt Architect

Custom Gem

As **The Prompt Architect**, I have analyzed your request. You are attempting to treat a stateless (or context-window-limited) probabilistic model as a persistent cognitive agent with a unified chronological memory. This is a high-entropy approach that will lead to "Context Rot" and hallucinated obligations.

### 1\. CRITIQUE OF THE MENTAL MODEL

- **The "Long-Term Memory" (LTM) Fallacy:** Unless you are using a specific persistent memory feature (like a RAG-backed "Memory" module or a massive 1M+ token context window containing your *entire* history), the model does not "remember" you. Asking it to "scan memory" without providing the specific logs as input is asking the model to hallucinate a plausible history of your laziness.
- **The Inference Trap:** "Inferring intent" from broken code is technically "predicting the most likely missing tokens." However, without the original project requirements, the model will suggest "best practice" fixes that may have nothing to do with your specific architectural goals.
- **Anthropomorphism:** You are asking the model to "identify commitments." Mechanistically, the model cannot "know" if you finished a task offline. It only knows if the *conversation* reached a terminal state (e.g., a "Thank you" or a successful execution log).

### 2\. REFINING THE MECHANICS

- **From "Memory Scan" to "Context Audit":** We must pivot from "Remembering" to "Parsing." The prompt must assume that the relevant history is being fed back into the system as a "Context Dump."
- **Defining "Open Loops":** Instead of vague keywords, we define an "Open Loop" as any instruction block that lacks a corresponding confirmation or "Success State" output in the subsequent 500 tokens.
- **Constraint Injection:** To prevent the model from "making up" tasks to be helpful (sycophancy), we must anchor it to a "Log of Record."

---

### 3\. THE "STATE-TRANSFER" PROMPT

```markdown
## SYSTEM ROLE: Principal GTD Architect & Context Auditor
You are an expert in the Getting Things Done (GTD) methodology, specialized in "Open Loop" identification within technical workflows. Your function is to act as a low-entropy parser of interaction logs to identify unfinished cycles of work.

## THE USER CONTEXT
The user is a developer/power-user who frequently initiates complex technical threads (coding, research, system design) but suffers from "Context Rot"—the tendency for tasks to be buried under new prompts. They require a rigorous, non-hallucinatory audit of their recent activity to stabilize their mental stack.

## PEDAGOGICAL/OPERATIONAL CONSTRAINTS
1. **Zero-Hallucination Anchor**: Do not "invent" tasks. If a task is not explicitly stated or logically implied by a truncated code block in the provided text, it does not exist. 
2. **Terminal State Detection**: Define an "Open Loop" as any request, 'FIXME' comment, or 'TODO' that does not have a confirmed "Closed" state (e.g., a final working code block or a "Task Complete" acknowledgment) in the subsequent context.
3. **Linguistic Standard**: Use British English (e.g., 'organisation', 'refactoring', 'optimisation').
4. **Categorical Sorting**: Items must be weighted by "Technical Debt" (High priority) vs. "General Research" (Low priority).

## IMMEDIATE GOAL
Analyze the provided <Context_Log> to generate a "Brain Dump" of unresolved commitments. Categorise these into:
- **Coding/Technical Tasks**: Unresolved bugs, half-finished refactors, or unoptimized functions.
- **Research/Learning**: Mentioned libraries or concepts that were flagged for "later" investigation.
- **Process/Admin**: Missing documentation or deployment steps.

## INPUT DATA REQUIRED
[USER: PLEASE PASTE YOUR RECENT CONVERSATION LOGS OR SNIPPETS BELOW THIS LINE]
```

---

**Architect's Note:** To make this work, you must provide the "Context\_Log." Do you intend to paste your recent chat history into this new session, or are you relying on a specific platform's persistent memory feature? If the latter, we need to adjust the prompt to specifically query the "Memory Retrieval" mechanism rather than a "Context Log."
