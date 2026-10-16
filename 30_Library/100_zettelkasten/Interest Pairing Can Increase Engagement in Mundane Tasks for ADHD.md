---
aliases: []
conformant: false
created: 2025-10-30T12:00:01+00:00
last_reviewed: '2025-12-16'
modified: 2026-10-14T00:00:00+01:00
non_conformance_reason: 'type hypothesis is not in the Frontmatter Contract type enum, but MOC - ADHD Experiments & Protocols defines the hypothesis lifecycle and queries on it. The note is an unresolved personal experiment with a pending Results Log, so it is not forced into claim. Left as-is pending a decision on whether the contract should add hypothesis. Same status as Body Doubling for ADHD Focus.'
permalink: llmeon/30-library/100-zettelkasten/interest-pairing-can-increase-engagement-in-mundane-tasks-for-adhd
source: '[[MOC - ADHD Experiments & Protocols]]'
status: draft
tags: [experiment, hypothesis, interest-pairing, TheHuman/Health/ADHD, TheHuman/Motivation, topic/productivity]
title: Interest Pairing Can Increase Engagement in Mundane Tasks for ADHD
type: hypothesis
---

## 1. The Hypothesis

> If I strictly pair a high-interest sensory input (Podcast, Audiobook, YouTube Essay) with a low-interest physical output (Dishes, Laundry, Admin),
> Then I will initiate the boring task significantly faster,
> Because the dopamine from the input lowers the "activation energy" required to start the output.

---

## 2. Experiment Protocol

- Duration: 1 Week.
- The Pair: Select one specific content source (e.g., "The Rest is History Podcast") and one specific chore (e.g., "Folding Laundry").
- The Rule: I am only allowed to listen to this podcast while doing this chore. If I stop folding, I must pause the audio.

---

## 3. Expected Outcome

- Success: I actually look forward to doing the laundry because I want to hear the story.
- Failure: The distraction of the audio makes me do the chore poorly or too slowly.

---

## 4. Results Log

- _(Log results here)_

---

Original Context:

This technique leverages the interest-driven nature of the ADHD brain to boost motivation. It connects to the concept of Temptation Bundling in [[SoT - Habit Formation Framework#2. Mechanism: The Four Laws (Atomic Habits)|Temptation Bundling]], which uses the same pairing as its own example (only listen to a podcast while running).

[extends:: [[SoT - The Interest-Based Nervous System in ADHD]], strength=4, confidence=high]

[extends:: [[Dopamine Management in ADHD Productivity]], strength=4, confidence=high]

[depends_on:: [[Limbic Friction is the Activation Energy for Habits]], strength=3, confidence=medium]

[depends_on:: [[Dopamine reward pathway dysfunction causes ADHD task initiation difficulty]], strength=3, confidence=medium]

## Related

- [[SoT - The Interest-Based Nervous System in ADHD]]—the general INCUP mechanism (Interest is one of the five "ignition keys"); this experiment applies the Interest key specifically by borrowing it from an unrelated stimulus rather than finding it in the task itself.
- [[Dopamine Management in ADHD Productivity]]—the sibling tactic, "The Dopamine Sandwich," sequences a reward before/after the task; Interest Pairing instead runs the stimulus _concurrently_ with the task, a distinct variant of the same core principle.
- [[Hyperfocus is a State of Intense Interest-Driven Focus in ADHD]]—the other end of the same mechanism: when interest is genuinely held, focus can be sustained, so a stable podcast or audiobook is a fair test of whether borrowed interest is enough.
- [[ADHD Causes Task Initiation Deficits Due to Dopamine Hyposensitivity]]—the initiation problem this experiment targets; the hypothesis predicts that faster starting is the measurable effect.
- [[Body Doubling for ADHD Focus]]—the other pending experiment in the same MOC, which also adds an external input to a task and so is worth comparing when both are logged.
- [[Limbic Friction is the Activation Energy for Habits]]—supplies the vault's general term for the "activation energy" this hypothesis's own Because-clause invokes.
- [[Finding Your Right Difficult A Strategy for ADHD Engagement]]—adjacent strategy: shaping the _task_ to be stimulating, rather than pairing it with an external stimulus.
- [[Novelty Effect]]—a caution rather than a support: this experiment leans on sustained _Interest_ (a stable podcast/audiobook draw), not _Novelty_ (which reliably wanes); worth distinguishing if the effect fades after the 1-week trial.
- [[MOC - ADHD Experiments & Protocols]]—the experiment-lifecycle hub this note belongs to (`Hypothesis → Experiment → Validation/Rejection`); it is picked up automatically by that MOC's Dataview query on `#hypothesis` + `status: pending`, but is linked here explicitly too. This also repairs the frontmatter `source:` field, which pointed at a non-existent "MOC - ADHD Task Management"—flagged as a best-fit repair (topical and lifecycle match), not a confirmed rename.
