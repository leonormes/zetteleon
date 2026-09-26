---
created: 2026-09-26 11:24:35+00:00
modified: 2026-09-26 11:24:51+00:00
permalink: llmeon/00-inbox/plan-to-improve-zettelkasten
---

## Verdict

Yes, but keep it small: one property, applied only from now on, plus one pilot project where the roles flip. You write; the LLM finds sources and attacks your arguments. Don't go back and tag the 1,584 existing notes. The label is only worth having if it changes how notes get written, and the politics/law project is where you'll find out whether it does.

## Where Your Plan Could Fail

- Back-tagging is a refactor in disguise. Sorting 1,584 notes by who wrote them is the "structure before reps" pattern again. Tag an old note only when you've actually rewritten it yourself.
- The label can say one thing while you do another. The audit's main finding (F1) is that you skipped the ownership step, which is paraphrasing in your own words. A property doesn't fix that. A strict rule for when you may apply it does.
- Agents will corrupt the signal unless told not to. The audit notes that a mass rewrite touched every note in the folder on 26 September. If the CLI agent can set the field or "tidy" your prose, the filter stops telling the truth. You need a rule in AGENTS.md.
- Name collision. Don't call the field `author`. Your Source and Literature notes very likely already use it for the book's author.
- It's a bet on the audit's open question. The audit found two of your notes contradicting each other: one on the collector's fallacy (gathering isn't the same as understanding), and one claiming that capturing lots and reviewing later is sustainable. Carrying on with LLM batches while you build your own layer is a bet on the second. That's fine, but set up a test that could prove it wrong (step 4).

## The Plan

### 1. Write the First Note, and Use the Property on it (Today)

- Write the first note before you set anything else up. The property gets defined by being used.
- In its frontmatter, add `own_words: true` as a checkbox. If the field is missing, the note isn't yours; you don't need to write `false`.
- The rule for applying it: _I drafted every sentence I kept. An LLM may have found sources or attacked the argument, but none of its wording survived._
  - LLM wrote a draft and you edited it → not `own_words`.
  - You rewrote it from scratch in your words → `own_words`.
  - This is your paraphrase test, turned into a field.

### 2. Guardrails (About 15 Minutes, after that First Note Exists)

- Register `own_words` in `SoT - Frontmatter Contract`, so the conformance checks don't flag it.
- Add two lines to AGENTS.md:
  - Agents never set, change or remove `own_words`.
  - Agents never edit the body of an `own_words` note. Suggestions go in chat or in a separate inbox note.
- To find your notes, use Obsidian search: `[own_words:true]`. Skip building a Base (saved filtered view) until you have enough notes to want a count.

### 3. The Pilot: Politics and Law Built on Emotion and Cooperation

Who does what:

| You | LLM |
|---|---|
| The thesis or question, your argument notes, and their Tensions sections | Finding which sources and chapters matter |
| Source notes for the 2–3 books the argument rests on | Making the strongest case for opposing views |
| Deciding when you've changed your mind (add a `revises` link) | Attacking your notes: what would prove them wrong, what they quietly assume |

Rule: anything an LLM drafts for this project stays in chat or `00_Inbox`. None of it goes into `100_zettelkasten` under this project. For every other topic, carry on as you are.

Order of work:

1. Hunch first. Write one arguable sentence before you read anything. If it isn't a claim yet, make it a `Q — …` note.
2. Search the vault for "cooperation", "emotion", "law" and "Rawls", so you link to existing notes rather than duplicating them.
3. Bring the hunch here. I'll name who would disagree most strongly and which sources would test it.
4. Read 2–3 of those sources. Write the source notes yourself, each with a What it Does not Show section. The audit singled this section out as your best existing practice.
5. Write your argument notes, each with a Tensions section. When the thesis changes, add a `revises` link instead of overwriting the old version.

One question to hold without answering yet: your philosophy-of-science notes argue that science is trustworthy because its _structure_ corrects individual bias. Is there a matching claim about law, and where would it break?

### 4. Make the Bet Testable

- Add one line to your Friday 16:30 review: _own_words notes created this week: n_.
- Prediction: at least 4 `own_words` notes in the pilot by Friday 23 October.
  - If you hit it: writing your own layer alongside the LLM notes works. Write that up as a note that settles the audit's open question, using your own numbers as evidence.
  - If you get 0–1: the problem is getting started, not labelling. The fix is smaller steps, maybe fewer LLM batches, not more structure.

### Deliberately Parked

Cleaning up the tags, the 179 notes with a blank `type`, sorting out the 91 unlinked notes, and back-tagging. The audit is right about all of them, and every one is a refactor. Come back to them only if the pilot works.

## Uncertainty

- I can't see AGENTS.md or the Frontmatter Contract. If a field that records where a note came from already exists, use it rather than adding `own_words`.
- The target of 4 is my guess at "one a week". Change it now if it's wrong, then don't renegotiate it until 23 October.

## Next Action

Create a new note in `00_Inbox`, add `own_words: true`, and write one sentence: your current hunch about how law grew out of emotion and cooperation, before you read anything.