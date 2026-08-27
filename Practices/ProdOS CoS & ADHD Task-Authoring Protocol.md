---
author: Hermes (consolidation)
created: 2026-08-26 07:16:07+00:00
modified: 2026-08-26 07:25:16+00:00
permalink: llmeon/00-inbox/head-cos-prod-os-protocol-task-organization
tags:
  - prodos
  - cos
  - adhd
  - executive-function
  - todoist
  - task-management
  - gtd
  - personal
  - input
title: HEAD COS prodOS protocol task organization
type: note
source: https://claude.ai/chat/178d7c69-c2ec-4ce4-a3b2-df2094318dac
captured: 2026-08-26T12:54:51+01:00 2026-08-26T12:54:51+01:00
status: processing
---

# ProdOS CoS & ADHD Task-Authoring Protocol — Consolidated Notes

Single consolidated reference for the personal productivity system, merged from two `00_Inbox/` captures (2026-08-18 + 2026-08-26). **This is the personal/ProdOS system, not FitFile work** — the work tasks (FTFL-868/619/942 etc.) are the *instances* the protocol was tested on, not the content.

The two halves: the **CoS Query Engine** (the LLM sweep architecture that produces tasks) and the **ADHD Prosthetic Task-Authoring Gate** (the six-field task format the CoS must emit). Together they externalise executive function: the CoS offloads the cognitive work the ADHD brain can't reliably do internally.

---

## 1. Source Index

| # | Source (original `00_Inbox/` file) | Date | Half |
|---|---|---|---|
| A | `Plan - ProdOS CoS Query Engine.md` | 2026-08-18 | CoS Query Engine architecture + implementation phases |
| B | `ADHD Prosthetic Executive Function Process.md` | 2026-08-26 | ADHD neuroscience + six-field task-authoring gate + rollout |

---

## 2. The Vision — LLM CoS as Executive-Function Prosthetic

A single unified protocol where the LLM **sweeps all inboxes → aggregates open loops → prioritises → pushes ADHD-optimised starter tasks to Todoist → logs** — one pass, zero context switching.

For an ADHD neuro-profile, standard Agile/GitHub-style tickets feel open-ended because the brain's DMN stays active (see §3), producing task paralysis. The CoS is not a passive task aggregator — it is an active **"Constraint Guardian"**: it enforces clarity before you start, externalises sequencing, and forces clean closure so you can switch.

### Inboxes swept (gather layer)

| Inbox | Data source | Contains |
|---|---|---|
| Teams Calendar | Events API / calendar scan | Meetings, deadlines, time blocks |
| Pieces LTM | REST API (`:39300/messages`) | Ambient context, recent work fragments |
| FitFile Email | ?? (needs scoping) | Actionable emails, requests, decisions |
| Jira (FTFL) | `cos-jira-fetch.py` (REST) | Open tickets, sprint work, blockers |
| GitKraken / GitLab | `gk pr list` (gk CLI) | Open MRs, CI status |
| Todoist | Todoist REST API v1 | Stale starter tasks, unprocessed captures |
| Obsidian vault | `obsidian files` / MCP | Unprocessed inbox notes, open HEAD notes |

### Current state (as of source dates)

**Already exists / proven:** `cos-work-review` skill (production), `routine-cos-synthesis.md`, `gk` CLI for GitLab/Jira, 2 successful end-to-end runs (12:26 + 12:57 pushed starter tasks), open HEAD note `How to unify the CoS Query Engine.md`.

**Missing then (most since landed):** Teams Calendar not polled · FF Email not checked · Pieces query not unified in cron flow · no prioritisation engine (now: urgency scoring in `cos-prioritise.py`) · Todoist push not asked first (AGENTS.md permission rule) · no single trigger (now: `cos-sweep` skill + `cos-sweep.py` script) · Obsidian `00_Inbox/` not checked.

---

## 3. ADHD Neuroscience — Three Independent Mechanisms

Research synthesis: these are **not willpower problems**. Three separately-studied neural deficits, each with a specific countermeasure.

### Mechanism 1 — DMN/TPN interference → task paralysis

- Neurotypical: Task Positive Network (TPN) cleanly suppresses Default Mode Network (DMN) during focused work.
- ADHD: DMN fails to deactivate → **simultaneous activation** → continuous internal cross-talk (tangential thoughts, anxieties, associative thinking).
- Open-ended ticket → DMN generates implicit requirements → overwhelms limited working memory → system shuts down; procrastination as protective mechanism.
- **Key finding:** not comprehension failure or low motivation — direct neural dysregulation. Russell Ramsay's "implementation deficit" framing.

### Mechanism 2 — Delay discounting → can't visualise completion

- Hypodopaminergic frontostriatal circuits + DLPFC (future-goal holding). Dopamine regulates reward anticipation/salience → **steep delay discounting** (value of a reward collapses with time distance).
- An open-ended ticket = delayed, abstract reward → brain fails to generate dopaminergic momentum for initiation.
- **Key finding:** you can't visualise finishing — not for lack of trying, but because the internal machinery that generates the image is under-resourced. Corroborates Barkley's "temporal myopia".

### Mechanism 3 — Attention residue → can't switch to next task

- **Attention residue** (Leroy 2009): after switching, significant cognitive processing stays allocated to the previous task. Worst when: task left incomplete (open loop), deep engagement, self-initiated interruption.
- **Set-shifting** (unhooking + relocking attention) relies on working memory + inhibitory control — both compromised in ADHD.
- **Hyperfocus** as compensatory mechanism locks attention so tight that switching needs a massive reset — residue clings like a background app draining RAM.
- Costs: **23 min 15 s** to fully refocus after interruption (Gloria Mark, UC Irvine); 2.26 intervening tasks; ~1,200 app toggles/day; up to **40% of productive time** lost to switching; ~$450B/yr US estimate (widely cited, no single traceable source).

---

## 4. Evidence-Based Mitigations

| Mitigation | Mechanism it counters | What it is | In the protocol |
|---|---|---|---|
| **Episodic Future Thinking (EFT)** | Delay discounting (Mech 2) | Mentally project into the future, vividly imagine completion/reward. Process-focused and outcome-focused variants both effective; narrative EFT (NEFT) stronger. Activates prefrontal-mediotemporal goal salience. | The **"Done means"** field = externally-generated prospection standing in for the weaker self-generated version; **"Steps"** = process-focused variant. |
| **Implementation-focused CBT** | Task paralysis (Mech 1) | Ramsay/Safren: granular hyper-specific micro-action breakdown + written **"behavioral prescriptions"** (exact steps, anticipated barriers, pre-decided responses). Counteracts "procrastivity" (avoiding high-priority via lower-priority-but-productive work). Standard "use a planner" advice fails because it assumes intact time perception + initiation. | **"Steps"** = physical micro-actions in order; **"If stuck"** = behavioral prescription: [likely blocker] → [pre-decided response], bypassing the decision at peak depletion. |
| **Ready-to-Resume Plan (Leroy & Glomb 2018)** | Attention residue (Mech 3) | Write the exact next physical action / acknowledge completed state → signals state saved outside working memory → satisfies closure (Zeigarnik) → DMN releases the task. People who wrote the note were **~80% more likely** to reach the right call afterward vs switching cold. | **"On stop"** field: done/not done — blocker — next micro-step. Written *before* start so the exit criterion is pre-defined; filled at session end to close the loop. |
| **Time-blocking vs time-boxing** | Overwhelm / perfectionism (all) | *Blocking* = reserve calendar space. *Boxing* = **unyielding constraint**: fixed block, hard stop when the timer rings regardless of completion. Caps perfectionism; exposes time theft; replaces "will I finish perfectly?" with "what fits in this box?" | CoS Pre-Flight Negotiation: "You have 30 min — what is the exact visualisable output?" Reject over-broad answers; slice until it fits. Energy-match box duration (15–30 min). |
| **Somatic Switch / Somatic Initiation** | Inertia on transition (Mech 3) | Brief unrelated physical movement after a hard stop to force TPN online and sever the previous cognitive loop. | CoS hard-stop routine: Guillotine (stop at time) → State Capture (one sentence, next action parked) → Somatic Initiation. |
| **AI metacognitive scaffolding** | All — offloads executive burden | LLM as non-human dialogic agent: next-physical-step prompts (the "bottom rung"), digital body doubling (narration anchor), reframing the wall of overwhelm (brain-dump → top-3), RSD-safe emotional container. A "scaffold that disappears". | See §5 task fields. ⚠️ See §8 for the learned-helplessness risk. |

---

## 5. The CoS Query Engine — Gather → Synthesise → Prioritise → Push → Log

```
1. GATHER     Jira · GitLab · Pieces · Todoist · Calendar · Email · Obsidian
     ↓
2. SYNTHESISE Deduplicate · cross-reference · collapse → Unified Open Loops Register
     ↓
3. PRIORITISE Urgency × Impact × Effort × Staleness → Top 3–5 Next Actions
     ↓
4. GENERATE+PUSH  ADHD starter tasks (verb + object + timebox ≤15m) → Todoist Work
     ↓
5. LOG        Daily journal entry + SoT upsert
```

### Implementation phases

1. **Wire existing components into one trigger** — unified `cos-sweep` skill calling existing routines in order; add prioritisation; add starter-task generation; add journal append; test end-to-end. *Deliverable: one "cos sweep" trigger.* ✅ Landed — `cos-sweep.py --journal --push`.
2. **Calendar & email awareness** — Teams/Apple Calendar via `icalbuddy`/EventKit; email via `neomutt`+IMAP / Gmail API / Apple Mail scripting; surface time-conflicts; detect email-embedded action items.
3. **Decision: build vs wire** — start with wiring existing skills; if the chain gets long/fragile, switch to a single Python orchestrator calling each API directly and piping results to the LLM. (*Resolved toward the hybrid: scripted `cos-*.py` + agent-fetched GitKraken.*)
4. **Productionise** — cadence cron jobs (morning/lunch/EOD); delta detection; starter-task format verification; Todoist push confirmation gate.

### Starter task format (standard)

```
<action verb> + <object> + <timebox>   [≤15m]
```
- First word a concrete physical verb (Open / Run / Read / Draft / Check / Message)
- Contains exact path, URL, or file reference
- Timebox in brackets at the end
- ≤15 minutes (ADHD-friendly activation energy)

---

## 6. The Task-Authoring Gate — Six Required Fields

A standalone next-action in Todoist must satisfy all six fields to be ADHD-executable. The gate prevents **non-leaf nodes dressed up as actions** — the original failure ("Check status of X — re-assess next steps" = asking you to redo the executive-function deciding at the moment the task should have done it for you).

| # | Field | Purpose | Format |
|---|---|---|---|
| 1 | **Source Link** | Remove the lookup step; jump to context | `[TICKET-NAME ↗](url)` at start of description. If you can't link it, it's not actionable yet. |
| 2 | **Done Means** (outcome + completion signal) | Combat delay discounting; make finished state vivid (EFT) | One sentence, tangible endpoint, pulled from acceptance criteria — never invented. |
| 3 | **Steps** (process-focused EFT) | Externalise the sequence out of working memory | Numbered physical micro-actions in order. 1–4 steps; **>4 means the task isn't leaf-shaped**. |
| 4 | **If Stuck** (behavioral prescription) | Pre-decide the response to the most likely blocker | `[specific likely blocker] → [specific pre-decided move]`. One sentence. |
| 5 | **Source Context** (injected content) | Eliminate context-switching cost mid-execution | 2–3 sentences pulled from the ticket (open items, deps, acceptance criteria, last comment). Direct extraction, not rewrite. |
| 6 | **On Stop** (ready-to-resume / residue flushing) | Close the open loop; enable clean switching | Placeholder written *before* execution: done/not done — what blocked you — next micro-step. Filled at session end. |

**Gate rule:** if a field can't be filled, the ticket isn't ready — it goes back to the source for clarification rather than being pushed.

### The template vs the diagnosis

- Wrong: "make tasks smaller" — shrinking doesn't remove the implied project; the brain collapses the pebble back into the project and the resistance stays.
- Right: "make tasks atomic **and externally-scaffolded**" — addresses the mechanism (DMN noise, delay discounting, attention residue).
- A generic template works for trivial status checks (a Slack ping) but **breaks catastrophically for ADHD**, where re-assessment *is* the hard part. Each task's blocker/outcome must be custom-fitted to the ticket, not stamped uniformly.
- Empty description pointing back to Jira adds a lookup step; injected context trades a bit of length for a context-switch removal — net win. Source link keeps the task recoverable if Todoist is down.

---

## 7. Rollout — Live Instances (the work tasks that tested it)

Status header from source: **Live on FTFL-868, FTFL-619, FTFL-942; Argo task incomplete (needs Application name).**

| Task | Six-field outcome |
|---|---|
| **FTFL-868** (TFC workspace vars) | Done means: both vars set + `terraform plan` clean against `fitapp_demo_ukw`. Steps 1–4 incl. setting in TFC UI + triggering plan. If stuck: unknown IP range → default to current IP, note as follow-up. Context: 6-step rebuild, needs Jon Bradshaw sign-off, still Selected for Development. |
| **FTFL-619** (PostgreSQL HA audit) | Key insight: Azure auto-migrates same-zone HA to zone-redundant **1 Sept 2026 (7 days out)** — old wording buried the deadline. Steps: list Flexible Servers in both subscriptions → check `zone`/`standby_availability_zone` in Terraform → note findings. If stuck: grep state/config for `standby_availability_zone` instead of portal-hunting. Escalation flagged (P2 vs deadline). |
| **FTFL-942** (Trivy metric alerts) | Scoped to **one** condition (new Critical CVE), not all four. If stuck: check broken log-based alerts / FTFL-9002 for query patterns. Success binary (alert working or not). |
| **ArgoCD sync timeout** | ⚠️ **Incomplete — blocker masquerading as a task.** Original cut off mid-word and never named the Application/ConfigMap. Not startable until the Application is named; candidates by convention: `spec.syncPolicy` on the Application, or global `timeout.reconciliation` in `argocd-cmd-params-cm`. |

### What's different now

| Before | After |
|---|---|
| Generic wrapper, empty descriptions, detail crammed into truncated titles, one task broke mid-word | Specific action linked to source with concrete outcome |
| No Done-means/Steps/If-stuck/Context/On-stop | All six fields present, written before execution |
| Task paralysis (can't visualise endpoint) | Done-means counters delay discounting |
| Attention residue (no closure signal) | On-stop = closure signal |
| Context-switch cost (no injected context) | Context field removes lookup |

**The mechanism:** this is not "tasks are smaller now" — it's "the executive-function work is externalised now." Cognitive load shifts from working memory (under-resourced) to the task architecture (persistent).

---

## 8. Caveats & Risks

- **Learned helplessness / cognitive offloading risk:** the gate externalises executive function deliberately. Over-reliance risks atrophying internal capacity and "Stockholm Syndrome of AI dependency" (unquestioning acceptance eroding agency). Counter: the On-stop field captures *what you did*, not just whether; reviewing those notes builds metacognitive awareness. The cut-off research section ("Risks of Cognitive Offloading") addresses exactly this — find the full version.
- **Research integrity:** "Crumb Protocol" is *not* Leroy's term — her published intervention is the **Ready-to-Resume Plan**; the Capture/Close/Clear/Cue/Commit sequence is a productivity blog's systematisation. Don't cite as Leroy. The **$450B** figure is cited everywhere but has no single traceable source (valid as colour, not a protocol foundation). EFT and implementation-focused CBT are real; ADHD-specific *Todoist-task-design* application is extrapolation, not a published methodology.
- **Incomplete rollout:** only four tasks updated; GitLab/Grafana/Obsidian integration aspirational; no standing alarm mechanism yet (open question: should the CoS set OS-level alarms for bounded sessions?).
- **Confidence:** High on protocol design, medium on research synthesis, low on unpublished claims.

---

## 9. Next Steps

**Immediate:** clarify the Argo task (name the Application → complete field 4) · test one task this week (FTFL-868) and report: did the six-field gate pull you in more? did the If-stuck blocker occur?

**Consolidation:** establish the gate as the standard for all future `cos-sweep` Todoist tasks (unfillable → back to source) · monitor On-stop fields over 2–3 weeks to surface **recurring** blockers (systemic, not individual).

**Expansion (after gate holds a week):** wire GitLab MR reviews + Grafana alerts into the same gate (don't expand sources until the template is proven on one) · Obsidian↔Todoist bridge using the same six-field structure via Advanced URI deep links.

**Structural:** re-weight priority by deadline visibility (FTFL-619 P2 vs 7-day deadline) · decide on OS-level alarms.

---

## 10. Related Notes & Vault Integration

Planned home per source: `cos-prodOS-protocol-august-2026.md` (this consolidation supersedes it).

Related notes (referenced in sources — verify existence before relying):
- `gtd-action-system.md` — canonical GTD reference (Projects, Outcomes, Sequences, Next Actions, Starter Tasks)
- `ADHD.md` — personal ADHD profile (consider creating)
- `todoist-config.md` — Todoist structure (six-project runway, nine-label stack, filters)
- `obsidian-todoist-bridge.md` — Advanced URI plugin setup
- `20_Thinking/21_Workbench/HEAD - How to unify the CoS Query Engine.md` — open unification question
- `20_Thinking/21_Workbench/CoS Ideas.md`

Backlinks: the four live tasks (FTFL-868/619/942, ArgoCD) embody this protocol; `cos-sweep` label — check periodically whether new tasks satisfy the gate.

Status tags: `#protocol/live` (gate live on 868, tested/live on 619/942) · `#protocol/incomplete` (ArgoCD) · `#research/neuroscience` · `#system/escalate` (FTFL-619 1 Sept deadline).

---

## 11. Key References

- Russell Ramsay (adult ADHD implementation deficits) · Russell Barkley (ADHD as self-regulation deficit / external scaffolding)
- Sophie Leroy, "Why Is It So Hard to Do My Work?" (2009) · Leroy & Glomb "Ready-to-Resume Plan" (2018)
- Gloria Mark (UC Irvine) — context-switch recovery 23m 15s, switching frequency
- EFT literature (delay discounting; process vs outcome focus; NEFT)
- fMRI DMN/TPN dysregulation in ADHD

---
*Consolidated 2026-08-26 from 2 inbox captures. Originals removed from `00_Inbox/` (recoverable via git history).*

In regards to the not being able to disengage with completed tasks, I have a different feeling. In my experience in programming I spend a lot of time in a frustrated or cognitive disonance state while trying to fix things or solve problems. When I finish a task and everything is green and satisfying that is a nice feeling so I linger. Starting something new means returning to that dissonant state. And after periods of focus I am tired.

## Verdict

You're right—that's a genuine mechanism difference, not just a different description of the same behaviour.

Different mechanism, not just a different feeling

"Cognitive inertia" in that text usually points to attention residue—unfinished Task A leaking into Task B (Sophie Leroy's research on task-switching). But residue is worst when Task A is left _unresolved_; a clean, decisive "green" should minimise it, not cause it. So residue probably isn't what's happening to you at that moment—what you're describing is an approach-avoidance calculus: stay in a resolved, pleasant state, or deliberately re-enter an unresolved, unpleasant one. That's your own "procrastination as emotion regulation" principle, just applied to switching rather than starting.

Sharper vocabulary, if useful

The frustrated state itself is closer to the Zeigarnik effect—the pull of an open, unresolved loop—than dissonance proper, which is technically about conflicting beliefs (though "I should be able to solve this" vs "I can't yet" has a fair dissonance reading too). Either way, it's the same tension your GTD capture habit already exists to defuse.

Where I'd push back

Mechanism isn't verdict, though. Rational avoidance can still cost real time if it's unbounded—the question isn't whether the linger makes sense, it's whether it _stays bounded_. And the fatigue is real (sustained focus genuinely depletes something)—but worth checking whether "tired" sometimes also doubles as justification for not re-entering the dissonant state. Rest and "push through anyway" are different fixes; only you can tell which one's actually needed in the moment.

Next action

Next time you hit green, note one line: did a stray thought about the just-finished task nag at you during the linger (residue's still live), and roughly how long before you were back at the keyboard. That tells you whether this is savouring—leave it alone—or the same unbounded-transition problem your entry-side timer already exists to solve.

## COS prodOS protocol task organization

**You**

Here is a brain dump about the cos prodOS protocol. Some might not make sense. I want you to create todoist tasks for any work needed to address these vague captured ideas

- I have a first run at the cos sweep. It's quite good but needs some extra tweaks.
- I need to set up GK. I'm still not sure what the fuss is about.
- it should check all renovate mr for why that can be merged and add then with a link
- I don't like the masses of text or adds to daily note. Seems pointless.
- check terraform cloud fit errored plans
- it should help clarify the inbox items. Is it is a work thing or should be a Jira ticket.
- separate work and personal tasks.
- cos helping me complete tasks.
- it should use pieces better to enrich my notes on the work done.
- need to feel with Inbox items. Probably better as a separate operation.

---

**Claude**

Let me first check whether "the cos sweep" and "GK" were defined in earlier conversations, and pull up your current Todoist structure so these land in the right place.

---

**You**

GK is gitkraken. I started using the gitlens vscode plugin. GK is the desktop app. I am not entirely sure what the benefits are. I like having a view of all my git repos and there state. But that is not really worth the subscription. Do a deep dive research into the features and what the main selling points are. Look for advantages for my system. I know it has some AI but why is that better than using Claude code or agy in the terminal? How should I use it when trying to do my Jira and gitlab work

---

**Claude**

### Verdict

**Skip GitKraken Desktop's paid tier for now. Try Kepler instead — it's free and closer to what you actually said you want.** The AI commit-message stuff isn't in the same category as Claude Code and isn't trying to be — it's a small model doing git ceremony (commit messages, PR blurbs), not reasoning. The genuinely new, relevant thing GitKraken has built is an agent-orchestration layer that sits *around* Claude Code, not instead of it — and the multi-repo version of that (Kepler) is currently free in public preview.

### The product family (this is why it's confusing)

"GitKraken" is now four things sharing one AI/backend layer:

| Product | What it is | You already have it? |
| --- | --- | --- |
| **GitLens** | VS Code extension | Yes — installed |
| **GitKraken Desktop** | Standalone GUI app | No — this is "GK" |
| **GitKraken CLI** | Terminal companion (`gk`) | No |
| **Kepler** | New multi-repo agent orchestrator | No, and it's new (launched mid-June 2026) |

### Selling points, honestly graded

**Visualisation (the actual original product)**  
The interactive commit graph colour-codes branches, merges, and tags, and you can drag and drop to merge or rebase, with an integrated terminal so you're not forced to leave the GUI for anything the visual layer doesn't cover. This is genuinely good, but it's the least interesting part for you — GitLens already gives you a chunk of this per-repo inside VS Code. [MakerStack](https://makerstack.co/reviews/gitkraken-review/) [G2](https://www.g2.com/products/axosoft-gitkraken-desktop/reviews)

**GitKraken AI**  
Generates commit messages, explains commits and branches, drafts PR text, resolves merge conflicts, and lets you customise the AI provider and prompts. You can point it at OpenAI, Gemini, Claude, Azure, Mistral, Ollama, or your own API key — but the default bundled model on the Pro plan is Gemini 2.0 Flash with 250,000 AI tokens per week. That's a small, fast, cheap model doing a narrow job — not a reasoning engine. [GitKraken AI Features Overview +2](https://help.gitkraken.com/gitkraken-desktop/gkd-gitkraken-ai/)

**Agent Sessions View** (the actually new bit)  
A Left Panel mode that organises worktrees around coding agent sessions, status, and quick actions, explicitly supporting Claude Code, Codex CLI, Copilot CLI, Gemini CLI, and OpenCode. The Agent Sessions panel shows pending permission requests from Claude Code with allow and deny actions, so you can keep Claude working without switching into the worktree, and a bell icon and "Waiting for input" label appear when an agent needs attention — so you stop tabbing between terminals to check if a session stalled. Only event metadata is sent; prompt content, agent output, and source code are not captured, for what that's worth on privacy. [GitKraken Desktop FAQs | Answers to Common Questions +4](https://help.gitkraken.com/gitkraken-desktop/faq/)

**Kepler — the one that matches what you said you want**  
Kepler is GitKraken's Agentic Development Environment that coordinates multiple AI coding agents and manages everything from generated code to merged PR in one surface. A database migration, an API change, and a front-end update spanning three repos become one Task instead of three disconnected branches, with shared context and cross-repo conflict detection. Kepler connects to Jira, Trello, Linear, GitHub Issues, GitLab Issues, and Azure DevOps, and is currently in public preview — a free GitKraken account is all you need. [Introducing Kepler: GitKraken's Delivery Engine for Agent-Driven Development +3](https://gitkraken.com/blog/introducing-kepler-the-delivery-engine-for-agent-driven-development)

### Your actual question: why would this beat Claude Code (or another terminal agent) directly?

**It doesn't try to.** Nowhere in GitKraken's own positioning does it claim to out-reason Claude Code — the split is deliberate:

- **Claude Code**: does the thinking and the editing.
- **GitKraken's job**: visibility and plumbing around that — it can detect when an agent working outside the app in a terminal is actively editing a worktree, and surfaces a shortcut to open that worktree with the live diff already in view, and routes agent experiments through Git so work is preserved permanently rather than living in ephemeral checkpoints that vanish when you close the session. [GitKraken](https://gitkraken.com/blog/gitkraken-desktop-go-deep-on-one-repo-with-an-agent-riding-along) [Developers Digest](https://www.developersdigest.tech/blog/gitkraken-claude-code)
- **GitKraken MCP**: an MCP server that gives agents access to GitKraken's integrations and features, which GitKraken says helps agents understand your codebase in a way that lowers token usage and improves output — that's a vendor claim about *feeding* Claude Code better context, not replacing it. I'd treat "improves output" as marketing until you've tried it. [GitKraken](https://gitkraken.com/blog/gitkraken-claude-code)

So the honest reframe of your question: it's not GitKraken-AI-vs-Claude-Code. It's "do I run enough *parallel* Claude Code sessions across enough repos that I need a dashboard for them?" If you're running one session at a time in one repo, none of this earns its keep. If you're routinely juggling infra/app/Helm-chart repos in parallel — plausible, given your role — the orchestration layer has real value.

### Jira + GitLab workflow, practically

Two separate mechanisms, easy to conflate:

1. **Smart commits** (via the Git Integration for Jira app): perform actions on Jira issues directly from a single commit — prefix your commit message with the issue key, e.g. "GIT-4322 – updated the plugin", and use `#comment`, transition commands etc. to update Jira without leaving git. GitLab.com and GitLab CE/EE are both supported hosting integrations for this. [Smart Commits Overview | Git Integration for Jira Cloud +3](https://help.gitkraken.com/git-integration-for-jira-cloud/smart-commits-overview-gij-cloud/)
2. **Kepler**, day-to-day: pull an issue's URL, hand it to an agent with context attached, and take the result through to a reviewed, mergeable change — instead of manually copying a Jira URL into a terminal. This is the bit that could plausibly *replace* some of what you were about to build yourself in the cos sweep (the Renovate MR triage task in particular overlaps with what Launchpad/Kepler already try to do) — worth checking before you build that from scratch. [GitKraken](https://www.gitkraken.com/blog/why-we-built-kepler-one-engineers-frustration-with-fifteen-open-terminals)

### Pricing reality check

Sources disagree with each other by 2× on exact figures — this smells like a mid-2026 pricing restructure not yet fully reflected everywhere (GitKraken confirmed existing Pro subscriptions with 3–10 seats were automatically moved to the new Advanced tier, and Teams moved to Business). Best current read: [GitKraken](https://www.gitkraken.com/blog/smarter-workflows-built-in-ai-better-developer-experience)

| Tier | ~Price/seat/mo | Gets you |
| --- | --- | --- |
| Community | Free | GitLens basics, CLI — public repos only |
| Pro | $8–10 | Private repos, GitKraken AI, **GitKraken MCP**, Jira Cloud + Trello issue links, Shared Cloud Workspaces up to 25 repos |
| Advanced | $12–14 | \+ Self-hosted GitLab/GitHub, Jira Data Center, single-domain SSO, 2× AI credits |

**Unknown I can't resolve for you**: whether FitFile runs GitLab/Jira cloud or self-hosted (NHS-adjacent orgs often go self-hosted for compliance) — that alone decides Pro vs Advanced if you ever pay.

### Next action

Go to `gitkraken.com/kepler/download`, sign in with a free account, and connect exactly one FitFile repo plus your Jira project — see if the Task view earns its keep before you spend anything.

---

**Claude**

Knowledge