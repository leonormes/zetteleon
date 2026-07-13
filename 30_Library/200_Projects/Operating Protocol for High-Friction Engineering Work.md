---
created: 2026-05-15T08:22:55+00:00
modified: 2026-07-13T08:44:45+00:00
permalink: llmeon/30-library/200-projects/operating-protocol-for-high-friction-engineering-work
project_category: refined_deployment
project_name: Refined Deployment
project_status: active
title: Operating Protocol for High-Friction Engineering Work
type: null
---

Given my difficulty initiating tasks and the nature of these projects we have discussed give me a protocol or process for getting this work done Here is a tactical protocol designed to lower the barrier to entry for complex, high-friction engineering work. It treats human attention much like a Lean software delivery pipeline: optimising for small batches, limiting work-in-progress, and ensuring fast feedback loops. Phase 1: The Pre-Flight Routine (State Management) * Master Internal Triggers: Difficulty initiating is rarely about a lack of technical skill; it is often driven by the subconscious overwhelm of tackling massive, ambiguous architectural changes. Acknowledge the discomfort of the "blank IDE" before beginning. * Move to Focus: Before sitting down to map out the GitOps changes or Entra ID policies, engage in brief physical movement. Taking the dog for a brisk walk around the block serves as a powerful neurological reset, priming the brain for sustained mental effort and focus. Phase 2: The "Walking Skeleton" Initiation * Timebox the Atomic Action: Commit to doing just one thing at a time. Set a strict timebox of 15 to 25 minutes to execute only the very first, atomic action identified in your planning phase (e.g., writing the first Terraform resource block or querying the k8s cluster state). * Banish Perfection: Do not attempt to architect the perfect end-to-end deployment pipeline on the first attempt. The objective is simply to overcome inertia; start now and get perfect later. Phase 3: The "Unschedule" * Plan the Downtime First: Instead of staring down an open-ended, gruelling block of configuration work, schedule your breaks, meals, and leisure activities before scheduling the work itself. * Guilt-Free Play: Knowing exactly when you will stop working provides a psychological safety net. It replaces the dread of endless work with the promise of guaranteed, guilt-free downtime. Phase 4: Radical WIP Limits * Embrace Finitude: When designing and overhauling multiple distributed systems, attention is a strictly finite resource. You cannot execute all of these upgrades simultaneously. * Enforce Limits: Limit your personal Work-In-Progress (WIP) just as you would in a team delivery environment. Focus exclusively on one major project at a time and creatively neglect the others until the active task reaches a defined, testable milestone.

---

Claude

## Operating Protocol for High-Friction Engineering Work

### 1. Critique of the Draft

It's recognisable productivity literature with an ADHD label sticker on top—Pomodoro, Unschedule, WIP limits, a walk before work. The components are real, but the assembly is generic. Specific gaps:

1. "Walking skeleton" is misappropriated. It's Alistair Cockburn's term for the thinnest end-to-end _architectural_ slice, not "just start". Borrowing a software-design term for a personal-productivity move sounds clever but loses precision.
2. No engagement with your context. You have at least six active streams (omop-cli, mkuh-prd-4, stress tests, GitOps optimisation, Entra/PIM, break-glass) plus a day job. _"Limit your WIP"_ is advice without a mechanism. Which do you stop?
3. State management gets one bullet. This is the whole game for ADHD initiation, and it deserves the most detail in the protocol, not the least.
4. The timebox is plain Pomodoro. Fine, but doesn't address what happens when the timer goes off and the dopamine isn't there.
5. "Banish perfection" is advice, not a protocol. Telling a perfectionist not to be perfect doesn't work. You need a structural mechanism that makes perfection mechanically impossible.
6. Unschedule is named but not implemented. Neil Fiore's technique has specific rules (mark blocks _after_ you complete them, ≥30 minutes of uninterrupted quality counts, work expands inside the leftover space). The draft just says "plan breaks first".
7. No body doubling / external accountability. One of the most evidence-backed ADHD interventions, missing entirely.
8. Doesn't address mid-session stalls. Initiation is one problem; getting unstuck after you've started is a different one with different remedies.
9. No shutdown ritual. Unclosed loops occupy background processing—bigger initiation problem tomorrow.
10. No environmental friction reduction. Initiation friction lives in the seconds before the first keystroke. Where are your terminals, scratchpads, dashboards, notes app?
11. No connection to what you've already built. Across our three previous projects, we established a repeatable pattern: `scoping-v0.md` with three questions, 15-minute box. The protocol should generalise _that_, not import unrelated templates.
12. No demand-avoidance awareness. Rigid protocols trigger the "don't tell me what to do, even when it's me telling me" response and fail silently.

---

### 2. Principles Underpinning the Protocol

If a tactic violates one of these, it won't survive the day you need it most.

1. Initiation is a state problem. Discipline is what you do _after_ you're in state. Getting in state is engineering, not effort.
2. Decide once, execute often. Every decision at execution time is a chance to bail. Pre-decide.
3. Friction is the enemy at execution; structure is the enemy at planning. Reverse them and you fail twice.
4. WIP=1 is operational, not aspirational. Needs a parking lot, not just intent.
5. Capture is sacred. Anything that fires mid-session goes to inbox, never into the current work.
6. Energy ≠ time. Bind tasks to states and times, not to dates.
7. External signal beats internal signal. Calendars, body doubles, deadlines, public commitments.
8. Closing matters as much as opening. Unclosed loops cost background CPU.
9. The protocol must be cheap on bad days. If it's complex, you won't run it on the day you most need it.
10. Novelty is fuel, not a luxury. Engineer it into boring work; don't wait for it to appear.

---

### 3. The Protocol

Five layers: Daily, Weekly, Per-Session, Per-Project, Stall-Break. Each is self-contained—the per-session loop runs whether or not the weekly review happened.

#### 3.1 Daily Layer—"Today's One Thing"

Once per day, ideally as the first work act (before email, before Slack):

1. Open one file: `daily/YYYY-MM-DD.md`.
2. Write one sentence: _"Today's one thing is: ___."_
3. Bind it to a window: _"Between ___ and ___."_
4. Identify the first physical action—5 minutes or less.
5. Write the stop signal—what observable thing means today's one thing is done?

Time-boxed to 3 minutes. No daily plan beyond this. The temptation to plan a whole day's schedule is the trap; you won't follow it, and not following it produces shame, which kills tomorrow's initiation.

Everything else that arrives today goes to inbox, not to today's plan.

#### 3.2 Weekly Layer—"WIP=1 Review"

Once per week (Friday afternoon or Sunday evening—pick one and never the other), 30 minutes:

| Question | Output |
| --- | --- |
| What is my single active project this week? | One named project, written down |
| What does "active" mean for it? | The next concrete deliverable + focus hours allocated |
| What's parked? | List, each with the trigger to un-park |
| What's dead and I haven't admitted it? | Be honest. Mark dead. |
| What landed in inbox this week needing clarifying? | Convert to projects, parked items, or actions |
| What's my energy forecast for next week? | Heavy meetings? Travel? Sleep debt? Adjust ambition. |

The parked list is the WIP-limit mechanism. _"Creatively neglecting"_ projects is meaningless unless they have a written home.

Applying this to your current load right now:

- Active: one of { `omop-cli mega-merge`, `mkuh-prd-4 stabilisation`, `break-glass` }
- Parked: the other two + stress test scoping + GitOps audit + Entra IaC
- Each parked item gets an explicit re-entry trigger (_"un-park stress test scoping when mkuh-prd-4 has gone 14 days without fire"_).

#### 3.3 Per-Session Layer—"The 90-Minute Block"

The smallest unit of real work. Run this when you're starting a session, not when planning one.

Pre-flight (5 min):

1. Physical: stand up, water, walk 60 seconds. Not negotiable.
2. Close: email, Slack, every non-essential tab. _Visibly close them._
3. Open: the one file you'll touch, the one terminal, the one dashboard. No more.
4. Write one line at the top of your scratch file: _"This session is for ___, until ___ (clock time)."_
5. Timer for 75 minutes, not 90. The last 15 are reserved.

Work (75 min):

- Touch only the one file / terminal / dashboard.
- Anything that fires (idea, distraction, unrelated task) → one-line entry in `inbox.md`. Do not act on it.
- If you stall for >5 minutes: run the Stall-Break protocol (§3.5). Don't push through.

Closing ritual (15 min)—non-negotiable:

1. Write one paragraph in the project log: what you did, what's next, where the bookmark is.
2. Commit code (even broken—`wip:` prefix is your friend).
3. Update `<project>/next-action.md` so future-you re-enters in 60 seconds.
4. Close terminals, close tabs.
5. Stand up, leave the room ≥5 minutes.

A session without a close costs you tomorrow's initiation.

#### 3.4 Per-Project Layer—"The Scoping Pattern"

You've already built this across our three conversations. Codify it.

Every new project starts with one file: `<project>/scoping-v0.md`. Three questions, two sentences each, 15-minute box:

1. Single primary outcome / driver / sub-project?
2. Primary beneficiary?
3. Definition of done, concretely?

That file is the project's birth certificate. Until it exists, the project is a wish, not a project. After it exists, natural planning can begin.

Template:

```markdown
# <project>/scoping-v0.md
Created: <date>
Time-box: 15 minutes

## 1. Single primary driver / sub-project
…

## 2. Primary beneficiary
…

## 3. Definition of done
…

## Status
- [ ] Scoped (this file exists)
- [ ] Natural-planned (Phase 1–5 doc exists)
- [ ] First session executed
- [ ] Active / Parked / Dead: ___
```

For each of the three new projects in our conversation, this file is the literal next action. Not the trigger list. Not the natural plan. The three-sentence file.

#### 3.5 Stall-Break Layer—"When Stuck"

When you stall mid-session (>5 minutes of zero-progress staring), do not push through. Run this short script.

1. Diagnose in one word:

| Word | Means |
| --- | --- |
| Unclear | I don't know what I'm doing |
| Hard | I know what to do but the next step is genuinely difficult |
| Boring | I know what and how, but my brain refuses |
| Anxious | I'm avoiding because of fear (breaking something, judgment, failure) |
| Depleted | Tank's empty—nothing's coming |

1. Apply the matching response:

| Diagnosis | Response |
| --- | --- |
| Unclear | Stop coding. Open a markdown scratch. Write the next 3 actions in plain English. Then return. |
| Hard | Step the problem down: smallest possible test, draw on paper, or rubber-duck to Claude. |
| Boring | Engineer novelty: change scenery, new music, narrate aloud, body-double. |
| Anxious | Name the fear in writing. Identify the smallest reversible action that tests it. |
| Depleted | Honour it. Run the closing ritual. Go outside. Come back tomorrow. |

1. Log the stall in `stalls.md` with date + diagnosis. After a month, patterns surface that point at structural fixes.

---

### 4. Over-Advice

#### 4.1 Body Doubling

Single most evidence-backed ADHD intervention outside medication. Options ranked by friction:

- Synchronous human: colleague on a silent video call, friend on Discord, Focusmate (50-minute sessions with strangers, both on camera, working in silence).
- Asynchronous human: Slack/Discord channel where you announce "starting 90 min on X" and report at the end.
- AI body double: lowest friction—open a chat, tell Claude what you're doing and the stop signal, report back at close.

For high-stakes initiation (break-glass especially), synchronous human is worth the cost.

#### 4.2 Environmental Friction Reduction

Before the session is ever scheduled:

- Bookmark the dashboards you'll need (Grafana, ArgoCD, Azure portal scoped to subscription)
- Save terminal layouts per project (tmux session, iTerm window arrangement)
- Keep `next-action.md` open at session-end so re-entry is one click
- One scratchpad per active project, always at the same path
- Notes app capture shortcut on phone home screen

Friction at the keystroke level is where minutes of avoidance compound into days of delay.

#### 4.3 Capture-everything Inbox

A single `inbox.md` (or your notes app's inbox). Everything that interrupts a session, everything from Slack worth keeping, every shower thought. One line, no editing, no triage. Process during weekly review only.

This is the dam that protects sessions from the river of incoming.

#### 4.4 The next-action.md Trick

At session close, the _last_ thing you write is `<project>/next-action.md` containing one line: _"Next session: do X, starting at file Y, running command Z."_

Sitting down tomorrow becomes reading one line, not reconstructing context. This single habit pays for itself within a week.

#### 4.5 Energy Mapping

Track for two weeks: at each hour you tried to work, score 1–5 on focus quality. Patterns emerge:

- High-state hours → hard/novel work (audit, architecture, scoping)
- Mid-state hours → meetings, code review, comms
- Low-state hours → admin, ticket triage, cleanup

Scheduling break-glass design at 4pm Friday is a planning error, not a discipline failure.

#### 4.6 Public Commitment with a Safety Valve

For projects that must land but lack external deadlines: create one. Tell your manager. Tell the customer. Put a date in writing. RSD-aware framing: _"I commit to delivering X by Y; if I can't, I'll let you know by Z."_ The safety valve preserves dignity if life intervenes; the commitment provides external signal.

#### 4.7 Medication, Sleep, Exercise

The protocol assumes baseline conditions. If you're under-slept, under-exercised, or your medication regimen is unstable, no protocol will rescue you. Saying this directly because it's true, not as judgment: optimise the substrate before optimising the technique.

#### 4.8 The "Ugh fIeld" Technique

Notice topics or files you flinch away from. Those flinches are signal. Make a list. Each item gets one 15-minute box of _"just look at it, don't fix it"_ before any other work happens. The ugh often dissolves on contact.

#### 4.9 Protocol Decay

This protocol will decay. Every protocol does. Symptoms:

- Sessions starting without pre-flight
- No weekly review for three weeks running
- WIP back at 4+
- `inbox.md` is a wall of unprocessed lines

When you notice decay, don't restart from zero with a new protocol. One weekly review fixes it. Restarting from zero is its own avoidance pattern.

#### 4.10 The Over-engineering Trap

This entire response is itself the trap your ADHD brain will try to fall into: spending three hours making the protocol perfect instead of doing the work. The protocol as written is sufficient. Do not iterate it. Use it for three weeks, then iterate.

---

### 5. Your Next Physical Action

15-minute box. One file.

Open your notes app. Create `operating/protocol-v0.md`.

Answer three questions, one or two sentences each:

1. When this week is my weekly review going to live? Pick a 30-minute slot, put it in your calendar now, recurring weekly. (Friday afternoon or Sunday evening—pick one and never the other.)
2. What is my single active project for next week? Pick one from your current load. The other five are parked, with re-entry triggers to be written _at_ the first weekly review—not now.
3. What body-doubling option will I trial this fortnight? (Focusmate / colleague / Discord / AI Claude session). Just name it. Don't sign up today.

That's it. Don't implement the rest of the protocol today. Don't write `scoping-v0.md` for any of the three new projects today. Don't restructure your notes app today.

Three answers. One calendar invite. Stop.

Next week's review is where you decide which one of your active projects gets scoped first—and that's where this whole sequence (capture → clarify → scope → plan → execute) finally meets the road.

## Phase 1: Purpose and Principles

 - Purpose: Why are we undertaking this project? What defines its success? Is the main goal to ensure stability during peak clinical data loads, or to evaluate the resilience of the OMOP data pipelines under pressure?
 - Executive Issues: How does this relate to the broader technical strategy, priorities, and goals of the organisation?
 - Principles: What are the boundaries, standards, or policies that apply to this test? (e.g., maintaining adherence to data privacy regulations, ensuring zero disruption to live production workloads, or capping cloud compute costs).

## Phase 2: Vision/Outcome

 - Ideal Scenario: What does "wild success" look like? Imagine the project is complete: you have a comprehensive report on cluster behaviour, clearly identified breaking points, and a successfully tuned cluster configuration.
 - Quality & Monitoring: How will you monitor the progress? How will you know if the project is on course? What data do you need, and when?

## Phase 3: Brainstorming

 - Resources & Personnel: Whose input do you need? Whose input could you use? (e.g., DevOps engineers, data scientists familiar with the OMOP common data model, or network specialists).
 - Precedents: Has anything like this been done before? What mistakes or successes can you learn from?
 - Research: What might you need to know before initiating the load? (e.g., understanding K8s pod eviction thresholds, network latency bottlenecks, or OMOP data distributions).
 - Risks: What could happen? (e.g., potential cascading cluster crashes, data corruption during the stress test, or out-of-memory errors).

## Phase 4: Organising

 - Operations: What is the timing for the stress tests? Are there any hard deadlines? Who is going to do the work, and how do you ensure complete delivery?
 - Equipment & Tools: What specific tools do you need, and when? (e.g., load generation tools, Grafana/Prometheus dashboards for monitoring, scaling up K8s compute nodes).
 - Administration: Who is strictly accountable for this project's success, and what are the lines of communication?

## Phase 5: Next Actions

 - The Next Step: What is the next physical, visible activity that progresses this project toward completion?
 - Process Actions: If more planning or information is required to get comfortable, determine the next action to make that happen. For example, the very next action could be: _"Draft an email to the DevOps lead to schedule a whiteboard session regarding the K8s load testing parameters."_

## Clarifying a Fuzzy Project: Stress Testing Trigger List

### 1. The Real Problem (Quick Reframe)

You're not actually stuck on _clarifying_—you're stuck because "stress test the clusters with OMOP data" is not yet a project, it's a _fuzzy aspiration_. Natural Planning Model assumes the input is a single, well-bounded outcome. If you feed it a vague commitment, every phase becomes equally vague (which is exactly what the LLM produced—see §3).

The missing step between Capture and Natural Planning is Scoping: turning the fuzzy aspiration into one or more well-defined projects. _That_ is what a trigger list is for.

---

### 2. Scoping Trigger List (The Deliverable)

Work through this once. Answer in writing—even one-word answers count. The goal is to expose ambiguity, not produce a polished brief.

#### A. What Kind of Test, Actually?

These are _different projects_ with different tools, durations, and risk profiles. Pick one:

- Load—find max sustainable throughput
- Soak/Endurance—behaviour over hours/days (memory leaks, cert expiry, log rotation)
- Spike—sudden surge handling (HPA reaction time)
- Chaos—failure injection (node loss, network partition, Vault outage)
- Capacity planning—predictive model: "X patients/hour needs Y nodes"
- Scalability—does it scale linearly, or does coordination overhead dominate?
- Performance regression—detect degradations between releases

#### B. What is the System Under Test?

You have at least three candidates hiding inside "the clusters":

- B1. `omop-cli` itself—Spot VM orchestration + DuckDB merge pipeline
- B2. An AKS cluster _running_ an OMOP workload (ingestion/query path)
- B3. The cross-cluster data path (EOE → Azure FW DNAT → MKUH)

Plus the sidecars that always break first in your environment: Vault/VSO secret delivery, ArgoCD reconciliation, cert-manager DNS-01.

#### C. Workload Profile

- Read-heavy, write-heavy, or mixed?
- What is "OMOP data" doing here—ingest, transform, query, export?
- Synthetic (from `omop-cli`) or replayed real traffic?
- Steady arrival rate or bursty/diurnal?

#### D. Success Criteria—Discovery Vs Validation

Two opposite postures, can't do both at once:

- Discovery: "Find the unknown breaking point" → open-ended, you stop when something breaks
- Validation: "Prove it can handle 10× peak" → fixed target, you stop when SLO is met

#### E. Blast Radius & Safety

- Dedicated test cluster, or shared infra?
- Customer-facing impact possible? (MKUH is healthcare—this matters)
- Compute budget ceiling (£)?
- Real PHI risk, or synthetic-only?
- Kill criteria: what single observation aborts the test immediately?

#### F. Deliverable Shape

What artefact lets you tick this off and walk away?

- One-off report (markdown + Grafana screenshots)?
- Tuned config committed to GitOps repo (HPA/VPA/PDB/requests/limits)?
- SLO document?
- Runbook for capacity planning?
- Recurring CI job (kube-burner in a pipeline)?

#### G. Time, Budget, People

- "Summer"—calendar window vs. focus hours?
- Sole operator, or stakeholders to consult?
- Compute £ ceiling?

#### H. Definition of Done

> Complete this sentence: "I will know this project is finished when ___ exists / is committed / is signed off by ___."

If you can't complete it, you don't have a project yet—you have a theme.

---

### 3. Critique of the LLM Response (`stress_tests.md`)

It's a competent generic template, not a useful plan for _your_ environment. Specific gaps:

1. Generic, not contextualised. It never names `omop-cli`, `mkuh-prd-4`, ArgoCD, Vault/VSO, Azure Firewall, cert-manager—the systems where you've been bleeding for months. A genuine plan should leverage that pain.
2. Conflates 3+ projects into one. Stress-testing the _generation pipeline_ (`omop-cli`), an _AKS workload_ (ingestion under load), and a _cross-cluster network path_ are three distinct projects. The plan forces you to natural-plan all of them simultaneously, which is impossible.
3. No baseline phase. You cannot "stress" a system whose steady-state you haven't characterised. The first sub-project of any stress test is "establish baseline RED/USE metrics." The plan omits this.
4. No kill criteria. A stress test plan without explicit abort conditions is reckless—especially against a healthcare customer environment.
5. Risk section is bland. Missing your actual risks: ArgoCD auto-sync racing imperative test changes (a recurring pattern for you), Vault token TTL under sustained load, Let's Encrypt rate limits, cross-tenant blast radius, NHS regulatory exposure.
6. Brainstorming under-seeds. No concrete tools mentioned: `k6`, `kube-burner`, `Chaos Mesh`/`Litmus`, `Vegeta`, KEDA load tests, `clusterloader2`. No methodologies: USE (Brendan Gregg), RED (Tom Wilkie), SLO-driven testing.
7. "Next Action" is wrong for your role. It says _"Draft an email to the DevOps lead"_—you are the Principal Platform Engineer. You don't escalate to yourself.
8. No observability prerequisite check. You can't stress-test what you can't measure. Are SLIs defined? Are the right Prometheus series being scraped? Is there a dashboard ready _before_ load is applied?
9. No test-data lifecycle. Generation, loading, teardown, retention. You literally have a tool for this (`omop-cli`)—the plan should make it the first-class load generator.

---

### 4. Over-Advice (Things You Didn't Ask About)

#### 4.1 The ADHD-specific Failure Mode here

Natural Planning can become procrastination by sophistication—you produce a beautiful plan and never run a test. Counter-measure: time-box planning to 90 minutes total. Output is a one-page brief, not a treatise. If you exceed 90 minutes, the project is still too fuzzy—go back to scoping.

#### 4.2 Use `omop-cli` as the Load Generator

You don't need `k6` for the data plane. You're building a tool that produces 10M synthetic OMOP patients on Spot VMs. That tool IS the load generator. Frame the stress test as: "use `omop-cli` to drive `mkuh-prd-4` to breaking, observe what fails first." This collapses two projects into one and feeds dogfooding into both.

#### 4.3 USE and RED as Structuring Lenses

- USE (Utilisation, Saturation, Errors)—for every resource (CPU, memory, disk, network, IOPS)
- RED (Rate, Errors, Duration)—for every request-driven service

If your Grafana dashboards don't already give you USE+RED views per node and per service, build _those_ before applying load. That's a self-contained, completable sub-project.

#### 4.4 Search for prior Art before Planning

Before brainstorming, spend 30 minutes searching the Fitfile wiki / GitLab / Slack archives for:

- Previous load tests
- Post-incident reports (real-world stress tests already happened—read them)
- Capacity documents
Cheap, high-yield, novelty-rewarding.

#### 4.5 Decompose Now, Sequence Later

I'd suggest the captured aspiration splits into three projects, run in this order:

1. P1: Observability readiness for OMOP workloads on AKS _(prerequisite, 1–2 weeks)_
2. P2: Capacity model for OMOP ingestion on a single AKS cluster _(main stress test, 3–4 weeks)_
3. P3: Resilience profile of the cross-cluster path under load _(follow-up, 2–3 weeks)_

Natural-plan only P1 first. The other two will sharpen once P1 is done.

#### 4.6 Write a Hypothesis, not just a Target

Every stress test scenario should be a falsifiable statement:

> _"We hypothesise that at 5,000 patients/sec ingestion sustained for 1 hour, the bottleneck will be DuckDB merge throughput rather than Vault token refresh or ArgoCD reconciliation latency."_

This forces precision and makes the test outcome interesting regardless of result.

#### 4.7 The "Boring" Pre-flight Checklist

Before any actual load:

- [ ] ArgoCD auto-sync disabled on target apps (you've been bitten by this)
- [ ] Vault token TTLs documented for the test duration
- [ ] cert-manager `extraArgs` for DNS-01 persisted in GitOps (your outstanding item)
- [ ] Grafana dashboard URL pinned in the project brief
- [ ] Kill switch documented (one command to stop generation)
- [ ] Cost alert configured on the test subscription

---

### 5. Your Next Physical Action

Open your notes app. Create one file: `stress-test/scoping-v0.md`.

In that file, answer only three questions—one or two sentences each, no more:

1. Which sub-project am I starting with—P1 (observability), P2 (single-cluster capacity), or P3 (cross-cluster resilience)?
2. What single breaking point would be most valuable to discover?
3. What one observation would make me abort the test immediately?

That's it. Don't write the trigger list answers yet. Don't natural-plan yet. Just those three questions. Target: 15 minutes.

Once `scoping-v0.md` exists with three answers, you have a project. Then—and only then—run the trigger list (§2) against the chosen sub-project, and _only then_ start Phase 1 of Natural Planning.
