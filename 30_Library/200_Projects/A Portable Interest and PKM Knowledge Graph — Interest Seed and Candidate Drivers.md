---
conformant: false
created: 2026-09-14T00:00:00+00:00
modified: 2026-09-14T11:52:25+00:00
non_conformance_reason: "Reference/data artifact (ranked interest-node list), not one of the 5 canonical TAC note types; seeded per Method §1 of [[A Portable Interest and PKM Knowledge Graph]]. Renamed 2026-09-15 from 'Reference - Vault Interest Map' — that title collided with a pre-existing, unrelated note at 30_Library/SoT/Reference - Vault Interest Map.md (created 2026-06-10), which caused several backlinks to silently resolve to the wrong note. See that note's own Related section for the disambiguation record."
permalink: llmeon/30-library/200-projects/interest-driver-project-tag-frequency-seed-and-candidate-drivers
tags: [domain/pkm, topic/metacognition, topic/self-inquiry]
title: A Portable Interest and PKM Knowledge Graph — Interest Seed and Candidate Drivers
type: concept
---

## Status

Auto-derived seed, not yet elicited. Per [[A Portable Interest and PKM Knowledge Graph]]'s own Principle #2—"elicit before classifying"—this list is observational only. It's generated from how often notes tagged to a topic have been written, which is evidence of sustained attention, not a confirmed interest, and it says nothing yet about affordance, experienced outcome, or driver. Every node below needs to survive contact with the project's laddering method (§3) before it means anything beyond "I have written a lot about this."

## Method Used here

Counted tag frequency across the vault (`obsidian tags counts sort=count`, run 2026-09-14) and grouped related tags into named interest clusters. Frequency is a proxy for engagement—note-writing volume—not engagement itself; it will overweight topics that are easy to atomise into notes (software, networking) and underweight embodied or non-written interests (archery, music) relative to their true pull. Treat the ranking as a starting hypothesis, not a result.

## Interest Nodes (Observed; Ordered by Vault Volume Only, not Importance)

| Interest | Vault evidence (tag · count) | Mode observed in vault | Confidence |
|---|---|---|---|
| ADHD / neurodivergent cognition | `#TheHuman/Health/ADHD` · 223, `#executive-function` · 32, `#dopamine` · 22 | analyse, apply to self, organise | low (auto) |
| PKM / Zettelkasten / knowledge architecture | `#topic/pkm` · 68, `#domain/pkm` · 34, `#topic/knowledge-architecture` · 58 | practise, organise, create | low (auto) |
| Software engineering (general) | `#SoftwareEngineering` · 248 | practise, create | low (auto) |
| Networking & cloud infrastructure | `#SoftwareEngineering/Networking` · 97, `#kubernetes` · 36, `#argocd` · 47, `#aws`/`#azure` · 22/23 | practise, create, troubleshoot | low (auto) |
| LLM / agentic AI | `#domain/llm` · 106, `#topic/agent-architecture` · 56 | analyse, build, discuss | low (auto) |
| Epistemology / philosophy of science | `#epistemology` · 85, `#philosophy-of-science` · 53 | analyse, discuss | low (auto) |
| Productivity systems / GTD | `#topic/productivity` · 144, `#gtd` · 36, `#time-management` · 22 | practise, organise | low (auto) |
| Psychology / cognition / mental models | `#TheHuman/Psychology` · 77, `#mental_models` · 32 | analyse, apply to self | low (auto) |
| Security | `#security` · 50 | practise | low (auto) |
| Mathematics | `#topic/maths` · 33, `#mathematics`/`#math` · 8/8 | analyse, appreciate | low (auto) |
| Archery | `#archery` · 17, `#domain/archery` · 6 | practise | low (auto) |
| Physics (relativity, quantum) | `#physics` · 14, `#quantum-mechanics` · 4, `#relativity` · 2 | analyse, appreciate | low (auto) |
| Bessie's education / family | `#bessie` · 42 | support, teach, organise | low (auto) |
| Habits, virtue, character, Stoicism | `#TheHuman/Habits` · 59, `#virtue` · 18, `#stoicism` · 3 | analyse, apply to self | low (auto) |
| Zen / Japanese philosophy / fables | `#zen` · 9, `#Japanese_culture` · 6, `#fable` · 7 | consume, appreciate | low (auto) |
| Communication & relationships | `#communication` · 31, `#relationship` · 23 | analyse, apply to self | low (auto) |
| Music | `#music` · 9 | consume, appreciate | low (auto) |

## Today's Engagement Episode (2026-09-14)

Asked Claude (via Claude Code) to semantic-search the vault for what I've written about why I keep a PKM and what I think knowledge is for; the result was synthesised into [[Why I Do a PKM and What I Think Knowledge Is For]]. Immediately afterwards, asked for interest-tracking to begin—which surfaced [[A Portable Interest and PKM Knowledge Graph]] as a project already scoped but not yet seeded with data. This episode is itself PKM-interest evidence worth keeping once the driver layer gets built: the pull was toward _understanding my own motivation for the system_, not toward using the system for something external. Untested candidate association, not yet a driver node per Principle #2: [[Curiosity is Taking an Interest in Experience for its Own Sake]].

## Next step

This seed only completes the first bullet of Method §1 ("what I actually do"). The rest of §1 (when each interest began/intensified/faded, typical triggers, what attracts vs repels, how it feels before/during/after) and all of §2–§4 (comparison, laddering, candidate-driver nodes) need direct answers, not inference from tag counts—that's the project's own Principle #2, and inventing them would defeat the point. Suggested next real step: pick 3–5 interests from the table above and run the §2 comparison questions ("which two produce a similar experience despite different subject matter?") as a live conversation.

## Related

- [[A Portable Interest and PKM Knowledge Graph]]—the project this seeds.
- [[Why I Do a PKM and What I Think Knowledge Is For]]—today's synthesis note; PKM itself is one of the interest nodes above.
- [[HEAD - How Should Interests Stay Aligned Across Obsidian, Calibre, Todoist, Hookmark, and NotebookLM]]—the downstream mechanical counterpart.

## Candidate Drivers (Proposed)

Per [[A Portable Interest and PKM Knowledge Graph]] Method §4, status vocabulary below (`proposed` = emerged from one or two ladders, not yet tested).

### Feedback-Rich Deliberate Practice—`proposed`, 2026-09-14

Definition: DevOps observability, PKM, archery technique, automation, and structured learning may share one candidate driver—a preference for activities offering clear challenge, interpretable feedback, adjustment, and visible improvement (the loop described in [[A Competence Feedback Loop Turns Early Success Into Durable Interest]]).

Source and status: Proposed by research captured in [[tmp_atoms_what-drives-a-persons-interests]], which is explicit that this is "a hypothesis to examine through evidence in your graph, not a settled explanation of you." Recorded here as `proposed`, not `supported`—it has not yet survived the project's own laddering method (§3) or evidence standard.

What would test it: Per [[How to Interrogate a Candidate Interest Driver]]—check whether feedback-rich activities _without_ mastery progression or aesthetic payoff also hold attention; if not, "feedback loop" alone is too broad and the real driver is a narrower bundle (feedback + progressive competence + meaningful stakes).

Do not treat as settled. This entry exists so the hypothesis is recorded and falsifiable, not so it gets used as an explanation before it has been tested.

### Epistemic Safety Through Situational Awareness—`proposed`, 2026-09-14

Definition: A candidate driver proposed directly by research captured in [[tmp_atoms_chaos-and-situational-awareness]] and [[tmp_atoms_psychology-of-over-preparing]]: a strong motivation to build causal models of systems interacted with, because understanding relevant dependencies, risks, limits, and response options makes action feel safe and agentic. The source formulation, kept close to source wording since it was written directly for this project:

> "I am drawn to first principles because understanding creates agency, competence, and epistemic safety. When rejection or failure sensitivity is active, that healthy drive can become fused with a need to prevent shame and prove adequacy. My task is not to abandon depth, but to distinguish curiosity-led understanding from threat-led certainty seeking."

Source and status: Proposed across two related sessions—one starting from an AWS/network-adapter example, one starting from over-preparation and information-seeking generally. Both explicitly frame this as a hypothesis, not settled: "This should become a candidate driver node, not an established final truth." Recorded here as `proposed`, consistent with [[A Portable Interest and PKM Knowledge Graph]] Method §4—it has not yet survived the laddering method (§3) or the evidence standard.

Domains it may touch: cloud engineering, programming, PKM, mathematics—and, per the over-preparation source, any domain where deep system understanding is both professionally rational and emotionally regulating.

Mechanism proposed (kept as a hypothesis chain, not asserted fact):

```text
Confusing or opaque situation → perceived uncertainty
  → threat assessment / vigilance
  → may activate epistemic safety through situational awareness
  → motivates first-principles investigation, systems mapping, observability-seeking
  → may reduce operational uncertainty and perceived exposure

Failure / criticism sensitivity → may amplify the need for epistemic safety
```

The over-preparation source adds a parallel, narrower mechanism worth testing against the same driver: uncertainty → threat appraisal → anxiety/vigilance → research/checking/documenting → immediate relief → the nervous system credits the search with preventing danger → lower tolerance for ordinary uncertainty next time (see [[Reassurance-Seeking Relieves Anxiety Without Testing Whether the Feared Outcome Was Real]]).

Related candidate labels not yet separately tested (the source explicitly warns against collapsing these into one label prematurely—kept as a decomposition of the same cluster, not five independent drivers): competence security, agency through understanding, shame-avoidant overlearning, aesthetic-systemic curiosity. Rival/co-existing explanations offered by the source: professional conscientiousness, production-risk management, aesthetic-systemic curiosity (may co-exist rather than compete).

What would test it—per [[How to Interrogate a Candidate Interest Driver]] and the source's own questions:

1. When no one will assess you and there's no operational risk, do you still seek first principles? (If yes, curiosity/aesthetic order are doing independent work, not just this driver.)
2. Can you comfortably use a documented pattern while flagging uncertainty and deferring deeper learning—or does that still feel like exposure?
3. What's most painful: not knowing, being unable to explain, making an error, being observed erring, needing help, or causing harm? (Different answers imply different drivers.)
4. Which domains offer deep understanding with no competence display (private reading, etc.)—does the pull remain there too?
5. Which domains with the same first-principles appeal are avoided anyway—what does that reveal?
6. What would falsify this: repeatedly choosing difficult private inquiry with no audience, utility, status, or performance payoff would show the drive is more than defence.

Do not treat as settled, and do not collapse into a single "fear of being stupid" label—the source is explicit both that an authentic attraction to deep structure and elevated emotional stakes around not understanding can be true at once, and that this needs testing against contrasts, not narrative fluency alone.
