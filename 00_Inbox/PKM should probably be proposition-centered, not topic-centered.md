---
created: 2026-05-04T08:01:26+00:00
modified: 2026-05-12T13:12:01+00:00
tags: [Literature]
title: PKM should probably be proposition-centered, not topic-centered
---

- "What evidence supports it?"
- "What would change my mind?"

That is a much more valuable system.

## The Key Shift

Instead of organizing around subjects, organize around beliefs, questions, models, and evidence.

So instead of:

- Networking
- TLS
- Kubernetes networking
- TCP/IP

you create notes like:

- Packet capture is often the fastest way to collapse uncertainty in network debugging
- Most "network problems" in distributed systems are actually naming, timeout, or policy problems
- TLS failures are frequently trust-store problems rather than cryptographic problems
- Cilium changes the observability and failure model of Kubernetes networking

Those are worth having because they are:

- arguable
- refinable
- testable
- connectable
- useful in future decisions

## My Recommendation: Proposition-centered, not Proposition-only

This is the important nuance.

From your notes around 4:00 PM, you were also capturing the counterarguments: Ryle, Polanyi, Russell, and the point that concepts may be compositionally fundamental even if propositions are the main bearers of truth. I think that's right.

So I would not define your PKM as:

- "a database of facts"
- or "only propositions"

I would define it as:

> A system for maintaining, testing, and revising what I think is true, plus the concepts, evidence, questions, and procedures needed to support that.

That gives propositions the center of gravity without pretending all knowledge is propositional.

## What Should Go in Your PKM

Here's a practical taxonomy.

| Note type            | What it is for                                 | Should it exist?            | Example                                                                                          |
| -------------------- | ---------------------------------------------- | --------------------------- | ------------------------------------------------------------------------------------------------ |
| Claim / Proposition  | Something you think may be true or false       | Yes, primary unit           | "Packet traces usually outperform dashboards for root-cause analysis of opaque network failures" |
| Concept              | A definition or distinction needed for thought | Yes, but supporting role    | "Congestion control", "epistemic status", "service mesh"                                         |
| Evidence / Source    | Why you believe a claim                        | Yes, but don't over-collect | Quote from a book, benchmark, incident, paper                                                    |
| Question             | An unresolved tension or uncertainty           | Yes                         | "When does eBPF actually reduce debugging clarity?"                                              |
| Procedure / Playbook | Know-how that isn't just belief-that           | Yes                         | "How to debug DNS-01 cert-manager failures"                                                      |
| Index / Map          | A structured entry point into an area          | Yes, sparingly              | "Network debugging map"                                                                          |
| Topic bucket         | Generic holding area with undigested info      | Usually no                  | "Networking"                                                                                     |

So: topic notes should mostly become maps or indexes, not the core content.

## What Should _not_ Go in it

You do not need to rephrase entire books into your own words just to feel like you've learned them.

That usually produces low-value notes because they are:

- too broad
- too passive
- too detached from your actual beliefs
- hard to revisit
- hard to update

A good rule:

> If a note does not sharpen a concept, record a claim, preserve evidence, capture a question, or encode a useful procedure, it probably doesn't belong.

## A Better Reading Workflow

For books like networking books, don't ask:

- "What should I capture?"

Ask:

- "What in this changed, sharpened, or challenged my thinking?"

### Capture only These

1. Claims that surprised you
2. Claims you disagree with
3. Claims that explain repeated real-world failures
4. Conceptual distinctions
5. Procedures you'll actually reuse
6. Open questions created by the text

### Don't Capture These

- generic summaries
- textbook restatements
- definitions you can easily look up unless they matter to your reasoning
- exhaustive chapter notes

## Example: Bad Note Vs Useful Note

### Low-value Note

Networking

- TCP is connection-oriented
- UDP is connectionless
- Routers forward packets
- DNS resolves names

This is basically a school notebook or reference summary.

### Better Note Set

Claim: Most application teams misdiagnose latency as "the network" when the dominant cause is queueing, retries, or overload higher in the stack.

Evidence:

- repeated operational incidents
- chapter/source references
- packet traces vs app metrics comparison

Question: In what situations is "it's the network" actually the right first hypothesis?

Procedure: Quick triage sequence for suspected network latency

Concept: Queueing delay vs propagation delay vs processing delay

Now the notes are doing cognitive work.

## A Strong Definition of Your PKM

I think this is close to the formulation you're reaching for:

Or even more sharply:

[A PKM is a belief revision system, not an information warehouse..md](A%20PKM%20is%20a%20belief%20revision%20system,%20not%20an%20information%20warehouse..md)

That is the distinction you've been circling.

## Why This is Better than a Personal Wiki

Because a wiki mostly optimizes for retrieval.

Your system seems to need to optimize for:

- clarification
- synthesis
- contradiction
- revision
- decision support
- writing

A wiki says:

- "Here is what networking is."

A thinking PKM says:

- "Here is what I currently believe about network failures, why, and what might falsify that."

That is much closer to actual intellectual progress.

## The Danger to Avoid

There are two failure modes here.

### 1\. Turning Everything into Topic Buckets

You already dislike this. Good instinct.

### 2\. Turning Everything into Brittle "claims" with no Supporting Structure

This is the opposite trap.

If everything is a proposition, you can lose:

- shared vocabulary
- tacit skill
- procedures
- unresolved ambiguity
- context

So the right model is:

- propositions as the center
- concepts as scaffolding
- evidence as grounding
- questions as tension
- procedures as embodied know-how

## A Simple Operating Rule

When reading, thinking, or working, ask of each note:

1. Is this a claim?
2. If not, is it a concept I need in order to make claims?
3. If not, is it evidence for or against a claim?
4. If not, is it a question worth keeping open?
5. If not, is it a reusable procedure?
6. If none of those, why am I keeping it?

That last question will kill a lot of pointless notes.

## A Minimal Note Structure

For proposition notes, a simple format is enough:

Title: complete sentence claim

Why I think this: short rationale

Evidence / sources: links, quotes, cases

Counterpoints: what pushes against it

Confidence: low / medium / high

What would change my mind: falsifier or update condition

That lets you revise beliefs instead of hoarding facts.

## If You want a Practical System to Start Tomorrow

Use just five note types:

- Claim
- Concept
- Question
- Evidence
- Procedure

And one rule:

> No topic notes unless they are maps that point to claims/questions/procedures.

So "Networking" can exist only as an index note linking to:

- claims about network behaviour
- debugging procedures
- conceptual distinctions
- unresolved questions

## My Blunt view

You are right to feel that a lot of conventional Obsidian-style note-taking becomes pointless.

If it's just:

- facts
- copied ideas
- chapter summaries
- topical buckets

then it often becomes a prettier version of reference material you already own.

The value appears when the system contains:

- your judgments
- your distinctions
- your uncertainty
- your evidence
- your revisions over time

That is actual thinking.

## Best One-sentence Definition

If you want a concise definition of your PKM, I'd use this:

> My PKM is a structured record of what I think, why I think it, how confident I am, and how those beliefs change over time.

If you want, I can turn this into a concrete PKM schema for either Obsidian or Heptabase—for example, exact note types, tags/properties, and templates for claim/concept/question/procedure notes.
