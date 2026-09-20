---
conformant: false
created: 2026-09-14T00:00:00+00:00
modified: 2026-09-19T15:44:50+00:00
non_conformance_reason: "Reference/data artifact (ranked interest-node list), not one of the 5 canonical TAC note types; seeded per Method §1 of [[A Portable Interest and PKM Knowledge Graph]]. Renamed 2026-09-15 from 'Reference - Vault Interest Map' — that title collided with a pre-existing, unrelated note at 30_Library/SoT/Reference - Vault Interest Map.md (created 2026-06-10), which caused several backlinks to silently resolve to the wrong note. See that note's own Related section for the disambiguation record."
permalink: llmeon/30-library/200-projects/interest-driver-project-tag-frequency-seed-and-candidate-drivers
tags: [12/, domain/pkm, topic/metacognition, topic/self-inquiry]
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
| Habits, virtue, character, Stoicism | `#TheHuman/Habits` · 59, `#virtue` · 18, `#stoicism` · 3 | analyse, apply to self | low (auto) |
| Zen / Japanese philosophy / fables | `#zen` · 9, `#Japanese_culture` · 6, `#fable` · 7 | consume, appreciate | low (auto) |
| Communication & relationships | `#communication` · 31, `#relationship` · 23 | analyse, apply to self | low (auto) |
| Music | `#music` · 9 | consume, appreciate | low (auto) |

## Excluded: Life Foci (Not Interest Nodes)

Per Leon, 2026-09-15: these are a focus for life, not an interest in the sense this project studies—they don't compete for attention the way an interest does, and running them through the same driver-elicitation machinery (why does this matter to me? what would I keep if it had no utility?) would be a category error. Kept here rather than deleted, since the tag evidence is real and may still be useful context elsewhere (e.g. as a `context` node in the Graph Model that amplifies or inhibits other interests, per [[A Portable Interest and PKM Knowledge Graph]] §"What the Project Maps").

| Excluded | Vault evidence (tag · count) | Reason for exclusion |
|---|---|---|
| Bessie's education / family | `#bessie` · 42 | Life focus, not an interest—per Leon's direct correction, 2026-09-15 |

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

### First-Principles Modelling, Turned Inward and Outward—`proposed`, 2026-09-15

A Compare/Contrast pass (§2) across the fuller interest set, grounded in vault evidence rather than tag counts (a fork research pass this session searched `100_zettelkasten/`, HEAD notes, `90_Audits/`, `99_Archive/`, the trashed early drafts of this project, and `01_journals/Dailies/`—287 entries—for genuine first-person material). This strengthens, rather than replaces, the Epistemic Safety candidate above.

Definition: a pull toward building a legible, mechanism-level model of whatever system is in front of him—sometimes an external technical system (cloud infrastructure, security, LLM internals, physics), sometimes a domain's own foundations (maths: [[Public perception of maths is incomplete]]'s "My Thoughts" section explicitly identifies with the engineer/creator side over the mechanic/application side, and diagnoses school maths as failing to expose the "engineering mindset"), sometimes himself (ADHD studied as "an engineering problem" per [[SoT - The Interest-Based Nervous System in ADHD|Reference - Vault Interest Map]]; [[Discipline Is a Property of External Structure More Than of Will]] applies Lewin's `B = f(P, E)` with a full typed-edge argument graph and its own `## Tensions & Gaps` section to his own willpower).

The finding this pass adds: the same orientation appears to explain two very differently-shaped clusters at once—

1. Domains with huge vault volume but almost no first-person reflective voice (cloud/DevOps, security, LLM/agentic AI, physics, epistemology, Stoicism, Zen)—engaged with as _content to organise and analyse_.
2. Domains with comparatively thin tag volume but the richest personal-voice evidence in the vault (PKM, ADHD, discipline, archery)—engaged with as _practice to reflect on_.

The candidate mechanism: modelling an external system doesn't require narrating why it matters to you; modelling yourself does, by necessity. If this holds, richness of reflective writing is not evidence of a stronger interest—it's an artefact of whether the system being modelled is external or is himself.

Specificity check (a good sign, not a gap): the candidate correctly does _not_ explain Music. He doesn't attempt to model music theory or compose; the operative criterion there ([[Asking Why a Song Exists Helps Determine its Authenticity]]) is about the _artist's_ originating motivation, not his own systems-understanding. A driver that explains some interests and not others—correctly—is stronger evidence than one stretched to fit everything (Evidence Standard: Specificity).

Complication for the existing Feedback-Rich Deliberate Practice candidate above, recorded per Principle #12: cloud/DevOps, security, and LLM/agentic AI are all feedback-rich domains (logs, errors, test results) that nonetheless show almost no personal reflective voice—so feedback-richness alone does not predict where the reflective pull shows up. It may be necessary but not sufficient, or it may only bind when the practice is embodied/self-referential (archery, PKM) rather than professional/external (cloud, security)—not yet distinguished.

What would test it, per [[How to Interrogate a Candidate Interest Driver]]: does first-principles investigation persist in domains with zero audience, utility, or performance payoff? Are there systems he's had ample opportunity to model but has conspicuously not—and what differs about those cases?

Do not treat as settled—this is a Compare pass over existing writing, not yet tested against live behaviour (Method §5).

### Process/Construction Legitimises, Consumption Needs Defending—`proposed`, 2026-09-15

A second, independent pattern from the same evidence pass, recurring across three domains that share no subject matter: maths (creator vs. mechanic, above), PKM ([[Why I Do a PKM and What I Think Knowledge Is For]]: explicit rejection of "the polished-wiki model" in favour of a process that "captures the messy journey"—"the value sits in the network a summary rests on, not the summary itself"), and music, where [[The Distinction Between Appreciation and Creation]] reads as an explicit philosophical defence of pure consumption ("learning is not a failed attempt at creation; it is a successful attempt at becoming a more sophisticated appreciator… both roles are valid")—the fact that appreciation-without-creation needed defending at all is itself evidence that creation/construction is his default standard for what counts as legitimate engagement.

Epistemic caution: the maths and PKM evidence is explicit first-person commentary ("My Thoughts," "I want to use writing…"); the appreciation/creation and music-authenticity notes are general third-person claims he chose to write in this framing, not direct self-report. Treat this candidate as resting on weaker-grade evidence than the one above until that gap is closed.

Incomplete ladder, recorded honestly per Method §3 rather than forced to a root: the evidence establishes the _pattern_ (construction over consumption, recurring) but doesn't yet reach a terminal "why." Open question, per Principle #11 (preserve competing explanations): is this a corollary of the driver above (building a first-principles model requires active construction) or an independent aesthetic/epistemic value—the music case is the discriminating evidence, since there he isn't the one constructing at all, only judging whether someone else's construction was authentic. That the pattern still shows up when he's a judge rather than a builder leans toward "independent," but one case is not enough to conclude it.

### Methodological Flag, not a driver—2026-09-15

ADHD may function partly as a `context` node (per the Graph Model's node kinds) rather than purely as its own `interest`—[[Why I Do a PKM and What I Think Knowledge Is For]] frames PKM's whole rationale around compensating for "an ADHD working memory [that] can't hold it all at once." Not reclassified here; flagged for Leon's call, since it changes how several edges in the eventual graph should be drawn (`enabled-by`/`amplifies` vs. its own `provides`/`may-satisfy` chain).

### Excluded from This Pass

Per Leon's correction, 2026-09-15: Bessie's education/family is a life focus, not an interest, and was not searched or analysed in this pass (see the Excluded section above).

### Correction from Leon, 2026-09-15—vault-mining Produced Two Errors

This is the exact failure mode Principle #9 warned about ("absence may also reflect lack of exposure, access, energy, confidence, or opportunity") and the seed note's own §"Method Used here" flagged in advance ("will… underweight embodied or non-written interests… relative to their true pull"). Recorded per Principle 12/#15 rather than silently rewritten.

DevOps/cloud/security/LLM—not thin engagement, wrong evidence source. Leon: "The devops stuff is for a different reason. I think it fails the pkm protocol because it is just info about the things I am doing at work. The reflection is me doing the actual work outside the vault." The near-zero reflective voice found in this pass is not evidence of weaker pull—it's evidence that this vault isn't where that reflection happens. Practice and reflection occur through the paid work itself, off-vault. This _strengthens_ the First-Principles Modelling candidate's plausible reach (it may genuinely extend to these domains, not stop at their edge)—but leaves open, un-answered by this correction, whether the drive there is terminal (intrinsic pull, expressed through the job) or instrumental (professional conscientiousness, distinguishable per Principle #10). That distinction needs Leon's direct answer, not inference: would the pull survive with the paycheck and audience removed?

Music—actively wrong, not just thin. Leon: "I used to be a musician and spent all day everyday practicing and playing and listening." The "Process/Construction Legitimises, Consumption Needs Defending" candidate above used music as its third leg, characterising him as staying in consume/appreciate mode and needing to philosophically defend that. This was false—built on a coincidental pair of notes, not on his history. Leon: "The mentions of music in this vault are just from a conversation I was having with Bessie about the difference between real human music and plastic manufactured music." [[Asking Why a Song Exists Helps Determine its Authenticity]] and [[The Distinction Between Appreciation and Creation]] are not autobiographical self-permission-giving—the first came from a conversation with his daughter about a topic, and the second's link to music was this project's own mis-association, not the note's own content (it names F1 and film as its examples, not music).

Consequence for Process/Construction Legitimises: downgraded—two domains (maths, PKM), not three. Music needs to be re-elicited properly, live, not re-inferred from the vault, before it can support or weaken any candidate. The interest-node table's "Music" row (`consume, appreciate`, low confidence, tag-count-derived) is now known to be materially incomplete—a sustained, intense, practice-heavy period is entirely unrepresented in this vault.

Standing questions for Leon, not yet answered:

- Music: when did daily practice/playing stop, and why? What did it give you that nothing since has replaced, or what got replaced and by what?
- DevOps/cloud/security: does the pull hold with the paycheck, audience, and operational stakes removed—e.g. would you go deep on a system with no professional relevance at all?
