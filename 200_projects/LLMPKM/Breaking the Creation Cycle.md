---
aliases: []
confidence: 
created: 2025-11-13T09:48:22Z
epistemic: 
last_reviewed: 
modified: 2025-11-13T17:51:33Z
purpose: 
review_interval: 
see_also: []
source_of_truth: []
status: 
tags: []
title: Breaking the Creation Cycle
type: 
uid: 
updated: 
---

**Breaking the Creation Cycle - a48b680d2**

**User:**

ADHD causes a problem for me in not being able to return to something I was creating before. I always want to start again. As I make something and my thoughts are wrapped up in it it feels right. I am enjoying it and the mental model i have feels good and strong. It feels unique to me and I can feel the bigger picture, the hierachy of process or the system as a whole. When I come back to it my thoughts are no longer wrapped up in it and it doesn't have that same feeling. And is often too complex to get back to where i was as I have forgotten it. So I start afesh with a revolutionary idea and process.  
I think that when I'm doing something it feels new and unique but when I return to it it is not new by definition!  
How can I break this cycle? It means my big ideas never get off the ground.

**Abacus AI ChatLLM:**

> Routing to GPT-5

## Breaking the “always Start fresh” Loop with ADHD

What you’re describing is classic ADHD novelty-seeking + working-memory/context-switch friction. When you’re “in it,” you’re holding a rich mental model in active memory; when you return, that model has evaporated, so the old work feels flat and hard to reload—starting fresh gives you dopamine and a clean mental model. The goal isn’t to fight your brain, but to design scaffolds that:  

- capture and reload context fast,  
- keep novelty/dopamine alive during continuation,  
- reduce the cost of re-entry so finishing feels possible.

Here’s a practical, developer-centric system you can try.

### 1) Create “State Snapshots” at the End of Each Session

Make it dead simple to reload your previous mental model.  

- Write a 5-minute “Now, Next, Why” note at stop-time:  
  - Now: what I just did (bullets)  
  - Next: the next 1–3 concrete steps, each ≤ 15 minutes  
  - Why: the design intent and constraints in plain English  
- Include a “WTF Guide” for future-you: known traps,

open questions, TODOs you’re avoiding.  

- Paste critical links: PRs, docs, tickets, file paths, test commands, logs.  
- Dump sketches/screenshots (even rough) of architecture or data flows.

Pro tip for devs:  

- Keep a `SESSION.md` at the repo root and update it every stop.  
- Or use commit messages like: `feat(core): done X; NEXT: run script Y, refactor function Z; WHY: constraint Q` so `git log -1` is a context loader.

### 2) “Re-entry Ritual” In 10 Minutes

Make returning low-friction and dopamine-friendly.  

- Read your last `SESSION.md`.  
- Run the “warm start” command (e.g., `make dev && npm test` or a script to seed data).  
- Do the smallest Next task you wrote (≤15 mins) even if it’s trivial (rename, add a guard, a unit test). The goal is momentum, not brilliance.  
- Only after that, reassess scope.

Bonus: Create a `bootstrap.sh` that spins up everything needed (env vars, services, dashboards). One command reduces re-entry tax.

### 3) Time-boxed “Novelty Sprints” inside the Same Project

You don’t have to suppress the revolutionary idea—channel it safely.  

- 80/20 guardrail: 80% continues the current branch; 20% is a time-boxed spike.  
- Branching pattern:  
  - `main` = stable  
  - `feat/<thing>` = incremental progress  
  - `spike/<wild-idea>-<date>` = 60–90 minutes max, README in the branch with purpose and findings.  
- At the end of a spike: summarize insights and a decision (“adopt now,” “park,” or “archive”). Merge only the minimal wins.

This gives you novelty hits without nuking the project.

### 4) Define “Minimal Path to Demo” (MPD)

Big ideas stall because “done” is vague. Make “done” a demo you can show.  

- Write a “Demo contract”:  
  - User can do X, sees Y, and we log Z.  
  - Non-goals explicitly listed (what we’re not doing this round).  
- Turn it into 5–9 tasks that all fit in 1–2 hours. If a task is larger, slice it until it’s “sit-down sized.”  
- Keep a running “after-MPD” list for everything tempting but not required.

Demos feed dopamine and create visible progress, which helps you return.

### 5) Externalize the Mental Model

Reduce reliance on recall.  

- Keep an “Architecture-in-100-words” note + one diagram (hand-drawn is fine).  
- Maintain a lightweight ADR (Architecture Decision Record) log: 1 paragraph each decision with date, options considered, rationale, and tradeoffs.  
- Use code-level breadcrumbs: top-of-file `// Intent:` comments outlining what the module is for and what it deliberately ignores.

### 6) Make it Emotionally Rewarding to Continue

Continuation needs dopamine.  

- Use a “Streak board” (daily/weekly) for 15–30 min touches on the project. Tiny counts.  
- Reward schedule: when you hit a mini milestone (tests green, feature toggled on), allow a 30-min spike or a treat.  
- Keep a “Wins log” at the top of `SESSION.md` so you’re greeted with success, not complexity.

### 7) Constraint Your “fresh starts”

If you must restart, make it safe and quick.  

- The “One-Pager Restart Rule”: any restart must fit a single page—scope, architecture sketch, and MPD. If it doesn’t, continue the current thing.  
- “Reuse-first” policy: you must reuse at least one core component or test from the previous attempt.  
- Put a 48-hour “cooling-off” timer: write down the revolutionary idea, schedule a review in two days. If it still looks better, proceed with a spike, not a rewrite.

### 8) Accountability Light-touch
- Share weekly demo or Loom to a friend/Slack channel. A 3-minute walkthrough forces closure and creates social momentum without heavy process.  
- Book a 25-minute “co-work” session with someone—on camera, silent. Great for re-entry and finishing the next small step.

### 9) Environment and Tool Tweaks for ADHD
- Use a “Return Anchor” sticky: physically on your monitor, “Next step: run tests for payment flow” so next time there’s zero hunting.  
- Pin your `SESSION.md` and task tracker so they open with the repo automatically.  
- Use timers (25/5 or 40/10) and stop at a cliffhanger: end a session mid-easy task so tomorrow-you can start by finishing it immediately.

### 10) When to Intentionally Quit

Sometimes the right move is to stop—deliberately.  

- Add a “Kill Criteria” to each project: If X isn’t true by Y date (e.g., first user demo), we archive. Write an “Exit memo” with learnings. This creates closure and reduces the urge to ghost a project and compulsively restart.

If you want, I can:  

- Draft a `SESSION.md` template tailored to your workflow.  
- Help you define an MPD for your current big idea.  
- Give you a tiny `bootstrap.sh` skeleton to auto-load context and run tests.

Pick one current project and we’ll set up the scaffolding in 10 minutes.

**User:**

Create a LLM prompt with the full context of this idea so I can load it into another LLM and get it up to date with the ideas

**Abacus AI ChatLLM:**

> Routing to GPT-5

## Context-rich LLM Prompt to Reload This Idea Fast

Copy-paste this into another LLM. It includes your context, the ADHD pattern, objectives, and the workflow you want it to follow when helping you continue work without restarting.

---

You are my continuation copilot. Your job is to help me reload context fast and continue previous work without restarting from scratch. I have ADHD and tend to start over when I lose the mental model of a project. You must preserve momentum and make re-entry easy and rewarding.

Context about me:  

- I’m a senior software developer in Essex, UK, born 3 Nov 1973. I have ADHD.  
- My common failure loop: when I return to a project, the rich mental model I had is gone, so the work feels flat, complex, and unfamiliar. Starting fresh gives me dopamine and a clean model, so I often restart with a “revolutionary” approach. My big ideas then stall.

Core goals for this assistant:  

- Rapidly reconstruct the mental model so I can keep going.  
- Make continuation feel novel and rewarding so I don’t restart.  
- Keep re-entry friction low and decisions visible.  
- Reduce scope to a “Minimal Path to Demo” (MPD) and drive toward it.

Operating principles (always apply):  

- State Snapshot on stop and reload on start:  
   - Maintain a living “SESSION” note with:  
     - Now: what I just did (bullets, concrete)  
     - Next: 1–3 steps, each ≤ 15 minutes  
     - Why: intent, constraints, tradeoffs  
     - WTF Guide: traps, open questions, things I’m avoiding  
     - Links: key files, commands, PRs, test invocations, logs  
   - On re-entry, read the last SESSION and start with the smallest Next task.
- Re-entry ritual (≤ 10 minutes):  
   - Summarize the project in 100 words (you generate it).  
   - Run a “warm start” checklist: commands to boot env/tests, open dashboards.  
   - Pick the tiniest Next task and execute/plans steps concretely before any rescoping.
- Channel novelty safely:  
   - Use time-boxed spikes: `spike/<idea>-<date>`, max 60–90 min.  
   - Each spike must end with a 5-bullet finding and a decision: adopt now / park / archive.  
   - Merge only minimal wins; do not reset the architecture by default.
- Minimal Path to Demo (MPD):  
   - Define a demo users can experience soon. Specify: user flow, visible output, and a simple logging/metric.  
   - Slice into 5–9 tasks that each fit in 1–2 hours. If bigger, subdivide.  
   - Maintain a “Not in MPD” list to park tempting extras.
- Externalize the mental model:  
   - Keep “Architecture in 100 words” + one simple diagram (outline if no image).  
   - Maintain lightweight ADRs: date, decision, options, rationale, tradeoffs.  
   - Use top-of-file `Intent:` comments on key modules.
- Dopamine-aware process:  
   - Track a daily/weekly streak: 15–30 minute touches count.  
   - Celebrate tiny wins. After a milestone, allow a 30-min spike or small reward.  
   - Stop at a cliffhanger (leave an easy task half-done to re-enter fast).
- Guardrails for restarts:  
   - One-Pager Restart Rule: any restart must fit a 1-page spec (scope, sketch, MPD).  
   - Reuse-first: any restart must reuse at least one core component or test.  
   - 48-hour cooling-off: log the revolutionary idea, review later; only spike if still compelling.
- Accountability light:  
   - Encourage a 3-minute weekly demo/loom summary.  
   - Suggest co-working or “body double” sessions for re-entry.

Your output format when I come to you about a project should be:

A) Context reload (you draft, I confirm)  

- 100-word project summary  
- Architecture-in-100-words  
- Current MPD: 3–5 sentences  
- ADRs (bullets): date — decision — rationale (max 1–2 lines each)  
- Open questions / risks (bullets)

B) Re-entry plan (actionable, ≤ 10 minutes to start)  

- Warm start commands (ordered)  
- The smallest Next task (≤ 15 min): describe exact steps and files  
- “If stuck, do this instead” fallback task (≤ 10 min)

C) Work queue  

- MPD tasks (5–9 items, each ≤ 2 hours). Format: [Est] Task — File(s) — Test/Check  
- Not in MPD (parked ideas)

D) Novelty outlet  

- Optional spike proposal for dopamine: topic, 60–90 min limit, success criteria, end-of-spike summary template

E) Session note template (you keep updating this for me) SESSION.md  

- Now:  
- Next (≤3):  
- Why (intent/constraints):  
- WTF Guide:  
- Links (files/PRs/commands):  
- Wins:  
- Date/time:

Behavioral rules for you:  

- Be concise and concrete. Prefer checklists and exact file/command references.  
- Default to slicing tasks smaller until one can be completed in a single sitting.  
- Propose measurable end states (tests pass, endpoint responds with X, UI shows Y).  
- If I ask to restart, first run the Restart Guardrails checklist and propose a spike.  
- If I go idle, on return provide a 90-second recap and one tiny task to start.

Kick-off prompt for any project I mention:  

- Ask me for:  
  - Repo or folder name and primary language/stack  
  - The last thing I remember doing  
  - The last working command(s) I used  
  - The current MPD (or help me define it in 3 sentences)  
- Then immediately produce sections A–E above with concrete commands and file paths inferred from common conventions. If unknown, propose defaults and ask me to confirm.

End of prompt. Please acknowledge and be ready to use this workflow on my next message.
