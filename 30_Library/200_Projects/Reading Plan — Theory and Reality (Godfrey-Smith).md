---
conformant: true
created: 2026-09-16T00:00:00+00:00
modified: 2026-09-19T15:45:03+00:00
permalink: llmeon/30-library/200-projects/reading-plan-theory-and-reality-godfrey-smith
tags: [philosophy-of-science, prodos/project, reading]
title: Reading Plan — Theory and Reality (Godfrey-Smith)
type: project
---

## Goal

Read _Theory and Reality_ (Peter Godfrey-Smith)—Calibre id 1611, 2nd edition (2021), University of Chicago Press, ISBN 9780226771137—to use the ideas, not archive the book. Success is being able to, from memory alone:

- State the book's central problem: how science can be a fallible, historically-changing, socially-organised activity and still deliver knowledge of a mind-independent world.
- Give the strongest case for and the strongest objection to each major position (empiricism, Popper, Kuhn, sociology of science, naturalism, realism, Bayesianism/truth-simplicity-models).
- Explain how later positions respond to problems raised by earlier ones.
- Connect at least a handful of ideas to standing questions in this PKM about truth, disagreement, and pluralism.

## Correction: Edition Mismatch in the Source Draft

Action before building any chapter scaffolding: open the book's actual contents page (2 minutes) and copy the 14 real chapter titles into the roadmap table below. The thematic arc is edition-independent and safe to rely on now:

$$
\text{Empiricism} \rightarrow \text{Popper} \rightarrow \text{Kuhn} \rightarrow \text{social/historical critiques} \rightarrow \text{naturalism} \rightarrow \text{realism} \rightarrow \text{explanation, truth \& models}
$$

## Note Architecture (Mapped to This Vault's Actual Schema)

| Layer               | Vault type                                              | Location                                                     | Cardinality                       |
| ------------------- | ------------------------------------------------------- | ------------------------------------------------------------ | --------------------------------- |
| Book hub            | `prodos.kind: moc`                                      | `30_Library/MoC/MOC - Theory and Reality (Godfrey-Smith).md` | One, created now                  |
| Chapter scaffolding | plain body section, not a separate note per chapter     | inside this project note, "Reading Log" below                | One running log                   |
| Durable idea        | `prodos.kind: atomic`, `type: concept` or `type: claim` | `30_Library/100_zettelkasten/`                               | 0–1 per chapter, only when earned |

Do not pre-build 14 chapter notes. A chapter note earns its own file only if it grows past what fits as a log entry here—most won't. This avoids the draft's own stated failure mode ("one enormous book summary" vs. "a separate note for every term") while cutting the administrative overhead of 14 boilerplate files.

A durable atomic note earns its place only if at least one is true: it changes/clarifies an existing belief, it's likely to recur, it connects two existing areas of this vault, it's a disagreement worth returning to, or it will support future writing. Name it as the claim itself (see the real example: [[Developing an Idea Differs From Presenting a New One]]), not as a topic label.

## The Chapter Loop (Streamlined)

Two short contacts per chapter, not one long passive read.

Before reading (2–3 min): skim headings, recall the previous chapter's central question, write one prediction and one question you want answered.

While reading: three margin marks only—`!` (central claim), `?` (confusion), `→` (links to an existing vault note). Don't stop for every unfamiliar name; only when it blocks the argument.

Closed-book recall (5 min, before rereading anything): what question did the chapter address, what answer did it give, 2–3 main reasons, one example, the strongest objection, what's still confusing. This retrieval step is the one that actually builds durable memory—everything else is scaffolding around it.

Verify: reopen the chapter, correct errors under a `## Corrections` line, add only what changes the argument.

Log entry: append a short block to the Reading Log below—question / answer / reasons / objection / my view / typed link(s) to existing notes (`supports →`, `challenges →`, `refines →`, `contrasts-with →`, `exemplifies →`).

Durable note (0 or 1): promote to `100_zettelkasten/` only if it clears the bar above.

Every 2–3 chapters, interleave: pick two positions just read and compare them head-to-head (e.g. Popper vs. Kuhn—refutation or paradigm-guided puzzle-solving?) rather than reviewing each in isolation. This produces better graph edges than linking everything back only to the MoC.

## Using an LLM in This Loop

Only _after_ the closed-book recall attempt, never before—a supplied summary short-circuits the retrieval step that makes the reading stick. Four roles only:

1. Examiner—Socratic questioning against the chapter log, one question at a time, no answers revealed.
2. Critic—given a recall/argument reconstruction, flag missing premises, conflated views, the strongest objection, one counterexample.
3. Connector—given two chapter log entries, return only their shared question, their incompatible claims, and one candidate typed link.
4. Formatter—turn a log entry into 3–5 retrieval questions with a separate answer key.

In every case: paste the note, ask it to distinguish supplied text from inference, and flag uncertainty rather than inventing book content.

## Stopping Rule per Chapter

One log entry. At most one durable note. Two to three retrieval questions. At least one typed link to something already in the vault. One unresolved question. Then move on—polishing notes is not the same as thinking.

Low-energy version: read one section, close the book, write three bullets from memory, check them, add one typed link. That's enough; consistency beats an elaborate system used twice.

## After the Final Chapter

Close the book and, before rereading any log entries: write the book's overall journey in ~500 words, complete the position-map table in the MoC, pick the five most consequential durable notes, write one open question for further reading, and write a one-line personal-view statement. Then reopen the log and correct the synthesis without deleting the original attempt. Final check: explain the book aloud for ten minutes to an imagined friend—if you can state the central disputes, give examples, name objections, and connect the chapters, it's usable knowledge.

## Reading Log

_Append one entry per chapter as you go. Do not pre-fill._

## First Actions

1. Open the book's contents page; confirm the 14 real chapter titles.
2. Create `MOC - Theory and Reality (Godfrey-Smith).md` in `30_Library/MoC/` with the guiding question, the position-map table (Empiricism / Popper / Kuhn / sociology of science / naturalism / realism / truth-simplicity-models), and an `entry_points` link to this project note.
3. Read chapter 1 using the loop above.
4. Delete or archive `00_Inbox/Give me a break down and synopsis of the chapters.md` once this plan is confirmed to replace it.
