---
created: 2026-07-16T00:00:00+00:00
method: full link-graph extraction, keyword clustering, hub reading, bridge tracing
modified: 2026-07-16T09:40:48+00:00
permalink: llmeon/output/analysis-hidden-research-agenda-of-100-zettelkasten-2026-07-16
scope: 30_Library/100_zettelkasten (1,110 notes)
title: Analysis - Hidden Research Agenda of 100_zettelkasten (2026-07-16)
type: analysis
---

## The Hidden Research Agenda of Your Zettelkasten

Corpus statistics: 1,110 notes. Largest connected component: 611 notes. 360 separate components. 216 orphan notes (no links in or out). 60 link targets cited ≥5 times that live _outside_ the collection (mostly in `30_Library/SoT/` and `30_Library/MoC/`).

Evidence labels used throughout: [S] directly supported by multiple notes · [I] plausible inference · [?] speculative.

---

### A. Executive Synthesis

This is not a general-interest vault. It is a single, sustained engineering project pointed at one problem: an ADHD software engineer building an external executive function, and increasingly trying to implement it in software. The corpus reads as a systems engineer who has turned his professional toolkit—feedback loops, state machines, gateways, access control, verifiability—onto his own cognition. Five clusters (ADHD neurology, GTD-descended productivity, Zettelkasten method, LLM/agentic engineering, and networking infrastructure) are not parallel interests; they converge. The ADHD notes define the _requirements_, the productivity and PKM notes define the _design patterns_, the LLM/agent notes define the _implementation substrate_, and the infrastructure notes supply both the day-job material and the _metaphor library_ ("Cognitive Firewalls", "DNS as Path Steering"). A sixth, quieter thread—shame, self-trust, RSD, epistemology of belief—is the _why_: the cost of the untreated problem, and the emotional safety-engineering that makes the rest usable. The thinker this suggests is a builder-theorist who trusts mechanisms over willpower, propositions over topics, and iteration over perfection—and who has already written down the exact failure mode this analysis finds in the graph itself (capture is easy; processing is hard).

---

### B. Theme Map

| # | Theme | Size (approx.) | Evidence notes | What it seems to mean | Type | Confidence |
|---|-------|------|----------------|----------------------|------|------------|
| 1 | ADHD executive function & task initiation | ~130 titles | "ADHD Task Initiation Deficits Due to Dopamine Hyposensitivity", "ADHD Paralysis is the Inability to Start a Task Until it Becomes an Emergency", "The Interest-Based Nervous System in ADHD", "ADHD Overthinking is a Substitute for Action", "The Five-Step Initiation Chain for Neuro-Variable Execution", "ADHD Task-Paralysis Reflects DMN-FPN Maturational Lag, Not Willpower Failure" | Mechanistic (neurological, not moral) account of why starting is hard; the requirements document for everything else | Personal + research | High [S] |
| 2 | Productivity system design (GTD lineage) | ~146 titles | "A Next Action Must Be the Absolute Next Physical Visible Activity Required to Move a Situation Forward", "A Project Playlist is a Sequence of Small Tasks to Rebuild Momentum", "A Startup Ritual Eases the Transition into a Project Mindset", "Practice - Deferred low-pressure review", "Cognitive Firewalls" | Design patterns for low-activation-energy work; GTD re-derived from ADHD first principles rather than adopted wholesale | Practical | High [S] |
| 3 | PKM / Zettelkasten method | ~80 titles | "Creating Meaningful Links", "2c. Propositions Are the only Thing that Can Be Wrong", "Claim - Capture is easy but processing is hard", "MOC - ADHD and PKM Systems", "Claim - Treat the system as iterative not perfectable" | Proposition-centred, falsifiable notes as the unit of thought; the vault is self-aware about its own method | Practical + theoretical | High [S] |
| 4 | LLM / agentic engineering | ~85 titles | "Agentic Autonomy as State Machine Logic", "LLM Wiki Concept", "Local-First Obsidian with MCP and RAG Is the Best-Fit Substrate for Data-Sovereign PKM", "MCP Architecture Separates Host, Server, and LLM into Distinct Roles", "Minimum Viable Context for LLMs Prevents Hallucination via Structural Boundaries", "Agent-First Implementation Cycle" | Context engineering as a discipline; agents as constrained state machines; the vault itself as machine-readable context | Practical + research | High [S] |
| 5 | Networking, identity & cloud infrastructure | ~100 titles | "API Gateways Manage and Secure Application Interfaces", DNS series (delegation, zone transfers, glue records), "Concept - TCP Three-Way Handshake", AWS ALB series, "Enterprise Agentic Systems Require Containerised Gateways with OAuth and RBAC", OAuth/token/Entra notes | Day-job study notes (DevOps/platform), but repeatedly mined for cognitive metaphors | Professional | High [S] |
| 6 | Information theory, cybernetics & systems | ~84 titles | "Shannon's Information Theory - Information as Uncertainty", "7-cybernetics", "5c-emergence", "Information as Perceivable Pattern", "The Conflict Between Semantic and Shannon Information", "Prediction Error Breaks Feedback Loops" | The unifying theory layer: feedback, entropy, control—applied both to machines and to the self | Theoretical | Medium-high [S] |
| 7 | Epistemology & mental models | ~87 titles | "Flawed Mental Models Limit Mastery" (13 inbound links), "The Map is Not the Territory" (10 inbound), "Pragmatism Defines Truth by Practical Consequences", "Bayesian Updating Adjusts Beliefs as New Evidence Arrives", "Myopic understanding" | Mastery = model fidelity, not information volume; "bug in the model" as the limiting factor on performance | Theoretical | High [S] |
| 8 | Shame, self-trust & identity | ~70 titles | "I have a lot of shame about my life" (20 links), "Inaction Erodes Self-Trust", "Why Others' Opinions Can Feel Undeservedly Powerful", "Rejection Sensitive Dysphoria (RSD)", "A False Belief Does Not Diminish a Person's Worth", "Locating Truth-Status in Persons Is What Wounds, Not Believing in Truth" | The emotional cost-ledger of the inaction loop; also the motive for making ideas falsifiable _instead of_ selves | Personal | High [S] |
| 9 | Mathematics as a learning project | ~52 titles | "Calculus (Definition)" (13 inbound), "Abstraction and Generalization Are Core Mathematical Methods", "Abstraction as Climbing a Hill", "Beauty Is a Guiding Value in Mathematics" | A deliberate adult re-learning of maths, approached through abstraction rather than procedure | Personal learning | Medium [S] |
| 10 | Virtue, mastery & philosophy of living | ~40 titles | "Miyamoto Musashi" (highest-degree note in the collection, 23 links), Covey habit notes, "Process Over Outcome Mindset", family/relationship notes | Character as practice; Musashi as the model of process-driven mastery under emotional control | Personal | Medium [S] |

---

### C. Conceptual Bridges

Bridges are ordered by strength of evidence. Co-occurrence counts are from full-text pattern matching across all 1,110 notes.

#### 1. ADHD ↔ PKM/GTD—the Load-bearing Bridge (200 Notes touch Both) [S]

The central proposition of the whole vault, stated explicitly in "MOC - ADHD and PKM Systems": _"for an ADHD brain, capture is cheap and processing is expensive—and the emotional response to that asymmetry (perfectionism, novelty-seeking) makes it worse."_ The Claim series ("Claim - Capture is easy but processing is hard", "Claim - Novelty-craving drives self-defeating system-hopping", "Claim - Treat the system as iterative not perfectable") plus the open question "Q - Iterating versus system-hopping" form a genuine research programme with falsifiable claims and discriminating tests. This is the most mature thinking in the vault.

#### 2. ADHD ↔ AI/agents—AI as Prosthetic Executive Function (14+ Explicit Bridge Notes) [S]

"Leveraging AI and Templates for ADHD Productivity", "Mindful LLM Research Workflow for ADHD", "Digital Tools Help Externalize Memory and Structure for ADHD Developers", "Plan To Plan-Just-In-Time for ADHD", "Low Activation Cost Effect". The heavily-cited external hub is literally titled "SoT - Prosthetic Executive Function". The larger idea: what GTD did with paper and contexts, agents can do with context windows and tools—automate the expensive _processing_ step that ADHD makes prohibitive.

#### 3. RAG/context Engineering ↔ Proposition-centred Notes [S]

"2c. Propositions Are the only Thing that Can Be Wrong" argues atomic, claim-shaped notes make thinking falsifiable; "LLM Reasoning Efficiency is Proportional to Structural Constraint" and "Minimum Viable Context for LLMs Prevents Hallucination via Structural Boundaries" argue the _same structural discipline_ makes notes better LLM context. "Local-First Obsidian with MCP and RAG…" and "LLM Wiki Concept" complete it: the vault is deliberately being engineered as a substrate that serves human cognition and machine retrieval _simultaneously_. This is the most original bridge in the corpus—note format as a shared interface between brain and model.

#### 4. Cybernetics/feedback ↔ Motivation [S]

"Rapid Feedback Loops are Essential for ADHD Motivation" (explicitly: shrink the idea-to-feedback loop; TDD and REPLs as dopamine infrastructure), "Prediction Error Breaks Feedback Loops", "Objective Scoreboards", "Celebrate Small Successes to Build Routine Momentum". The larger idea: motivation is a control-systems problem—the ADHD brain needs a shorter loop between actuator and sensor, exactly like any unstable controller.

#### 5. Agent Architecture ↔ Human Action Initiation [I—strong]

"Agentic Autonomy as State Machine Logic" (agent "autonomy" is really constrained execution inside a developer-defined graph) mirrors "The Five-Step Initiation Chain for Neuro-Variable Execution" (human initiation engineered as a five-stage pipeline with triggers, zero-calculation first actions, and bounded sessions). Add "Agentic Autonomy Accelerates Fastest in Domains Where Success Is Verifiable" next to "Objective Scoreboards" and the isomorphism is hard to miss: both agents and ADHD humans perform best when constraint replaces open-ended judgement and success is externally verifiable. No single note states this equivalence outright—it is the strongest _implicit_ thesis in the vault.

#### 6. Infrastructure ↔ Cognition Metaphors [S for Instances, I for the pattern]

Explicit instances: "Cognitive Firewalls" (deep/shallow work separation as network segmentation), "DNS as Path Steering", "Externalize Memory Aggressively (cognitive offloading)" (RAM/disk hierarchy), "Concurrent Task Overload Creates Non-Linear Administrative Overhead" (scheduler thrashing). The recurring move: take a mechanism that keeps distributed systems reliable, and port it to attention management. Gateways/ACLs ↔ attention filtering; queuing disciplines ↔ task triage.

#### 7. Epistemology ↔ self-worth—falsifiability as Emotional Safety [I]

"Locating Truth-Status in Persons Is What Wounds, Not Believing in Truth", "A False Belief Does Not Diminish a Person's Worth", "Your emotions are real but they are your responsibility", alongside the RSD cluster. Inference: the proposition-centred note format is doing double duty as _emotional_ technology—when claims live in notes rather than in the self, being wrong stops being an identity wound. This connects the PKM cluster to the shame cluster through a single mechanism. Confidence: medium; the pieces exist, the connection is never stated.

---

### D. Inferred Learning Agenda (Ranked)

1. Build a prosthetic executive function. _[S—near-explicit]_ The requirements come from cluster 1, the design patterns from cluster 2, the substrate from clusters 3–4. Evidence: "SoT - Prosthetic Executive Function" (cited 7×), "MOC - ProdOS", the Claim/Q/Practice note-type machinery.
2. Design AI-assisted knowledge workflows you own end-to-end. _[S]_ "Local-First Obsidian with MCP and RAG…" makes data sovereignty non-negotiable; "LLM Wiki Concept" targets persistence across sessions; "Agent-First Implementation Cycle", MCP notes, evaluation-pipeline notes fill in the engineering.
3. Understand action initiation mechanistically enough to intervene. _[S]_ From basal-ganglia pathways and DMN-FPN lag through to the Five-Step Initiation Chain—a complete problem → mechanism → intervention arc.
4. Converge on a unified feedback/information/control theory spanning machines and mind. _[I]_ Shannon, cybernetics, prediction error, verifiability, scoreboards. The notes circle this; no note yet names it.
5. Decouple self-worth from performance and from being right. _[S—personal]_ The shame/RSD/self-trust cluster, plus the epistemology-as-safety bridge (C7).
6. Professional depth in identity, networking and platform engineering. _[S]_ Entra, OAuth, zero trust, DNS, ALB, CUE—steady accretion of work-domain mastery, increasingly cross-pollinated with the agent notes ("Enterprise Agentic Systems Require Containerised Gateways with OAuth and RBAC").
7. Re-learn mathematics through abstraction. _[S, lower intensity]_ The calculus/abstraction cluster; appears motivated by cluster 7's model-fidelity thesis.

One-sentence version: you are trying to design a control system for your own attention, specified by ADHD neuroscience, patterned on GTD/Zettelkasten, implemented on a local-first LLM stack, and emotionally underwritten by an epistemology that makes being wrong safe.

---

### E. Gaps and Opportunities

#### Structural Gaps (Measured, not iNferred)

1. The graph enacts the exact failure mode the notes theorise. 216 orphans (19.5%) and 360 disconnected components; only 55% of notes are in the main component. "Claim - Capture is easy but processing is hard" is _empirically confirmed by its own vault_. Orphans include genuinely central material: "ADHD routines should be based on intrinsic motivation not external pressure", "Action Initiation Involves a Balance Between Direct and Indirect Pathways in the Basal Ganglia", "Bayesian Updating Adjusts Beliefs as New Evidence Arrives".
2. A 20-citation hub is in the bin. "Neuro-Variable Execution, Spatial Cognition & Knowledge Architecture" is referenced by ~20 zettels but the file now lives in `.trash/`. That's the single highest-value repair available.
3. Hub notes live outside the collection. ~60 targets cited ≥5× resolve to `30_Library/SoT/` and `30_Library/MoC/` (e.g. "SoT - Agentic AI Design Patterns", 23 citations). Fine if intentional, but it means the zettelkasten's synthesis layer is not itself zettel-shaped. Also "HEAD New chat" (13 citations) is a junk-titled hub that needs renaming.
4. The falsification machinery is barely used. Only 8 Claim notes, 2 Q notes, 4 Practice notes against 1,084 plain notes. The house style described in "MOC - ADHD and PKM Systems" (hub → claims → support) exists but covers a tiny fraction of the corpus.

#### Intellectual Gaps

1. The central tension is live and unresolved: "Outsourcing Writing to AI Bypasses the Cognitive Strain That Builds Professional Competence" directly opposes "Leveraging AI and Templates for ADHD Productivity" and the whole prosthetic-executive-function agenda. When is the prosthesis a wheelchair and when is it muscle atrophy? No note adjudicates. Related: "PKM Generates Unique Insights via Personal Context That AI Cannot Replicate" sits uneasily beside the push to make the vault machine-readable.
2. "Q - Iterating versus system-hopping" is marked `status: open` and lists candidate discriminating tests—but no note records an actual test being run.
3. No measurement layer. "Objective Scoreboards" and the verifiability thesis exist, but there are no notes instrumenting _your own_ system: no metrics on initiation latency, processing throughput, or ritual adherence. The vault preaches feedback loops and has none about itself.
4. Biology is nearly absent. Sleep, exercise, and medication—the highest-effect-size ADHD interventions in the literature—barely appear next to ~130 cognitive/architectural notes. [S: absence measured]
5. The infra↔cognition metaphor is productive but one-directional and unsystematised. A handful of explicit ports ("Cognitive Firewalls", "DNS as Path Steering") with no note about the _method_ itself—when does the metaphor illuminate and when does it mislead? ("The Map is Not the Territory" is sitting right there.)
6. Semantic vs Shannon information ("The Conflict Between Semantic and Shannon Information") is the natural theoretical bridge between the information-theory cluster and RAG/relevance—currently a single underdeveloped note.

---

### F. Next-Step Research Plan (30 Days)

Designed for low activation energy: each week has one theme, and every item starts with a first physical action.

#### Week 1—Repair the Graph (Mechanical, nOvel, sAtisfying)

- Restore the trashed hub. First action: move "Neuro-Variable Execution, Spatial Cognition & Knowledge Architecture" out of `.trash/` back into the vault. (~20 broken references fixed in one move.)
- Rename "HEAD New chat" to what it actually contains. First action: open it and read the first paragraph.
- Adopt five orphans. First action: open "Action Initiation Involves a Balance Between Direct and Indirect Pathways in the Basal Ganglia" and add one link to "The Five-Step Initiation Chain for Neuro-Variable Execution". (Suggested pairs in the add-on section below.)

#### Week 2—Run the Open Experiment

- Answer "Q - Iterating versus system-hopping" empirically. First action: create a note "Log - System Changes" with today's date. For 30 days, one line per system change: what changed, trigger (friction-in-use vs shiny-tool), cost. The note already lists the discriminating tests—you just need data.
- Instrument one metric (gap 7). First action: add a single daily line—"initiation latency on first deep task"—to your daily note template. Crude beats absent.

#### Week 3—Write the Adjudication Notes (The tHinking wEek)

- "Q - Prosthesis or Atrophy?" First action: create the note, link "Outsourcing Writing to AI…" and "Leveraging AI and Templates…", and write one candidate rule (e.g. _outsource retrieval and formatting, never outsource the first draft of a claim_). This is your vault's most important unwritten note.
- "Claim - Constraint enables initiation in humans and agents alike." First action: create it and link "Agentic Autonomy as State Machine Logic" and "The Five-Step Initiation Chain for Neuro-Variable Execution". Makes bridge C5 explicit and falsifiable.
- "Claim - Verifiable success criteria are a shared requirement of agents and ADHD brains." Links: "Agentic Autonomy Accelerates Fastest in Domains Where Success Is Verifiable", "Objective Scoreboards", "Rapid Feedback Loops are Essential for ADHD Motivation".

#### Week 4—Extend the Frontier (Reading)

- Perceptual control theory (William T. Powers)—the missing formalism for agenda item 4; behaviour as control of perception unifies your prediction-error, feedback and motivation notes. Connects to: "7-cybernetics", "Prediction Error Breaks Feedback Loops". First action: search "Powers perceptual control theory" and capture one note.
- Distributed cognition (Hutchins) / extended mind (Clark & Chalmers)—the academic literature for "prosthetic executive function"; your idea has a citation trail. Connects to: "Externalize Memory Aggressively", "Digital Tools Help Externalize Memory…". First action: fetch the Clark & Chalmers 1998 paper abstract.
- Semantic information (Floridi) vs Shannon—develops gap 10. Connects to: "The Conflict Between Semantic and Shannon Information", "Information as Perceivable Pattern".
- Spaced retrieval / testing effect—the missing memory layer behind "Practice - Deferred low-pressure review". First action: one note on the testing effect, linked to "ADHD Working Memory Deficits Create a Compulsive Re-Planning Loop".

#### The 10 Research Directions (Summary lIst)

1. Prosthesis vs atrophy—the AI-outsourcing boundary rule (Week 3; the keystone).
2. Constraint-enables-initiation—humans and agents as the same control problem (Week 3).
3. Verifiability as a personal design principle—objective oracles for your own tasks (Weeks 2–3).
4. Perceptual control theory as the unifying formalism (Week 4).
5. Extended-mind literature under the prosthetic-executive-function agenda (Week 4).
6. Iterating vs system-hopping—close the open question with logged data (Week 2).
7. Semantic vs Shannon information as the theory of RAG relevance (Week 4).
8. Spaced retrieval—the vault's missing memory/review layer (Week 4).
9. Biology as infrastructure—sleep/exercise/medication notes to balance the architectural bias (backlog).
10. A method note on infra↔cognition metaphors—when the port works, when the map lies (backlog).

---

### Optional Add-ons

#### Personal Ontology (Distilled)

- The Actor stack: Interest-Based Nervous System → Activation Cost → Initiation Chain → Next Physical Action → Feedback Loop → Momentum.
- The System stack: Capture → (expensive) Processing → Proposition notes → Links → MOC/SoT synthesis → LLM context.
- The Threat model: Novelty-craving → System-hopping; Perfectionism → Paralysis; Inaction → Shame → RSD → more inaction.
- The Value layer: Process over outcome; iteration over perfection; truth located in propositions, not persons; Musashi as exemplar.

#### Recurring Vocabulary and Implied Meanings

| Term | Implied meaning in your usage |
|------|------------------------------|
| SoT | Long-form synthesis report; the "source of truth" layer above zettels |
| MOC / HEAD | Hub notes; HEAD appears to be chat-derived research entry points |
| Claim / Q / Practice | Falsifiable statement / open question / actionable pattern—your epistemic type system |
| Neuro-variable | Your preferred, de-pathologised term for ADHD-pattern cognition |
| Activation cost | Energy needed to start; the quantity every design pattern tries to minimise |
| System-hopping | The anti-pattern: novelty-driven migration destroying accumulated structure |
| Prosthetic executive function | The whole project's name for itself |
| LLM Wiki | Persistent agent-maintained knowledge base; anti-stateless-RAG |
| Cognitive firewall | Structural separation protecting deep work |
| MVU | Minimum Viable Understanding—the model-fidelity threshold for competence |

#### Main Concept Hubs (Graph vIew, by tOtal dEgree within the cOllection)

```
Miyamoto Musashi (23) ─────────────┐
Flawed Mental Models Limit Mastery (21) ──┤── EPISTEMOLOGY/CHARACTER
I have a lot of shame about my life (20) ─┘
MOC - ADHD and PKM Systems (20) ───┐
Cognitive Load (19) ───────────────┤── ADHD × PKM CORE
The Interest-Based Nervous System in ADHD (18) ─┤
Executive Function Challenges are Central to ADHD (16) ─┘
Creating Meaningful Links (17) ────┐
Information Addiction in Overthinkers (17) ─┤── METHOD/INFORMATION
Shannon's Information Theory (16) ─┘
External gravity wells (outside collection): SoT - Agentic AI Design Patterns (23 in),
SoT - Microsoft Entra Identity (20 in), SoT - ADHD Neurology & Core Concepts (16 in)
```

#### Notes that Should Probably Be Linked but Aren't

- "ADHD routines should be based on intrinsic motivation not external pressure" (orphan) ↔ "The Interest-Based Nervous System in ADHD"
- "Action Initiation Involves a Balance Between Direct and Indirect Pathways in the Basal Ganglia" (orphan) ↔ "The Five-Step Initiation Chain for Neuro-Variable Execution"
- "Bayesian Updating Adjusts Beliefs as New Evidence Arrives" (orphan) ↔ "Prediction Error Breaks Feedback Loops"
- "Abstraction and Generalization Are Core Mathematical Methods" (orphan) ↔ "Abstraction as Climbing a Hill"
- "Cognitive Firewalls" ↔ "Cal Newport's Deep Work Method Involves Rigorous Time Blocking to Maximize Concentration"
- "Agentic Autonomy as State Machine Logic" ↔ "The Five-Step Initiation Chain for Neuro-Variable Execution" (the C5 bridge, currently implicit)
- "Outsourcing Writing to AI Bypasses the Cognitive Strain…" ↔ "Leveraging AI and Templates for ADHD Productivity" (the live contradiction—link them with a contrastive link, per your own "Creating Meaningful Links" taxonomy)
- "AWS ALB Best Practices" (orphan) ↔ "Creating an AWS Application Load Balancer (ALB)"

---

_Method note: link graph extracted from all `[[wikilinks]]` in 1,110 files; clusters via title/full-text pattern matching; ~25 hub and bridge notes read in full. Counts are exact; cluster sizes approximate (keyword-based, overlapping). Confidence labels mark the boundary between measurement and interpretation._
