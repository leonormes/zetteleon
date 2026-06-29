---
title: Psychological Safety Primer — Transforming Team Ways of Working
source: https://gemini.google.com/app/bd855ef5efc22a11
captured: 2026-06-16
status: refined
type: reference
tags:
- psychological-safety
- ways-of-working
- engineering-culture
- dora-metrics
- trunk-based-development
- facilitation
created: 2026-06-16
modified: 2026-06-16
project_name: Team work
permalink: llmeon/30-library/200-projects/psychological-safety-primer
---

# Psychological Safety Primer — Transforming Team Ways of Working

> [!abstract] What this note is
> A human-centred playbook for shifting a team's *ways of working* — **without dictating the solution**. The aim is to architect the conditions in which the team co-creates and *owns* the change.
> Grounded in [[Accelerate]] (Westrum culture, transformational leadership), [[Git for Teams]] (the social side of version control), and [[Trunk-Based Development]] / the *Software Developer's Guidebook* (blamelessness, sustainable pace, autonomy).

> [!tip] Core premise
> You cannot *mandate* a cultural shift. You can only architect the environment where it naturally emerges.

---

## 1. What Psychological Safety Looks Like in the Pipeline

[[Psychological Safety]] is not "being nice." It is the shared belief that the team is safe for **interpersonal risk-taking**. In a [[Westrum Generative Culture]], failure triggers *inquiry*, not scapegoating.

Translate that into the three moments where blame usually creeps into a deployment pipeline:

**Broken builds → a system success, not a human failure.**
The automated feedback loop did its job: it caught the issue *before* production.
- *Avoid:* "Who broke the build?"
- *Instead:* "What gap in local testing or CI let this merge through?"

**Missed estimates → newly discovered complexity.**
Software is complex knowledge work, not manufacturing. A missed estimate means you *learned something* you didn't know at planning.
- *Instead:* "What did we discover mid-sprint? How does it adjust the roadmap, and how do we slice work thinner next time?"

**Production incidents → remediation and learning only.**
[[Blameless Post-Mortem|Blameless post-mortems]] are mandatory. Operate on the **Retrospective Prime Directive** as a literal working assumption:

> [!quote] The Prime Directive (Norm Kerth)
> "Regardless of what we discover, we understand and truly believe that everyone did the best job they could, given what they knew at the time, their skills and abilities, the resources available, and the situation at hand."

The operating belief: every engineer made the best decision available given their information, context, and tools *at that moment*.

---

## 2. The "Ways of Working" Kickoff

**Goal:** introduce the *why* without triggering defensiveness. Validate past effort; invite the team to design a less stressful future.

> **Suggested title:** *Designing Our Next Chapter — Reducing Friction & Reclaiming Time*
> **Duration:** 90 minutes

| Phase | Time | What you do | Why it works |
|---|---|---|---|
| **1 — Prime Directive** | 10 min | Read the Prime Directive aloud (above). | Disarms defensiveness up front. Current processes weren't "wrong" — they were survival mechanisms you now have the luxury to outgrow. |
| **2 — Connect the "why" to their pain** | 20 min | Skip "business value" and "velocity." Name *their* friction: long merge times, deployment-day stress, the cognitive load of huge branches. | People mobilise around relief from their own pain, not abstract KPIs. |
| **3 — "What if" visioning** | 20 min | Introduce [[Trunk-Based Development]] and [[Westrum Generative Culture]] as *options* to solve the pain above — never as mandates. | Framing as choice preserves ownership. |
| **4 — Co-creation** | 40 min | Move straight into a co-creation exercise (§3) to capture *their* ideas. | The room leaves having built something, not received orders. |

> [!tip] The reframe to land in Phase 2
> "The goal isn't to squeeze more code out of you. It's to build a system where you work at a [[Sustainable Pace|sustainable pace]], merge with confidence, and go home without worrying about production."

---

## 3. Co-Creation Strategies — Dictation → Ownership

You are a **facilitator, not a dictator**. Three techniques, in increasing order of democratisation:

### Strategy 1 — Lightweight [[Value Stream Mapping]] (find the bottlenecks)
- **How:** Draw a horizontal line: *"Idea / Ticket Created" → "Code Running in Production."* The team marks pain / waiting / frustration with red sticky notes.
- **Why:** Don't *tell* them PR reviews are slow — let the map *prove* it. They'll then propose smaller batches and trunk-based flow to fix the bottlenecks *they* identified.

### Strategy 2 — "Even Over" Statements (define the culture)
- **How:** The team drafts 3–4 trade-offs in the form **"[Good Thing A] *even over* [Good Thing B]."**
	- *"Learning and mentoring **even over** immediate delivery speed."*
	- *"A green, stable `main` **even over** finishing my individual feature."*
- **Why:** Forces alignment on what wins when push comes to shove. Becomes a shared North Star for [[Even Over Statements|behavioural change]].

### Strategy 3 — [[Lean Coffee]] (prioritise process changes)
- **How:** Everyone writes one process to **start / stop / change**. Group duplicates → dot-vote → discuss the top items for ~8 minutes each.
- **Why:** Stops the loudest voices dominating. You fix what the *majority* cares about first.

---

## 4. Handling Resistance

Per [[Git for Teams]], version-control and deployment practices are inherently **social** — changing them triggers social anxiety. Read the behaviour, name the fear, pivot with empathy.

**"We don't have time for all these tests / pairing. We just need to ship."**
- *Underlying fear:* being reprimanded for slowed velocity during the learning curve.
- *Pivot:* "I hear you — I'll run air-cover with Product. We're sprinting, but the job is a marathon. Look at how much time we lost to bug-fixing last month; the goal is to reclaim it. What's one small, safe area to try this in?"

**"Trunk-based will never work here — the code's too tangled, people will break `main`."**
- *Underlying fear:* distrust of teammates' code quality; losing the safety net of long-lived branches.
- *Pivot:* "You've got deep context on this architecture — you're right, we can't flip a switch overnight. What safety nets (feature flags, specific CI checks) would we need *first* to make merging smaller chunks feel safe?"

**Silence / crossed arms / disengagement.**
- *Underlying fear:* change fatigue, or a belief that input will be ignored anyway.
- *Pivot:* Use [[Humble Inquiry]]. Never call them out in the group. Take it to a 1-on-1 or walking meeting: "I noticed you were quiet. You've been here a while and I value your read on this — what am I missing?"

---

## 5. Measuring Cultural Health — Leading Indicators

[[DORA Metrics]] (Deployment Frequency, Lead Time, MTTR, Change Failure Rate) are *trailing* indicators of a healthy culture. To steer in real time, watch these **leading** human signals:

1. **[[Amy Edmondson]] Psychological Safety Pulse** — quarterly, anonymous, 1–5 scale (e.g. *"If I make a mistake here, it's often held against me"*; *"It's safe to take a risk on this team"*). Track the **trend**, not the absolute number.
2. **Meeting participation equality** — in low-trust teams, 1–2 senior engineers hold ~80% of the airtime. Rising equality of speaking time = rising trust.
3. **PR comment tone** — a shift from prescriptive ("Fix this", "You forgot X") to inquisitive ("Have you considered Y?"). More *questions* over *commands* = rising empathy.
4. **Self-reported incidents go *up* (at first)** — counter-intuitively healthy: people have stopped hiding mistakes. Track how often the team proactively flags its own errors for shared learning.

---

## Sources

- **[[Accelerate]]** — Forsgren, Humble & Kim. Westrum organisational typology; psychological safety as a predictor of delivery performance.
- **[[Git for Teams]]** — Emma Jane Hogbin Westby. The social and political dimension of version control; empathy and trust.
- **[[Trunk-Based Development]]** + *Software Developer's Guidebook* — optimising for learning, blamelessness, sustainable pace, team autonomy.
- Original capture: [Gemini session](https://gemini.google.com/app/bd855ef5efc22a11) (2026-06-16).

---

## Next Actions

- [ ] **Decide the trigger event.** Pick the *one* piece of pain to anchor the kickoff (candidate: the blocked staging environment / stalled release pipeline). Write one sentence: *"The friction we're fixing is ___."*
- [ ] **Block 90 minutes** in the calendar and paste the §2 agenda table into the invite body.
- [ ] **Pre-write the Prime Directive** on slide 1 / the whiteboard so it's the first thing the room sees.
- [ ] **Pick one Phase-4 exercise** (default: **Value Stream Mapping** — lowest barrier, most visual).
- [ ] **Link this note** to any existing `[[CI-CD]]`, `[[Retrospectives]]`, or pipeline-remediation notes in the vault.

---

> [!note] Refactor notes
> Converted from a raw Gemini capture into vault-ready form: British English throughout, LLM framing removed, concepts wikilinked, canonical quote attributed, and an actionable checklist added. Frontmatter `status`/`type` set to `refined`/`reference` — **adjust to match your own taxonomy** (the original capture used `head`/`input`/`processing`).